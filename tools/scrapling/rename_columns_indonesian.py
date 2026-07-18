"""
Rename columns to Bahasa Indonesia
"""
import pandas as pd
from datetime import datetime

print("="*100)
print("RENAME COLUMNS TO BAHASA INDONESIA")
print("="*100)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Load master dataset
df = pd.read_csv('../../data/processed/esdm_master_sulawesi_nickel_2016_2026.csv')
print(f"✅ Loaded: {len(df):,} records")

# Define column mapping (English -> Bahasa Indonesia)
column_mapping = {
    # Identifiers
    'company_id': 'id_perusahaan',
    'permit_id': 'id_izin',
    'permit_number': 'nomor_izin',
    
    # Company info
    'company_name_minerbaone': 'nama_perusahaan_minerbaone',
    'company_name_cgs': 'nama_perusahaan_cgs',
    'address': 'alamat',
    'email': 'email',
    'phone': 'telepon',
    
    # Location
    'province': 'provinsi',
    'location_full': 'lokasi_lengkap',
    'latitude': 'lintang',
    'longitude': 'bujur',
    
    # Permit details
    'permit_type': 'jenis_izin',
    'commodity': 'komoditas',
    'operational_phase': 'tahap_operasi',
    'status_cnc': 'status_cnc',
    'year_issued': 'tahun_terbit',
    'permit_start_date': 'tanggal_mulai_izin',
    'permit_end_date': 'tanggal_berakhir_izin',
    
    # Area
    'area_hectares': 'luas_hektar',
    
    # Capacity (from CGS)
    'capacity_input_tonnes_year': 'kapasitas_input_ton_tahun',
    'capacity_output_tonnes_year': 'kapasitas_output_ton_tahun',
    'ni_equivalent_tonnes_year': 'ekuivalen_nikel_ton_tahun',
    'output_product_type': 'jenis_produk_output',
    
    # Investment (from BPS PMDN)
    'investment_miliar_rp': 'investasi_miliar_rp',
    
    # Data quality metadata
    'data_source': 'sumber_data',
    'cgs_match_score': 'skor_pencocokan_cgs',
    'capacity_confidence': 'kepercayaan_kapasitas',
    'investment_confidence': 'kepercayaan_investasi',
    'investment_source': 'sumber_investasi',
    'investment_methodology': 'metodologi_investasi',
    'data_scraped_at': 'waktu_scraping'
}

# Rename columns
df_renamed = df.rename(columns=column_mapping)

print(f"\n✅ Columns renamed: {len(column_mapping)} columns")
print(f"\nColumn mapping:")
for old, new in list(column_mapping.items())[:10]:
    print(f"  {old:35s} → {new}")
print(f"  ... (showing first 10)")

# Save renamed dataset
output_file = '../../data/processed/esdm_master_sulawesi_nikel_2016_2026_id.csv'
df_renamed.to_csv(output_file, index=False)

print(f"\n💾 Saved renamed dataset:")
print(f"   File: {output_file}")
print(f"   Records: {len(df_renamed):,}")
print(f"   Columns: {len(df_renamed.columns)}")

# Show sample
print(f"\n📋 Sample data (first 3 rows, key columns):")
sample_cols = [
    'nama_perusahaan_minerbaone',
    'provinsi',
    'luas_hektar',
    'kapasitas_input_ton_tahun',
    'kapasitas_output_ton_tahun',
    'investasi_miliar_rp'
]
print(df_renamed[sample_cols].head(3).to_string(index=False))

# Print column list for reference
print(f"\n📝 All columns in Bahasa Indonesia:")
for i, col in enumerate(df_renamed.columns, 1):
    print(f"  {i:2d}. {col}")

print(f"\n✅ DONE!")
print("="*100)
