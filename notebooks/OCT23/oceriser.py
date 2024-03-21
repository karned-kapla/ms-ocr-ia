import json
import os
from functools import partial
from multiprocessing import Pool

import matplotlib.pyplot as plt
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

import pprint

os.environ['USE_TORCH'] = '1'

path = '/home/skit/formation/ml/datas/final'
model_detection = 'linknet_resnet34'
model_recognition = 'crnn_vgg16_bn'
folder = model_detection + '__' + model_recognition


def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


create_folder(folder)


def ocr_treatment(img_path, model_detection, model_recognition):
    doc = DocumentFile.from_images(img_path)
    predictor = ocr_predictor(model_detection, model_recognition, pretrained = True, assume_straight_pages = False,
                              preserve_aspect_ratio = True, det_bs = 4, reco_bs = 1024)
    result = predictor(doc)
    return result


def ocr_display(result):
    synthetic_pages = result.synthesize()
    plt.figure(figsize = (15, 15))
    plt.imshow(synthetic_pages[0]);
    plt.axis('off');
    plt.show()


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


def save_block(result, file_name='result'):
    json_data = result.export()
    text_blocks = extract_text_blocks(json_data)
    with open(file_name + '.blk.txt', 'w') as f:
        for i, block in enumerate(text_blocks, start = 1):
            f.write(f"{block}\n")


def save_json(result, file_name='result'):
    data = result.export()
    with open(file_name + '.json.bad', 'w') as f:
        pprint.pprint(data, stream=f)


def save_txt(result, file_name='result'):
    with open(file_name + '.txt', 'w') as f:
        f.write(result.render())


totreat = []

with open('to_ocr.txt', 'r') as f:
    files = f.read().splitlines()

treated_files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

for file in files:
    temp = file + '.txt'
    if temp not in treated_files:
        totreat.append(file)


def treat(file, folder, model_detection, model_recognition):
    print(file)
    img_path = os.path.join(path, file)
    result = ocr_treatment(img_path, model_detection, model_recognition)

    path_file = folder + '/' + file

    save_json(result, path_file)
    save_txt(result, path_file)
    save_block(result, path_file)


with Pool(4) as p:
    p.map(partial(treat, folder = folder, model_detection = model_detection, model_recognition = model_recognition),
          totreat)
