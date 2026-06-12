import requests
import json

API_KEY = '06fd644648629502353deaed29fc6383'

# 1. Get all subjects
url_sub = f'https://webapi.bps.go.id/v1/api/list/model/subject/domain/0000/key/{API_KEY}/'
subs_data = requests.get(url_sub).json().get('data', [])
subs = subs_data[1] if len(subs_data) > 1 else []

print("=== SUBJECTS TERKAIT EKSPOR / PAD ===")
sub_ids = []
for s in subs:
    title = s.get('title', '').lower()
    if 'ekspor' in title or 'impor' in title or 'perdagangan' in title or 'pendapatan' in title or 'keuangan' in title or 'pad' in title or 'pdrb' in title:
        print(f"Subjek ID: {s.get('sub_id')}, Nama: {s.get('title')}")
        sub_ids.append(s.get('sub_id'))

# 2. Get variables for those subjects
print("\n=== VARIABEL TERKAIT ===")
for sub_id in sub_ids:
    # Paginate variables? Usually 1 page has 10 vars. Better query page 1 to 5.
    for page in range(1, 4):
        url_var = f'https://webapi.bps.go.id/v1/api/list/model/var/domain/0000/subject/{sub_id}/page/{page}/key/{API_KEY}/'
        resp = requests.get(url_var).json()
        if 'data' not in resp or len(resp['data']) < 2:
            break
        vars_resp = resp['data'][1]
        for v in vars_resp:
            title = v.get('title', '').lower()
            if 'ekspor' in title or 'pad' in title or 'pendapatan asli daerah' in title or 'pdrb' in title:
                print(f"[Subjek {sub_id}] Var ID: {v.get('var_id')}, Nama: {v.get('title')}")
