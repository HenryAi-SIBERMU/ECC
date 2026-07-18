"""
Fix dataset: Tambahkan 5 exact match yang ketemu di MinerbaOne
Dan hapus file temporary di processed folder
"""
import pandas as pd
import numpy as np
import os

print("="*100)
print("FIX DATASET: TAMBAH EXACT MATCH & CLEAN PROCESSED FOLDER")
print("="*100)

# ====================================================================================
# STEP 1: Load datasets
# ====================================================================================
print("\nSTEP 1: Loading datasets...")

# Load current fixed dataset
df_fixed = pd.read_csv('../../data/processed/esdm_master_sulawesi_nikel_2016_2026_id_fixed.csv')
print(f"Dataset fixed: {len(df_fixed):,} rows")

# Load check results
df_check = pd.read_csv('../../data/processed/cgs_in_minerbaone_check.csv')
print(f"Check results: {len(df_check)} CGS companies")

# Load MinerbaOne full data
df_permits = pd.read_csv('output/full/minerbaone_permits.csv')
df_details = pd.read_csv('output/full/minerbaone_details.csv')
print(f"MinerbaOne permits: {len(df_permits):,}")
print(f"MinerbaOne details: {len(df_details):,}")

# Load CGS for capacity data
df_cgs = pd.read_csv('output/cgs_dataset_extracted.csv')
print(f"CGS smelters: {len(df_cgs):,}")

# ====================================================================================
# STEP 2: Find exact matches to add
# ====================================================================================
print("\n" + "="*100)
print("STEP 2: Find exact matches to add back...")
print("="*100)

exact_matches = df_check[df_check['found_in_minerbaone'] == 'YES - EXACT']
print(f"\nFound {len(exact_matches)} exact matches:")

for idx, row in exact_matches.iterrows():
    print(f"  - {row['cgs_name']} (ID: {row['company_id']})")

# ====================================================================================
# STEP 3: For each exact match, find all permits and merge with CGS
# ====================================================================================
print("\n" + "="*100)
print("STEP 3: Merging exact matches with CGS data...")
print("="*100)

rows_to_add = []

