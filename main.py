from starlette.responses import PlainTextResponse

import json

from fastapi import FastAPI, UploadFile, File, HTTPException
from uuid import uuid4
from pathlib import Path

from ocr import ocr_image
from my_csv import extract_word

app = FastAPI()


def save_upload(file):
    folder = "uploads"
    Path(folder).mkdir(parents = True, exist_ok = True)
    try:
        file_extension = Path(file.filename).suffix
        if file_extension not in ['.jpeg', '.png', '.jpg']:
            raise ValueError("Invalid file type. Only .jpeg, .png and .jpg are allowed.")
        random_file_name = f"{uuid4().hex}{file_extension}"
        full_path = Path(folder) / random_file_name
        with full_path.open("wb") as buffer:
            contents = file.file.read()
            buffer.write(contents)
    except ValueError as e:
        raise HTTPException(status_code = 400, detail = str(e))
    except Exception as e:
        print(f"Unable to save file: {e}")
        raise HTTPException(status_code = 500, detail = "Something went wrong while saving the file.")
    finally:
        file.file.close() if 'file' in locals() else None

    return full_path, random_file_name


def save_json(full_path, random_file_name, model_detection, model_recognition):
    try:
        result = ocr_image(full_path, model_detection, model_recognition)
        folder = "json"
        Path(folder).mkdir(parents = True, exist_ok = True)
        full_path = Path(folder) / random_file_name
        full_path = full_path.with_suffix('.json')
        with open(full_path, 'w') as f:
            f.write(result)
    except Exception as e:
        print(f"OCR processing failed: {e}")
        raise HTTPException(status_code = 500, detail = "OCR processing failed.")

    return full_path, result


@app.post("/json")
def json(file: UploadFile = File(...),
           model_detection: str = 'db_resnet34',
           model_recognition: str = 'crnn_vgg16_bn'):
    full_path, random_file_name = save_upload(file)
    full_path_json, result = save_json(full_path, random_file_name, model_detection, model_recognition)
    return json.loads(result)


@app.post("/word_csv", response_class=PlainTextResponse)
def csv(file: UploadFile = File(...),
           model_detection: str = 'db_resnet34',
           model_recognition: str = 'crnn_vgg16_bn'):
    full_path, random_file_name = save_upload(file)
    full_path_json, result = save_json(full_path, random_file_name, model_detection, model_recognition)
    full_path_csv, result = extract_word(full_path_json, random_file_name)
    return result

