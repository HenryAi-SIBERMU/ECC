import requests

API_KEY = "06fd644648629502353deaed29fc6383"

# Data PAD ternyata ada di Domain Provinsi dengan Vervar = Kab/Kota
# Kita cek VAR 787 di domain Provinsi dan lihat breakdown-nya
domains_prov = {
    "7100": "Sulawesi Utara",
    "7200": "Sulawesi Tengah",
    "7300": "Sulawesi Selatan",
    "7400": "Sulawesi Tenggara",
    "7500": "Gorontalo",
    "7600": "Sulawesi Barat"
}

# Cek domain 7300 (Sulsel) dengan Var 787, th 116
url = f"https://webapi.bps.go.id/v1/api/list/model/data/domain/7300/var/787/th/116/key/{API_KEY}/"
resp = requests.get(url).json()

print("Domain 7300 Var 787 Status:", resp.get('data-availability', 'N/A'))
if resp.get('data-availability') == 'available':
    vervars = resp.get('vervar', [])
    turvars = resp.get('turvar', [])
    tahuns = resp.get('tahun', [])
    print(f"Vervar (baris): {len(vervars)}")
    for v in vervars[:10]:
        print(f"  {v['val']}: {v['label']}")
    print(f"Turvar (kolom): {len(turvars)}")
    for t in turvars[:5]:
        print(f"  {t['val']}: {t['label']}")
    print(f"Tahun: {[t['label'] for t in tahuns]}")
    
    # Sampel data
    dc = resp.get('datacontent', {})
    print(f"\nSampel datacontent ({len(dc)} keys):")
    for k, v in list(dc.items())[:5]:
        print(f"  {k}: {v}")
