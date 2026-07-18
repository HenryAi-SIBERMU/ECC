"""
ESDM Data Merger
Merges MinerbaOne + CGS + BPS PMDN data into master dataset
While preserving all original files
"""
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from datetime import datetime
import os

print("="*100)
print("ESDM DATA MERGER - MinerbaOne + CGS + BPS PMDN")
print("="*100)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# ============================================================================
# STEP 1: Load All Source Data
# ============================================================================
print("STEP 1: Loading source datasets...")
print("-"*100)

# 1.1 MinerbaOne Permits (IUP/IUPK only - actual licenses)
print("\n📋 Loading MinerbaOne permits...")
df_permits = pd.read_csv('output/full/minerbaone_permits.csv')
print(f"   Total permits: {len(df_permits):,}")

# Filter to actual licenses (IUP/IUPK) excluding applications (IPP)
df_permits_actual = df_permits[df_permits['jenis_perizinan'].isin(['IUP', 'IUPK', 'KK', 'PKP2B'])].copy()
print(f"   Actual licenses (IUP/IUPK/KK/PKP2B): {len(df_permits_actual):,}")

# Filter to nickel only
df_permits_nickel = df_permits_actual[
    df_permits_actual['komoditas'].str.contains('ikel', case=False, na=False)
].copy()
print(f"   Nickel permits: {len(df_permits_nickel):,}")

# 1.2 MinerbaOne Company Details
print("\n🏢 Loading MinerbaOne company details...")
df_details = pd.read_csv('output/full/minerbaone_details.csv')
print(f"   Total companies: {len(df_details):,}")

# 1.3 CGS Smelter Dataset
print("\n🏭 Loading CGS nickel smelter dataset...")
df_cgs = pd.read_csv('output/cgs_dataset_extracted.csv')
print(f"   Total smelters: {len(df_cgs):,}")

# Filter to Sulawesi only
df_cgs_sulawesi = df_cgs[df_cgs['Province'].str.contains('Sulawesi', case=False, na=False)].copy()
print(f"   Sulawesi smelters: {len(df_cgs_sulawesi):,}")

# 1.4 BPS PMDN Investment Data
print("\n💰 Loading BPS PMDN investment data...")
df_pmdn = pd.read_csv('../../data/raw/bps_pad/bps_investasi_pmdn_sulawesi_2016_2026.csv')
print(f"   Total records: {len(df_pmdn):,}")

# Filter to nilai only (not jumlah proyek)
df_pmdn_nilai = df_pmdn[df_pmdn['indikator'] == 'Investasi PMDN - Nilai (Juta Rp)'].copy()
print(f"   Investment values (2016-2023): {len(df_pmdn_nilai):,}")

print(f"\n✅ All source data loaded successfully")

# ============================================================================
# STEP 2: Prepare MinerbaOne Data
# ============================================================================
print("\n" + "="*100)
print("STEP 2: Preparing MinerbaOne data...")
print("-"*100)

# Merge permits with company details
df_minerbaone = df_permits_nickel.merge(
    df_details[['id_badan_usaha', 'nama_badan_usaha', 'alamat', 'email', 'no_telp']],
    on='id_badan_usaha',
    how='left'
)
# Rename for clarity
df_minerbaone.rename(columns={
    'nama_badan_usaha': 'nama',
    'no_telp': 'telp'
}, inplace=True)
print(f"\n✅ Merged permits with company details: {len(df_minerbaone):,} rows")

