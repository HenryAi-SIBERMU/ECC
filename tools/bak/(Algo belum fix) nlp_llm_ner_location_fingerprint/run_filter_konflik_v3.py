"""
Script: Filter Konflik Agraria TanahKita → Sulawesi Only (v3 LLM NER)
Menggunakan LLM OpenAI untuk filter rows yang relevan ke Sulawesi secara Zero-Shot.
Output: sulawesi_konflik_agraria_tanahkita_v3.csv (hanya baris Sulawesi yang divalidasi AI)
"""

import pandas as pd
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

sys.path.insert(0, os.path.dirname(__file__))
from ner_llm_extractor import deduce_sulawesi_province_llm

SRC = "data/processed/sulawesi_konflik_agraria_tanahkita.csv"
DST = "data/processed/sulawesi_konflik_agraria_tanahkita_v3.csv"

SULAWESI_PROVINCES = [
    'Sulawesi Tengah', 'Sulawesi Tenggara', 'Sulawesi Selatan',
    'Sulawesi Utara', 'Sulawesi Barat', 'Gorontalo'
]

SOURCE_COLS = ['judul', 'deskripsi', 'lokasi']

print("=== LLM NER Filter Pipeline (OpenAI): TanahKita -> Sulawesi Only ===")
print(f"Input : {SRC}")
print(f"Output: {DST}")
print()

# Step 1: Load sumber asli (v1)
df = pd.read_csv(SRC)
df['tahun'] = pd.to_numeric(df['tahun'], errors='coerce')
print(f"Total rows asli   : {len(df)}")

# Step 2: Jalankan NER per baris via ThreadPoolExecutor untuk kecepatan
def process_row(idx, row):
    combined = ' '.join([str(row[c]) for c in SOURCE_COLS if pd.notna(row[c])])
    # LLM deduction
    res_prov = deduce_sulawesi_province_llm(combined)
    return idx, res_prov

print("Processing rows with LLM OpenAI...")
results = {}
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(process_row, idx, row): idx for idx, row in df.iterrows()}
    
    for future in tqdm(as_completed(futures), total=len(futures), desc="Calling LLM"):
        idx, res_prov = future.result()
        results[idx] = res_prov

df['provinsi_ner_llm'] = df.index.map(results)

print()
print("=== Distribusi NER LLM Provinsi ===")
print(df['provinsi_ner_llm'].value_counts().to_string())

# Step 3: Filter hanya Sulawesi
df_sulawesi = df[df['provinsi_ner_llm'].isin(SULAWESI_PROVINCES)].copy()

print()
print(f"Rows Sulawesi (LLM Validated) : {len(df_sulawesi)}")
print(f"Rows dibuang                  : {len(df) - len(df_sulawesi)} (Luar Sulawesi)")

# Step 4: Simpan v3
df_sulawesi.to_csv(DST, index=False)
print(f"\nSaved: {DST}")

# Step 5: Validasi angka Sosial 2 & 3
df_sulawesi['dampak_masyarakat_jiwa'] = pd.to_numeric(
    df_sulawesi['dampak_masyarakat_jiwa'], errors='coerce').fillna(0)

keywords_air = 'nelayan|pesisir|laut|tambak|air|sungai|DAS|danau|irigasi|banjir'
df_darat = df_sulawesi[~df_sulawesi['sektor'].str.contains(keywords_air, case=False, na=False)]

sosial2 = df_darat['dampak_masyarakat_jiwa'].sum()
sosial3 = len(df_darat[df_darat['indikasi_kriminalisasi'] == True])

print()
print("=== Angka Sosial setelah LLM NER filter ===")
print(f"Sosial 2 (Jiwa Terdampak) : {sosial2:,.0f}")
print(f"Sosial 3 (Kriminalisasi)  : {sosial3}")

print()
print("=== Per Provinsi (LLM) ===")
for prov in SULAWESI_PROVINCES:
    dp = df_darat[df_darat['provinsi_ner_llm'] == prov]
    jiwa = dp['dampak_masyarakat_jiwa'].sum()
    krim = len(dp[dp['indikasi_kriminalisasi'] == True])
    print(f"  {prov:<25}: jiwa={jiwa:>8,.0f}, krim={krim}")

print()
print("Pipeline selesai.")
