import requests

url = 'http://127.0.0.1:8000/'
file = {'file': open('test/image.jpg', 'rb')}
resp = requests.post(url=url, files=file)
print(resp.json())