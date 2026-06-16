"""
ETL KPA CATAHU: Extract Data MASALAH IZIN (bukan konflik)
Target: Data izin bermasalah, HGU kadaluarsa, IPPKH dicabut, izin ilegal
Author: Data Team
Date: 2026-06-15
"""

import PyPDF2
import re
import pandas as pd
import glob

# List all CATAHU PDFs
pdf_files = glob.glob('data/raw/konflik_kpa_ylbhi_tanahkita/catahu*.pdf') + \
            glob.glob('data/raw/konflik_kpa_ylbhi_tanahkita/Catahu*.pdf') + \
            glob.glob('data/raw/konflik_kpa_ylbhi_tanahkita/CATAHU*.pdf')

pdf_files = sorted(set(pdf_files))

print(f"📄 Found {len(pdf_files)} CATAHU PDFs\n")
for pdf in pdf_files:
    print(f"  - {pdf.split('/')[-1]}")

# Keywords untuk masalah izin (BUKAN konflik biasa)
keywords_masalah_izin = [
    # Status izin
    'izin berakhir', 'izin habis', 'izin kadaluarsa', 'izin dicabut',
    'HGU habis', 'HGU berakhir', 'HGU kadaluarsa', 'HGU dicabut',
    'IPPKH habis', 'IPPKH kadaluarsa', 'IPPKH dicabut',
    'IUP dicabut', 'IUP bermasalah', 'IUP ilegal',
    
    # Pelanggaran izin
    'tanpa HGU', 'tidak memiliki HGU', 'tidak punya HGU',
    'tanpa izin', 'tidak berizin', 'tidak ada izin',
    'melanggar izin', 'pelanggaran izin', 'izin tidak sah',
    
    # Masalah dokumen
    'dokumen tidak lengkap', 'dokumen bermasalah',
    'AMDAL tidak ada', 'tanpa AMDAL', 'AMDAL bermasalah',
    
    # Operasi ilegal
    'operasi ilegal', 'beroperasi tanpa', 'ilegal karena',
    
    # Tumpang tindih
    'tumpang tindih', 'overlap'
]

# Collect all findings
all_findings = []

