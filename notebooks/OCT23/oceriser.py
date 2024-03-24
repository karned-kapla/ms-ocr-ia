import json
import logging
import os
import time
from functools import partial
from multiprocessing import Pool

import matplotlib.pyplot as plt
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

import pprint

from tqdm import tqdm

os.environ['USE_TORCH'] = '1'

path = '/home/skit/formation/ml/datas/final'

models_detection = [
    'db_resnet34',
    'db_resnet50',
    'db_mobilenet_v3_large',
    'linknet_resnet18',
    'linknet_resnet34',
    'linknet_resnet50'
]

models_recognition = [
    'crnn_vgg16_bn',
    'crnn_mobilenet_v3_small',
    'crnn_mobilenet_v3_large',
    'master',
    'sar_resnet31',
    'vitstr_small',
    'vitstr_base',
    'parseq'
]

el_pos = 0
el_tot = 0


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
        pprint.pprint(data, stream = f)


def save_txt(result, file_name='result'):
    with open(file_name + '.txt', 'w') as f:
        f.write(result.render())


def constuct_totreat(folder):
    global el_pos
    global el_tot

    totreat = []

    with open('to_ocr.txt', 'r') as f:
        files = f.read().splitlines()

    treated_files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

    for file in files:
        temp = file + '.txt'
        if temp not in treated_files:
            totreat.append(file)

    el_pos = 0
    el_tot = len(totreat)

    return totreat


def treat(file, folder, model_detection, model_recognition):
    time_start = time.time()
    global el_pos
    global el_tot

    el_pos += 1
    logging.info(f"{el_pos} / {el_tot} " + file)
    img_path = os.path.join(path, file)
    result = ocr_treatment(img_path, model_detection, model_recognition)

    path_file = folder + '/' + file

    save_json(result, path_file)
    save_txt(result, path_file)
    save_block(result, path_file)

    time_end = time.time()
    logging.info(f"{time_end - time_start} sec")

    del result


def treat_model(model_detection, model_recognition):
    folder = model_detection + '__' + model_recognition
    time_start = time.time()

    print(model_detection)
    print(model_recognition)

    totreat = constuct_totreat(folder)

    for file in tqdm(totreat):
        treat(file, folder, model_detection, model_recognition)

    time_end = time.time()
    duration = time_end - time_start
    duration = round(duration / 60, 2)
    print(f"Duration: {duration} min")
    print('done !')


for model_detection in models_detection:
    for model_recognition in models_recognition:
        treat_model(model_detection, model_recognition)
