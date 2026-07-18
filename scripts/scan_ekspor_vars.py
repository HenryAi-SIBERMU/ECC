import requests

API_KEY = "06fd644648629502353deaed29fc6383"

# Temukan semua variabel Ekspor per Provinsi sekitar range VAR 793-900
print("=== SCAN VARIABEL EKSPOR PER PROVINSI ===")
SULAWESI_KEYWORDS = ['sulawesi', 'ekspor', 'impor', 'perdagangan', 'export']

interesting = []
for var_id in range(793, 850):
    url = f"https://webapi.bps.go.id/v1/api/list/model/data/domain/0000/var/{var_id}/th/116/key/{API_KEY}/"
    try:
        resp = requests.get(url, timeout=10).json()
        if isinstance(resp, dict) and resp.get('data-availability') == 'available':
            var_info = resp.get('var', [{}])
            var_label = var_info[0].get('label', '') if var_info else ''
            vervars = resp.get('vervar', [])
            # Yang punya provinsi sebagai vervar (>30 vervar)
            if len(vervars) >= 30:
                interesting.append({'var_id': var_id, 'label': var_label, 'vervar_count': len(vervars)})
                print(f"VAR {var_id} [{len(vervars)} prov]: {var_label}")
    except Exception as e:
        pass

print(f"\nTotal variabel dengan breakdown provinsi: {len(interesting)}")
