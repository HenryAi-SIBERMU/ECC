import requests

API_KEY = "06fd644648629502353deaed29fc6383"

# Var 787 di domain 7100 = Akses Internet, BUKAN PAD!
# Kita perlu cari Var ID yang benar untuk PAD di domain Nasional (0000)
# Di domain 0000, Var 787 = "Realisasi Penerimaan Pemerintah Kabupaten/Kota" - ini yang benar!

# Mari cari subject "Keuangan" di domain 0000 dan list semua var-nya yang terkait PAD
url_sub = f"https://webapi.bps.go.id/v1/api/list/model/subject/domain/0000/key/{API_KEY}/"
resp = requests.get(url_sub).json()
subs = resp.get('data', [[], []])[1] if 'data' in resp else []

keuangan_sub = None
for s in subs:
    t = s.get('title', '').lower()
    if 'keuangan' in t or 'fiskal' in t or 'apbd' in t or 'pemerintah daerah' in t:
        print(f"Sub {s.get('sub_id')}: {s.get('title')}")
        keuangan_sub = s.get('sub_id')

print(f"\n--- Cari semua Var di Subject Keuangan ({keuangan_sub}) ---")
if keuangan_sub:
    url_var = f"https://webapi.bps.go.id/v1/api/list/model/var/domain/0000/subject/{keuangan_sub}/key/{API_KEY}/"
    resp2 = requests.get(url_var).json()
    vars_list = resp2.get('data', [[], []])[1] if 'data' in resp2 else []
    for v in vars_list:
        t = v.get('title', '')
        if any(k in t.lower() for k in ['pad', 'pendapatan', 'apbd', 'anggaran', 'penerimaan']):
            print(f"  VAR {v.get('var_id')}: {t}")
