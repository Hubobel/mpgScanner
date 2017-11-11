import requests
import json
import os
def Wetter():
    url = 'http://api.wunderground.com/api/35a8e37c649985d5/conditions/lang:DL/q/Germany/pws:ILUDWIGS227.json'
    response = requests.get(url)
    data_response = response.json()
    temperatur=(data_response['current_observation']['temp_c'])
    wetter=(data_response['current_observation']['weather'])
    feuchte=(data_response['current_observation']['relative_humidity'])
    return temperatur,wetter,feuchte

temperatur,wetter,feuchte = Wetter()
print(wetter)
print(feuchte)
print(temperatur)
url_zitat = 'http://api.hubobel.de/facts/9999'
resp_zitat = requests.get(url_zitat)
data_zitat = resp_zitat.json()

for i in data_zitat:
    print(data_zitat[i])