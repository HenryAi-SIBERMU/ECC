"""
RECREATE CORRECT DATASET - Full Pipeline
Recreates esdm_master_sulawesi_nikel_2016_2026_id.csv from scratch
"""
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from datetime import datetime
import os

print("="*100)
print("RECREATE CORRECT DATASET - FULL PIPELINE")
print("="*100)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# ============================================================================
# STEP 1: Load Source Data
# ============================================================================
print("STEP 1: Loading source data...")
print("-"*100)

# Get script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, '..', '..')

# Load MinerbaOne data
df_permits = pd.read_csv(os.path.join(script_dir, 'output/full/minerbaone_permits.csv'))
df_details = pd.read_csv(os.path.join(script_dir, 'output/full/minerbaone_details.csv'))
df_cgs = pd.read_csv(os.path.join(script_dir, 'output/cgs_dataset_extracted.csv'))
df_pmdn = pd.read_csv(os.path.join(project_root, 'data/raw/bps_pmdn/bps_investasi_pmdn_sulawesi_2016_2026.csv'))

print(f"✅ Loaded all source data")

# ============================================================================
# STEP 2: Filter to Sulawesi Nickel Permits
# ============================================================================
print("\nSTEP 2: Filtering to Sulawesi nickel permits...")
print("-"*100)

# Filter to actual licenses
df_permits_actual = df_permits[df_permits['jenis_perizinan'].isin(['IUP', 'IUPK', 'KK', 'PKP2B'])].copy()

# Filter to nickel
df_permits_nickel = df_permits_actual[
    df_permits_actual['komoditas'].str.contains('ikel', case=False, na=False)
].copy()

# Kabupaten to province mapping
kabupaten_to_province = {
    'MOROWALI': 'Central Sulawesi', 'MOROWALI UTARA': 'Central Sulawesi',
    'BANGGAI': 'Central Sulawesi', 'BANGGAI LAUT': 'Central Sulawesi',
    'BANGGAI KEPULAUAN': 'Central Sulawesi', 'POSO': 'Central Sulawesi',
    'TOJO UNA-UNA': 'Central Sulawesi', 'TOLI-TOLI': 'Central Sulawesi',
    'BUOL': 'Central Sulawesi', 'PARIGI MOUTONG': 'Central Sulawesi',
    'DONGGALA': 'Central Sulawesi', 'SIGI': 'Central Sulawesi',
    'KONAWE': 'South East Sulawesi', 'KONAWE UTARA': 'South East Sulawesi',
    'KONAWE SELATAN': 'South East Sulawesi', 'KONAWE KEPULAUAN': 'South East Sulawesi',
    'KOLAKA': 'South East Sulawesi', 'KOLAKA UTARA': 'South East Sulawesi',
    'KOLAKA TIMUR': 'South East Sulawesi', 'BOMBANA': 'South East Sulawesi',
    'WAKATOBI': 'South East Sulawesi', 'BUTON': 'South East Sulawesi',
    'BUTON UTARA': 'South East Sulawesi', 'BUTON TENGAH': 'South East Sulawesi',
    'BUTON SELATAN': 'South East Sulawesi', 'MUNA': 'South East Sulawesi',
    'MUNA BARAT': 'South East Sulawesi',
    'LUWU': 'South Sulawesi', 'LUWU TIMUR': 'South Sulawesi',
    'LUWU UTARA': 'South Sulawesi', 'BONE': 'South Sulawesi',
    'GORONTALO': 'Gorontalo', 'GORONTALO UTARA': 'Gorontalo',
}

def map_kabupaten_to_province(lokasi):
    if pd.isna(lokasi):
        return None
    lokasi = lokasi.upper()
    for kab, prov in kabupaten_to_province.items():
        if kab in lokasi:
            return prov
    return None

# Merge with company details
df_minerbaone = df_permits_nickel.merge(
    df_details[['id_badan_usaha', 'nama_badan_usaha', 'alamat', 'email', 'no_telp']],
    on='id_badan_usaha',
    how='left'
)

