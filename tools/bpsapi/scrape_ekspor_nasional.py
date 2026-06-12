#!/usr/bin/env python3
"""
BPS Ekspor Nasional Scraper
CELIOS ECC Intelligence System

Scrape data ekspor nasional dari BPS website
Berdasarkan temuan: ekspor hanya tersedia di level nasional
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import logging
import json

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EksporNasionalScraper:
    """Scraper untuk data ekspor nasional BPS"""
    
    def __init__(self):
        self.base_url = "https://www.bps.go.id"
        self.exim_url = "https://www.bps.go.id/id/exim"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def test_exim_page(self):
        """Test akses ke halaman ekspor-impor"""
        logger.info("🌐 Testing BPS Exim page...")
        
        try:
            response = self.session.get(self.exim_url, timeout=30)
            logger.info(f"  ✅ Status: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Save HTML
                output_dir = Path("output")
                output_dir.mkdir(exist_ok=True)
                
                html_path = output_dir / "bps_exim_page.html"
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                logger.info(f"  📄 HTML saved: {html_path}")
                
                # Look for forms/selects
                forms = soup.find_all('form')
                selects = soup.find_all('select')
                buttons = soup.find_all('button', string=lambda x: x and 'buat' in x.lower())
                
                logger.info(f"  📋 Found {len(forms)} forms")
                logger.info(f"  📋 Found {len(selects)} selects")
                logger.info(f"  🔘 Found {len(buttons)} 'Buat' buttons")
                
                # Look for API endpoints in JavaScript
                scripts = soup.find_all('script', src=lambda x: x and '.js' in x)
                logger.info(f"  📜 Found {len(scripts)} JS files")
                
                return {
                    'status': 'accessible',
                    'forms': len(forms),
                    'selects': len(selects),
                    'html_path': str(html_path)
                }
            else:
                return {'status': 'failed', 'code': response.status_code}
                
        except Exception as e:
            logger.error(f"  ❌ Error: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_ekspor_data_manual_instructions(self):
        """Generate manual download instructions for ekspor data"""
        
        instructions = """
# PANDUAN DOWNLOAD DATA EKSPOR NASIONAL

## URL Akses
https://www.bps.go.id/id/exim

## Langkah-Langkah

### 1. Pilih Tipe Data
- **Pilih**: Ekspor

### 2. Pilih Agregasi
**Opsi A - Menurut Kode HS** (Recommended untuk sektor):
- HS 2 Digit (kategori umum)
- HS Full (detail lengkap)

**Opsi B - Menurut Pelabuhan**:
- Breakdown per pelabuhan ekspor

**Opsi C - Menurut Negara/Wilayah**:
- Breakdown per negara tujuan

### 3. Pilih Periode
- **Tahun**: 2016 - 2024 (pilih multiple)
- **Bulan**: Pilih semua atau tahunan saja

### 4. Pilih Kode HS (jika pilih opsi A)

**Kode HS 2 Digit yang Relevan untuk ECC:**
```
01 - Hewan Hidup
03 - Ikan dan Udang
08 - Buah-buahan
09 - Kopi, Teh, Rempah
15 - Minyak Nabati
16 - Olahan Daging/Ikan
24 - Tembakau
27 - Bahan Bakar Mineral
44 - Kayu dan Produk Kayu
47 - Pulp Kayu
72 - Besi dan Baja
85 - Mesin Elektrik
87 - Kendaraan
```

### 5. Generate & Download
1. Klik **"Buat Tabel"**
2. Tunggu tabel muncul
3. Klik **"Unduh"**
4. Format: CSV atau Excel

## Output Files

Naming convention:
```
ekspor_nasional_{agregasi}_{tahun_awal}-{tahun_akhir}.csv
```

Contoh:
- `ekspor_nasional_hs2digit_2016-2024.csv`
- `ekspor_nasional_pelabuhan_2016-2024.csv`
- `ekspor_nasional_negara_2016-2024.csv`

## Lokasi Penyimpanan
```
c:\\Users\\yooma\\OneDrive\\Desktop\\duniahub\\client\\4. Celios2\\tools\\bpsapi\\output\\ekspor\\
```

## Estimasi Waktu
- Per dataset: 5-10 menit
- Total (3 datasets recommended): ~30 menit

## Troubleshooting
- **Tabel tidak muncul**: Kurangi range tahun atau kurangi jumlah kode HS
- **Browser hang**: Data terlalu besar, pilih aggregate lebih tinggi (HS 2 Digit, bukan Full)
- **Download gagal**: Coba format berbeda (CSV ↔ Excel)
"""
        
        return instructions


def main():
    """Main function"""
    print("="*80)
    print("BPS Ekspor Nasional Scraper")
    print("Testing data access methods")
    print("="*80)
    
    scraper = EksporNasionalScraper()
    
    # Test exim page
    print("\n[1/2] Testing BPS Exim Page Access...")
    result = scraper.test_exim_page()
    
    if result['status'] == 'accessible':
        print(f"✅ Exim page accessible")
        print(f"📋 Forms: {result['forms']}")
        print(f"📋 Selects: {result['selects']}")
        print(f"📄 HTML: {result['html_path']}")
    else:
        print(f"❌ Cannot access exim page")
    
    # Generate manual instructions
    print("\n[2/2] Generating Manual Download Instructions...")
    instructions = scraper.get_ekspor_data_manual_instructions()
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    instrpath = output_dir / "PANDUAN_DOWNLOAD_EKSPOR_NASIONAL.md"
    with open(instrpath, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"✅ Instructions saved: {instrpath}")
    
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"✅ Exim page: {'Accessible' if result['status'] == 'accessible' else 'Not accessible'}")
    print(f"📄 Manual instructions: {instrpath}")
    print(f"\n⚠️  RECOMMENDATION: Use manual download approach")
    print(f"   Website uses JavaScript form that's difficult to automate")
    print(f"   Manual download takes ~30 minutes for full dataset")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
