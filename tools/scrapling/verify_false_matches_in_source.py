"""
Script untuk verifikasi false matches:
1. Cek apakah nama perusahaan MinerbaOne dari false match list ada di data MinerbaOne asli
2. Cek apakah nama perusahaan CGS dari false match list ada di data CGS asli
3. Identifikasi data yang perlu ditambahkan ke master dataset

Author: AI Assistant
Date: 2026-06-12
"""

import pandas as pd
from pathlib import Path

# False match list dari user
false_matches = [
    ("ADHI KARTIKO PRATAMA", "Adhikara Cipta Mulia", 65.0),
    ("ANDALAN ENERGI NUSANTARA", "Integra Mining Nusantara", 62.0),
    ("ANEKA TAMBANG", "Anugrah Tambang Sejahtera", 63.0),
    ("APOLLO NICKEL INDONESIA", "Kolaka Nickel Indonesia", 70.0),
    ("ARGA MORINI INDAH", "Artha Mining Industry", 63.0),
    ("ARGA MORINI INDOTAMA", "Artha Mining Industry", 63.0),
    ("ARTHA BUMI MINERAL", "Artabumi Sentra Industri", 67.0),
    ("BHUMI KARYA UTAMA", "Surya Saga Utama", 61.0),
    ("BUMI DUA MINERAL", "Macika Mineral Industri", 62.0),
    ("BUMI INDAH SULTRA", "Bukit Smelter Indonesia", 65.0),
    ("BUMI NIKEL NUSANTARA", "Integra Mining Nusantara", 64.0),
    ("CAHAYA MURNI SEJAHTERA", "Cahaya Smelter Indonesia", 65.0),
    ("CIPTA DJAYA SELARAS MINING", "Integra Mining Nusantara", 60.0),
    ("FATWA BUMI SEJAHTERA", "Mapan Asri Sejahtera", 70.0),
    ("GEMILANG MULTI MINERAL", "Asia Mining Minerals", 62.0),
    ("GEOMINERAL INTI PERKASA", "Sambas Minerals Mining", 62.0),
    ("GERBANG MULTI SEJAHTERA", "Mapan Asri Sejahtera", 60.0),
    ("HENGJAYA MINERALINDO", "Genba Multi Mineral", 62.0),
    ("INDONUSA ARTA MULYA", "Artha Mining Industry", 60.0),
    ("INTEGRA MINING NUSANTARA INDONESIA", "Tsingshan Steel Indonesia", 64.0),
    ("JAGAD RAYATAMA", "Surya Saga Utama", 73.0),
    ("KONAWE NIKEL NUSANTARA", "Integra Mining Nusantara", 65.0),
    ("KONAWE UTARA INDO MINERAL MINING", "Asia Mining Minerals", 65.0),
    ("MADANI SEJAHTERA", "Mapan Asri Sejahtera", 78.0),
    ("MEGA TAMBANG INDONESIA", "PT MBG Nikel Indonesia", 64.0),
    ("MINERAL BUMI NUSANTARA", "Artabumi Sentra Industri", 61.0),
    ("MULAI DARI INDONESIA", "Bukit Smelter Indonesia", 65.0),
    ("MULTI DINAR KARYA", "Genba Multi Mineral", 61.0),
    ("MULTI MENTARI INTERNUSA", "Lestari Smelter Indonesia", 62.0),
    ("MUSHAR UTAMA SULTRA", "Surya Saga Utama", 74.0),
    ("ODDELL INDONESIA", "Bukit Smelter Indonesia", 62.0),
    ("PAM MINERAL", "Genba Multi Mineral", 60.0),
    ("PINHARD INDONESIA", "Tsingshan Steel Indonesia", 67.0),
    ("PONGKERU MINERAL UTAMA", "Titan Mineral Utama", 73.0),
    ("PUTRA KENDARI SEJAHTERA", "Mapan Asri Sejahtera", 74.0),
    ("PUTRA KONAWE UTAMA", "Surya Saga Utama", 65.0),
    ("PUTRA MEKONGGA SEJAHTERA", "Mapan Asri Sejahtera", 64.0),
    ("PUTRA SULAWESI MINNING", "Sulawesi Mining Investment", 62.0),
    ("ROHUL ENERGI INDONESIA", "Bintang Smelter Indonesia", 60.0),
    ("ROSHINI INDONESIA", "Kolaka Nickel Indonesia", 65.0),
    ("SINAR JAYA SULTRA UTAMA", "Surya Saga Utama", 67.0),
    ("SINOSTEEL INDONESIA MINING", "Walsin Nickel Industrial Indonesia", 60.0),
    ("SUMBER MINERAL ABADI", "Genba Multi Mineral", 62.0),
    ("SUMBER PERMATA SELARAS", "PT Metal Smelt Indo Selaras", 61.0),
    ("TAMBANG INDONESIA SEJAHTERA", "Anugrah Tambang Sejahtera", 77.0),
    ("TAMBANG MINERAL MAJU", "Asia Mining Minerals", 65.0),
    ("TIMAH INVESTASI MINERAL", "Macika Mineral Industri", 61.0),
    ("TIRAN INDONESIA", "Kolaka Nickel Indonesia", 63.0),
    ("TONIA MITRA SEJAHTERA", "Anugrah Tambang Sejahtera", 65.0),
    ("TOSHIDA INDONESIA", "Kolaka Nickel Indonesia", 60.0),
    ("TOTAL PRIMA INDONESIA", "Lestari Smelter Indonesia", 61.0),
    ("VALE INDONESIA", "Kolaka Nickel Indonesia", 65.0),
    ("VALE INDONESIA", "Lestari Smelter Indonesia", 67.0),
    ("WIJAYA INTI NUSANTARA", "Integra Mining Nusantara", 62.0),
]