df_minerbaone['province'] = df_minerbaone['lokasi_perizinan'].apply(map_kabupaten_to_province)
df_sulawesi = df_minerbaone[df_minerbaone['province'].notna()].copy()

print(f"✅ Sulawesi nickel permits: {len(df_sulawesi):,}")

# ============================================================================
# STEP 3: Fuzzy Match with CGS
# ============================================================================
print("\nSTEP 3: Fuzzy matching with CGS...")
print("-"*100)

df_cgs_sulawesi = df_cgs[df_cgs['Province'].str.contains('Sulawesi', case=False, na=False)].copy()

def fuzzy_match_company(name1, name2):
    if pd.isna(name1) or pd.isna(name2):
        return 0
    return fuzz.token_sort_ratio(str(name1).upper(), str(name2).upper())

merged_rows = []

for idx, permit in df_sulawesi.iterrows():
    company_name = permit['nama_badan_usaha']
    province = permit['province']
    
    best_match = None
    best_score = 0
    
    for cgs_idx, smelter in df_cgs_sulawesi.iterrows():
        if smelter['Province'] != province:
            continue
        
        score = fuzzy_match_company(company_name, smelter['Smelter Name'])
        if score > best_score:
            best_score = score
            best_match = smelter
    
    row_data = {
        'id_perusahaan': permit['id_badan_usaha'],
        'id_izin': permit['id_perizinan'],
        'nomor_izin': permit['nomor_izin'],
        'nama_perusahaan_minerbaone': permit['nama_badan_usaha'],
        'alamat': permit['alamat'],
        'email': permit['email'],
        'telepon': permit['no_telp'],
        'provinsi': province,
        'lokasi_lengkap': permit['lokasi_perizinan'],
        'jenis_izin': permit['jenis_perizinan'],
        'komoditas': 'Nikel',
        'fase_operasi': permit['tahap_kegiatan'],
        'status_cnc': permit['status_cnc'],
        'tahun_terbit': permit['tanggal_berlaku'][:4] if pd.notna(permit['tanggal_berlaku']) else np.nan,
        'tanggal_mulai_izin': permit['tanggal_berlaku'],
        'tanggal_berakhir_izin': permit['tanggal_berakhir'],
        'luas_hektar': permit['luas_ha'],
        'tanggal_scraping': permit['scraped_at'],
    }
    
    if best_match is not None and best_score >= 60:
        row_data['nama_perusahaan_cgs'] = best_match['Smelter Name']
        row_data['latitude'] = best_match.get('Latitude')
        row_data['longitude'] = best_match.get('Longitude')
        row_data['kapasitas_input_ton_tahun'] = best_match.get('Input Capacity (Tonnes) ')
        row_data['kapasitas_output_ton_tahun'] = best_match.get('Output Capacity (Tonnes)')
        row_data['kapasitas_ni_ekuivalen_ton_tahun'] = best_match.get('Ni metal equivalent (tonnes)')
        row_data['tipe_produk_output'] = best_match.get('Output Product ')
        row_data['sumber_data'] = 'minerbaone+cgs'
        row_data['skor_kecocokan_cgs'] = best_score
        row_data['kepercayaan_kapasitas'] = 'high' if best_score >= 80 else 'medium'
    else:
        row_data['nama_perusahaan_cgs'] = np.nan
        row_data['latitude'] = np.nan
        row_data['longitude'] = np.nan
        row_data['kapasitas_input_ton_tahun'] = np.nan
        row_data['kapasitas_output_ton_tahun'] = np.nan
        row_data['kapasitas_ni_ekuivalen_ton_tahun'] = np.nan
        row_data['tipe_produk_output'] = np.nan
        row_data['sumber_data'] = 'minerbaone'
        row_data['skor_kecocokan_cgs'] = np.nan
        row_data['kepercayaan_kapasitas'] = 'none'
    
    merged_rows.append(row_data)

