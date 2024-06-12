import os
import json
import numpy as np
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

os.environ['USE_TORCH'] = '1'


def ocr_image(path, model_detection='db_resnet34', model_recognition='crnn_vgg16_bn'):
    result = ocr_treatment(path, model_detection, model_recognition)
    data = clean_json(result.export())
    return data


def ocr_treatment(img_path,
                  model_detection,
                  model_recognition):

    predictor = ocr_predictor(model_detection,
                              model_recognition,
                              pretrained = True,
                              assume_straight_pages = False,
                              preserve_aspect_ratio = True,
                              det_bs = 4,
                              reco_bs = 1024)

    doc = DocumentFile.from_images(img_path)
    result = predictor(doc)
    return result


def clean_json(data):
    class NumpyArrayEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return super().default(obj)

    return json.dumps(data, cls=NumpyArrayEncoder, indent=4)