# Map kabupaten to province (Sulawesi kabupatens only)
kabupaten_to_province = {
    # Central Sulawesi
    'MOROWALI': 'Central Sulawesi',
    'MOROWALI UTARA': 'Central Sulawesi',
    'BANGGAI': 'Central Sulawesi',
    'BANGGAI LAUT': 'Central Sulawesi',
    'BANGGAI KEPULAUAN': 'Central Sulawesi',
    'POSO': 'Central Sulawesi',
    'TOJO UNA-UNA': 'Central Sulawesi',
    'TOLI-TOLI': 'Central Sulawesi',
    'BUOL': 'Central Sulawesi',
    'PARIGI MOUTONG': 'Central Sulawesi',
    'DONGGALA': 'Central Sulawesi',
    'SIGI': 'Central Sulawesi',
    
    # South East Sulawesi
    'KONAWE': 'South East Sulawesi',
    'KONAWE UTARA': 'South East Sulawesi',
    'KONAWE SELATAN': 'South East Sulawesi',
    'KONAWE KEPULAUAN': 'South East Sulawesi',
    'KOLAKA': 'South East Sulawesi',
    'KOLAKA UTARA': 'South East Sulawesi',
    'KOLAKA TIMUR': 'South East Sulawesi',
    'BOMBANA': 'South East Sulawesi',
    'WAKATOBI': 'South East Sulawesi',
    'BUTON': 'South East Sulawesi',
    'BUTON UTARA': 'South East Sulawesi',
    'BUTON TENGAH': 'South East Sulawesi',
    'BUTON SELATAN': 'South East Sulawesi',
    'MUNA': 'South East Sulawesi',
    'MUNA BARAT': 'South East Sulawesi',
    
    # South Sulawesi
    'LUWU': 'South Sulawesi',
    'LUWU TIMUR': 'South Sulawesi',
    'LUWU UTARA': 'South Sulawesi',
    'BONE': 'South Sulawesi',
    'SOPPENG': 'South Sulawesi',
    'WAJO': 'South Sulawesi',
    'SIDENRENG RAPPANG': 'South Sulawesi',
    'PINRANG': 'South Sulawesi',
    'ENREKANG': 'South Sulawesi',
    'TANA TORAJA': 'South Sulawesi',
    'TORAJA UTARA': 'South Sulawesi',
    'GOWA': 'South Sulawesi',
    'TAKALAR': 'South Sulawesi',
    'JENEPONTO': 'South Sulawesi',
    'BANTAENG': 'South Sulawesi',
    'BULUKUMBA': 'South Sulawesi',
    'SINJAI': 'South Sulawesi',
    'MAROS': 'South Sulawesi',
    'PANGKAJENE DAN KEPULAUAN': 'South Sulawesi',
    'BARRU': 'South Sulawesi',
    'PARE-PARE': 'South Sulawesi',
    'PALOPO': 'South Sulawesi',
    
    # North Sulawesi
    'MINAHASA': 'North Sulawesi',
    'MINAHASA UTARA': 'North Sulawesi',
    'MINAHASA SELATAN': 'North Sulawesi',
    'MINAHASA TENGGARA': 'North Sulawesi',
    'BOLAANG MONGONDOW': 'North Sulawesi',
    'BOLAANG MONGONDOW UTARA': 'North Sulawesi',
    'BOLAANG MONGONDOW SELATAN': 'North Sulawesi',
    'BOLAANG MONGONDOW TIMUR': 'North Sulawesi',
    'KEPULAUAN SANGIHE': 'North Sulawesi',
    'KEPULAUAN TALAUD': 'North Sulawesi',
    'KEPULAUAN SIAU TAGULANDANG BIARO': 'North Sulawesi',
    
    # West Sulawesi
    'MAJENE': 'West Sulawesi',
    'POLEWALI MANDAR': 'West Sulawesi',
    'MAMASA': 'West Sulawesi',
    'MAMUJU': 'West Sulawesi',
    'MAMUJU UTARA': 'West Sulawesi',
    'MAMUJU TENGAH': 'West Sulawesi',
    'PASANGKAYU': 'West Sulawesi',
    
    # Gorontalo
    'GORONTALO': 'Gorontalo',
    'GORONTALO UTARA': 'Gorontalo',
    'BONE BOLANGO': 'Gorontalo',
    'POHUWATO': 'Gorontalo',
    'BOALEMO': 'Gorontalo',
}

# Parse location to extract province
df_minerbaone['lokasi_upper'] = df_minerbaone['lokasi_perizinan'].fillna('').str.upper()

def map_kabupaten_to_province(lokasi):
    """Map kabupaten name to province"""
    if pd.isna(lokasi):
        return None
    lokasi = lokasi.upper()
    # Try to find matching kabupaten
    for kab, prov in kabupaten_to_province.items():
        if kab in lokasi:
            return prov
    return None

df_minerbaone['province_parsed'] = df_minerbaone['lokasi_upper'].apply(map_kabupaten_to_province)

# Filter to Sulawesi only
df_minerbaone_sulawesi = df_minerbaone[df_minerbaone['province_parsed'].notna()].copy()
print(f"✅ Sulawesi nickel permits: {len(df_minerbaone_sulawesi):,}")

# Parse year from tanggal_berlaku
df_minerbaone_sulawesi['tanggal_berlaku'] = pd.to_datetime(
    df_minerbaone_sulawesi['tanggal_berlaku'], 
    errors='coerce'
)
df_minerbaone_sulawesi['year_issued'] = df_minerbaone_sulawesi['tanggal_berlaku'].dt.year