df_merged = pd.DataFrame(merged_rows)
print(f"✅ Merged: {len(df_merged):,} rows")
print(f"   Matched with CGS: {df_merged['nama_perusahaan_cgs'].notna().sum():,}")

# ============================================================================
# STEP 4: Add Investment Allocation
# ============================================================================
print("\nSTEP 4: Allocating investment...")
print("-"*100)

df_pmdn_nilai = df_pmdn[df_pmdn['indikator'] == 'Investasi PMDN - Nilai (Juta Rp)'].copy()
df_pmdn_pivot = df_pmdn_nilai.pivot_table(
    index='provinsi',
    columns='tahun',
    values='nilai',
    aggfunc='sum'
).reset_index()

province_mapping = {
    'Central Sulawesi': 'Sulawesi Tengah',
    'South East Sulawesi': 'Sulawesi Tenggara',
    'South Sulawesi': 'Sulawesi Selatan',
}

capacity_by_province = df_merged.groupby('provinsi')['kapasitas_input_ton_tahun'].sum().to_dict()

def allocate_investment(row):
    province = row['provinsi']
    year = row['tahun_terbit']
    capacity = row['kapasitas_input_ton_tahun']
    
    if pd.isna(province) or pd.isna(year) or pd.isna(capacity):
        return None
    
    year = int(year)
    pmdn_province = province_mapping.get(province)
    if pmdn_province is None:
        return None
    
    pmdn_row = df_pmdn_pivot[df_pmdn_pivot['provinsi'] == pmdn_province]
    if len(pmdn_row) == 0 or year not in pmdn_row.columns:
        return None
    
    provincial_pmdn = pmdn_row[year].values[0]  # Juta Rp
    total_capacity = capacity_by_province.get(province, 0)
    
    if total_capacity == 0:
        return None
    
    # Convert Juta to Miliar, allocate 40% to mining
    mining_pmdn = (provincial_pmdn / 1000) * 0.4
    smelter_investment = (capacity / total_capacity) * mining_pmdn
    
    return smelter_investment

df_merged['investasi_miliar_rp'] = df_merged.apply(allocate_investment, axis=1)
df_merged['kepercayaan_investasi'] = df_merged['investasi_miliar_rp'].apply(
    lambda x: 'medium' if pd.notna(x) else 'none'
)
df_merged['sumber_investasi'] = 'bps_pmdn_allocated'
df_merged['metodologi_investasi'] = 'Provincial PMDN allocated proportionally by capacity (40% mining assumption)'

print(f"✅ Investment allocated: {df_merged['investasi_miliar_rp'].notna().sum():,} rows")

# ============================================================================
# STEP 5: Fix False Matching (Split scores <80)
# ============================================================================
print("\nSTEP 5: Fixing false matches (split score <80)...")
print("-"*100)

df_merged['skor_kecocokan_cgs'] = pd.to_numeric(df_merged['skor_kecocokan_cgs'], errors='coerce')

high_confidence = (df_merged['skor_kecocokan_cgs'] >= 80)
no_match = df_merged['skor_kecocokan_cgs'].isna()
false_match = ~high_confidence & ~no_match

print(f"   High confidence (≥80): {high_confidence.sum():,}")
print(f"   False match (<80): {false_match.sum():,}")
print(f"   No match: {no_match.sum():,}")

# Keep high confidence and no match
df_keep = df_merged[high_confidence | no_match].copy()

# Split false matches
df_to_split = df_merged[false_match].copy()
unmerged_rows = []

