import requests

API_KEY = "06fd644648629502353deaed29fc6383"

# Cek Var 787 di domain 7100 - apa sebenarnya
url = f"https://webapi.bps.go.id/v1/api/list/model/data/domain/7100/var/787/th/116/key/{API_KEY}/"
resp = requests.get(url).json()

print("Subject:", resp.get('subject'))
print("Var:", resp.get('var'))
print("Availability:", resp.get('data-availability'))
print("\nVervar:")
for v in resp.get('vervar', []):
    print(f"  {v['val']}: {v['label']}")
print("\nTurvar:")
for t in resp.get('turvar', []):
    print(f"  {t['val']}: {t['label']}")
print("\nDatacontent type:", type(resp.get('datacontent')))
dc = resp.get('datacontent')
if isinstance(dc, dict):
    for k, v in list(dc.items())[:5]:
        print(f"  {k}: {v}")
elif isinstance(dc, list):
    print("  [List]:", dc[:5])
