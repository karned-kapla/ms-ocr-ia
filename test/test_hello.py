import requests

url = 'http://0.0.0.0:1234/'
resp = requests.get(url=url)
print(resp.json())