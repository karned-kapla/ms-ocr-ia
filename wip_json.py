import json
from wip_ocr import extract_text_all

with open('temp/test.png.json', 'r') as f:
    data = json.load(f)

print(data)
result = extract_text_all(data)

print(result)