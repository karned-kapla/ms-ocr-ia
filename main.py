from fastapi import FastAPI, UploadFile, File
from uuid import uuid4
from pathlib import Path

app = FastAPI()


@app.post("/")
def upload(file: UploadFile = File(...)):
    try:
        folder = "uploads"
        file_extension = Path(file.filename).suffix  # get file extension
        random_file_name = f"{uuid4().hex}{file_extension}"
        full_path = Path(folder) / random_file_name
        with full_path.open("wb") as buffer:
            contents = file.file.read()  # read file
            buffer.write(contents)
    except Exception as e:
        print(f"Unable to save file: {e}")
        return None
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}
