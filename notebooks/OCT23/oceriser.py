import os
import json

os.environ['USE_TORCH'] = '1'

import matplotlib.pyplot as plt

from doctr.io import DocumentFile
from doctr.models import ocr_predictor

path = '/home/skit/formation/ml/datas/final'
model = 'linknet_resnet50'

def ocr_treatment(img_path):
	doc = DocumentFile.from_images(img_path)
	predictor = ocr_predictor('linknet_resnet18', pretrained=True, assume_straight_pages=False, preserve_aspect_ratio=True, det_bs=4, reco_bs=1024)
	result = predictor(doc)
	return result

def ocr_display(result):
	synthetic_pages = result.synthesize()
	plt.figure(figsize=(15, 15))
	plt.imshow(synthetic_pages[0]); plt.axis('off'); plt.show()


def extract_text_blocks(json_data):
    text_blocks = []
    for page in json_data["pages"]:
        for block in page["blocks"]:
            text = ""
            for line in block["lines"]:
                for word in line["words"]:
                    text += word["value"] + " "
            text_blocks.append(text.strip())
    return text_blocks


def ocr_display_text(result):
	json_data = result.export()
	text_blocks = extract_text_blocks(json_data)
	for i, block in enumerate(text_blocks, start=1):
		print(f"Block {i}: {block}")


def save_json(result, file_name='result'):
	with open(file_name + '.json', 'w') as f:
		f.write(json.dumps(result.export()))


def save_txt(result, file_name='result'):
	with open(file_name + '.txt', 'w') as f:
		f.write(result.render())

totreat = []

with open('to_ocr.txt', 'r') as f:
	files = f.read().splitlines()

import os
treated_files = [f for f in os.listdir(model) if os.path.isfile(os.path.join(model, f))]

for file in files:
	temp = file + '.txt'
	if temp not in treated_files:
		totreat.append(file)

from multiprocessing import Pool

def treat(file):
	print(file)
	img_path = os.path.join(path, file)
	result = ocr_treatment(img_path)
	save_txt(result, model + '/' + file)

with Pool(4) as p:
    print(p.map(treat, totreat))