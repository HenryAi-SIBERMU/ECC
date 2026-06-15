import os
import csv
import shutil
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw' / 'amdal_leaks'
LOG_FILE = RAW_DIR / '_download_log.csv'
CSV_PARSED = BASE_DIR / 'data' / 'processed' / 'amdal_parsed_limbah_b3.csv'

# Kategori
ngo_domains = ['aeer.or.id', 'walhi.or.id', 'jatam.org', 'tuk.or.id', 'satyabumi.org', 'lifemosaic.net', 'cri.org', 'ti.or.id', 'theprakarsa.org', 'aji.or.id']
gov_domains = ['go.id']
academic_domains = ['ac.id', 'semanticscholar.org', 'repository']

# Buat folder baru
official_dir = RAW_DIR / 'official_amdal'
ngo_dir = RAW_DIR / 'ngo_reports'
corp_dir = RAW_DIR / 'corporate_reports'
academic_dir = RAW_DIR / 'academic_reports'
other_dir = RAW_DIR / 'other_reports'

for d in [official_dir, ngo_dir, corp_dir, academic_dir, other_dir]:
    os.makedirs(d, exist_ok=True)

# 1. Klasifikasi dari Log
file_category_map = {}

if LOG_FILE.exists():
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['status'] == 'OK':
                url = row['url']
                domain = urlparse(url).netloc.lower()
                file_name = row['file']
                
                cat = 'Other'
                target_dir = other_dir
                
                if any(gov in domain for gov in gov_domains):
                    cat = 'Official AMDAL'
                    target_dir = official_dir
                elif any(ngo in domain for ngo in ngo_domains):
                    cat = 'NGO Report'
                    target_dir = ngo_dir
                elif any(aca in domain for aca in academic_domains):
                    cat = 'Academic Report'
                    target_dir = academic_dir
                else:
                    if 'dlh.sultengprov.go.id' in domain:
                        cat = 'Official AMDAL'
                        target_dir = official_dir
                    elif 'com' in domain or 'co.id' in domain or 'net' in domain:
                        cat = 'Corporate Report'
                        target_dir = corp_dir
                        
                file_category_map[file_name] = cat
                
                # Move file
                src = RAW_DIR / file_name
                dst = target_dir / file_name
                if src.exists():
                    shutil.move(str(src), str(dst))

print(f"[*] Berhasil memindahkan file PDF ke sub-folder masing-masing kategori.")

# 2. Update CSV Parsed
if CSV_PARSED.exists():
    rows = []
    with open(CSV_PARSED, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        if 'kategori_sumber' not in fieldnames:
            fieldnames.insert(2, 'kategori_sumber') # insert after company_guess
            
        for row in reader:
            file_name = row['file']
            row['kategori_sumber'] = file_category_map.get(file_name, 'Unknown')
            rows.append(row)
            
    with open(CSV_PARSED, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"[*] Berhasil menambahkan kolom 'kategori_sumber' di CSV hasil parsing.")
else:
    print(f"[!] File {CSV_PARSED} tidak ditemukan.")
