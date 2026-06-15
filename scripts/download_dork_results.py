import os
import requests
from pathlib import Path
import urllib3

urllib3.disable_warnings()

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw' / 'amdal_leaks'

PDF_URLS = [
    # Global Tailings Portal context
    "https://globaltailingsreview.org/wp-content/uploads/2020/09/GTR-TZH-compendium.pdf",
    "https://www.levinsources.com/assets/pages/General-findings-deck-v5-FINAL.pdf",
    
    # AMDAL & Audits
    "https://www.fcx.com/sites/fcx/files/documents/sustainability/audits/2024-2025PTFIEnvironmentalAuditExec.pdf",
    "https://cri.org/wp-content/uploads/2024/01/The-response-of-Huayou-Cobalt.pdf",
    "https://www.fcx.com/sites/fcx/files/documents/sustainability/audits/2021-2022PTFIEnvironmentalAuditExec.pdf"
]

def download_pdfs():
    os.makedirs(RAW_DIR, exist_ok=True)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for url in PDF_URLS:
        filename = url.split('/')[-1]
        filepath = RAW_DIR / filename
        
        if filepath.exists():
            print(f"[Skip] {filename} sudah ada.")
            continue
            
        print(f"[Download] Menyedot {filename}...")
        try:
            r = requests.get(url, headers=headers, stream=True, timeout=30, verify=False)
            if r.status_code == 200:
                with open(filepath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"  -> Sukses tersimpan di data/raw/amdal_leaks/{filename}")
            else:
                print(f"  -> Gagal (HTTP {r.status_code})")
        except Exception as e:
            print(f"  -> Error: {e}")

if __name__ == "__main__":
    print(f"Memulai proses download ke folder: {RAW_DIR}")
    download_pdfs()
    print("Selesai!")
