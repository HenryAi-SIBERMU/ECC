#!/usr/bin/env python3
"""
Ekstraksi data IKU (Indeks Kualitas Udara) dari SLHI 2015-2018
Target: 6 provinsi Sulawesi × 4 tahun = 24 data points
"""

import pdfplumber
import pandas as pd
from pathlib import Path
import re

print("="*80)
print("🔍 Ekstraksi IKU dari SLHI 2015-2018")
print("="*80)

# Target provinsi
PROVINSI_TARGET = [
    'Sulawesi Utara',
    'Sulawesi Tengah', 
    'Sulawesi Selatan',
    'Sulawesi Tenggara',
    'Gorontalo',
    'Sulawesi Barat'
]

# Variations for matching
PROVINSI_VARIATIONS = {
    'Sulawesi Utara': ['sulawesi utara', 'sulut', 'sul ut'],
    'Sulawesi Tengah': ['sulawesi tengah', 'sulteng', 'sul teng'],
    'Sulawesi Selatan': ['sulawesi selatan', 'sulsel', 'sul sel'],
    'Sulawesi Tenggara': ['sulawesi tenggara', 'sultra', 'sul tra'],
    'Gorontalo': ['gorontalo'],
    'Sulawesi Barat': ['sulawesi barat', 'sulbar', 'sul bar']
}

def match_provinsi(text):
    """Match text to target provinsi"""
    text_lower = text.lower()
    for prov, variations in PROVINSI_VARIATIONS.items():
        for var in variations:
            if var in text_lower:
                return prov
    return None

def extract_iku_from_pdf(pdf_path, year):
    """
    Extract IKU data from SLHI PDF
    Returns: list of dicts with {Provinsi, IKU, Tahun, Halaman}
    """
    print(f"\n📖 Processing: {pdf_path.name}")
    
    results = []
    
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"   Total pages: {total_pages}")
        
        # Strategy: Search for keywords related to IKU/air quality
        keywords = ['indeks kualitas udara', 'iku', 'kualitas udara', 'air quality']
        
        for page_num, page in enumerate(pdf.pages, 1):
            try:
                text = page.extract_text() or ""
                text_lower = text.lower()
                
                # Check if page contains relevant keywords
                has_keyword = any(kw in text_lower for kw in keywords)
                
                if not has_keyword:
                    continue
                
                # Try to extract tables
                tables = page.extract_tables()
                
                if tables:
                    for table_idx, table in enumerate(tables):
                        if not table:
                            continue
                        
                        # Convert to DataFrame for easier processing
                        try:
                            df = pd.DataFrame(table[1:], columns=table[0])
                        except:
                            df = pd.DataFrame(table)
                        
                        # Look for provinsi and numeric values
                        for idx, row in df.iterrows():
                            row_text = ' '.join([str(cell) for cell in row if cell])
                            
                            # Match provinsi
                            prov = match_provinsi(row_text)
                            if not prov:
                                continue
                            
                            # Extract numeric values (IKU typically 70-100)
                            numbers = re.findall(r'\b(\d{1,3}[.,]\d{1,2}|\d{2,3})\b', row_text)
                            
                            for num_str in numbers:
                                # Normalize number format
                                num_str = num_str.replace(',', '.')
                                try:
                                    iku = float(num_str)
                                    
                                    # Validate IKU range (70-100 = realistic for Sulawesi)
                                    if 70 <= iku <= 100:
                                        results.append({
                                            'Provinsi': prov,
                                            'IKU': iku,
                                            'Tahun': year,
                                            'Halaman': page_num,
                                            'Tabel': table_idx + 1
                                        })
                                        print(f"   ✅ Found: {prov} = {iku} (page {page_num})")
                                except ValueError:
                                    continue
                
                # Also try direct text extraction for IKU mentions
                if 'sulawesi' in text_lower and any(kw in text_lower for kw in keywords):
                    lines = text.split('\n')
                    for line in lines:
                        prov = match_provinsi(line)
                        if prov:
                            # Look for numbers near provinsi name
                            numbers = re.findall(r'\b(\d{1,3}[.,]\d{1,2}|\d{2,3})\b', line)
                            for num_str in numbers:
                                num_str = num_str.replace(',', '.')
                                try:
                                    iku = float(num_str)
                                    if 70 <= iku <= 100:
                                        # Check if not duplicate
                                        if not any(r['Provinsi'] == prov and r['IKU'] == iku and r['Halaman'] == page_num for r in results):
                                            results.append({
                                                'Provinsi': prov,
                                                'IKU': iku,
                                                'Tahun': year,
                                                'Halaman': page_num,
                                                'Tabel': 0  # Text extraction
                                            })
                                            print(f"   ✅ Found (text): {prov} = {iku} (page {page_num})")
                                except ValueError:
                                    continue
                
            except Exception as e:
                print(f"   ⚠️  Error on page {page_num}: {str(e)}")
                continue
    
    print(f"   📊 Total extracted: {len(results)} data points")
    return results

