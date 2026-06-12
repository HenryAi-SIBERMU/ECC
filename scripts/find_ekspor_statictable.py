import requests

API_KEY = "06fd644648629502353deaed29fc6383"

# BPS punya endpoint statictable untuk tabel-tabel yang dipublish di website
# Cari tabel statis dengan keyword ekspor

keywords = ['ekspor', 'export', 'perdagangan luar negeri']

for page in range(1, 6):
    url = f"https://webapi.bps.go.id/v1/api/list/model/statictable/domain/0000/page/{page}/key/{API_KEY}/"
    try:
        resp = requests.get(url, timeout=15).json()
        tables = resp.get('data', [[], []])[1] if 'data' in resp else []
        if not tables:
            print(f"Halaman {page}: kosong, stop.")
            break
        for t in tables:
            title = t.get('title', '').lower()
            if any(k in title for k in keywords):
                print(f"[TABLE {t.get('table_id')}] {t.get('title')}")
    except Exception as e:
        print(f"Error halaman {page}: {e}")
        break

print("\nDone.")
