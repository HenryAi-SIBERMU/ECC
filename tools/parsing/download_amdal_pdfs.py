"""
Download AMDAL PDFs
===================
Membaca hasil dorking dari amdal_dork_results.csv,
lalu mengunduh semua PDF yang ditemukan ke folder:
    data/raw/amdal_leaks/

Usage:
    python tools/parsing/download_amdal_pdfs.py
"""

import os
import csv
import time
import hashlib
import requests
import urllib3
from pathlib import Path

urllib3.disable_warnings()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
INPUT_CSV = BASE_DIR / 'data' / 'processed' / 'amdal_dork_results.csv'
OUTPUT_DIR = BASE_DIR / 'data' / 'raw' / 'amdal_leaks'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def make_safe_filename(url, company):
    """Generate a safe filename from company name + URL hash."""
    url_hash = hashlib.md5(url.encode()).hexdigest()[:6]
    safe_company = "".join(c for c in company if c.isalnum() or c in (' ', '_')).strip()
    safe_company = safe_company[:40].replace(' ', '_')
    return f"{safe_company}_{url_hash}.pdf"

def download_pdfs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if not INPUT_CSV.exists():
        print(f"[!] File input tidak ditemukan: {INPUT_CSV}")
        return

    log_file = OUTPUT_DIR / '_download_log.csv'
    downloaded = []
    skipped = []
    failed = []

    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [r for r in reader if r.get('pdf_link') and r['pdf_link'].strip().startswith('http')]

    print(f"[*] Ditemukan {len(rows)} URL PDF yang valid dari hasil dorking.")
    print(f"[*] Target folder: {OUTPUT_DIR}\n")

    for i, row in enumerate(rows, 1):
        url = row['pdf_link'].strip()
        company = row.get('nama_perusahaan', 'UNKNOWN')
        filename = make_safe_filename(url, company)
        filepath = OUTPUT_DIR / filename

        if filepath.exists():
            print(f"[{i}/{len(rows)}] Skip (sudah ada): {filename}")
            skipped.append({'company': company, 'url': url, 'file': filename, 'status': 'SKIP'})
            continue

        print(f"[{i}/{len(rows)}] Mengunduh untuk: {company}")
        print(f"    URL: {url}")

        try:
            resp = requests.get(url, headers=HEADERS, stream=True, timeout=30, verify=False)
            if resp.status_code == 200 and 'pdf' in resp.headers.get('content-type', '').lower():
                with open(filepath, 'wb') as out:
                    for chunk in resp.iter_content(8192):
                        out.write(chunk)
                size_kb = filepath.stat().st_size // 1024
                print(f"    -> OK ({size_kb} KB) disimpan sebagai: {filename}")
                downloaded.append({'company': company, 'url': url, 'file': filename, 'status': 'OK'})
            else:
                print(f"    -> Lewati (bukan PDF atau HTTP {resp.status_code})")
                failed.append({'company': company, 'url': url, 'file': '', 'status': f'HTTP_{resp.status_code}'})
        except Exception as e:
            print(f"    -> Gagal: {e}")
            failed.append({'company': company, 'url': url, 'file': '', 'status': f'ERROR'})

        time.sleep(1)  # jeda agar tidak diblokir

    # Tulis log
    with open(log_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['company', 'url', 'file', 'status'])
        writer.writeheader()
        writer.writerows(downloaded + skipped + failed)

    print(f"\n{'='*50}")
    print(f"[SELESAI] Berhasil: {len(downloaded)} | Lewati: {len(skipped)} | Gagal: {len(failed)}")
    print(f"[LOG] Disimpan di: {log_file}")

if __name__ == "__main__":
    download_pdfs()
