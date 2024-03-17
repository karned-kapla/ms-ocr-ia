import requests

url = 'http://0.0.0.0:8000/'
file = {'file': open('test/img02.jpg', 'rb')}
resp = requests.post(url=url, files=file)
print(resp.json())