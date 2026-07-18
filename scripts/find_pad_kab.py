import requests

API_KEY = "06fd644648629502353deaed29fc6383"

# Cari Var ID yang ada PAD/keuangan di domain kab/kota
test_domains = {
    "7301": "Kab. Kepulauan Selayar (Sulsel)",
    "7306": "Kab. Gowa (Sulsel)",
    "7201": "Kab. Banggai Kepulauan (Sulteng)",
    "7101": "Kab. Bolaang Mongondow (Sulut)"
}

print("=== Cari subject di setiap Kab/Kota ===")
for dom_id, dom_name in test_domains.items():
    print(f"\n[Domain {dom_id}] {dom_name}")
    url_sub = f"https://webapi.bps.go.id/v1/api/list/model/subject/domain/{dom_id}/key/{API_KEY}/"
    subs = requests.get(url_sub).json().get('data', [[], []])[1]
    for s in subs:
        title = s.get('title', '').lower()
        if any(k in title for k in ['keuangan', 'pad', 'anggaran', 'pendapatan', 'apbd', 'fiskal']):
            print(f"  -> Sub {s.get('sub_id')}: {s.get('title')}")
    break  # Test satu dulu
