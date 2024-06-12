import json
import pandas as pd

with open('json/1b45ec3176e54cb2a6b07caf758023c0.json', 'r') as f:
    data = json.load(f)

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
df.to_csv('csv/1b45ec3176e54cb2a6b07caf758023c0.csv', index = False)