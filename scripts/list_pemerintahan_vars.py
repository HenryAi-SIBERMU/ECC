import requests

API_KEY = "06fd644648629502353deaed29fc6383"

# Cek semua var di Subject 101 (Pemerintahan) domain 0000
for page in range(1, 5):
    url = f"https://webapi.bps.go.id/v1/api/list/model/var/domain/0000/subject/101/page/{page}/key/{API_KEY}/"
    resp = requests.get(url).json()
    vars_list = resp.get('data', [[], []])[1] if 'data' in resp else []
    if not vars_list:
        break
    for v in vars_list:
        t = v.get('title', '')
        print(f"VAR {v.get('var_id')}: {t}")
