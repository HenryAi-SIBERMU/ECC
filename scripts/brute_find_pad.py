import requests

API_KEY = "06fd644648629502353deaed29fc6383"

# Var 787 di domain 0000 = Realisasi Penerimaan Pemerintah Kabupaten/Kota
# Vervar = kategori (bukan provinsi) - hanya ada 14 baris = 14 kategori = data nasional agregat

# Cari VAR PAD yang punya vervar PROVINSI/KABUPATEN
# Coba search kata kunci PAD, pendapatan, realisasi
keywords = ['787', '788', '789', '790', '791', '792']

for var_id in range(780, 800):
    url = f"https://webapi.bps.go.id/v1/api/list/model/data/domain/0000/var/{var_id}/th/116/key/{API_KEY}/"
    try:
        resp = requests.get(url, timeout=15).json()
        if isinstance(resp, dict) and resp.get('data-availability') == 'available':
            var_info = resp.get('var', [{}])
            var_label = var_info[0].get('label', '') if var_info else ''
            vervars = resp.get('vervar', [])
            print(f"VAR {var_id} '{var_label}': {len(vervars)} vervar")
            if len(vervars) > 10:
                print(f"  Sample vervar: {vervars[0]['label']}, {vervars[1]['label'] if len(vervars) > 1 else ''}")
    except:
        pass
