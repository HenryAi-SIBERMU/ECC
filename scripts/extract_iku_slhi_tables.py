#!/usr/bin/env python3
"""
Ekstrak tabel IKU (Indeks Kualitas Udara) dari PDF SLHI
Menggunakan pdfplumber untuk parsing tabel yang lebih akurat
Target: Data kualitas udara Sulawesi 2017-2024
"""

import pdfplumber
import pandas as pd
import os
import re
from pathlib import Path

pdf_dir = Path(r'c:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\data\raw\sulut_kualitas_air')
output_dir = Path(r'c:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\data\processed')

pdfs = sorted(pdf_dir.glob('SLHI_*.pdf'))

# Keywords untuk mencari halaman IKU
keywords = ['indeks kualitas udara', 'iku', 'pm2.5', 'pm10', 'polutan']

print("="*70)
print("📊 Ekstraksi Tabel IKU dari SLHI PDFs")
print("="*70)

all_data = []

for pdf_path in pdfs:
    year = pdf_path.stem.split("_")[1]
    print(f"\n📖 Processing: {pdf_path.name} (Tahun {year})")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            found_pages = []
            
            # Scan untuk halaman yang mengandung keyword + sulawesi
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if not text:
                    continue
                
                text_lower = text.lower()
                
                # Cek keyword IKU
                has_iku_keyword = any(kw in text_lower for kw in keywords)
                has_sulawesi = 'sulawesi' in text_lower
                has_provinsi = 'provinsi' in text_lower or 'province' in text_lower
                
                if has_iku_keyword and (has_sulawesi or has_provinsi):
                    found_pages.append(i)
                    print(f"   ✓ Page {i+1}: Contains IKU + Sulawesi/Provinsi")
            
            if not found_pages:
                print(f"   ℹ️  No IKU pages found")
                continue
            
            # Extract tables from found pages
            print(f"   📄 Extracting tables from {len(found_pages)} pages...")
            
            for page_num in found_pages:
                page = pdf.pages[page_num]
                tables = page.extract_tables()
                
                if not tables:
                    continue
                
                print(f"   📋 Page {page_num+1}: Found {len(tables)} table(s)")
                
                for table_idx, table in enumerate(tables):
                    if not table or len(table) < 2:
                        continue
                    
                    # Convert to DataFrame
                    df = pd.DataFrame(table[1:], columns=table[0])
                    
                    # Debug: show first row
                    print(f"      Table {table_idx+1}: {df.shape[0]} rows x {df.shape[1]} cols")
                    print(f"      Columns: {list(df.columns)[:5]}")
                    
                    # Look for Sulawesi provinces
                    sulawesi_keywords = ['sulawesi utara', 'sulawesi selatan', 'sulawesi tengah', 
                                        'sulawesi tenggara', 'sulawesi barat', 'gorontalo']
                    
                    # Try to find province column
                    province_col = None
                    for col in df.columns:
                        if col and ('provinsi' in str(col).lower() or 'province' in str(col).lower()):
                            province_col = col
                            break
                    
                    if not province_col:
                        # Try first column
                        province_col = df.columns[0]
                    
                    # Filter for Sulawesi provinces
                    sulawesi_rows = df[df[province_col].apply(
                        lambda x: any(kw in str(x).lower() for kw in sulawesi_keywords) if pd.notna(x) else False
                    )]
                    
                    if not sulawesi_rows.empty:
                        print(f"      ✅ Found {len(sulawesi_rows)} Sulawesi rows!")
                        print(f"         Provinces: {sulawesi_rows[province_col].tolist()}")
                        
                        # Save raw table for manual inspection
                        output_file = output_dir / f"iku_{year}_page{page_num+1}_table{table_idx+1}.csv"
                        df.to_csv(output_file, index=False, encoding='utf-8-sig')
                        print(f"         💾 Saved to: {output_file.name}")
                        
                        # Try to extract IKU values
                        for _, row in sulawesi_rows.iterrows():
                            prov = row[province_col]
                            
                            # Look for numeric columns (possible IKU values)
                            for col in df.columns:
                                if col != province_col:
                                    val = row[col]
                                    if pd.notna(val):
                                        # Try to extract number
                                        match = re.search(r'(\d+[.,]?\d*)', str(val))
                                        if match:
                                            num_val = match.group(1).replace(',', '.')
                                            try:
                                                num_val = float(num_val)
                                                if 0 < num_val < 100:  # IKU range usually 0-100
                                                    all_data.append({
                                                        'Tahun': year,
                                                        'Provinsi': prov,
                                                        'Indeks Kualitas Udara': num_val,
                                                        'Kolom': col,
                                                        'Halaman': page_num + 1,
                                                        'Sumber': pdf_path.name
                                                    })
                                                    print(f"         • {prov}: {num_val}")
                                            except:
                                                pass
    
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

print("\n" + "="*70)
if all_data:
    df_result = pd.DataFrame(all_data)
    output_final = output_dir / "iku_sulawesi_extracted_slhi.csv"
    df_result.to_csv(output_final, index=False, encoding='utf-8-sig')
    
    print(f"✅ Total {len(all_data)} data points extracted")
    print(f"💾 Saved to: {output_final}")
    
    print("\n📊 Summary by Year:")
    print(df_result.groupby('Tahun').size())
    
    print("\n📍 Summary by Province:")
    print(df_result.groupby('Provinsi').size())
else:
    print("❌ No IKU data found")
    print("\n💡 REKOMENDASI:")
    print("   Cek file CSV mentah yang di-generate di folder data/processed/")
    print("   Mungkin format tabel perlu parsing manual atau OCR")

print("="*70)
