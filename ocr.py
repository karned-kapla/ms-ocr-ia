import json
from doctr.io import DocumentFile
from doctr.models import ocr_predictor


def ocr_image(path):
    model = ocr_predictor(pretrained = True)
    doc = DocumentFile.from_images(path)
    document = model(doc)

    json_export = document.export()

    return json_export
