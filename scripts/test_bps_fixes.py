import requests

API_KEY = "06fd644648629502353deaed29fc6383"

print("--- CEK DOMAIN ---")
url_domain = f"https://webapi.bps.go.id/v1/api/domain/type/all/key/{API_KEY}/"
resp = requests.get(url_domain).json()
print("Domain status:", resp.get("status"))
if 'data' in resp and len(resp['data']) > 1:
    print("Jumlah domain:", len(resp['data'][1]))

print("\n--- CEK EKSPOR TANPA TH ---")
url_eks = f"https://webapi.bps.go.id/v1/api/list/model/data/domain/0000/var/2346/key/{API_KEY}/"
resp_eks = requests.get(url_eks).json()
print("Ekspor status:", resp_eks.get("status"))
if resp_eks.get('data-availability') == 'available':
    print("Data Tersedia!")
    datacontent = resp_eks.get('data', [[], []])[1].get('datacontent', {})
    print("Jumlah data:", len(datacontent))
else:
    print("Message:", resp_eks.get('message'))
