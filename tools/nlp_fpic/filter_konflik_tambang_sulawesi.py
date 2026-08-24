"""
Script: Filter Konflik Agraria Tambang di Sulawesi
Tujuan: Extract data konflik pertambangan yang mengindikasikan pelanggaran FPIC
Author: Data Team
Date: 2026-06-15
"""

import pandas as pd
import re

# Load data konflik agraria yang sudah di-filter LLM v3
df = pd.read_csv('data/processed/sulawesi_konflik_agraria_tanahkita_v3.csv')

print(f"Total konflik dalam database v3: {len(df)}")
print(f"Columns: {df.columns.tolist()}")

# Filter 1: Tidak diperlukan lagi karena v3.csv sudah 100% Sulawesi
df_sulawesi = df.copy()
print(f"\nKonflik di Sulawesi (Pre-filtered by LLM): {len(df_sulawesi)}")

# Filter 2: Sektor Pertambangan
mining_keywords = ['Pertambangan', 'Tambang', 'Mining', 'Nikel', 'Nickel', 'Emas', 'Gold', 
                   'Batubara', 'Coal', 'IUP', 'Mineral']

df_mining = df_sulawesi[df_sulawesi['status'].str.contains('|'.join(mining_keywords), case=False, na=False)]
print(f"Konflik pertambangan di Sulawesi: {len(df_mining)}")

# Filter 3: Indikasi Pelanggaran FPIC (menggunakan NLP Regex Boundaries)
fpic_keywords = [
    r'\btanpa konsultasi\b', r'\btanpa persetujuan\b', r'\btanpa sosialisasi\b', 
    r'\btidak dilibatkan\b', r'\btidak ada izin\b', r'\bmasyarakat adat\b', r'\badat\b',
    r'\bpenolakan\b', r'\bmenolak\b', r'\btolak\b', r'\bprotes\b', r'\bkonflik\b', 
    r'\bkriminalisasi\b', r'\bpenggusuran\b', r'\bmenggusur\b', r'\bperampasan\b', 
    r'\bmerampas\b', r'\bsengketa\b', r'\bokupasi\b', r'\btanpa sepengetahuan\b', 
    r'\btidak pernah ada pemberitahuan\b', r'\btanah leluhur\b', r'\bmengambil tanah\b',
    r'\bmerusak\b', r'\bkerusakan\b', r'\bilegal\b'
]

def check_fpic_violation(text):
    """Check if text contains FPIC violation indicators using regex boundaries"""
    if pd.isna(text):
        return False
    text_lower = str(text).lower()
    return any(re.search(kw, text_lower) for kw in fpic_keywords)

df_mining['indikasi_fpic_violation'] = df_mining['deskripsi'].apply(check_fpic_violation)

# Filter 4: Filter 1 Dekade Terakhir (2014-2024)
df_mining = df_mining[(df_mining['tahun'] >= 2014) & (df_mining['tahun'] <= 2024)].copy()

df_fpic_strict = df_mining[df_mining['indikasi_fpic_violation'] == True]

print(f"Konflik dengan indikasi pelanggaran FPIC (strict, 2014-2024): {len(df_fpic_strict)}")

# For visualization purposes, use ALL mining conflicts in Sulawesi within the timeframe
# We'll mark which ones have explicit FPIC violations
df_mining['indikasi_fpic'] = df_mining['indikasi_fpic_violation']
df_output_all = df_mining.copy()

print(f"Total konflik pertambangan Sulawesi (untuk visualisasi): {len(df_output_all)}")

# Extract perusahaan names dari deskripsi dan judul
def extract_company_names(row):
    """Extract PT/CV company names from text"""
    text = str(row['deskripsi']) + ' ' + str(row['judul'])
    if pd.isna(text):
        return None
    # Pattern: PT [Nama Perusahaan]
    pattern = r'PT\.?\s+([A-Z][A-Za-z\s&\(\)]+?)(?=\s+(?:yang|dengan|di|untuk|dari|pada|melakukan|mendapat|memiliki|berkonflik|vs|VS|,)|[,\.]|$)'
    matches = re.findall(pattern, str(text))
    if matches:
        # Clean up matches
        companies = [m.strip() for m in matches if len(m.strip()) > 3]
        return '; '.join(list(set(companies))[:3])  # Max 3 unique companies
    return None

df_output_all['nama_perusahaan'] = df_output_all.apply(extract_company_names, axis=1)

# Extract lokasi provinsi dari LLM NER column
df_output_all['provinsi'] = df_output_all['provinsi_ner_llm']

# Create output dataset
output_columns = ['tahun', 'judul', 'deskripsi', 'provinsi', 'lokasi', 'status', 'nama_perusahaan', 'indikasi_fpic', 'detail_url']
df_output = df_output_all[output_columns].copy()

# Sort by year descending
df_output = df_output.sort_values('tahun', ascending=False)

# Save to processed folder
output_path = 'data/processed/sulawesi_konflik_tambang_fpic.csv'
df_output.to_csv(output_path, index=False, encoding='utf-8')

print(f"\n✅ Dataset saved to: {output_path}")
print(f"Total konflik exported: {len(df_output)}")

# Print sample
print("\n📋 Sample Data (5 terbaru):")
print("="*100)
for idx, row in df_output.head(5).iterrows():
    print(f"\n{row['tahun']} | {row['lokasi']}")
    print(f"Judul: {row['judul']}")
    print(f"Perusahaan: {row['nama_perusahaan']}")
    print(f"Deskripsi: {row['deskripsi'][:200]}...")
    print("-"*100)

# Generate summary statistics
print("\n📊 SUMMARY STATISTICS:")
print("="*100)
print(f"Total konflik pertambangan Sulawesi: {len(df_output)}")
print(f"Konflik dengan indikasi eksplisit pelanggaran FPIC: {df_output['indikasi_fpic'].sum()}")
print(f"\nDistribusi per tahun:")
print(df_output['tahun'].value_counts().sort_index(ascending=False).head(10))
print(f"\nDistribusi per provinsi:")
print(df_output['provinsi'].value_counts())
print(f"\nDistribusi per sektor:")
print(df_output['status'].value_counts())
print(f"\nPerusahaan yang disebutkan (non-null):")
print(df_output[df_output['nama_perusahaan'].notna()]['nama_perusahaan'].value_counts().head(10))

print("\n✅ Script completed successfully!")
