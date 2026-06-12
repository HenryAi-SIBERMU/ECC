"""
Fix False Matching - Pisahkan Match Yang Salah Jadi Baris Terpisah
Threshold: Match dengan skor <80% akan dipisah
"""
import pandas as pd
import numpy as np

print("="*100)
print("FIX FALSE MATCHING - UNMERGE DATA YANG SALAH MATCH")
print("="*100)

# Load current merged data
df = pd.read_csv('../../data/processed/esdm_master_sulawesi_nickel_2016_2026_id.csv')
print(f"\nData awal: {len(df):,} rows")

# Identify matched rows (yang ada CGS data)
has_cgs = df['nama_perusahaan_cgs'].notna()
print(f"Rows dengan CGS match: {has_cgs.sum():,}")

# Separate by match score
df['skor_kecocokan_cgs'] = pd.to_numeric(df['skor_kecocokan_cgs'], errors='coerce')

high_confidence = (df['skor_kecocokan_cgs'] >= 80)
medium_confidence = (df['skor_kecocokan_cgs'] >= 70) & (df['skor_kecocokan_cgs'] < 80)
low_confidence = (df['skor_kecocokan_cgs'] >= 60) & (df['skor_kecocokan_cgs'] < 70)
no_match = df['skor_kecocokan_cgs'].isna()

print(f"\n📊 DISTRIBUSI MATCH SCORE:")
print(f"  ✅ High confidence (80-100): {high_confidence.sum():,} rows")
print(f"  ⚠️  Medium confidence (70-79): {medium_confidence.sum():,} rows")
print(f"  ❌ Low confidence (60-69): {low_confidence.sum():,} rows")
print(f"  ⭕ No match: {no_match.sum():,} rows")

# ====================================================================================
# STEP 1: Keep high confidence matches (skor >= 80)
# ====================================================================================
df_keep = df[high_confidence | no_match].copy()
print(f"\n✅ KEEP (high confidence + no match): {len(df_keep):,} rows")

# ====================================================================================
# STEP 2: Unmerge medium + low confidence matches (skor 60-79)
# ====================================================================================
df_to_split = df[medium_confidence | low_confidence].copy()
print(f"🔧 TO SPLIT (medium + low confidence): {len(df_to_split):,} rows")

# Create 2 separate rows for each false match
unmerged_rows = []

for idx, row in df_to_split.iterrows():
    # Row A: MinerbaOne permit only (remove CGS data)
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
    
    # Row B: CGS smelter as separate record (create new IDs)
    row_cgs = row.copy()
    # Clear MinerbaOne specific fields
    row_cgs['id_perusahaan'] = np.nan  # No company ID from MinerbaOne
    row_cgs['id_izin'] = np.nan
    row_cgs['nomor_izin'] = np.nan
    row_cgs['nama_perusahaan_minerbaone'] = np.nan
    row_cgs['alamat'] = np.nan  # Will use CGS location
    row_cgs['email'] = np.nan
    row_cgs['telepon'] = np.nan
    row_cgs['lokasi_lengkap'] = row['provinsi']  # Use province from match
    row_cgs['jenis_izin'] = np.nan
    row_cgs['komoditas'] = 'Nikel'  # Keep commodity
    row_cgs['fase_operasi'] = 'OPERASI PRODUKSI'  # Assume operational
    row_cgs['status_cnc'] = np.nan
    row_cgs['tahun_terbit'] = np.nan
    row_cgs['tanggal_mulai_izin'] = np.nan
    row_cgs['tanggal_berakhir_izin'] = np.nan
    row_cgs['luas_hektar'] = np.nan  # CGS doesn't have area data
    row_cgs['sumber_data'] = 'cgs_only'
    row_cgs['kepercayaan_kapasitas'] = row['kepercayaan_kapasitas']  # Keep original
    # Keep: nama_perusahaan_cgs, kapasitas_*, latitude, longitude, tipe_produk_output
    unmerged_rows.append(row_cgs)

df_unmerged = pd.DataFrame(unmerged_rows)
print(f"✅ Created {len(df_unmerged):,} unmerged rows ({len(df_to_split)} x 2)")

# ====================================================================================
# STEP 3: Combine all rows
# ====================================================================================
df_final = pd.concat([df_keep, df_unmerged], ignore_index=True)
print(f"\n📊 FINAL DATASET: {len(df_final):,} rows")
print(f"  = {len(df_keep):,} (kept) + {len(df_unmerged):,} (unmerged)")