for pdf_path in pdf_files:
    year = re.search(r'(\d{4})', pdf_path.split('/')[-1])
    year = year.group(1) if year else 'unknown'
    
    print(f"\n{'='*80}")
    print(f"Processing: {pdf_path.split('/')[-1]} (Year: {year})")
    print(f"{'='*80}")
    
    try:
        pdf_file = open(pdf_path, 'rb')
        reader = PyPDF2.PdfReader(pdf_file)
        
        # Extract all text
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
        
        pdf_file.close()
        
        # Search for masalah izin
        paragraphs = full_text.split('\n\n')
        
        for para_idx, para in enumerate(paragraphs):
            para_clean = para.strip()
            if len(para_clean) < 100:  # Skip short paragraphs
                continue
                
            para_lower = para_clean.lower()
            
            # Check if contains masalah izin keywords
            has_masalah_izin = any(keyword.lower() in para_lower for keyword in keywords_masalah_izin)
            
            if has_masalah_izin:
                # Extract company names
                companies = re.findall(r'PT\.?\s+([A-Z][A-Za-z\s&\(\)\.]+?)(?=\s+(?:yang|dengan|di|untuk|dari|pada|melakukan|mendapat|memiliki|berkonflik|vs|VS|tidak|tanpa|,)|[,\.\n]|$)', para_clean)
                companies = [c.strip() for c in companies if len(c.strip()) > 3]
                companies = list(set(companies))[:3]  # Max 3 unique
                
                # Extract location (Sulawesi)
                sulawesi_match = re.search(r'(Sulawesi\s+\w+|Sulteng|Sultra|Sulsel|Sulbar|Sulut|Gorontalo)', para_clean, re.IGNORECASE)
                location = sulawesi_match.group(1) if sulawesi_match else None
                
                # Extract numbers (luas, korban, dll)
                numbers = re.findall(r'(\d+[\.,]?\d*)\s*(hektar|ha|jiwa|keluarga|KK)', para_clean, re.IGNORECASE)
                
                # Extract specific masalah izin
                masalah_types = []
                if 'hgu' in para_lower and ('habis' in para_lower or 'berakhir' in para_lower or 'kadaluarsa' in para_lower):
                    masalah_types.append('HGU Kadaluarsa/Habis')
                if 'tanpa hgu' in para_lower or 'tidak memiliki hgu' in para_lower or 'tidak punya hgu' in para_lower:
                    masalah_types.append('Tanpa HGU')
                if 'ippkh' in para_lower and ('habis' in para_lower or 'kadaluarsa' in para_lower or 'dicabut' in para_lower):
                    masalah_types.append('IPPKH Bermasalah')
                if 'iup' in para_lower and ('dicabut' in para_lower or 'bermasalah' in para_lower or 'ilegal' in para_lower):
                    masalah_types.append('IUP Bermasalah')
                if 'tanpa izin' in para_lower or 'tidak berizin' in para_lower or 'tidak ada izin' in para_lower:
                    masalah_types.append('Tanpa Izin')
                if 'amdal' in para_lower and ('tidak ada' in para_lower or 'tanpa' in para_lower or 'bermasalah' in para_lower):
                    masalah_types.append('AMDAL Bermasalah')
                if 'operasi ilegal' in para_lower or 'beroperasi tanpa' in para_lower:
                    masalah_types.append('Operasi Ilegal')
                if 'tumpang tindih' in para_lower or 'overlap' in para_lower:
                    masalah_types.append('Tumpang Tindih')
                
                if not masalah_types:
                    masalah_types.append('Izin Bermasalah (general)')
                
                all_findings.append({
                    'tahun_laporan': year,
                    'nama_perusahaan': '; '.join(companies) if companies else None,
                    'lokasi': location,
                    'jenis_masalah_izin': '; '.join(masalah_types),
                    'excerpt': para_clean[:400],
                    'luas_ha': None,
                    'dampak_jiwa': None
                })
                
                # Extract luas and dampak
                for num, unit in numbers:
                    if unit.lower() in ['hektar', 'ha']:
                        all_findings[-1]['luas_ha'] = num.replace(',', '')
                    elif unit.lower() in ['jiwa', 'keluarga', 'kk']:
                        all_findings[-1]['dampak_jiwa'] = num.replace(',', '')
                
                print(f"✓ Found masalah izin (companies: {companies}, masalah: {masalah_types})")
        
        print(f"✓ Processed {len(reader.pages)} pages")
        
    except Exception as e:
        print(f"❌ Error processing {pdf_path}: {e}")
        continue

print(f"\n{'='*80}")
print(f"📊 EXTRACTION SUMMARY")
print(f"{'='*80}")
print(f"Total findings: {len(all_findings)}")

# Create DataFrame
df = pd.DataFrame(all_findings)

# Filter hanya yang ada perusahaan atau lokasi Sulawesi
df = df[(df['nama_perusahaan'].notna()) | (df['lokasi'].notna())]

print(f"Findings dengan perusahaan/lokasi: {len(df)}")

# Save to CSV
output_path = 'data/processed/kpa_masalah_izin_perusahaan.csv'
df.to_csv(output_path, index=False, encoding='utf-8')

print(f"\n✅ Data saved to: {output_path}")
print(f"\n📋 SAMPLE DATA (first 10):")
print("="*80)
for idx, row in df.head(10).iterrows():
    print(f"\n{idx+1}. TAHUN LAPORAN: {row['tahun_laporan']}")
    print(f"   Perusahaan: {row['nama_perusahaan']}")
    print(f"   Lokasi: {row['lokasi']}")
    print(f"   Jenis Masalah: {row['jenis_masalah_izin']}")
    print(f"   Luas: {row['luas_ha']} ha | Dampak: {row['dampak_jiwa']} jiwa")
    print(f"   Excerpt: {row['excerpt'][:200]}...")
    print("-"*80)

# Statistics
print(f"\n📊 STATISTICS:")
print(f"{'='*80}")
print(f"\nJenis Masalah Izin (Top 10):")
masalah_count = df['jenis_masalah_izin'].str.split('; ').explode().value_counts()
print(masalah_count.head(10))

print(f"\nPer Tahun Laporan:")
print(df['tahun_laporan'].value_counts().sort_index())

print(f"\nPer Lokasi (Sulawesi):")
print(df[df['lokasi'].notna()]['lokasi'].value_counts())

print("\n✅ ETL Completed!")
