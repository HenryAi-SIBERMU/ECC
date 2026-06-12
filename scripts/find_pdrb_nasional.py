import requests

API_KEY = "06fd644648629502353deaed29fc6383"

print("Cari Var PDRB di Domain 0000")
for p in range(1, 10):
    url = f"https://webapi.bps.go.id/v1/api/list/model/var/domain/0000/page/{p}/key/{API_KEY}/"
    try:
        resp = requests.get(url).json()
        if 'data' in resp and len(resp['data']) > 1:
            for v in resp['data'][1]:
                t = v.get('title', '').lower()
                if 'pdrb' in t and 'lapangan usaha' in t:
                    print(v.get('var_id'), v.get('title'))
    except: pass