# Paths
base_dir = Path(__file__).parent.parent.parent
minerbaone_file = base_dir / "tools/scrapling/output/full/minerbaone_companies.csv"
cgs_file = base_dir / "tools/scrapling/output/cgs_dataset_extracted.csv"
master_file = base_dir / "data/processed/esdm_master_sulawesi_nickel_2016_2026_id.csv"

print("=" * 80)
print("VERIFIKASI FALSE MATCHES")
print("=" * 80)

# Load data
print("\n[1] Loading datasets...")
df_minerbaone = pd.read_csv(minerbaone_file)
df_cgs = pd.read_csv(cgs_file)
df_master = pd.read_csv(master_file)

print(f"    - MinerbaOne companies: {len(df_minerbaone)} records")
print(f"    - CGS smelters: {len(df_cgs)} records")
print(f"    - Current master: {len(df_master)} records")

# Normalize names for matching
df_minerbaone['nama_normalized'] = df_minerbaone['nama'].str.upper().str.strip()
df_cgs['nama_normalized'] = df_cgs['Smelter Name'].str.upper().str.strip()

# Prepare results
minerbaone_results = []
cgs_results = []

print("\n[2] Checking MinerbaOne false matches...")
for minerbaone_name, cgs_name, score in false_matches:
    match = df_minerbaone[df_minerbaone['nama_normalized'] == minerbaone_name.upper()]
    
    if len(match) > 0:
        minerbaone_results.append({
            'nama_minerbaone': minerbaone_name,
            'nama_cgs_paired': cgs_name,
            'match_score': score,
            'found_in_minerbaone': 'YES',
            'company_id': match.iloc[0]['id_perusahaan'],
            'total_permits': len(match)
        })
    else:
        minerbaone_results.append({
            'nama_minerbaone': minerbaone_name,
            'nama_cgs_paired': cgs_name,
            'match_score': score,
            'found_in_minerbaone': 'NO',
            'company_id': None,
            'total_permits': 0
        })

print("\n[3] Checking CGS false matches...")
unique_cgs_names = list(set([name for _, name, _ in false_matches]))
for cgs_name in unique_cgs_names:
    match = df_cgs[df_cgs['nama_normalized'] == cgs_name.upper()]
    
    if len(match) > 0:
        cgs_results.append({
            'nama_cgs': cgs_name,
            'found_in_cgs': 'YES',
            'province': match.iloc[0]['Province'] if 'Province' in match.columns else None,
            'regency': match.iloc[0]['Regency'] if 'Regency' in match.columns else None,
        })
    else:
        cgs_results.append({
            'nama_cgs': cgs_name,
            'found_in_cgs': 'NO',
            'province': None,
            'regency': None,
        })

# Convert to DataFrames
df_minerbaone_results = pd.DataFrame(minerbaone_results)
df_cgs_results = pd.DataFrame(cgs_results)

# Save results
output_dir = base_dir / "tools/scrapling/output"
minerbaone_output = output_dir / "false_match_verification_minerbaone.csv"
cgs_output = output_dir / "false_match_verification_cgs.csv"

df_minerbaone_results.to_csv(minerbaone_output, index=False, encoding='utf-8-sig')
df_cgs_results.to_csv(cgs_output, index=False, encoding='utf-8-sig')

print(f"\n[4] Results saved:")
print(f"    - MinerbaOne verification: {minerbaone_output}")
print(f"    - CGS verification: {cgs_output}")

# Summary statistics
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

found_minerbaone = df_minerbaone_results[df_minerbaone_results['found_in_minerbaone'] == 'YES']
not_found_minerbaone = df_minerbaone_results[df_minerbaone_results['found_in_minerbaone'] == 'NO']

print(f"\nMinerbaOne Companies:")
print(f"  - Found in source data: {len(found_minerbaone)} / {len(df_minerbaone_results)}")
print(f"  - NOT found in source data: {len(not_found_minerbaone)} / {len(df_minerbaone_results)}")

if len(not_found_minerbaone) > 0:
    print(f"\n  Companies NOT FOUND:")
    for _, row in not_found_minerbaone.iterrows():
        print(f"    - {row['nama_minerbaone']}")

found_cgs = df_cgs_results[df_cgs_results['found_in_cgs'] == 'YES']
not_found_cgs = df_cgs_results[df_cgs_results['found_in_cgs'] == 'NO']

print(f"\nCGS Smelters:")
print(f"  - Found in source data: {len(found_cgs)} / {len(df_cgs_results)}")
print(f"  - NOT found in source data: {len(not_found_cgs)} / {len(df_cgs_results)}")

if len(not_found_cgs) > 0:
    print(f"\n  Smelters NOT FOUND:")
    for _, row in not_found_cgs.iterrows():
        print(f"    - {row['nama_cgs']}")

print("\n" + "=" * 80)
print("NEXT STEPS")
print("=" * 80)
print("""
1. Review the verification files to see which companies/smelters were found
2. If all MinerbaOne companies are found, they should be added as separate rows in the master
3. If all CGS smelters are found, they should be added as separate rows in the master
4. Current false matches should be SPLIT into 2 separate rows:
   - Row 1: MinerbaOne company data (without CGS match)
   - Row 2: CGS smelter data (without MinerbaOne match)
""")
