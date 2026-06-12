import requests
import json

API_KEY = '06fd644648629502353deaed29fc6383'

print("=== DAFTAR SEMUA SUBJECT BPS NASIONAL ===")
for page in range(1, 10):
    url_sub = f'https://webapi.bps.go.id/v1/api/list/model/subject/domain/0000/page/{page}/key/{API_KEY}/'
    resp = requests.get(url_sub).json()
    if 'data' not in resp or len(resp['data']) < 2:
        break
    subs = resp['data'][1]
    for s in subs:
        print(f"ID: {s.get('sub_id')} | Nama: {s.get('title')}")
