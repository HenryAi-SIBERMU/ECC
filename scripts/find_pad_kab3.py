import requests

API_KEY = "06fd644648629502353deaed29fc6383"

# Cek Subject 101 (Pemerintahan)
url_var = f"https://webapi.bps.go.id/v1/api/list/model/var/domain/7301/subject/101/key/{API_KEY}/"
resp = requests.get(url_var).json()
vars_list = resp.get('data', [[], []])[1] if 'data' in resp else []
print(f"Subject Pemerintahan (101) - Domain 7301:")
for v in vars_list:
    print(f"  Var {v.get('var_id')}: {v.get('title')}")

# Cari keyword PAD
for v in vars_list:
    t = v.get('title', '').lower()
    if any(k in t for k in ['pad', 'pendapatan', 'anggaran', 'apbd', 'penerimaan']):
        print(f"\nFOUND: Var {v.get('var_id')}: {v.get('title')}")
        
        # Cek data untuk Var yang ditemukan
        var_id = v.get('var_id')
        url_data = f"https://webapi.bps.go.id/v1/api/list/model/data/domain/7301/var/{var_id}/th/116/key/{API_KEY}/"
        data_resp = requests.get(url_data).json()
        print(f"  Data availability: {data_resp.get('data-availability', 'N/A')}")
