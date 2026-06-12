import requests
import json
API_KEY = '06fd644648629502353deaed29fc6383'
url = f'https://webapi.bps.go.id/v1/api/list/model/data/domain/0000/var/286/key/{API_KEY}/'
resp = requests.get(url).json()
print("Keys:", resp.keys())
print("Data availability:", resp.get('data-availability'))
print("DataContent snippet:")
dc = resp.get('datacontent', {})
for k, v in list(dc.items())[:5]:
    print(f"{k}: {v}")
