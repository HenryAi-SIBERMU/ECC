import csv
from urllib.parse import urlparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / 'data' / 'raw' / 'amdal_leaks' / '_download_log.csv'
OUTPUT_MD = BASE_DIR / 'scratch' / 'pdf_classification.md'

ngo_domains = ['aeer.or.id', 'walhi.or.id', 'jatam.org', 'tuk.or.id', 'satyabumi.org', 'lifemosaic.net', 'cri.org', 'ti.or.id', 'theprakarsa.org']
gov_domains = ['go.id']
academic_domains = ['ac.id', 'semanticscholar.org', 'repository']

official_amdal_files = []
ngo_files = []
corporate_files = []
academic_files = []
other_files = []

with open(LOG_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['status'] == 'OK':
            url = row['url']
            domain = urlparse(url).netloc.lower()
            file_name = row['file']
            company = row['company']

            # Determine category
            if any(gov in domain for gov in gov_domains):
                official_amdal_files.append((file_name, company, domain, url))
            elif any(ngo in domain for ngo in ngo_domains):
                ngo_files.append((file_name, company, domain, url))
            elif any(aca in domain for aca in academic_domains):
                academic_files.append((file_name, company, domain, url))
            else:
                # Assume corporate or other
                if 'dlh.sultengprov.go.id' in domain: # double check
                    official_amdal_files.append((file_name, company, domain, url))
                elif 'com' in domain or 'co.id' in domain or 'net' in domain:
                    corporate_files.append((file_name, company, domain, url))
                else:
                    other_files.append((file_name, company, domain, url))

with open(OUTPUT_MD, 'w', encoding='utf-8') as f:
    f.write("# Klasifikasi Dokumen Hasil Dorking\n\n")
    
    f.write("## 1. Official AMDAL / Dokumen Pemerintah (go.id)\n")
    for file, comp, dom, url in official_amdal_files:
        f.write(f"- **{file}** ({comp}) - Sumber: {dom}\n")
        
    f.write("\n## 2. Laporan NGO / LSM\n")
    for file, comp, dom, url in ngo_files:
        f.write(f"- **{file}** ({comp}) - Sumber: {dom}\n")
        
    f.write("\n## 3. Laporan Perusahaan (Corporate/Audit/ESG)\n")
    for file, comp, dom, url in corporate_files:
        f.write(f"- **{file}** ({comp}) - Sumber: {dom}\n")
        
    f.write("\n## 4. Akademis / Jurnal\n")
    for file, comp, dom, url in academic_files:
        f.write(f"- **{file}** ({comp}) - Sumber: {dom}\n")
        
    f.write("\n## 5. Lainnya\n")
    for file, comp, dom, url in other_files:
        f.write(f"- **{file}** ({comp}) - Sumber: {dom}\n")

print(f"Classification saved to {OUTPUT_MD}")
