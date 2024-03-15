import requests

url = 'http://0.0.0.0:1234/'
file = {'file': open('test/image.jpg', 'rb')}
resp = requests.post(url=url, files=file)
print(resp.json())