print(f"   Year range: {df_minerbaone_sulawesi['year_issued'].min():.0f} - {df_minerbaone_sulawesi['year_issued'].max():.0f}")

# ============================================================================
# STEP 3: Match MinerbaOne with CGS (Add Capacity Data)
# ============================================================================
print("\n" + "="*100)
print("STEP 3: Matching MinerbaOne permits with CGS smelters...")
print("-"*100)

def fuzzy_match_company(minerbaone_name, cgs_name):
    """Fuzzy match company names"""
    if pd.isna(minerbaone_name) or pd.isna(cgs_name):
        return 0
    return fuzz.token_sort_ratio(str(minerbaone_name).upper(), str(cgs_name).upper())

# Prepare matching
matched_records = []
unmatched_minerbaone = []

print("\n🔍 Matching process:")
print(f"   MinerbaOne nickel permits (Sulawesi): {len(df_minerbaone_sulawesi)}")
print(f"   CGS smelters (Sulawesi): {len(df_cgs_sulawesi)}")

for idx, permit in df_minerbaone_sulawesi.iterrows():
    company_name = permit['nama']
    province = permit['province_parsed']
    
    # Try to match with CGS
    best_match = None
    best_score = 0
    
    for cgs_idx, smelter in df_cgs_sulawesi.iterrows():
        if smelter['Province'] != province:
            continue  # Must be same province
        
        score = fuzzy_match_company(company_name, smelter['Smelter Name'])
        if score > best_score:
            best_score = score
            best_match = smelter
    
    # If good match (score > 60), add CGS data
    if best_match is not None and best_score >= 60:
        matched_record = permit.copy()
        matched_record['cgs_smelter_name'] = best_match.get('Smelter Name')
        matched_record['cgs_match_score'] = best_score
        # Note: Column names have trailing spaces!
        matched_record['capacity_input_tonnes'] = best_match.get('Input Capacity (Tonnes) ')
        matched_record['capacity_output_tonnes'] = best_match.get('Output Capacity (Tonnes)')
        matched_record['ni_metal_equivalent_tonnes'] = best_match.get('Ni metal equivalent (tonnes)')
        matched_record['output_product'] = best_match.get('Output Product ')
        matched_record['latitude'] = best_match.get('Latitude')
        matched_record['longitude'] = best_match.get('Longitude')
        matched_record['data_source'] = 'minerbaone+cgs'
        matched_record['capacity_confidence'] = 'high' if best_score >= 80 else 'medium'
        matched_records.append(matched_record)
    else:
        # No match, keep MinerbaOne data only
        unmatched = permit.copy()
        unmatched['cgs_smelter_name'] = None
        unmatched['cgs_match_score'] = None
        unmatched['capacity_input_tonnes'] = None
        unmatched['capacity_output_tonnes'] = None
        unmatched['ni_metal_equivalent_tonnes'] = None
        unmatched['output_product'] = None
        unmatched['latitude'] = None
        unmatched['longitude'] = None
        unmatched['data_source'] = 'minerbaone'
        unmatched['capacity_confidence'] = 'none'
        unmatched_minerbaone.append(unmatched)

df_matched = pd.DataFrame(matched_records)
df_unmatched = pd.DataFrame(unmatched_minerbaone)

print(f"\n✅ Matching complete:")
if len(df_minerbaone_sulawesi) > 0:
    print(f"   Matched with CGS: {len(df_matched):,} ({len(df_matched)/len(df_minerbaone_sulawesi)*100:.1f}%)")
    print(f"   Unmatched: {len(df_unmatched):,} ({len(df_unmatched)/len(df_minerbaone_sulawesi)*100:.1f}%)")
else:
    print(f"   ⚠️ No Sulawesi permits found! Check location parsing logic.")

# Show sample matches
if len(df_matched) > 0:
    print(f"\n📊 Sample matches (top 5):")
    for idx, row in df_matched.head(5).iterrows():
        print(f"   • {row['nama'][:50]:50s} ↔ {row['cgs_smelter_name']:30s} (score: {row['cgs_match_score']:.0f})")

# Combine matched and unmatched
df_merged = pd.concat([df_matched, df_unmatched], ignore_index=True)

# ============================================================================
# STEP 4: Add Investment Data from BPS PMDN
# ============================================================================
print("\n" + "="*100)
print("STEP 4: Allocating BPS PMDN investment to smelters...")
print("-"*100)

