#!/usr/bin/env python3
"""
Ekstrak data IKU historis 2014-2018 dari SLHI lama (2017, 2018, 2019)
SLHI biasanya publish data retrospektif beberapa tahun ke belakang
"""

import pdfplumber
import pandas as pd
from pathlib import Path

pdf_dir = Path(r'c:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\data\raw\sulut_kualitas_air')

# Target: cari data 2014-2018 dari SLHI lama
target_pdfs = [
    ('SLHI_2017.pdf', [2014, 2015, 2016, 2017]),  # Mungkin ada data retrospektif
    ('SLHI_2018.pdf', [2014, 2015, 2016, 2017, 2018]),
    ('SLHI_2019.pdf', [2014, 2015, 2016, 2017, 2018, 2019]),
]

print("="*70)
print("🔍 Mencari Data IKU Historis (2014-2018) dari SLHI Lama")
print("="*70)

all_data = []
sulawesi_keywords = ['sulawesi utara', 'sulawesi selatan', 'sulawesi tengah', 
                    'sulawesi tenggara', 'sulawesi barat', 'gorontalo']

for pdf_name, target_years in target_pdfs:
    pdf_path = pdf_dir / pdf_name
    print(f"\n📖 Processing: {pdf_name}")
    print(f"   Target years: {target_years}")
    
    if not pdf_path.exists():
        print(f"   ⚠️  File not found")
        continue
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Scan halaman yang mungkin punya tabel IKU
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if not text:
                    continue
                
                text_lower = text.lower()
                
                # Cek keyword
                has_iku = 'kualitas udara' in text_lower or 'iku' in text_lower
                has_sulawesi = any(kw in text_lower for kw in sulawesi_keywords)
                
                if not (has_iku and has_sulawesi):
                    continue
                
                # Extract tables
                tables = page.extract_tables()
                if not tables:
                    continue
                
                for table in tables:
                    if not table or len(table) < 2:
                        continue
                    
                    df = pd.DataFrame(table[1:], columns=table[0])
                    
                    # Find province column
                    province_col = None
                    for col in df.columns:
                        if col and 'provinsi' in str(col).lower():
                            province_col = col
                            break
                    
                    if not province_col:
                        province_col = df.columns[0]
                    
                    # Find Sulawesi rows
                    sulawesi_rows = df[df[province_col].apply(
                        lambda x: any(kw in str(x).lower() for kw in sulawesi_keywords) if pd.notna(x) else False
                    )]
                    
                    if sulawesi_rows.empty:
                        continue
                    
                    print(f"   ✅ Page {page_num+1}: Found {len(sulawesi_rows)} Sulawesi rows")
                    
                    # Try to find year columns matching target years
                    for year in target_years:
                        year_cols = [col for col in df.columns if str(year) in str(col)]
                        
                        for year_col in year_cols:
                            for _, row in sulawesi_rows.iterrows():
                                prov = row[province_col]
                                val = row[year_col]
                                
                                if pd.notna(val):
                                    try:
                                        # Extract number
                                        import re
                                        match = re.search(r'(\d+[.,]?\d*)', str(val))
                                        if match:
                                            num_val = float(match.group(1).replace(',', '.'))
                                            
                                            # Filter: IKU biasanya 70-100
                                            if 70 <= num_val <= 100:
                                                all_data.append({
                                                    'Tahun': year,
                                                    'Provinsi': prov,
                                                    'IKU': num_val,
                                                    'Sumber': pdf_name,
                                                    'Halaman': page_num + 1
                                                })
                                                print(f"      • {year} - {prov}: {num_val}")
                                    except:
                                        pass
    
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

print("\n" + "="*70)
if all_data:
    df_result = pd.DataFrame(all_data)
    
    # Remove duplicates
    df_result = df_result.drop_duplicates(subset=['Tahun', 'Provinsi'], keep='first')
    
    print(f"✅ Found {len(df_result)} historical data points")
    
    print("\n📊 Coverage by Year:")
    print(df_result.groupby('Tahun').size())
    
    print("\n📋 Data Preview:")
    print(df_result.sort_values(['Tahun', 'Provinsi']))
    
    # Save
    output_file = 'data/processed/iku_sulawesi_historical_2014_2018.csv'
    df_result.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n💾 Saved to: {output_file}")
else:
    print("❌ No historical IKU data found in these PDFs")
    print("\n💡 ALTERNATIF:")
    print("   1. Coba download SLHI tahun 2014-2016 dari website BPS/KLHK")
    print("   2. Scrape Portal Open Data Provinsi untuk data historis")
    print("   3. Gunakan interpolasi untuk estimate missing years")

print("="*70)
