import requests
import json

API_KEY = "06fd644648629502353deaed29fc6383"
BASE_URL = "https://webapi.bps.go.id/v1/api"
MFD_SULTENG = "7200000"

print("Memeriksa ketersediaan tabel Populasi untuk Sulawesi Tengah di BPS SIMDASI...")

# 1. Cari Table ID
table_id = None
avail_years = []
for mms_id in [519, 531, 520]:
    url = f"{BASE_URL}/interoperabilitas/datasource/simdasi/id/23/wilayah/{MFD_SULTENG}/mms_id/{mms_id}/key/{API_KEY}/"
    resp = requests.get(url).json()
    tables = resp.get("data", [{}, {}])[1].get("data", []) if len(resp.get("data", [])) > 1 else []
    for t in tables:
        j = t.get("judul", "").lower()
        if "penduduk" in j and "kabupaten" in j and ("kepadatan" in j or "pertumbuhan" in j) and "pdrb" not in j:
            table_id = t.get("id_tabel")
            avail_years = t.get("ketersediaan_tahun", [])
            break
    if table_id:
        break

print(f"Table ID: {table_id}")
print(f"Tahun yang dinyatakan 'Ada' oleh server BPS: {avail_years}")

print("\nMari kita buktikan dengan mencoba nge-PING API BPS untuk tahun 2015 (yang bolong) vs 2017 (yang ada)")

# Uji tahun 2015 (Bolong)
url_2015 = f"{BASE_URL}/interoperabilitas/datasource/simdasi/id/25/id_tabel/{table_id}/wilayah/{MFD_SULTENG}/tahun/2015/key/{API_KEY}/"
resp_2015 = requests.get(url_2015).json()
print(f"\nResponse BPS untuk tahun 2015:")
print(json.dumps({"data-availability": resp_2015.get("data-availability")}, indent=2))

# Uji tahun 2017 (Ada)
url_2017 = f"{BASE_URL}/interoperabilitas/datasource/simdasi/id/25/id_tabel/{table_id}/wilayah/{MFD_SULTENG}/tahun/2017/key/{API_KEY}/"
resp_2017 = requests.get(url_2017).json()
print(f"\nResponse BPS untuk tahun 2017:")
print(json.dumps({"data-availability": resp_2017.get("data-availability")}, indent=2))
