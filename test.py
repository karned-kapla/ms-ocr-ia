import requests

url = 'http://localhost:8900/csv/words?model_detection=db_resnet34&model_recognition=crnn_vgg16_bn'

files = {'file': open('notebooks/image.jpg', 'rb')}
response = requests.post(url, files=files)

with open('result.csv', 'w') as f:
    f.write(response.text)

