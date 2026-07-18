#!/usr/bin/env python3
"""
Google Dorking untuk mencari data IKU historis (2014-2018)
Target: SLHI lama, publikasi BPS, portal archive
"""

import requests
import time
from pathlib import Path

print("="*70)
print("🔍 Google Dorking - IKU Historical Data (2014-2018)")
print("="*70)

# Query list
queries = [
    # SLHI Official
    '"Status Lingkungan Hidup Indonesia" 2014 filetype:pdf',
    '"Status Lingkungan Hidup Indonesia" 2015 filetype:pdf',
    '"Status Lingkungan Hidup Indonesia" 2016 filetype:pdf',
    '"SLHI" 2014 "indeks kualitas udara" filetype:pdf',
    '"SLHI" 2015 "indeks kualitas udara" filetype:pdf',
    '"SLHI" 2016 "indeks kualitas udara" filetype:pdf',
    
    # SLHI + BPS Domain
    'site:bps.go.id "SLHI" 2014 filetype:pdf',
    'site:bps.go.id "SLHI" 2015 filetype:pdf',
    'site:bps.go.id "SLHI" 2016 filetype:pdf',
    'site:archive.bps.go.id "Status Lingkungan Hidup" 2014..2016',
    
    # BPS Provinsi Sulawesi
    'site:sulutprov.bps.go.id "indeks kualitas udara" 2014..2018',
    'site:sultengprov.bps.go.id "kualitas udara" 2014..2018',
    'site:sulsel.bps.go.id "IKU" 2014..2018',
    'site:sultraprov.bps.go.id "lingkungan hidup" 2014..2018',
    'site:gorontaloprov.bps.go.id "IKLH" 2014..2018',
    
    # Archive.org
    'site:web.archive.org "iklh.menlhk.go.id" "sulawesi"',
    'site:web.archive.org inurl:bps.go.id "indeks kualitas udara"',
    
    # Data Terbuka
    'site:data.go.id "kualitas udara" "sulawesi" 2014..2018',
    'site:satu-data.go.id "indeks kualitas udara" 2014..2018',
]

output_file = Path('docs/DORKING_RESULTS_IKU_HISTORICAL.md')

with open(output_file, 'w', encoding='utf-8') as f:
    f.write('# Hasil Google Dorking - IKU Historis (2014-2018)\n\n')
    f.write(f'Generated: {time.strftime("%Y-%m-%d %H:%M:%S")}\n\n')
    f.write('---\n\n')
    
    print(f"\n📝 Generating search queries...")
    print(f"   Total: {len(queries)} queries")
    
    for idx, query in enumerate(queries, 1):
        print(f"\n[{idx}/{len(queries)}] {query}")
        
        # Generate Google search URL
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        
        f.write(f'## Query {idx}\n\n')
        f.write(f'**Search:** `{query}`\n\n')
        f.write(f'**Link:** [{search_url}]({search_url})\n\n')
        f.write('**Status:** 🔍 Manual review required\n\n')
        f.write('**Notes:**\n')
        f.write('- [ ] Checked\n')
        f.write('- [ ] Results found\n')
        f.write('- [ ] Data downloaded\n')
        f.write('- [ ] Data extracted\n\n')
        f.write('---\n\n')
        
        time.sleep(0.1)  # Prevent rate limiting

print(f"\n✅ Search queries generated!")
print(f"📄 Output saved to: {output_file}")
print(f"\n💡 NEXT STEPS:")
print(f"   1. Open the markdown file")
print(f"   2. Click each Google search link")
print(f"   3. Review results manually")
print(f"   4. Download any SLHI/publikasi yang relevan")
print(f"   5. Check off the checkboxes as you go")
print(f"\n🎯 TARGET: Find SLHI 2014, 2015, 2016 or BPS publications")
print("="*70)
