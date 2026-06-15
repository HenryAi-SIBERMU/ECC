import os
import requests
from pathlib import Path
import pdfplumber
import re
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw' / 'ngo_reports'

URLS = {
    'ARKL_Morowali.pdf': 'https://www.tuk.or.id/wp-content/uploads/buku-arkl-morowali-full-report.pdf',
    'AEER_HPAL_Tantangan.pdf': 'https://www.aeer.or.id/wp-content/uploads/2023/07/Teknologi-HPAL-Dalam-Industri-Nikel-Tantangan-Baru-bagi-Lingkungan-di-Indonesia.pdf'
}

def download_pdfs():
    os.makedirs(RAW_DIR, exist_ok=True)
    for filename, url in URLS.items():
        filepath = RAW_DIR / filename
        if not filepath.exists():
            print(f"Downloading {filename}...")
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                r = requests.get(url, headers=headers, stream=True, timeout=30, verify=False)
                if r.status_code == 200:
                    with open(filepath, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"Downloaded {filename}")
                else:
                    print(f"Failed to download {filename}: HTTP {r.status_code}")
            except Exception as e:
                print(f"Error downloading {filename}: {e}")
        else:
            print(f"Skipped {filename}, already exists.")

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings()
    download_pdfs()