for idx, match in exact_matches.iterrows():
    cgs_name = match['cgs_name']
    company_id = match['company_id']
    
    print(f"\n🔍 Processing: {cgs_name}")
    
    # Get all permits for this company
    company_permits = df_permits[df_permits['id_badan_usaha'] == company_id].copy()
    print(f"   Found {len(company_permits)} permits")
    
    # Get company details
    company_detail = df_details[df_details['id_badan_usaha'] == company_id]
    
    # Get CGS data
    cgs_data = df_cgs[df_cgs['Smelter Name'].str.upper() == cgs_name.upper()]
    
    if len(cgs_data) == 0:
        print(f"   ⚠️  CGS data not found, skipping...")
        continue
    
    cgs_row = cgs_data.iloc[0]
    print(f"   ✅ CGS data found")
    print(f"      Capacity input: {cgs_row.get('Input Capacity (Tonnes) ', 'N/A')}")
    print(f"      Capacity output: {cgs_row.get('Output Capacity (Tonnes)', 'N/A')}")
    
    # Merge each permit with CGS data
    for pidx, permit in company_permits.iterrows():
        # Map kabupaten to province (simplified - use from original dataset logic)
        row_data = {
            'id_perusahaan': permit['id_badan_usaha'],
            'id_izin': permit['id_perizinan'],
            'nomor_izin': permit['nomor_izin'],
            'nama_perusahaan_minerbaone': company_detail.iloc[0]['nama_badan_usaha'] if len(company_detail) > 0 else cgs_name,
            'nama_perusahaan_cgs': cgs_name,
            'alamat': company_detail.iloc[0]['alamat'] if len(company_detail) > 0 else np.nan,
            'email': company_detail.iloc[0]['email'] if len(company_detail) > 0 else np.nan,
            'telepon': company_detail.iloc[0]['no_telp'] if len(company_detail) > 0 else np.nan,
            'provinsi': cgs_row.get('Province', np.nan),
            'lokasi_lengkap': permit['lokasi_perizinan'],
            'latitude': cgs_row.get('Latitude', np.nan),
            'longitude': cgs_row.get('Longitude', np.nan),
            'jenis_izin': permit['jenis_perizinan'],
            'komoditas': 'Nikel',
            'fase_operasi': permit['tahap_kegiatan'],
            'status_cnc': permit['status_cnc'],
            'tahun_terbit': permit['tanggal_berlaku'][:4] if pd.notna(permit['tanggal_berlaku']) else np.nan,
            'tanggal_mulai_izin': permit['tanggal_berlaku'],
            'tanggal_berakhir_izin': permit['tanggal_berakhir'],
            'luas_hektar': permit['luas_ha'],
            'kapasitas_input_ton_tahun': cgs_row.get('Input Capacity (Tonnes) ', np.nan),
            'kapasitas_output_ton_tahun': cgs_row.get('Output Capacity (Tonnes)', np.nan),
            'kapasitas_ni_ekuivalen_ton_tahun': cgs_row.get('Ni metal equivalent (tonnes)', np.nan),
            'tipe_produk_output': cgs_row.get('Output Product ', np.nan),
            'investasi_miliar_rp': np.nan,  # Will be filled later
            'sumber_data': 'minerbaone+cgs',
            'skor_kecocokan_cgs': 100.0,  # Exact match
            'kepercayaan_kapasitas': 'high',
            'kepercayaan_investasi': 'none',
            'sumber_investasi': np.nan,
            'metodologi_investasi': np.nan,
            'tanggal_scraping': permit['scraped_at']
        }
        
        rows_to_add.append(row_data)
    
    print(f"   ✅ Added {len(company_permits)} records")

df_to_add = pd.DataFrame(rows_to_add)
print(f"\n✅ Total rows to add: {len(df_to_add)}")

# ====================================================================================
# STEP 4: Remove duplicate exact matches from fixed dataset
# ====================================================================================
print("\n" + "="*100)
print("STEP 4: Remove old split versions of these companies...")
print("="*100)

# Remove CGS-only records for these exact match companies
exact_match_names = exact_matches['cgs_name'].tolist()
print(f"Removing CGS-only records for: {exact_match_names}")

mask_to_remove = (
    df_fixed['nama_perusahaan_cgs'].isin(exact_match_names) & 
    df_fixed['nama_perusahaan_minerbaone'].isna()
)
removed_count = mask_to_remove.sum()
print(f"Removing {removed_count} CGS-only duplicate records...")

df_cleaned = df_fixed[~mask_to_remove].copy()
print(f"Dataset after removal: {len(df_cleaned):,} rows")

# ====================================================================================
# STEP 5: Add new merged records
# ====================================================================================
print("\n" + "="*100)
print("STEP 5: Adding new merged records...")
print("="*100)

df_final = pd.concat([df_cleaned, df_to_add], ignore_index=True)
print(f"✅ Final dataset: {len(df_final):,} rows")

# Sort by company name
df_final = df_final.sort_values('nama_perusahaan_minerbaone', na_position='last').reset_index(drop=True)

# ====================================================================================
# STEP 6: Statistics
# ====================================================================================
print("\n" + "="*100)
print("STATISTIK FINAL")
print("="*100)

print(f"\n📋 TOTAL RECORDS:")
print(f"  Total rows: {len(df_final):,}")
print(f"  MinerbaOne permits: {df_final['nama_perusahaan_minerbaone'].notna().sum():,}")
print(f"  Matched dengan CGS: {(df_final['nama_perusahaan_cgs'].notna() & df_final['nama_perusahaan_minerbaone'].notna()).sum():,}")
print(f"  CGS standalone: {(df_final['nama_perusahaan_cgs'].notna() & df_final['nama_perusahaan_minerbaone'].isna()).sum():,}")

