from starlette.responses import PlainTextResponse
import json
from fastapi import FastAPI

from models.model_input_data import InputData
from my_csv import extract_word
from my_file import save_upload
from my_json import save_json
from my_txt import extract_text_blocks
import gc

app = FastAPI(
    title="OCR",
    description="API OCR.",
    version="1.3.0"
)


def create_json (request):
    full_path, random_file_name = save_upload(request.file)
    full_path_json, result = save_json(
        full_path=full_path,
        random_file_name=random_file_name,
        model_detection=request.model_detection,
        model_recognition=request.model_recognition
    )
    return full_path_json, result, random_file_name


@app.post("/json/all")
def json_all(request: InputData):
    full_path_json, result, random_file_name = create_json(request)
    gc.collect()
    return json.loads(result)


@app.post("/csv/words", response_class=PlainTextResponse)
def csv_words(request: InputData):
    full_path_json, result, random_file_name = create_json(request)
    full_path_csv, result = extract_word(full_path_json, random_file_name)
    gc.collect()
    return result


@app.post("/txt/blocks-words", response_class=PlainTextResponse)
def txt_blockswords(request: InputData):
    full_path_json, result, random_file_name = create_json(request)
    datas = extract_text_blocks(full_path_json)
    datas = "\n".join(datas)
    gc.collect()
    return datas

