from uuid import uuid4
from pathlib import Path
from fastapi import HTTPException


def save_upload(file):
    folder = "uploads"
    Path(folder).mkdir(parents = True, exist_ok = True)
    try:
        file_extension = Path(file.filename).suffix
        if file_extension not in ['.jpeg', '.png', '.jpg', '.tiff', '.pdf']:
            raise ValueError("Invalid file type. Only .jpeg, .jpg, .png, .tiff and .pdf are allowed.")
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