print(f"\n✅ MATCH QUALITY:")
has_match = df_final['nama_perusahaan_cgs'].notna() & df_final['nama_perusahaan_minerbaone'].notna()
if has_match.sum() > 0:
    matched_scores = df_final[has_match]['skor_kecocokan_cgs']
    print(f"  Matched records: {len(matched_scores):,}")
    print(f"  Average score: {matched_scores.mean():.1f}")
    print(f"  Score 100 (exact): {(matched_scores == 100).sum():,}")
    print(f"  Score 90-99: {((matched_scores >= 90) & (matched_scores < 100)).sum():,}")
    print(f"  Score 80-89: {((matched_scores >= 80) & (matched_scores < 90)).sum():,}")

print(f"\n💰 DATA COMPLETENESS:")
print(f"  Luas lahan: {df_final['luas_hektar'].notna().sum():,}/{len(df_final)} ({df_final['luas_hektar'].notna().sum()/len(df_final)*100:.1f}%)")
print(f"  Kapasitas input: {df_final['kapasitas_input_ton_tahun'].notna().sum():,}/{len(df_final)} ({df_final['kapasitas_input_ton_tahun'].notna().sum()/len(df_final)*100:.1f}%)")
print(f"  Kapasitas output: {df_final['kapasitas_output_ton_tahun'].notna().sum():,}/{len(df_final)} ({df_final['kapasitas_output_ton_tahun'].notna().sum()/len(df_final)*100:.1f}%)")

# ====================================================================================
# STEP 7: Save final clean dataset
# ====================================================================================
print("\n" + "="*100)
print("STEP 7: Saving final clean dataset...")
print("="*100)

output_file = '../../data/processed/esdm_master_sulawesi_nikel_2016_2026_id.csv'
df_final.to_csv(output_file, index=False)
print(f"💾 SAVED: {output_file}")

# ====================================================================================
# STEP 8: Clean processed folder - DELETE temporary files
# ====================================================================================
print("\n" + "="*100)
print("STEP 8: Cleaning processed folder...")
print("="*100)

files_to_delete = [
    '../../data/processed/esdm_master_sulawesi_nickel_2016_2026_metadata.txt',  # Old metadata
    '../../data/processed/esdm_master_sulawesi_nikel_2016_2026_id_fixed.csv',  # Temporary fixed
    '../../data/processed/esdm_split_report.csv',  # Temporary report
    '../../data/processed/cgs_in_minerbaone_check.csv',  # Temporary check
]

deleted = []
not_found = []

for file_path in files_to_delete:
    if os.path.exists(file_path):
        os.remove(file_path)
        deleted.append(file_path.split('/')[-1])
        print(f"  ❌ DELETED: {file_path.split('/')[-1]}")
    else:
        not_found.append(file_path.split('/')[-1])
        print(f"  ⚠️  NOT FOUND: {file_path.split('/')[-1]}")

print(f"\n✅ Deleted {len(deleted)} files")
if len(not_found) > 0:
    print(f"⚠️  {len(not_found)} files not found (already deleted?)")

# ====================================================================================
# SUMMARY
# ====================================================================================
print("\n" + "="*100)
print("✅ SELESAI!")
print("="*100)

print(f"""
RINGKASAN:
- Added {len(df_to_add)} records dari exact match (5 companies)
- Removed {removed_count} duplicate CGS-only records
- Final dataset: {len(df_final):,} rows
- Matched dengan CGS: {has_match.sum():,} records
- Deleted {len(deleted)} temporary files

FINAL CLEAN FILE:
📁 data/processed/esdm_master_sulawesi_nikel_2016_2026_id.csv
   → {len(df_final):,} rows
   → Hanya match score ≥80 atau exact match
   → Folder processed sudah CLEAN

EXACT MATCHES YANG DITAMBAHKAN:
{chr(10).join(f'  ✅ {name}' for name in exact_match_names)}
""")
