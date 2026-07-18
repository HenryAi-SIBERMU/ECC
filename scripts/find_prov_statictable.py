import requests

API_KEY = "06fd644648629502353deaed29fc6383"

# Coba static table per Provinsi - cari di domain provinsi Sulawesi
# Cek domain 7300 (Sulsel) untuk tabel statis ekspor
domains_to_check = {
    "7300": "Sulawesi Selatan",
    "7200": "Sulawesi Tengah",
    "7100": "Sulawesi Utara"
}

keywords_ekspor = ['ekspor', 'export', 'perdagangan luar']
keywords_pad = ['pad', 'pendapatan asli', 'apbd', 'keuangan daerah', 'realisasi']

for dom_id, dom_name in domains_to_check.items():
    print(f"\n=== {dom_name} (Domain {dom_id}) ===")
    for page in range(1, 4):
        url = f"https://webapi.bps.go.id/v1/api/list/model/statictable/domain/{dom_id}/page/{page}/key/{API_KEY}/"
        try:
            resp = requests.get(url, timeout=15).json()
            tables = resp.get('data', [[], []])[1] if 'data' in resp else []
            if not tables:
                break
            for t in tables:
                title = t.get('title', '').lower()
                if any(k in title for k in keywords_ekspor + keywords_pad):
                    print(f"  [TABLE {t.get('table_id')}] {t.get('title')}")
        except Exception as e:
            print(f"  Error: {e}")
            break
    break  # Test 1 domain dulu
