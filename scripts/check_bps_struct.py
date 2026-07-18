import requests

API_KEY = '06fd644648629502353deaed29fc6383'
url_sub = f'https://webapi.bps.go.id/v1/api/list/model/subject/domain/0000/key/{API_KEY}/'
subs = requests.get(url_sub).json().get('data', [])

print(type(subs[0]))
print(subs[0])