# Pivot PMDN data for easier access
df_pmdn_pivot = df_pmdn_nilai.pivot_table(
    index='provinsi',
    columns='tahun',
    values='nilai',
    aggfunc='sum'
).reset_index()

print(f"\n💰 PMDN by province (2016-2023):")
for idx, row in df_pmdn_pivot.iterrows():
    total = row[2016:2024].sum()
    print(f"   {row['provinsi']:25s}: {total:10,.1f} Miliar Rp")

# Map province names
province_mapping = {
    'Central Sulawesi': 'Sulawesi Tengah',
    'South East Sulawesi': 'Sulawesi Tenggara',
    'South Sulawesi': 'Sulawesi Selatan',
    'North Sulawesi': 'Sulawesi Utara',
    'West Sulawesi': 'Sulawesi Barat',
    'Gorontalo': 'Gorontalo'
}

# Calculate total capacity per province
capacity_by_province = df_merged.groupby('province_parsed').agg({
    'capacity_input_tonnes': 'sum'
}).reset_index()
capacity_by_province.columns = ['province', 'total_capacity']

print(f"\n🏭 Total capacity by province:")
for idx, row in capacity_by_province.iterrows():
    print(f"   {row['province']:25s}: {row['total_capacity']:12,.0f} tonnes/year")

# Allocate investment
def allocate_investment(row):
    """Allocate provincial PMDN to individual smelter"""
    province = row['province_parsed']
    year = row['year_issued']
    capacity = row['capacity_input_tonnes']
    
    if pd.isna(province) or pd.isna(year) or pd.isna(capacity):
        return None
    
    # Get provincial PMDN for that year
    pmdn_province = province_mapping.get(province)
    if pmdn_province is None:
        return None
    
    pmdn_row = df_pmdn_pivot[df_pmdn_pivot['provinsi'] == pmdn_province]
    if len(pmdn_row) == 0 or year not in pmdn_row.columns:
        return None
    
    provincial_pmdn = pmdn_row[year].values[0]  # Miliar Rp
    
    # Get total capacity for that province
    total_capacity_row = capacity_by_province[capacity_by_province['province'] == province]
    if len(total_capacity_row) == 0:
        return None
    
    total_capacity = total_capacity_row['total_capacity'].values[0]
    
    if total_capacity == 0:
        return None
    
    # Assume 40% of PMDN goes to mining sector
    mining_pmdn = provincial_pmdn * 0.4
    
    # Allocate proportionally by capacity
    smelter_investment = (capacity / total_capacity) * mining_pmdn
    
    return smelter_investment

df_merged['investment_pmdn_allocated_miliar_rp'] = df_merged.apply(allocate_investment, axis=1)

# Add confidence flag
df_merged['investment_confidence'] = df_merged['investment_pmdn_allocated_miliar_rp'].apply(
    lambda x: 'medium' if pd.notna(x) else 'none'
)
df_merged['investment_source'] = 'bps_pmdn_allocated'
df_merged['investment_note'] = 'Provincial PMDN allocated proportionally by capacity (40% mining assumption)'

print(f"\n✅ Investment allocation complete:")
allocated = df_merged['investment_pmdn_allocated_miliar_rp'].notna().sum()
print(f"   Permits with investment: {allocated:,} ({allocated/len(df_merged)*100:.1f}%)")
print(f"   Total allocated: {df_merged['investment_pmdn_allocated_miliar_rp'].sum():,.1f} Miliar Rp")

# ============================================================================
# STEP 5: Create Final Master Dataset
# ============================================================================
print("\n" + "="*100)
print("STEP 5: Creating final master dataset...")
print("-"*100)

# Select and rename columns for clarity
df_master = df_merged[[
    # Identifiers
    'id_badan_usaha',
    'id_perizinan',
    'nomor_izin',
    
    # Company info
    'nama',
    'cgs_smelter_name',
    'alamat',
    'email',
    'telp',
    
    # Location
    'province_parsed',
    'lokasi_perizinan',
    'latitude',
    'longitude',
    
    # Permit details
    'jenis_perizinan',
    'komoditas',
    'tahap_kegiatan',
    'status_cnc',
    'year_issued',
    'tanggal_berlaku',
    'tanggal_berakhir',
    
    # Area
    'luas_ha',
    
    # Capacity (from CGS)
    'capacity_input_tonnes',
    'capacity_output_tonnes',
    'ni_metal_equivalent_tonnes',
    'output_product',
    
    # Investment (from BPS PMDN)
    'investment_pmdn_allocated_miliar_rp',
    
    # Data quality metadata
    'data_source',
    'cgs_match_score',
    'capacity_confidence',
    'investment_confidence',
    'investment_source',
    'investment_note',
    
    # Timestamp
    'scraped_at'
]].copy()