# Process all PDFs
all_data = []

pdfs = [
    ('data/raw/slhi_historical/SLHI_2015.pdf', 2015),
    ('data/raw/slhi_historical/SLHI_2016.pdf', 2016),
    ('data/raw/slhi_historical/SLHI_2017.pdf', 2017),
    ('data/raw/slhi_historical/SLHI_2018.pdf', 2018),
]

for pdf_path_str, year in pdfs:
    pdf_path = Path(pdf_path_str)
    
    if not pdf_path.exists():
        print(f"\n❌ File not found: {pdf_path}")
        continue
    
    data = extract_iku_from_pdf(pdf_path, year)
    all_data.extend(data)

print("\n" + "="*80)
print(f"✅ Extraction complete!")
print(f"📊 Total data points extracted: {len(all_data)}")

if all_data:
    # Convert to DataFrame
    df = pd.DataFrame(all_data)
    
    # Sort by year and provinsi
    df = df.sort_values(['Tahun', 'Provinsi'])
    
    # Remove duplicates (keep first occurrence)
    df_unique = df.drop_duplicates(subset=['Provinsi', 'Tahun'], keep='first')
    
    print(f"📊 Unique data points (after deduplication): {len(df_unique)}")
    
    # Save raw extraction
    output_raw = Path('data/processed/iku_2015_2018_raw.csv')
    df.to_csv(output_raw, index=False, encoding='utf-8-sig')
    print(f"💾 Raw data saved: {output_raw}")
    
    # Save cleaned data
    output_clean = Path('data/processed/iku_2015_2018_clean.csv')
    df_unique.to_csv(output_clean, index=False, encoding='utf-8-sig')
    print(f"💾 Clean data saved: {output_clean}")
    
    # Summary by year
    print("\n📈 Coverage by Year:")
    for year in sorted(df_unique['Tahun'].unique()):
        count = len(df_unique[df_unique['Tahun'] == year])
        print(f"   {year}: {count}/6 provinsi ({count/6*100:.0f}%)")
    
    # Summary by provinsi
    print("\n🗺️  Coverage by Provinsi:")
    for prov in PROVINSI_TARGET:
        years = df_unique[df_unique['Provinsi'] == prov]['Tahun'].tolist()
        if years:
            print(f"   {prov}: {years}")
        else:
            print(f"   {prov}: ❌ No data")
    
    # Display sample
    print("\n📋 Sample data:")
    print(df_unique.head(10).to_string(index=False))
    
else:
    print("\n⚠️  No data extracted. Manual inspection needed.")
    print("   SLHI PDFs may have different structures or IKU data in image format.")

print("\n" + "="*80)
print("✅ NEXT STEPS:")
print("   1. Review extracted data in data/processed/iku_2015_2018_clean.csv")
print("   2. If incomplete, manually inspect PDFs for table structure")
print("   3. Merge with existing 2019-2024 data")
print("="*80)
