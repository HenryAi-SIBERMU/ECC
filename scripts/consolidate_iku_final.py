#!/usr/bin/env python3
"""
Konsolidasi semua data IKU Sulawesi:
1. Data dari SLHI 2019-2023 (sudah ada)
2. Data 2024 dari Open Data Sulut
3. Data 2025 dari SLHI 2025
Output: Dataset IKU lengkap untuk dashboard
"""

import pandas as pd

print("="*70)
print("📊 Konsolidasi Final - Data IKU Sulawesi")
print("="*70)

# 1. Load data existing (2019-2023 + 2025)
df_existing = pd.read_csv('data/processed/iku_sulawesi_2019_2024_clean.csv')
print(f"\n✅ Loaded existing data: {len(df_existing)} rows")
print(f"   Years: {sorted(df_existing['Tahun'].unique())}")

# 2. Add 2024 data manually (dari Open Data Sulut + SLHI crosscheck)
data_2024 = [
    {'Tahun': 2024, 'Provinsi': 'Sulawesi Utara', 'IKU': 93.44, 'Sumber': 'Open Data Sulut 2024'},
    {'Tahun': 2024, 'Provinsi': 'Sulawesi Tengah', 'IKU': 92.93, 'Sumber': 'Estimasi SLHI 2025 (2023 baseline)'},
    {'Tahun': 2024, 'Provinsi': 'Sulawesi Selatan', 'IKU': 91.50, 'Sumber': 'Estimasi SLHI (2023 baseline +1)'},
    {'Tahun': 2024, 'Provinsi': 'Sulawesi Tenggara', 'IKU': 93.00, 'Sumber': 'Estimasi SLHI (2023 baseline)'},
    {'Tahun': 2024, 'Provinsi': 'Gorontalo', 'IKU': 93.50, 'Sumber': 'Estimasi SLHI (2023 baseline)'},
    {'Tahun': 2024, 'Provinsi': 'Sulawesi Barat', 'IKU': 92.50, 'Sumber': 'Estimasi SLHI (2023 baseline)'},
]

df_2024 = pd.DataFrame(data_2024)
print(f"\n➕ Adding 2024 data: {len(df_2024)} rows")

# 3. Combine
df_combined = pd.concat([df_existing, df_2024], ignore_index=True)

# Remove year 2025 (future projection, not needed for analysis 2014-2024)
df_combined = df_combined[df_combined['Tahun'] != 2025]

print(f"\n📦 Combined dataset: {len(df_combined)} rows")
print(f"   Years: {sorted(df_combined['Tahun'].unique())}")

# 4. Sort and clean
df_combined = df_combined.sort_values(['Tahun', 'Provinsi']).reset_index(drop=True)

# 5. Summary
print("\n📊 RINGKASAN FINAL:")
print("\nCoverage per Tahun:")
print(df_combined.groupby('Tahun').size())

print("\nCoverage per Provinsi:")
print(df_combined.groupby('Provinsi').size())

print("\n📋 Data Range:")
for prov in sorted(df_combined['Provinsi'].unique()):
    prov_data = df_combined[df_combined['Provinsi'] == prov]
    years = sorted(prov_data['Tahun'].tolist())
    iku_range = f"{prov_data['IKU'].min():.2f} - {prov_data['IKU'].max():.2f}"
    print(f"  {prov:20s}: {years[0]}-{years[-1]} (IKU: {iku_range})")

# 6. Save final dataset
output_file = 'data/processed/iku_sulawesi_2019_2024_final.csv'
df_combined.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"\n💾 Saved to: {output_file}")

# 7. Status missing years
print("\n" + "="*70)
print("📌 STATUS DATA:")
print("="*70)
print("✅ TERSEDIA: 2019-2024 (6 tahun)")
print("❌ HILANG: 2014-2018 (5 tahun)")
print("\n💡 REKOMENDASI untuk tahun hilang:")
print("   1. Scrape Portal Open Data Provinsi (kemungkinan ada)")
print("   2. Request manual ke BPS/KLHK regional")
print("   3. Gunakan linear interpolation/backfill dari 2019")
print("="*70)
