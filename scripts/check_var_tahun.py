import requests
API_KEY = '06fd644648629502353deaed29fc6383'

url_tahun = f'https://webapi.bps.go.id/v1/api/list/model/tahun/domain/0000/var/2346/key/{API_KEY}/'
resp = requests.get(url_tahun).json()
if 'data' in resp and len(resp['data']) > 1:
    for t in resp['data'][1][:5]:
        print(f"Var 2346 Tahun ID: {t['val']} - Label: {t['label']}")
else:
    print("Var 2346 tidak punya list tahun")

url_tahun = f'https://webapi.bps.go.id/v1/api/list/model/tahun/domain/0000/var/787/key/{API_KEY}/'
resp = requests.get(url_tahun).json()
if 'data' in resp and len(resp['data']) > 1:
    for t in resp['data'][1][:5]:
        print(f"Var 787 Tahun ID: {t['val']} - Label: {t['label']}")
