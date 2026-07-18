import os
import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Konfigurasi
URL_API = 'https://opendata.sulutprov.go.id/api/3/action/package_search'
QUERY = 'kualitas air'
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'raw', 'sulut_kualitas_air')

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print(f"Mencari dataset dengan query: '{QUERY}' di Open Data Sulut...")

try:
    response = requests.get(f"{URL_API}?q={requests.utils.quote(QUERY)}&rows=100", verify=False, timeout=15)
    response.raise_for_status()
    data = response.json()
except Exception as e:
    print(f"Gagal memanggil API: {e}")
    exit(1)

results = data.get('result', {}).get('results', [])
count = data.get('result', {}).get('count', 0)
print(f"Ditemukan {count} dataset.")

downloaded = 0
for idx, dataset in enumerate(results, start=1):
    title = dataset.get('title', f"dataset_{idx}")
    # Bersihkan nama file
    safe_title = "".join([c if c.isalnum() or c in [' ', '-'] else '_' for c in title]).strip()
    
    resources = dataset.get('resources', [])
    for res_idx, res in enumerate(resources, start=1):
        file_url = res.get('url')
        file_format = res.get('format', '').lower()
        if not file_format:
            file_format = file_url.split('.')[-1] if '.' in file_url else 'csv'
            
        filename = f"{safe_title}_{res_idx}.{file_format}"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        print(f"[{idx}/{count}] Mendownload: {filename} ...")
        try:
            r_file = requests.get(file_url, verify=False, timeout=20)
            r_file.raise_for_status()
            with open(filepath, 'wb') as f:
                f.write(r_file.content)
            downloaded += 1
            print(f"  -> Sukses tersimpan ({len(r_file.content)} bytes)")
        except Exception as e:
            print(f"  -> Gagal mendownload {file_url}: {e}")

print(f"Selesai! Total file yang didownload: {downloaded}")
