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

import numpy as np

os.environ['USE_TORCH'] = '1'


def ocr_treatment(img_path, model_detection, model_recognition):
    doc = DocumentFile.from_images(img_path)
    predictor = ocr_predictor(model_detection, model_recognition, pretrained = True, assume_straight_pages = False,
                              preserve_aspect_ratio = True, det_bs = 4, reco_bs = 1024)
    # print(predictor) # affichage du détail du model
    result = predictor(doc)
    # result.show()
    return result


def ocr_display(result):
    synthetic_pages = result.synthesize()
    plt.figure(figsize = (15, 15))
    plt.imshow(synthetic_pages[0])
    plt.axis('off')
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

    # Custom JSON encoder for NumPy arrays
    class NumpyArrayEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return super().default(obj)

    with open(file_name + '.json', 'w') as f:
        json.dump(data, f, cls=NumpyArrayEncoder, indent=4)


def save_txt(result, file_name='result'):
    with open(file_name + '.txt', 'w') as f:
        f.write(result.render())


def treat(file, model_detection='db_resnet34', model_recognition='crnn_vgg16_bn'):
    result = ocr_treatment(file, model_detection, model_recognition)

    save_json(result, file)
    save_txt(result, file)
    save_block(result, file)

    del result


treat(file = 'temp/test.png', model_detection = 'db_resnet34', model_recognition = 'crnn_vgg16_bn')
