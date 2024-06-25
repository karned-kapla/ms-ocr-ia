from pathlib import Path

from ocr import ocr_image
from fastapi import HTTPException


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
