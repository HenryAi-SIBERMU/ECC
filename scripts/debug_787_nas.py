import requests

API_KEY = "06fd644648629502353deaed29fc6383"

# Coba domain 0000 (Nasional) - Var 787 punya vervar Kab/Kota
# Tes th 116 langsung untuk cek vervar apa yang ada
url = f"https://webapi.bps.go.id/v1/api/list/model/data/domain/0000/var/787/th/116/key/{API_KEY}/"
resp = requests.get(url).json()

print("Domain 0000 Var 787 Status:", resp.get('data-availability'))
vervars = resp.get('vervar', [])
turvars = resp.get('turvar', [])
tahuns = resp.get('tahun', [])
dc = resp.get('datacontent', {})

print(f"\nVervar ({len(vervars)} items):")
# Filter yg mengandung Sulawesi
sulawesi_vv = []
for v in vervars:
    label = str(v.get('label', ''))
    if any(k in label.lower() for k in ['sulawesi', 'sulsel', 'sulteng', 'sulut', 'sultra', 'gorontalo', 'sulbar']):
        sulawesi_vv.append(v)
        print(f"  {v['val']}: {label}")
        
print(f"\nTurvar ({len(turvars)} items):")
for t in turvars:
    print(f"  {t['val']}: {t['label']}")

print(f"\nTahun: {[t['label'] for t in tahuns]}")
print(f"\nDatacontent type: {type(dc)}, len: {len(dc) if isinstance(dc, (dict, list)) else 'N/A'}")

if isinstance(dc, dict):
    print("\nSampel datacontent:")
    for k, v in list(dc.items())[:10]:
        print(f"  {k}: {v}")
elif isinstance(dc, list) and len(dc) > 0:
    print("\nDatacontent is list, first item:", dc[0])
