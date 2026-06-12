import requests
import json
API_KEY = '06fd644648629502353deaed29fc6383'
url = f'https://webapi.bps.go.id/v1/api/list/model/subject/domain/0000/key/{API_KEY}/'
resp = requests.get(url).json()
print(json.dumps(resp.get('data', []), indent=2))
