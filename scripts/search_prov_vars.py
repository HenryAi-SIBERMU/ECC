import requests

API_KEY = '06fd644648629502353deaed29fc6383'

# Cari subjek di Sulsel (7300)
url_sub = f'https://webapi.bps.go.id/v1/api/list/model/subject/domain/7300/key/{API_KEY}/'
subs = requests.get(url_sub).json().get('data', [[], []])[1]

sub_keuangan = None
sub_ekspor = None

for s in subs:
    title = s.get('title', '').lower()
    if 'keuangan' in title or 'pad' in title:
        sub_keuangan = s.get('sub_id')
    if 'ekspor' in title or 'impor' in title:
        sub_ekspor = s.get('sub_id')

print(f"Sulsel Subjek Keuangan: {sub_keuangan}, Ekspor: {sub_ekspor}")

def print_vars(sub_id, domain='7300'):
    if not sub_id: return
    for page in range(1, 3):
        url = f'https://webapi.bps.go.id/v1/api/list/model/var/domain/{domain}/subject/{sub_id}/page/{page}/key/{API_KEY}/'
        resp = requests.get(url).json()
        if 'data' in resp and len(resp['data']) > 1:
            for v in resp['data'][1]:
                print(f"Var {v.get('var_id')}: {v.get('title')}")

print("\n--- VAR KEUANGAN SULSEL ---")
print_vars(sub_keuangan)

print("\n--- VAR EKSPOR SULSEL ---")
print_vars(sub_ekspor)
