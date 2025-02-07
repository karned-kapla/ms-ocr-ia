import base64
from typing import Optional
from uuid import uuid4
from pathlib import Path
from fastapi import HTTPException
import magic

def guess_extension( mime_type: str ) -> Optional[str]:
    if mime_type == "image/jpeg":
        return ".jpg"
    elif mime_type == "image/png":
        return ".png"
    elif mime_type == "image/gif":
        return ".gif"
    elif mime_type == "image/bmp":
        return ".bmp"
    elif mime_type == "image/webp":
        return ".webp"
    elif mime_type == "image/tiff":
        return ".tiff"
    elif mime_type == "application/pdf":
        return ".pdf"
    else:
        return ".bin"

def guess_mime_type( file_data: bytes ) -> Optional[str]:
    mime_type = magic.Magic(mime=True).from_buffer(file_data)
    return mime_type

def save_upload(file_content_base64: str):
    folder = "uploads"
    Path(folder).mkdir(parents = True, exist_ok = True)
    try:
        file_extension = Path(file_content_base64.filename).suffix
        if file_extension not in ['.jpeg', '.png', '.jpg', '.tiff', '.tif', '.pdf']:
            raise ValueError("Invalid file type. Only .jpeg, .jpg, .png, .tiff and .pdf are allowed.")
        random_file_name = f"{uuid4().hex}{file_extension}"
        full_path = Path(folder) / random_file_name
        with full_path.open("wb") as buffer:
            contents = base64.b64decode(file_content_base64)
            buffer.write(contents)
    except ValueError as e:
        raise HTTPException(status_code = 400, detail = str(e))
    except Exception as e:
        print(f"Unable to save file: {e}")
        raise HTTPException(status_code = 500, detail = "Something went wrong while saving the file.")

    return full_path, random_file_name
