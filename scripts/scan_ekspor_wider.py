import requests

API_KEY = "06fd644648629502353deaed29fc6383"

# Scan lebih luas untuk Ekspor per Provinsi - coba range 2000-2500
print("=== SCAN VAR 1500-2500 CARI EKSPOR PER PROVINSI ===")

for var_id in list(range(1500, 1560)) + list(range(2000, 2060)) + list(range(2300, 2400)):
    url = f"https://webapi.bps.go.id/v1/api/list/model/data/domain/0000/var/{var_id}/th/116/key/{API_KEY}/"
    try:
        resp = requests.get(url, timeout=8).json()
        if isinstance(resp, dict) and resp.get('data-availability') == 'available':
            var_info = resp.get('var', [{}])
            var_label = var_info[0].get('label', '') if var_info else ''
            vervars = resp.get('vervar', [])
            if len(vervars) >= 30 and any(k in var_label.lower() for k in ['ekspor', 'export', 'perdagang']):
                print(f"VAR {var_id} [{len(vervars)} prov]: {var_label}")
    except:
        pass
    
print("Scan selesai!")