for idx, row in df_to_split.iterrows():
    # MinerbaOne row (remove CGS data)
    row_minerbaone = row.copy()
    row_minerbaone['nama_perusahaan_cgs'] = np.nan
    row_minerbaone['kapasitas_input_ton_tahun'] = np.nan
    row_minerbaone['kapasitas_output_ton_tahun'] = np.nan
    row_minerbaone['kapasitas_ni_ekuivalen_ton_tahun'] = np.nan
    row_minerbaone['tipe_produk_output'] = np.nan
    row_minerbaone['latitude'] = np.nan
    row_minerbaone['longitude'] = np.nan
    row_minerbaone['sumber_data'] = 'minerbaone'
    row_minerbaone['skor_kecocokan_cgs'] = np.nan
    row_minerbaone['kepercayaan_kapasitas'] = 'none'
    unmerged_rows.append(row_minerbaone)
    
    # CGS row (separate record)
    row_cgs = row.copy()
    row_cgs['id_perusahaan'] = np.nan
    row_cgs['id_izin'] = np.nan
    row_cgs['nomor_izin'] = np.nan
    row_cgs['nama_perusahaan_minerbaone'] = np.nan
    row_cgs['alamat'] = np.nan
    row_cgs['email'] = np.nan
    row_cgs['telepon'] = np.nan
    row_cgs['lokasi_lengkap'] = row['provinsi']
    row_cgs['jenis_izin'] = np.nan
    row_cgs['fase_operasi'] = 'OPERASI PRODUKSI'
    row_cgs['status_cnc'] = np.nan
    row_cgs['tahun_terbit'] = np.nan
    row_cgs['tanggal_mulai_izin'] = np.nan
    row_cgs['tanggal_berakhir_izin'] = np.nan
    row_cgs['luas_hektar'] = np.nan
    row_cgs['sumber_data'] = 'cgs_only'
    unmerged_rows.append(row_cgs)

df_unmerged = pd.DataFrame(unmerged_rows)
df_fixed = pd.concat([df_keep, df_unmerged], ignore_index=True)

print(f"✅ After split: {len(df_fixed):,} rows")

# ============================================================================
# STEP 6: Add Exact Matches Back
# ============================================================================
print("\nSTEP 6: Adding exact matches back...")
print("-"*100)

# 5 exact match companies
exact_matches = [
    'ANUGRAH TAMBANG SEJAHTERA',
    'GENBA MULTI MINERAL',
    'INTEGRA MINING NUSANTARA',
    'SAMBAS MINERALS MINING',
    'SURYA SAGA UTAMA'
]

# Remove CGS-only versions of these
mask_to_remove = (
    df_fixed['nama_perusahaan_cgs'].str.upper().isin(exact_matches) & 
    df_fixed['nama_perusahaan_minerbaone'].isna()
)
removed_count = mask_to_remove.sum()
df_cleaned = df_fixed[~mask_to_remove].copy()

print(f"   Removed {removed_count} CGS-only duplicates")

# Add exact matches
rows_to_add = []

for company_name in exact_matches:
    # Find in CGS
    cgs_match = df_cgs_sulawesi[df_cgs_sulawesi['Smelter Name'].str.upper() == company_name]
    if len(cgs_match) == 0:
        continue
    
    cgs_row = cgs_match.iloc[0]
    
    # Find all permits for this company in MinerbaOne
    minerbaone_matches = df_sulawesi[
        df_sulawesi['nama_badan_usaha'].str.upper() == company_name
    ]
    
    if len(minerbaone_matches) == 0:
        continue
    
    print(f"   Found {len(minerbaone_matches)} permits for {company_name}")
    
    for idx, permit in minerbaone_matches.iterrows():
        row_data = {
            'id_perusahaan': permit['id_badan_usaha'],
            'id_izin': permit['id_perizinan'],
            'nomor_izin': permit['nomor_izin'],
            'nama_perusahaan_minerbaone': permit['nama_badan_usaha'],
            'nama_perusahaan_cgs': cgs_row['Smelter Name'],
            'alamat': permit['alamat'],
            'email': permit['email'],
            'telepon': permit['no_telp'],
            'provinsi': permit['province'],
            'lokasi_lengkap': permit['lokasi_perizinan'],
            'latitude': cgs_row.get('Latitude'),
            'longitude': cgs_row.get('Longitude'),
            'jenis_izin': permit['jenis_perizinan'],
            'komoditas': 'Nikel',
            'fase_operasi': permit['tahap_kegiatan'],
            'status_cnc': permit['status_cnc'],
            'tahun_terbit': permit['tanggal_berlaku'][:4] if pd.notna(permit['tanggal_berlaku']) else np.nan,
            'tanggal_mulai_izin': permit['tanggal_berlaku'],
            'tanggal_berakhir_izin': permit['tanggal_berakhir'],
            'luas_hektar': permit['luas_ha'],
            'kapasitas_input_ton_tahun': cgs_row.get('Input Capacity (Tonnes) '),
            'kapasitas_output_ton_tahun': cgs_row.get('Output Capacity (Tonnes)'),
            'kapasitas_ni_ekuivalen_ton_tahun': cgs_row.get('Ni metal equivalent (tonnes)'),
            'tipe_produk_output': cgs_row.get('Output Product '),
            'investasi_miliar_rp': np.nan,
            'sumber_data': 'minerbaone+cgs',
            'skor_kecocokan_cgs': 100.0,
            'kepercayaan_kapasitas': 'high',
            'kepercayaan_investasi': 'none',
            'sumber_investasi': np.nan,
            'metodologi_investasi': np.nan,
            'tanggal_scraping': permit['scraped_at']
        }
        rows_to_add.append(row_data)