# Sort by company name
df_final = df_final.sort_values('nama_perusahaan_minerbaone', na_position='last').reset_index(drop=True)

# ====================================================================================
# STEP 4: Statistics
# ====================================================================================
print(f"\n" + "="*100)
print("STATISTIK FINAL")
print("="*100)

print(f"\n📋 TOTAL RECORDS:")
print(f"  Total rows: {len(df_final):,}")
print(f"  MinerbaOne permits: {df_final['nama_perusahaan_minerbaone'].notna().sum():,}")
print(f"  CGS smelters (matched): {(df_final['nama_perusahaan_cgs'].notna() & df_final['nama_perusahaan_minerbaone'].notna()).sum():,}")
print(f"  CGS smelters (standalone): {(df_final['nama_perusahaan_cgs'].notna() & df_final['nama_perusahaan_minerbaone'].isna()).sum():,}")

print(f"\n✅ MATCH QUALITY:")
has_match = df_final['nama_perusahaan_cgs'].notna() & df_final['nama_perusahaan_minerbaone'].notna()
matched_scores = df_final[has_match]['skor_kecocokan_cgs']
if len(matched_scores) > 0:
    print(f"  Matched records: {len(matched_scores):,}")
    print(f"  Average score: {matched_scores.mean():.1f}")
    print(f"  Min score: {matched_scores.min():.1f}")
    print(f"  Max score: {matched_scores.max():.1f}")
    print(f"  Score ≥90: {(matched_scores >= 90).sum():,}")
    print(f"  Score 80-89: {((matched_scores >= 80) & (matched_scores < 90)).sum():,}")

print(f"\n💰 DATA COMPLETENESS:")
print(f"  Luas lahan: {df_final['luas_hektar'].notna().sum():,}/{len(df_final)} ({df_final['luas_hektar'].notna().sum()/len(df_final)*100:.1f}%)")
print(f"  Kapasitas input: {df_final['kapasitas_input_ton_tahun'].notna().sum():,}/{len(df_final)} ({df_final['kapasitas_input_ton_tahun'].notna().sum()/len(df_final)*100:.1f}%)")
print(f"  Kapasitas output: {df_final['kapasitas_output_ton_tahun'].notna().sum():,}/{len(df_final)} ({df_final['kapasitas_output_ton_tahun'].notna().sum()/len(df_final)*100:.1f}%)")
print(f"  Investasi: {df_final['investasi_miliar_rp'].notna().sum():,}/{len(df_final)} ({df_final['investasi_miliar_rp'].notna().sum()/len(df_final)*100:.1f}%)")

# ====================================================================================
# STEP 5: Save
# ====================================================================================
output_file = '../../data/processed/esdm_master_sulawesi_nikel_2016_2026_id_fixed.csv'
df_final.to_csv(output_file, index=False)
print(f"\n💾 SAVED: {output_file}")

# Save detailed report of what was split
split_report_rows = []
for idx, row in df_to_split.iterrows():
    split_report_rows.append({
        'minerbaone_name': row['nama_perusahaan_minerbaone'],
        'cgs_name': row['nama_perusahaan_cgs'],
        'match_score': row['skor_kecocokan_cgs'],
        'province': row['provinsi'],
        'status': 'SPLIT - False match detected'
    })

df_split_report = pd.DataFrame(split_report_rows)
report_file = '../../data/processed/esdm_split_report.csv'
df_split_report.to_csv(report_file, index=False)
print(f"📋 SPLIT REPORT: {report_file}")

print(f"\n" + "="*100)
print("✅ SELESAI!")
print("="*100)
print(f"""
RINGKASAN:
- Original: {len(df):,} rows (dengan false matches)
- Fixed: {len(df_final):,} rows (false matches dipisah)
- Match berkualitas (score ≥80): {high_confidence.sum():,}
- Yang dipisah (score 60-79): {len(df_to_split):,} → jadi {len(df_unmerged):,} rows

FILE OUTPUT:
1. {output_file}
   → Dataset final dengan match yang sudah diperbaiki
   
2. {report_file}
   → Laporan match mana saja yang dipisah

NEXT STEP:
Review split_report.csv untuk lihat match mana saja yang dipisah
""")
