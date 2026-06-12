import requests

API_KEY = "06fd644648629502353deaed29fc6383"

# Tampilkan semua subject di Kab. Selayar
url_sub = f"https://webapi.bps.go.id/v1/api/list/model/subject/domain/7301/key/{API_KEY}/"
subs = requests.get(url_sub).json().get('data', [[], []])[1]
print(f"Total Subject di domain 7301: {len(subs)}")
for s in subs:
    print(f"  Sub {s.get('sub_id')}: {s.get('title')}")

# Coba cari variabel di subject pertama
print("\n=== COBA AMBIL VARIABEL DI SETIAP SUBJECT ===")
for s in subs[:5]:
    sub_id = s.get('sub_id')
    sub_title = s.get('title')
    url_var = f"https://webapi.bps.go.id/v1/api/list/model/var/domain/7301/subject/{sub_id}/key/{API_KEY}/"
    vars_resp = requests.get(url_var).json()
    vars_list = vars_resp.get('data', [[], []])[1] if 'data' in vars_resp else []
    if vars_list:
        print(f"\nSubject {sub_id} ({sub_title}):")
        for v in vars_list[:3]:
            print(f"  Var {v.get('var_id')}: {v.get('title')}")