df_to_add = pd.DataFrame(rows_to_add)
print(f"   Adding {len(df_to_add)} exact match records")

df_final = pd.concat([df_cleaned, df_to_add], ignore_index=True)
df_final = df_final.sort_values('nama_perusahaan_minerbaone', na_position='last').reset_index(drop=True)

print(f"✅ Final dataset: {len(df_final):,} rows")

# ============================================================================
# STEP 7: Statistics
# ============================================================================
print("\n" + "="*100)
print("STATISTIK FINAL")
print("="*100)

print(f"\n📋 TOTAL RECORDS:")
print(f"  Total rows: {len(df_final):,}")
print(f"  MinerbaOne permits: {df_final['nama_perusahaan_minerbaone'].notna().sum():,}")
print(f"  Matched dengan CGS: {(df_final['nama_perusahaan_cgs'].notna() & df_final['nama_perusahaan_minerbaone'].notna()).sum():,}")

has_match = df_final['nama_perusahaan_cgs'].notna() & df_final['nama_perusahaan_minerbaone'].notna()
if has_match.sum() > 0:
    matched_scores = df_final[has_match]['skor_kecocokan_cgs']
    print(f"\n✅ MATCH QUALITY:")
    print(f"  Matched records: {len(matched_scores):,}")
    print(f"  Average score: {matched_scores.mean():.1f}")
    print(f"  Score 100 (exact): {(matched_scores == 100).sum():,}")
    print(f"  Score 80-99: {((matched_scores >= 80) & (matched_scores < 100)).sum():,}")

# ============================================================================
# STEP 8: Save CORRECT File
# ============================================================================
print("\n" + "="*100)
print("STEP 8: Saving correct file...")
print("="*100)

output_file = os.path.join(project_root, 'data/processed/esdm_master_sulawesi_nikel_2016_2026_id.csv')
df_final.to_csv(output_file, index=False)
print(f"💾 SAVED: {output_file}")
print(f"   File size: {os.path.getsize(output_file) / 1024:.1f} KB")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*100)
print("✅ SELESAI! CORRECT FILE RECREATED")
print("="*100)

print(f"""
RINGKASAN:
- Total: {len(df_final):,} rows
- Matched dengan CGS (score ≥80 atau exact): {has_match.sum():,}
- Exact matches yang ditambahkan: {len(df_to_add)}

FILE OUTPUT:
📁 data/processed/esdm_master_sulawesi_nikel_2016_2026_id.csv
   → CORRECT spelling (nikel, bukan nickel)
   → {len(df_final):,} rows
   → Hanya match score ≥80 atau exact match

EXACT MATCHES:
{chr(10).join(f'  ✅ {name}' for name in exact_matches)}

NEXT STEP:
Delete the wrong file: esdm_master_sulawesi_nickel_2016_2026_id.csv
""")

print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*100)
