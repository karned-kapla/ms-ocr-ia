import json
from doctr.io import DocumentFile
from doctr.models import ocr_predictor


def word_to_dict(word):
    return {"value": word.value, "confidence": word.confidence}


def line_to_dict(line):
    return {"words": [word_to_dict(word) for word in line.words]}


def block_to_dict(block):
    return {"lines": [line_to_dict(line) for line in block.lines], "artefacts": []}


def page_to_dict(page):
    return {"dimensions": page.dimensions, "blocks": [block_to_dict(block) for block in page.blocks]}


def ocr_image(path):
    model = ocr_predictor(pretrained = True)
    doc = DocumentFile.from_images(path)
    document = model(doc)

    document_dict = {"pages": [page_to_dict(page) for page in document.pages]}

    json_output = json.dumps(document_dict, indent = 2)

    return json_output
