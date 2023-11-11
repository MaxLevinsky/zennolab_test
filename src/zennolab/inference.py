import datetime as dt
import os
import warnings

import cv2
import numpy as np
import pandas as pd
# from pathlib import Path
import torch
from tqdm import tqdm

from groundingdino.util.inference import load_model, load_image, predict, annotate
from preprocess import filter_out_empty_jsons

# Need to update pckgs
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


def inference(data_dir: str, output_dir: str, box_trs: float = 0.28, text_trs: float = 0.25,
              write_images: bool = False):

    # device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    if torch.cuda.is_available():
        device = 'cuda'
    else:
        device = 'cpu'

    root_gd = os.path.join('/home/src', 'GroundingDINO')
    # root_gd = os.path.join(Path(__file__).parents[1], 'GroundingDINO')
    ogc = os.path.join(root_gd, 'groundingdino/config/GroundingDINO_SwinB_cfg.py')  # GroundingDINO_SwinT_OGC, GroundingDINO_SwinB_cfg
    weights = os.path.join(root_gd, 'groundingdino_swinb_cogcoor.pth')  # groundingdino_swint_ogc, groundingdino_swinb_cogcoor
    model = load_model(model_config_path=ogc, model_checkpoint_path=weights)
    data = filter_out_empty_jsons(data_dir=data_dir)

    data['pred_bbox'] = None
    data['bbox'] = None
    for idx, row in tqdm(data.iterrows()):
        image_path = row['image_path']
        promt = row['promt']
        try:
            image_source, image = load_image(image_path)
            boxes, logits, phrases = predict(
                model=model,
                image=image,
                caption=promt,
                box_threshold=box_trs,
                text_threshold=text_trs,
                device='cuda',
            )
            # max_logit = np.argmax(logits.tolist())
            pred_boxes = boxes.tolist()
            # print(pred_boxes)
            # print(logits)
            # print(phrases)
            # ph = phrases.index('head')
            data['pred_bbox'][idx] = pred_boxes
            data['bbox'][idx] = pred_boxes[-1]
        except Exception as err:
            print(err)

        if write_images:
            annotated_frame = annotate(image_source=image_source, boxes=boxes, logits=logits, phrases=phrases)
            cv2.imwrite(os.path.join(output_dir, f'{idx}.jpg'), annotated_frame)

    return data


# Wrong bbox format
# def get_center_bbox(x1, y1, x2, y2):
#     x, y = (x1 + x2)/2, (y1 + y2)/2
#     return x, y


def get_euclidian_distance(x1, y1, x2, y2):
    return abs(np.sqrt((x2 - x1)**2 + (y2 - y1)**2))


def postprocess(input_dir: str, output_dir: str, metric_trs: float = 0.1):
    df = inference(data_dir=input_dir, output_dir=output_dir)
    df.to_csv(os.path.join(output_dir, 'inference_results.csv'))

    df['distance'] = None
    df['bool_metric'] = None

    for idx, item in df.iterrows():
        bbox = item['bbox']
        true_coordinates = item['true_coordinates'] #ast.literal_eval(item['true_coordinates'])

        try:
            x_pred, y_pred = float(bbox[0]), float(bbox[1])
        except Exception as err:
            print(err)
            continue
        x_true, y_true = true_coordinates['x'], true_coordinates['y']
        ed = get_euclidian_distance(x_pred, y_pred, x_true, y_true)
        df['distance'][idx] = ed

        if ed > metric_trs:
            df['bool_metric'][idx] = False
        else:
            df['bool_metric'][idx] = True

    return df


def calculate_and_save_metric(input_dir: str, output_dir: str):
    log = []
    df = postprocess(input_dir=input_dir, output_dir=output_dir)
    df.to_csv(os.path.join(output_dir, 'postprocess_results.csv'))
    true_metric = len(df[df['bool_metric'] == True])

    df = df.dropna()
    mean_metric = true_metric / len(df)
    mean_ed = np.mean(df['distance'].to_list())

    print(f'Mean accuracy - {mean_metric}')
    print(f'Mean distance- {mean_ed}')

    log.append({
        'Mean_accuracy': mean_metric,
        'Mean_distance': mean_ed
    })

    pd.DataFrame(log).to_csv(os.path.join(output_dir, 'result.csv'), index=False)
    df.to_csv(os.path.join(output_dir, 'artefacts.csv'), index=False)


if __name__ == '__main__':
    now = dt.datetime.now()
    calculate_and_save_metric('/home/markov.n/data/tasks/squirrels_head',
                              '/home/markov.n/zennolab_test/data/output')
    print(dt.datetime.now() - now)

