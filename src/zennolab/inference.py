import os
import warnings

import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm
import datetime as dt
from pathlib import Path

from groundingdino.util.inference import load_model, load_image, predict, annotate
from preprocess import filter_out_empty_jsons

# Need to update pckgs
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


def inference(data_dir: str, output_dir: str, box_trs: float = 0.35, text_trs: float = 0.25,
              write_images: bool = False, device: str = 'cpu'):
    root_gd = os.path.join('/home/src', 'GroundingDINO')
    ogc = os.path.join(root_gd, 'groundingdino/config/GroundingDINO_SwinT_OGC.py')
    weights = os.path.join(root_gd, 'groundingdino_swint_ogc.pth')
    model = load_model(model_config_path=ogc, model_checkpoint_path=weights)
    data = filter_out_empty_jsons(data_dir=data_dir)

    data['pred_bbox'] = None
    data['bbox'] = None
    for idx, row in tqdm(data.iterrows()):
        image_path = row['image_path']
        promt = row['promt']
        # print(promt)
        image_source, image = load_image(image_path)
        boxes, logits, phrases = predict(
            model=model,
            image=image,
            caption=promt,
            box_threshold=box_trs,
            text_threshold=text_trs,
            device=device,
        )
        try:
          max_logit = np.argmax(logits.tolist())
          pred_boxes = boxes.tolist()
          # print(pred_boxes)
          # print(max_logit)
          data['pred_bbox'][idx] = pred_boxes
          data['bbox'][idx] = pred_boxes[max_logit]
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

    df['distance'] = None
    df['bool_metric'] = None

    for idx, item in df.iterrows():
        bbox = item['bbox'] #ast.literal_eval(item['bbox'])
        true_coordinates = item['true_coordinates'] #ast.literal_eval(item['true_coordinates'])

        x_pred, y_pred = float(bbox[0]), float(bbox[1]) #get_center_bbox(float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3]))
        x_true, y_true = true_coordinates['x'], true_coordinates['y']
        ed = get_euclidian_distance(x_pred, y_pred, x_true, y_true)
        df['distance'][idx] = ed

        if ed > metric_trs:
            df['bool_metric'][idx] = False
        else:
            df['bool_metric'][idx] = True

    return df


def calculate_and_save_metric(input_dir: str, output_dir: str, device: str = 'cpu'):
    log = []
    df = postprocess(input_dir=input_dir, output_dir=output_dir, device=device)
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
    calculate_and_save_metric('/Users/nikitamarkov/Desktop/digital_roads/test_detection/data/input/the_center_of_the_gemstone',
                              '/Users/nikitamarkov/Desktop/digital_roads/test_detection/data/output')
    print(dt.datetime.now() - now)

