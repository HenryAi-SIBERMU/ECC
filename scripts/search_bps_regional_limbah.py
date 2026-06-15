import requests
import json

domains = [
    ("Sulawesi Utara", "7100"),
    ("Sulawesi Tengah", "7200"),
    ("Sulawesi Selatan", "7300"),
    ("Sulawesi Tenggara", "7400"),
    ("Gorontalo", "7500"),
    ("Sulawesi Barat", "7600")
]

keywords = ["limbah", "b3", "sampah", "beracun", "industri"]
# BPS API static table key
key = "82a7a4212555c82ff19fc1b47659a848"

print("Scanning BPS Regional API for Limbah B3...")
for prov, code in domains:
    found_any = False
    for kw in keywords:
        url = f"https://webapi.bps.go.id/v1/api/list/model/statictable/lang/ind/domain/{code}/keyword/{kw}/key/{key}/"
        try:
            resp = requests.get(url, verify=False, timeout=5)
            data = resp.json()
            if 'data' in data and data['data'] and isinstance(data['data'], list) and len(data['data']) > 1:
                tables = data['data'][1]
                for p in tables:
                    title = p['title'].lower()
                    if 'limbah' in title or 'b3' in title or 'beracun' in title:
                        print(f"[{prov}] ID={p['table_id']} | {p['title']}")
                        found_any = True
        except Exception as e:
            pass
    if not found_any:
        print(f"[{prov}] Tidak ditemukan tabel limbah.")

