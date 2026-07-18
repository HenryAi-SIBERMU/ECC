import requests
API_KEY = '06fd644648629502353deaed29fc6383'
url = f'https://webapi.bps.go.id/v1/api/list/model/data/domain/0000/var/286/key/{API_KEY}/'
resp = requests.get(url).json()
print("vervar:", [v['label'] for v in resp.get('vervar', [])])
print("turvar:", [v['label'] for v in resp.get('turvar', [])])