# Rename columns for clarity
df_master.columns = [
    'company_id',
    'permit_id',
    'permit_number',
    'company_name_minerbaone',
    'company_name_cgs',
    'address',
    'email',
    'phone',
    'province',
    'location_full',
    'latitude',
    'longitude',
    'permit_type',
    'commodity',
    'operational_phase',
    'status_cnc',
    'year_issued',
    'permit_start_date',
    'permit_end_date',
    'area_hectares',
    'capacity_input_tonnes_year',
    'capacity_output_tonnes_year',
    'ni_equivalent_tonnes_year',
    'output_product_type',
    'investment_miliar_rp',
    'data_source',
    'cgs_match_score',
    'capacity_confidence',
    'investment_confidence',
    'investment_source',
    'investment_methodology',
    'data_scraped_at'
]

print(f"\n✅ Master dataset created:")
print(f"   Total records: {len(df_master):,}")
print(f"   Columns: {len(df_master.columns)}")

# ============================================================================
# STEP 6: Generate Statistics & Save
# ============================================================================
print("\n" + "="*100)
print("STEP 6: Generating statistics and saving...")
print("-"*100)

# Statistics
print(f"\n📊 DATASET STATISTICS:")
print(f"\n🏢 Companies & Permits:")
print(f"   Total permits: {len(df_master):,}")
print(f"   Unique companies: {df_master['company_name_minerbaone'].nunique():,}")
print(f"   Operational: {(df_master['operational_phase'] == 'OPERASI PRODUKSI').sum():,}")
print(f"   Exploration: {(df_master['operational_phase'] == 'EKSPLORASI').sum():,}")

print(f"\n📍 Geographic Distribution:")
for province in df_master['province'].value_counts().head(10).items():
    print(f"   {province[0]:25s}: {province[1]:4,} permits")

print(f"\n📏 Area Coverage:")
total_area = df_master['area_hectares'].sum()
avg_area = df_master['area_hectares'].mean()
print(f"   Total area: {total_area:,.0f} hectares")
print(f"   Average area: {avg_area:,.0f} hectares")
print(f"   Permits with area data: {df_master['area_hectares'].notna().sum():,} ({df_master['area_hectares'].notna().sum()/len(df_master)*100:.1f}%)")

print(f"\n🏭 Capacity Data (from CGS):")
has_capacity = df_master['capacity_input_tonnes_year'].notna().sum()
print(f"   Permits with capacity: {has_capacity:,} ({has_capacity/len(df_master)*100:.1f}%)")
print(f"   Total input capacity: {df_master['capacity_input_tonnes_year'].sum():,.0f} tonnes/year")
print(f"   Total output capacity: {df_master['capacity_output_tonnes_year'].sum():,.0f} tonnes/year")
print(f"   Total Ni equivalent: {df_master['ni_equivalent_tonnes_year'].sum():,.0f} tonnes Ni/year")

print(f"\n💰 Investment Data (from BPS PMDN):")
has_investment = df_master['investment_miliar_rp'].notna().sum()
print(f"   Permits with investment: {has_investment:,} ({has_investment/len(df_master)*100:.1f}%)")
print(f"   Total allocated investment: {df_master['investment_miliar_rp'].sum():,.1f} Miliar Rp")
print(f"   Average per permit: {df_master['investment_miliar_rp'].mean():,.1f} Miliar Rp")

print(f"\n✅ Data Quality:")
print(f"   High confidence capacity: {(df_master['capacity_confidence'] == 'high').sum():,}")
print(f"   Medium confidence capacity: {(df_master['capacity_confidence'] == 'medium').sum():,}")
print(f"   Medium confidence investment: {(df_master['investment_confidence'] == 'medium').sum():,}")

# Save master dataset
output_file = '../../data/processed/esdm_master_sulawesi_nickel_2016_2026.csv'
os.makedirs(os.path.dirname(output_file), exist_ok=True)
df_master.to_csv(output_file, index=False)
print(f"\n💾 Master dataset saved:")
print(f"   File: {output_file}")
print(f"   Size: {os.path.getsize(output_file) / 1024:.1f} KB")

