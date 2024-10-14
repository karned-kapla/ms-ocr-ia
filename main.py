from starlette.responses import PlainTextResponse
import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from my_csv import extract_word
from my_file import save_upload
from my_json import save_json
from my_txt import extract_text_blocks
import gc

app = FastAPI()


@app.post("/json/all")
def json_all(file: UploadFile = File(...),
           model_detection: str = 'db_resnet34',
           model_recognition: str = 'crnn_vgg16_bn'):
    full_path, random_file_name = save_upload(file)
    full_path_json, result = save_json(full_path, random_file_name, model_detection, model_recognition)
    gc.collect()
    return json.loads(result)


@app.post("/csv/words", response_class=PlainTextResponse)
def csv_words(file: UploadFile = File(...),
           model_detection: str = 'db_resnet34',
           model_recognition: str = 'crnn_vgg16_bn'):
    full_path, random_file_name = save_upload(file)
    full_path_json, result = save_json(full_path, random_file_name, model_detection, model_recognition)
    full_path_csv, result = extract_word(full_path_json, random_file_name)
    gc.collect()
    return result


@app.post("/txt/blocks-words", response_class=PlainTextResponse)
def txt_blockswords(file: UploadFile = File(...),
           model_detection: str = 'db_resnet34',
           model_recognition: str = 'crnn_vgg16_bn'):
    full_path, random_file_name = save_upload(file)
    full_path_json, result = save_json(full_path, random_file_name, model_detection, model_recognition)
    datas = extract_text_blocks(full_path_json)
    datas = "\n".join(datas)
    gc.collect()
    return datas

