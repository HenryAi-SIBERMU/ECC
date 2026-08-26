import requests
import json

API_KEY = "06fd644648629502353deaed29fc6383"
BASE_URL = "https://webapi.bps.go.id/v1/api"
MFD_SULTENG = "7200000"

table_id = "WVRlTTcySlZDa3lUcFp6czNwbHl4QT09"

url_2015 = f"{BASE_URL}/interoperabilitas/datasource/simdasi/id/25/id_tabel/{table_id}/wilayah/{MFD_SULTENG}/tahun/2015/key/{API_KEY}/"
resp_2015 = requests.get(url_2015).json()

# Let's see if there is actually any DATA for Morowali in 2015, or just empty structure
data_arr = resp_2015.get("data", [])
print(f"Jumlah elemen dalam 'data': {len(data_arr)}")

has_morowali = False
if len(data_arr) > 1:
    rows = data_arr[1].get("data", [])
    print(f"Total baris (kab/kota) di tahun 2015: {len(rows)}")
    for r in rows:
        label = str(r.get("label", "")).lower()
        if "morowali" in label:
            has_morowali = True
            print(f"Found {label}: {json.dumps(r.get('variables', {}), indent=2)}")

if not has_morowali:
    print("Morowali TIDAK ADA di data 2015 BPS, meskipun status API bilang 'available'.")
