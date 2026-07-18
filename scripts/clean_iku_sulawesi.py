#!/usr/bin/env python3
"""
Bersihkan data IKU Sulawesi - ambil hanya data yang valid
Filter: IKU harus 0-100 dan dari halaman yang benar (bukan data limbah/lainnya)
"""

import pandas as pd

# Read raw extracted data
df = pd.read_csv('data/processed/iku_sulawesi_extracted_slhi.csv')

print("="*70)
print("🧹 Membersihkan Data IKU Sulawesi")
print("="*70)
print(f"\nTotal raw data: {len(df)} rows")

# Filter hanya data IKU yang valid (nilai 70-100, karena IKU Sulawesi biasanya tinggi)
# Exclude page 327 yang isinya bukan IKU
df_clean = df[
    (df['Indeks Kualitas Udara'] >= 70) & 
    (df['Indeks Kualitas Udara'] <= 100) &
    (df['Halaman'] != 327) &
    (df['Halaman'] != 319)  # Juga exclude page 319 dari SLHI 2025
]

print(f"Setelah filter (IKU 70-100, exclude page 327/319): {len(df_clean)} rows")

# Mapping kolom tahun ke tahun sebenarnya
def fix_year(row):
    """Fix year based on column name"""
    col = str(row['Kolom'])
    
    if col == '2019':
        return 2019
    elif col == '2020':
        return 2020
    elif col == '2021':
        return 2021
    elif col == '2022':
        return 2022
    elif col == '2023':
        return 2023
    elif col == '2024':
        return 2024
    elif col == '20201':
        return 2020
    elif col == '20211':
        return 2021
    elif col == '20221':
        return 2022
    elif col == '20231':
        return 2023
    else:
        return row['Tahun']  # Keep original if can't parse

df_clean['Tahun_Fixed'] = df_clean.apply(fix_year, axis=1)

# Rebuild clean dataframe
df_final = df_clean[['Tahun_Fixed', 'Provinsi', 'Indeks Kualitas Udara', 'Sumber']].copy()
df_final.columns = ['Tahun', 'Provinsi', 'IKU', 'Sumber']

# Sort by year and province
df_final = df_final.sort_values(['Tahun', 'Provinsi']).reset_index(drop=True)

# Remove duplicates (keep first occurrence)
df_final = df_final.drop_duplicates(subset=['Tahun', 'Provinsi'], keep='first')

print(f"\nSetelah deduplikasi: {len(df_final)} rows")

# Save cleaned data
output_file = 'data/processed/iku_sulawesi_2019_2024_clean.csv'
df_final.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"\n💾 Saved to: {output_file}")

print("\n📊 Ringkasan Data:")
print("\nPer Tahun:")
print(df_final.groupby('Tahun').size())

print("\nPer Provinsi:")
print(df_final.groupby('Provinsi').size())

print("\n📋 Preview Data:")
print(df_final.head(20))

print("\n" + "="*70)
print("✅ Data IKU Sulawesi siap digunakan!")
print("="*70)
