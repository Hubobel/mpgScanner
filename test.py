import json
import requests
datas = ['RTL','SAT11','PRO7','3SAT']
url = 'http://api.hubobel.de/tv/check'
resp = requests.post(url, json=datas)
data = resp.json()
print(data)