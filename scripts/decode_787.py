import requests

API_KEY = "06fd644648629502353deaed29fc6383"

url = f"https://webapi.bps.go.id/v1/api/list/model/data/domain/0000/var/787/th/116/key/{API_KEY}/"
resp = requests.get(url).json()

vervars = resp.get('vervar', [])
turvars = resp.get('turvar', [])
tahuns = resp.get('tahun', [])
dc = resp.get('datacontent', {})

print(f"Semua Vervar ({len(vervars)} items):")
for v in vervars:
    print(f"  Val={v['val']}: {v['label']}")

print(f"\nDatacontent:")
for k, val in dc.items():
    # Coba decode: key = vervar_val + var_id + turvar_val + tahun_val + turtahun
    # key 678701160: 6 = vervar, 787 = var, 0 = turvar, 116 = tahun, 0 = turtahun
    print(f"  Key={k}, Val={val:,}")
