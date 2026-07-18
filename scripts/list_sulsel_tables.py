import requests

API_KEY = "06fd644648629502353deaed29fc6383"

# Cari semua tabel statis di Sulsel (7300) - tampilkan semua
domain = "7300"
all_tables = []

for page in range(1, 20):
    url = f"https://webapi.bps.go.id/v1/api/list/model/statictable/domain/{domain}/page/{page}/key/{API_KEY}/"
    try:
        resp = requests.get(url, timeout=15).json()
        tables = resp.get('data', [[], []])[1] if 'data' in resp else []
        if not tables:
            print(f"Stop di halaman {page}")
            break
        all_tables.extend(tables)
    except Exception as e:
        print(f"Error: {e}")
        break

print(f"Total tabel di Sulsel: {len(all_tables)}")
print("\n--- Tabel yang relevan ---")
keys = ['ekspor', 'impor', 'perdagang', 'pad', 'pendapatan asli', 'apbd', 'keuangan', 'realisasi', 'investasi', 'nikel', 'tambang', 'pertambangan']
for t in all_tables:
    title = t.get('title', '').lower()
    if any(k in title for k in keys):
        print(f"[{t.get('table_id')}] {t.get('title')}")
