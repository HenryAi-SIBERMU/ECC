import requests

API_KEY = "06fd644648629502353deaed29fc6383"

# Tampilkan SEMUA Subject di domain 0000
url_sub = f"https://webapi.bps.go.id/v1/api/list/model/subject/domain/0000/key/{API_KEY}/"
resp = requests.get(url_sub).json()
subs = resp.get('data', [[], []])[1] if 'data' in resp else []

print(f"Total Subject di domain 0000: {len(subs)}")
for s in subs:
    print(f"  Sub {s.get('sub_id')}: {s.get('title')}")
