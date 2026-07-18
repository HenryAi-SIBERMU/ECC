import requests
import json

print("Scanning Open Data Sulawesi Utara (CKAN) untuk Limbah B3...")
url = "https://opendata.sulutprov.go.id/api/3/action/package_search"
params = {'q': 'limbah'}
try:
    resp = requests.get(url, params=params, verify=False, timeout=10)
    data = resp.json()
    if data.get('success'):
        results = data['result']['results']
        if results:
            for r in results:
                print(f"Dataset Ditemukan: {r.get('title')} | Organisasi: {r.get('organization', {}).get('title')}")
                for res in r.get('resources', []):
                    print(f"  - File: {res.get('name')} ({res.get('format')}) -> {res.get('url')}")
        else:
            print("Tidak ada dataset limbah di Open Data Sulut.")
    else:
        print("API Sulut merespons error.")
except Exception as e:
    print("Error akses Open Data Sulut:", e)

print("\nScanning Open Data Gorontalo (CKAN)...")
url2 = "https://data.gorontaloprov.go.id/api/3/action/package_search"
try:
    resp2 = requests.get(url2, params=params, verify=False, timeout=10)
    data2 = resp2.json()
    if data2.get('success'):
        results = data2['result']['results']
        if results:
            for r in results:
                print(f"Dataset Ditemukan: {r.get('title')} | Organisasi: {r.get('organization', {}).get('title')}")
        else:
            print("Tidak ada dataset limbah di Open Data Gorontalo.")
except Exception as e:
    print("Error akses Open Data Gorontalo:", e)
