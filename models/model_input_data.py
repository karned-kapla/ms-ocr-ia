from pydantic import BaseModel


class InputData(BaseModel):
    file: str
    model_detection: str = 'db_resnet34'
    model_recognition: str = 'crnn_vgg16_bn'
