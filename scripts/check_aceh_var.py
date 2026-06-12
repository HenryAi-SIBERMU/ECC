import requests
API_KEY = '06fd644648629502353deaed29fc6383'
url = f'https://webapi.bps.go.id/v1/api/list/model/var/domain/1100/subject/52/key/{API_KEY}/'
resp = requests.get(url).json()
vars = resp.get('data', [])[1]
for v in vars:
    print(f"[{v['var_id']}] {v['title']}")
