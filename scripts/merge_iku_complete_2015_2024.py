#!/usr/bin/env python3
"""
Merge IKU data 2015-2018 dengan 2019-2024
Final dataset: 2015-2024 (10 tahun)
"""

import pandas as pd
from pathlib import Path

print("="*80)
print("🔗 Merging IKU Data: 2015-2018 + 2019-2024")
print("="*80)

# Load 2015-2018 data
df_2015_2018 = pd.read_csv('data/processed/iku_2015_2018_clean.csv', encoding='utf-8-sig')
print(f"\n📂 Loaded 2015-2018: {len(df_2015_2018)} rows")
print(f"   Years: {sorted(df_2015_2018['Tahun'].unique())}")
print(f"   Provinsi: {sorted(df_2015_2018['Provinsi'].unique())}")

# Load 2019-2024 data
df_2019_2024 = pd.read_csv('data/processed/iku_sulawesi_2019_2024_final.csv', encoding='utf-8-sig')
print(f"\n📂 Loaded 2019-2024: {len(df_2019_2024)} rows")
print(f"   Years: {sorted(df_2019_2024['Tahun'].unique())}")
print(f"   Provinsi: {sorted(df_2019_2024['Provinsi'].unique())}")

# Standardize columns
df_2015_2018_clean = df_2015_2018[['Provinsi', 'IKU', 'Tahun']].copy()
df_2015_2018_clean['Sumber'] = 'SLHI ' + df_2015_2018['Tahun'].astype(str)

df_2019_2024_clean = df_2019_2024[['Provinsi', 'IKU', 'Tahun', 'Sumber']].copy()

# Merge
df_merged = pd.concat([df_2015_2018_clean, df_2019_2024_clean], ignore_index=True)

# Sort by year and provinsi
df_merged = df_merged.sort_values(['Tahun', 'Provinsi']).reset_index(drop=True)

print(f"\n✅ Merged dataset: {len(df_merged)} rows")
print(f"   Years: {sorted(df_merged['Tahun'].unique())}")
print(f"   Coverage: {len(df_merged['Tahun'].unique())} years (2015-2024)")

# Calculate coverage per year
print("\n📊 Coverage by Year:")
for year in sorted(df_merged['Tahun'].unique()):
    count = len(df_merged[df_merged['Tahun'] == year])
    print(f"   {year}: {count}/6 provinsi ({count/6*100:.0f}%)")

# Calculate coverage per provinsi
print("\n🗺️  Coverage by Provinsi:")
target_provinsi = [
    'Sulawesi Utara',
    'Sulawesi Tengah',
    'Sulawesi Selatan',
    'Sulawesi Tenggara',
    'Gorontalo',
    'Sulawesi Barat'
]

for prov in target_provinsi:
    df_prov = df_merged[df_merged['Provinsi'] == prov]
    years = sorted(df_prov['Tahun'].tolist())
    missing = [y for y in range(2015, 2025) if y not in years]
    
    print(f"   {prov}: {len(years)}/10 years")
    if missing:
        print(f"      Missing: {missing}")

# Identify gaps
print("\n❌ Data Gaps:")
for year in range(2015, 2025):
    df_year = df_merged[df_merged['Tahun'] == year]
    present = df_year['Provinsi'].tolist()
    missing = [p for p in target_provinsi if p not in present]
    
    if missing:
        print(f"   {year}: Missing {len(missing)} provinsi - {missing}")

# Save merged dataset
output_file = Path('data/processed/iku_sulawesi_2015_2024_merged.csv')
df_merged.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\n💾 Saved: {output_file}")

# Create summary stats
print("\n📈 Statistical Summary by Provinsi:")
for prov in target_provinsi:
    df_prov = df_merged[df_merged['Provinsi'] == prov]
    if len(df_prov) > 0:
        mean_iku = df_prov['IKU'].mean()
        min_iku = df_prov['IKU'].min()
        max_iku = df_prov['IKU'].max()
        print(f"   {prov}: Mean={mean_iku:.2f}, Min={min_iku:.2f}, Max={max_iku:.2f}")

# Display sample
print("\n📋 Sample Data (first 15 rows):")
print(df_merged.head(15).to_string(index=False))

print("\n" + "="*80)
print("✅ SUMMARY:")
total_possible = 6 * 10  # 6 provinsi × 10 tahun
total_collected = len(df_merged)
coverage_pct = (total_collected / total_possible) * 100
print(f"   Total data points: {total_collected}/{total_possible} ({coverage_pct:.1f}%)")
print(f"   Years covered: 2015-2024 (10 years)")
print(f"   Provinsi covered: 6 (all Sulawesi provinces)")
print("\n✅ NEXT STEPS:")
print("   1. Review gaps and decide: interpolate or accept as-is")
print("   2. If needed, fill gaps using interpolation")
print("   3. Use merged dataset for dashboard")
print("="*80)
