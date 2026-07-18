"""
ETL Sample: KPA CATAHU 2025 - Extract Data tentang Izin Tambang Ilegal & Sulawesi
Author: Data Team
Date: 2026-06-15
"""

import PyPDF2
import re
import pandas as pd

# Load PDF
pdf_path = 'data/raw/konflik_kpa_ylbhi_tanahkita/Catahu 2025_KPA.pdf'
pdf_file = open(pdf_path, 'rb')
reader = PyPDF2.PdfReader(pdf_file)

print(f"📄 Processing: {pdf_path}")
print(f"Total pages: {len(reader.pages)}\n")

# Extract all text
full_text = ""
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    full_text += f"\n\n=== PAGE {i+1} ===\n\n{text}"

pdf_file.close()

# Save full text for inspection
with open('data/raw/konflik_kpa_ylbhi_tanahkita/catahu_2025_full_text.txt', 'w', encoding='utf-8') as f:
    f.write(full_text)

print("✅ Full text extracted to: catahu_2025_full_text.txt\n")

# Search for keywords related to izin tambang ilegal and Sulawesi
keywords_izin_ilegal = [
    'izin ilegal', 'izin bermasalah', 'IUP ilegal', 'IUP bermasalah',
    'tanpa izin', 'tidak berizin', 'izin kadaluarsa', 'izin dicabut',
    'tambang ilegal', 'pertambangan ilegal', 'operasi ilegal',
    'melanggar izin', 'pelanggaran izin', 'izin tidak sah'
]

keywords_sulawesi = [
    'Sulawesi', 'Sulteng', 'Sultra', 'Sulsel', 'Sulbar', 'Sulut', 'Gorontalo',
    'Morowali', 'Kolaka', 'Konawe', 'Palu', 'Donggala', 'Makassar',
    'Luwu', 'Bone', 'Mamuju', 'Banggai', 'Tojo Una-Una', 'Bitung',
    'Enrekang', 'Sorowako', 'Wawonii', 'Kabaena'
]

keywords_pertambangan = [
    'tambang', 'pertambangan', 'IUP', 'mining', 'nikel', 'nickel',
    'batubara', 'coal', 'emas', 'gold', 'mineral', 'smelter',
    'IPPKH', 'HGU', 'konsesi'
]

print("🔍 SEARCHING FOR RELEVANT SECTIONS...\n")
print("="*80)

# Find paragraphs containing keywords
paragraphs = full_text.split('\n\n')
relevant_sections = []

for i, para in enumerate(paragraphs):
    para_lower = para.lower()
    
    # Check if paragraph contains izin ilegal keywords
    has_izin = any(keyword.lower() in para_lower for keyword in keywords_izin_ilegal)
    # Check if paragraph contains Sulawesi keywords
    has_sulawesi = any(keyword.lower() in para_lower for keyword in keywords_sulawesi)
    # Check if paragraph contains pertambangan keywords
    has_tambang = any(keyword.lower() in para_lower for keyword in keywords_pertambangan)
    
    if (has_izin or (has_sulawesi and has_tambang)) and len(para.strip()) > 100:
        relevant_sections.append({
            'paragraph_index': i,
            'text': para.strip(),
            'has_izin_ilegal': has_izin,
            'has_sulawesi': has_sulawesi,
            'has_pertambangan': has_tambang
        })

print(f"Found {len(relevant_sections)} relevant sections\n")

# Print relevant sections
for idx, section in enumerate(relevant_sections[:10]):  # Show first 10
    print(f"\n{'='*80}")
    print(f"SECTION {idx+1} (Paragraph {section['paragraph_index']})")
    print(f"Izin Ilegal: {section['has_izin_ilegal']} | Sulawesi: {section['has_sulawesi']} | Pertambangan: {section['has_pertambangan']}")
    print(f"{'-'*80}")
    print(section['text'][:500])  # Show first 500 chars
    if len(section['text']) > 500:
        print("...[truncated]...")
    print()

# Save relevant sections to CSV
if relevant_sections:
    df = pd.DataFrame(relevant_sections)
    output_path = 'data/processed/kpa_catahu_2025_izin_ilegal_sulawesi.csv'
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"\n✅ Relevant sections saved to: {output_path}")
    print(f"Total sections: {len(df)}")
else:
    print("\n⚠️ No relevant sections found")

# Additional: Extract tables (if any)
print("\n🔍 SEARCHING FOR TABLES/STATISTICS...\n")

# Look for patterns like "Tabel X" or numeric data patterns
table_patterns = [
    r'Tabel\s+\d+',
    r'Grafik\s+\d+',
    r'\d+\s+konflik',
    r'\d+\.?\d*\s+(hektar|ha|jiwa)',
    r'\d+\s+izin',
    r'\d+\s+IUP'
]

table_sections = []
for para in paragraphs:
    if any(re.search(pattern, para, re.IGNORECASE) for pattern in table_patterns):
        if len(para.strip()) > 50:
            table_sections.append(para.strip())

print(f"Found {len(table_sections)} sections with tables/statistics")
for idx, section in enumerate(table_sections[:5]):  # Show first 5
    print(f"\n{'='*80}")
    print(f"TABLE/STAT SECTION {idx+1}")
    print(f"{'-'*80}")
    print(section[:400])
    if len(section) > 400:
        print("...[truncated]...")

print("\n✅ ETL Sample completed!")
print(f"\n📊 SUMMARY:")
print(f"- Total pages: {len(reader.pages)}")
print(f"- Total paragraphs: {len(paragraphs)}")
print(f"- Relevant sections (izin ilegal/Sulawesi): {len(relevant_sections)}")
print(f"- Table/stat sections: {len(table_sections)}")
