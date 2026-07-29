import requests
import json

BASE_URL = "https://webapi.bps.go.id/v1/api"
API_KEY = "06fd644648629502353deaed29fc6383"
mfd = "7200000"

url_sub = f"{BASE_URL}/interoperabilitas/datasource/simdasi/id/22/wilayah/{mfd}/key/{API_KEY}/"
resp = requests.get(url_sub, timeout=10).json()

# Dump response to see it
with open("scratch_simdasi_resp.json", "w") as f:
    json.dump(resp, f, indent=2)

subjects = []
for item in resp.get("data", []):
    if isinstance(item, list):
        subjects.extend(item)

for sub in subjects:
    name = sub.get("subject", "").lower()
    print(f"Subjek: {sub.get('subject')} (ID: {sub.get('id')})")
