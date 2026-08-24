"""
Script: Filter Konflik Agraria TanahKita → Sulawesi Only (v2)
Menggunakan NER Location Fingerprint untuk filter rows yang relevan ke Sulawesi.
Output: sulawesi_konflik_agraria_tanahkita_v2.csv (hanya baris Sulawesi)
"""

import pandas as pd
import shutil
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from ner_location_deducer_agraria import deduce_sulawesi_province, deduce_kabupaten

SRC = "data/processed/sulawesi_konflik_agraria_tanahkita.csv"
DST = "data/processed/sulawesi_konflik_agraria_tanahkita_v2.csv"

SULAWESI_PROVINCES = [
    'Sulawesi Tengah', 'Sulawesi Tenggara', 'Sulawesi Selatan',
    'Sulawesi Utara', 'Sulawesi Barat', 'Gorontalo'
]

SOURCE_COLS = ['judul', 'deskripsi', 'lokasi', 'narasi']

print("=== NER Filter Pipeline: TanahKita -> Sulawesi Only ===")
print(f"Input : {SRC}")
print(f"Output: {DST}")
print()

# Step 1: Load sumber asli (v1)
df = pd.read_csv(SRC)
df['tahun'] = pd.to_numeric(df['tahun'], errors='coerce')
print(f"Total rows asli   : {len(df)}")

# Step 2: Jalankan NER per baris - provinsi + kabupaten
def deduce_row_prov(row):
    combined = ' '.join([str(row[c]) for c in SOURCE_COLS if pd.notna(row[c])])
    return deduce_sulawesi_province(combined, default_val='LUAR_SULAWESI')

def deduce_row_kab(row):
    combined = ' '.join([str(row[c]) for c in SOURCE_COLS if pd.notna(row[c])])
    return deduce_kabupaten(combined, default_val='')

df['provinsi_ner'] = df.apply(deduce_row_prov, axis=1)
df['kabupaten_ner'] = df.apply(deduce_row_kab, axis=1)

print()
print("=== Distribusi NER Provinsi ===")
print(df['provinsi_ner'].value_counts().to_string())

# Step 3: Filter hanya Sulawesi (exclude 'Sulawesi (unspecified)' untuk konservatif)
df_sulawesi = df[df['provinsi_ner'].isin(SULAWESI_PROVINCES)].copy()

print()
print(f"Rows Sulawesi     : {len(df_sulawesi)}")
print(f"Rows dibuang      : {len(df) - len(df_sulawesi)} (luar Sulawesi / unspecified)")

# Step 4: Simpan v2
df_sulawesi.to_csv(DST, index=False)
print(f"\nSaved: {DST}")
print()
print("=== Distribusi NER Kabupaten (Sulawesi only) ===")
print(df_sulawesi['kabupaten_ner'].value_counts().to_string())

# Step 5: Validasi angka Sosial 2 & 3
df_sulawesi['dampak_masyarakat_jiwa'] = pd.to_numeric(
    df_sulawesi['dampak_masyarakat_jiwa'], errors='coerce').fillna(0)

keywords_air = 'nelayan|pesisir|laut|tambak|air|sungai|DAS|danau|irigasi|banjir'
df_darat = df_sulawesi[~df_sulawesi['sektor'].str.contains(keywords_air, case=False, na=False)]

sosial2 = df_darat['dampak_masyarakat_jiwa'].sum()
sosial3 = len(df_darat[df_darat['indikasi_kriminalisasi'] == True])

print()
print("=== Angka Sosial setelah NER filter ===")
print(f"Sosial 2 (Jiwa Terdampak) : {sosial2:,.0f}")
print(f"Sosial 3 (Kriminalisasi)  : {sosial3}")

print()
print("=== Per Provinsi ===")
for prov in SULAWESI_PROVINCES:
    dp = df_darat[df_darat['provinsi_ner'] == prov]
    jiwa = dp['dampak_masyarakat_jiwa'].sum()
    krim = len(dp[dp['indikasi_kriminalisasi'] == True])
    print(f"  {prov:<25}: jiwa={jiwa:>8,.0f}, krim={krim}")

print()
print("Pipeline selesai.")
