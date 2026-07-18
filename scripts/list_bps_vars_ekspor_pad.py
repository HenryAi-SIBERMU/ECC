import requests
import json

API_KEY = '06fd644648629502353deaed29fc6383'

print("=== VARIABEL EKSPOR-IMPOR (SUBJEK 8) ===")
for page in range(1, 5):
    url = f'https://webapi.bps.go.id/v1/api/list/model/var/domain/0000/subject/8/page/{page}/key/{API_KEY}/'
    resp = requests.get(url).json()
    if 'data' not in resp or len(resp['data']) < 2:
        break
    vars = resp['data'][1]
    for v in vars:
        print(f"ID: {v.get('var_id')} | Nama: {v.get('title')}")

print("\n=== VARIABEL KEUANGAN (SUBJEK 13) ===")
for page in range(1, 5):
    url = f'https://webapi.bps.go.id/v1/api/list/model/var/domain/0000/subject/13/page/{page}/key/{API_KEY}/'
    resp = requests.get(url).json()
    if 'data' not in resp or len(resp['data']) < 2:
        break
    vars = resp['data'][1]
    for v in vars:
        print(f"ID: {v.get('var_id')} | Nama: {v.get('title')}")
