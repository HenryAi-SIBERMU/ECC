import requests
import json

BASE_URL = "https://webapi.bps.go.id/v1/api"
API_KEY = "06fd644648629502353deaed29fc6383"
mfd = "7200000"
sub_id = "Z2I4TjdNeVZqbkMyaTFCZVhBVkE4QT09"
table_id = "TEptbDV0QlRORVl6cjl0THhMbk02Zz09"

url_data = f"{BASE_URL}/interoperabilitas/datasource/simdasi/id/24/wilayah/{mfd}/id_subjek/{sub_id}/tabel/{table_id}/tahun/2023/key/{API_KEY}/"
resp = requests.get(url_data, timeout=10).json()
print("Status:", resp.get("status"))
if resp.get("status") == "OK":
    with open("scratch_simdasi_data.json", "w") as f:
        json.dump(resp, f, indent=2)
    print("Data dumped to scratch_simdasi_data.json")
