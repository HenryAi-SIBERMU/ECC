import requests
import json

BASE_URL = "https://webapi.bps.go.id/v1/api"
API_KEY = "06fd644648629502353deaed29fc6383"
mfd = "7200000"

# mms_ids for Kesehatan (522), Lingkungan (539), Pemukiman dan Perumahan (525)
target_mms = [522, 539, 525, 563]

for mms_id in target_mms:
    print(f"\n--- Fetching tables for MMS ID: {mms_id} ---")
    url = f"{BASE_URL}/interoperabilitas/datasource/simdasi/id/23/wilayah/{mfd}/mms_id/{mms_id}/key/{API_KEY}/"
    try:
        resp = requests.get(url, timeout=10).json()
        
        tables = []
        for item in resp.get("data", []):
            if isinstance(item, dict) and "data" in item:
                tables = item["data"]
        
        for t in tables:
            judul = t.get("judul", "").lower()
            if "diare" in judul or "ispa" in judul or "pencemaran" in judul or "kesehatan" in judul or "air" in judul or "desa" in judul:
                print(f"[{t.get('id_tabel')}] {t.get('judul')} (Level: {t.get('tingkat_penyajian')})")
    except Exception as e:
        print(e)
