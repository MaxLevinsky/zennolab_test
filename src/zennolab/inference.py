import os
import warnings

import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm
import datetime as dt
from pathlib import Path
from ultralytics import SAM

from groundingdino.util.inference import load_model, load_image, predict, annotate
from preprocess import filter_out_empty_jsons

# Need to update pckgs
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


def inference(data_dir: str, output_dir: str, box_trs: float = 0.28, text_trs: float = 0.25,
              write_images: bool = True, device: str = 'cpu'):
    # root_gd = os.path.join('/home/src', 'GroundingDINO')
    root_gd = os.path.join(Path(__file__).parents[1], 'GroundingDINO')
    ogc = os.path.join(root_gd, 'groundingdino/config/GroundingDINO_SwinB_cfg.py')  # GroundingDINO_SwinT_OGC, GroundingDINO_SwinB_cfg
    weights = os.path.join(root_gd, 'weights/groundingdino_swinb_cogcoor.pth')  # groundingdino_swint_ogc, groundingdino_swinb_cogcoor
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
                caption='squirrels . head',
                box_threshold=box_trs,
                text_threshold=text_trs,
                device=device,
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


def postprocess(input_dir: str, output_dir: str, metric_trs: float = 0.1, device: str = 'cpu'):
    df = inference(data_dir=input_dir, output_dir=output_dir, device=device)
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


def calculate_and_save_metric(input_dir: str, output_dir: str, device):
    log = []
    df = postprocess(input_dir=input_dir, output_dir=output_dir, device=device)
    df.to_csv(os.path.join(output_dir, 'postprocess_results.csv'))
    true_metric = len(df[df['bool_metric'] == True])

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
    calculate_and_save_metric('/Users/nikitamarkov/Desktop/digital_roads/test_detection/data/input/sam',
                              '/Users/nikitamarkov/Desktop/digital_roads/test_detection/data/output', 'cpu')
    print(dt.datetime.now() - now)


    # from segment_anything import SamPredictor, sam_model_registry
    #
    # sam_checkpoint = "sam_vit_h_4b8939.pth"
    # model_type = "vit_h"
    # sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    # sam.to(device='cpu')
    # predictor = SamPredictor(sam)
    #
    # input_box = np.array([0.47409895062446594, 0.36872392892837524, 0.3504016399383545, 0.3696969449520111])
    # masks, _, _ = predictor.predict(
    #     point_coords=None,
    #     point_labels=None,
    #     box=[0.47409895062446594, 0.36872392892837524, 0.3504016399383545, 0.3696969449520111],
    #     multimask_output=False,
    # )