# Save metadata/documentation
metadata = {
    'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'total_records': len(df_master),
    'sources': {
        'minerbaone': {
            'file': 'tools/scrapling/output/full/minerbaone_permits.csv',
            'records_used': len(df_minerbaone_sulawesi),
            'description': 'Mining permits from MinerbaOne portal (nickel only, Sulawesi)'
        },
        'cgs': {
            'file': 'data/raw/ESDM/CGS_Nickel_Smelter_Dataset_V1.xlsx',
            'records_used': len(df_cgs_sulawesi),
            'description': 'Nickel smelter capacity data from CGS/UMD dataset'
        },
        'bps_pmdn': {
            'file': 'data/raw/bps_pad/bps_investasi_pmdn_sulawesi_2016_2026.csv',
            'records_used': len(df_pmdn_nilai),
            'description': 'Provincial PMDN investment data from BPS (2016-2023)'
        }
    },
    'methodology': {
        'matching': 'Fuzzy string matching (threshold: 60%) by company name + province',
        'capacity': 'Direct merge from CGS dataset where matched',
        'investment': 'Provincial PMDN allocated proportionally by capacity (40% mining assumption)'
    },
    'confidence_levels': {
        'capacity_high': 'CGS match score >= 80',
        'capacity_medium': 'CGS match score 60-79',
        'capacity_none': 'No CGS match found',
        'investment_medium': 'Allocated from provincial PMDN',
        'investment_none': 'No capacity data or year mismatch'
    }
}

metadata_file = '../../data/processed/esdm_master_sulawesi_nickel_2016_2026_metadata.txt'
with open(metadata_file, 'w') as f:
    f.write("ESDM MASTER DATASET - METADATA\n")
    f.write("="*100 + "\n\n")
    f.write(f"Created: {metadata['created']}\n")
    f.write(f"Total Records: {metadata['total_records']:,}\n\n")
    
    f.write("DATA SOURCES:\n")
    f.write("-"*100 + "\n")
    for source, info in metadata['sources'].items():
        f.write(f"\n{source.upper()}:\n")
        f.write(f"  File: {info['file']}\n")
        f.write(f"  Records Used: {info['records_used']:,}\n")
        f.write(f"  Description: {info['description']}\n")
    
    f.write("\n\nMETHODOLOGY:\n")
    f.write("-"*100 + "\n")
    for key, value in metadata['methodology'].items():
        f.write(f"  {key.capitalize()}: {value}\n")
    
    f.write("\n\nCONFIDENCE LEVELS:\n")
    f.write("-"*100 + "\n")
    for key, value in metadata['confidence_levels'].items():
        f.write(f"  {key}: {value}\n")
    
    f.write("\n\nORIGINAL FILES PRESERVED:\n")
    f.write("-"*100 + "\n")
    f.write("  • tools/scrapling/output/full/minerbaone_permits.csv\n")
    f.write("  • tools/scrapling/output/full/minerbaone_details.csv\n")
    f.write("  • data/raw/ESDM/CGS_Nickel_Smelter_Dataset_V1.xlsx\n")
    f.write("  • data/raw/bps_pad/bps_investasi_pmdn_sulawesi_2016_2026.csv\n")

print(f"\n💾 Metadata saved:")
print(f"   File: {metadata_file}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*100)
print("MERGE COMPLETE!")
print("="*100)
print(f"""
✅ SUCCESS! Master dataset created with {len(df_master):,} nickel permits in Sulawesi

📁 OUTPUT FILES:
   • Master Dataset: data/processed/esdm_master_sulawesi_nickel_2016_2026.csv
   • Metadata: data/processed/esdm_master_sulawesi_nickel_2016_2026_metadata.txt

🔒 ORIGINAL FILES PRESERVED:
   • MinerbaOne: tools/scrapling/output/full/*.csv (UNCHANGED)
   • CGS: data/raw/ESDM/CGS_Nickel_Smelter_Dataset_V1.xlsx (UNCHANGED)
   • BPS PMDN: data/raw/bps_pad/bps_investasi_pmdn_sulawesi_2016_2026.csv (UNCHANGED)

📊 DATA COMPLETENESS:
   • Area (luas_ha): {df_master['area_hectares'].notna().sum()/len(df_master)*100:.1f}%
   • Capacity: {has_capacity/len(df_master)*100:.1f}%
   • Investment: {has_investment/len(df_master)*100:.1f}%

🎯 READY FOR ANALYSIS!
   Use: data/processed/esdm_master_sulawesi_nickel_2016_2026.csv
""")

print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*100)
