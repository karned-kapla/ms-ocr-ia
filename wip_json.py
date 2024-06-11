import json

with open('temp/test.png.json.bad', 'r') as f:
    data = json.load(f)

display(data)