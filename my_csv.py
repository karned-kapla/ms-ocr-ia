import json
from pathlib import Path
import pandas as pd


def extract_word(full_path, random_file_name):
    with open(full_path, 'r') as f:
        data = json.load(f)

    folder = "csv"
    Path(folder).mkdir(parents = True, exist_ok = True)
    full_path = Path(folder) / random_file_name
    full_path = full_path.with_suffix('.csv')

    datas = []
    for page in data['pages']:
        for block in page['blocks']:
            for line in block['lines']:
                for word in line['words']:
                    temp = []
                    temp.append(word['value'])
                    temp.append(word['confidence'])
                    for point in word['geometry']:
                        for coord in point:
                            temp.append(coord)
                    datas.append(temp)

    entetes = ['value', 'confidence', 'x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4']

    df = pd.DataFrame(datas, columns = entetes)
    df.to_csv(full_path, index = False)

    with open(full_path, 'r') as f:
        result = f.read()

    return full_path, result
