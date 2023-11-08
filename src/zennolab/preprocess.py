import os
import pandas as pd
import json
import ast
from collections import ChainMap


def read_json(json_path: str):
    """
    Read a file in json format

    :param json_path: A path to a json file
    :return:
    """
    try:
        with open(json_path) as f:
            data = json.load(f)
    except Exception as err:
        print(f'Can not load {json_path}, error {repr(err)}')
        return None

    return data


# def save_csv(csv_pth: str) -> None:
#     try:



def filter_out_empty_jsons(data_dir: str) -> pd.DataFrame:
    """

    :return:
    """
    filtered_json_list = []
    for root, dir, file in os.walk(data_dir):
        for filename in file:
            if filename.endswith('.json'):
                path = os.path.join(root, filename)
                data = read_json(path)
                if data is not None and len(data) != 0:
                    for i in data:  # In case of multiple centers

                        name_wo_ext = os.path.splitext(filename)
                        filtered_json_list.append({
                            'image_path': os.path.join(root, f'{name_wo_ext[0]}.jpg'),
                            'true_coordinates': i,
                            'promt': ' . '.join(root.split('/')[-1].split('_')[-2:])
                        })

    df = pd.DataFrame(filtered_json_list)
    return df


if __name__ == '__main__':
    df = filter_out_empty_jsons('/Users/nikitamarkov/Downloads/tasks')
    print(len(df))
    df.to_csv('/Users/nikitamarkov/Desktop/digital_roads/test_detection/filtered.csv', index=False)
    # print(df['true_coordinates'])
