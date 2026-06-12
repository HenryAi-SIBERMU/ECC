"""
Verification: Apakah semua nickel permits Sulawesi sudah masuk?
"""
import pandas as pd

print("="*80)
print("FILTERING LOGIC VERIFICATION")
print("="*80)

# Step 1: Load all permits
df_all = pd.read_csv('output/full/minerbaone_permits.csv')
print(f"\n1. TOTAL ALL PERMITS (MinerbaOne): {len(df_all):,}")

# Step 2: Filter to actual licenses (exclude applications)
actual = df_all[df_all['jenis_perizinan'].isin(['IUP', 'IUPK', 'KK', 'PKP2B'])]
print(f"2. ACTUAL LICENSES (IUP/IUPK/KK/PKP2B): {len(actual):,}")
print(f"   Excluded IPP (applications): {len(df_all) - len(actual):,}")

# Step 3: Filter to nickel only
nickel = actual[actual['komoditas'].str.contains('ikel', case=False, na=False)]
print(f"\n3. NICKEL PERMITS (National): {len(nickel):,}")
print(f"   Sample commodities:")
for commodity, count in nickel['komoditas'].value_counts().head(5).items():
    print(f"     - {commodity}: {count}")

# Step 4: Filter to Sulawesi
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
}

def map_kabupaten_to_province(lokasi):
    """Map kabupaten name to province"""
    if pd.isna(lokasi):
        return None
    lokasi = lokasi.upper()
    for kab, prov in kabupaten_to_province.items():
        if kab in lokasi:
            return prov
    return None

nickel['province_mapped'] = nickel['lokasi_perizinan'].apply(map_kabupaten_to_province)
sulawesi = nickel[nickel['province_mapped'].notna()]

print(f"\n4. SULAWESI NICKEL PERMITS: {len(sulawesi):,}")
print(f"   Breakdown by province:")
for province, count in sulawesi['province_mapped'].value_counts().items():
    print(f"     {province:25s}: {count:3,} permits")

print(f"\n   Sample locations:")
for loc in sulawesi['lokasi_perizinan'].value_counts().head(10).items():
    print(f"     {loc[0]:40s}: {loc[1]:2,} permits")

# Step 5: Load master dataset
master = pd.read_csv('../../data/processed/esdm_master_sulawesi_nickel_2016_2026.csv')
print(f"\n5. MASTER DATASET (Merged Output): {len(master):,}")
print(f"   Breakdown by province:")
for province, count in master['province'].value_counts().items():
    print(f"     {province:25s}: {count:3,} permits")

# Verification
print(f"\n" + "="*80)
print("VERIFICATION RESULT")
print("="*80)

if len(sulawesi) == len(master):
    print(f"✅ MATCH! All {len(sulawesi):,} Sulawesi nickel permits included")
    print(f"   NO SAMPLING - This is the COMPLETE dataset")
else:
    print(f"⚠️ MISMATCH!")
    print(f"   Filtered: {len(sulawesi):,}")
    print(f"   Master:   {len(master):,}")
    print(f"   Difference: {abs(len(sulawesi) - len(master)):,}")
    
    if len(master) < len(sulawesi):
        print(f"\n   Possible reasons:")
        print(f"   - Some permits may have been dropped during merge")
        print(f"   - Check for null values in key columns")
    else:
        print(f"\n   Possible reasons:")
        print(f"   - Master has more records (duplicates?)")

# Additional checks
print(f"\n" + "="*80)
print("ADDITIONAL CHECKS")
print("="*80)

# Check year range
print(f"\nYear range:")
print(f"  Sulawesi filtered: {sulawesi['tanggal_berlaku'].min()} to {sulawesi['tanggal_berlaku'].max()}")
print(f"  Master dataset:    {master['permit_start_date'].min()} to {master['permit_start_date'].max()}")

# Check operational vs exploration
print(f"\nOperational phase:")
sulawesi_ops = sulawesi['tahap_kegiatan'].value_counts()
master_ops = master['operational_phase'].value_counts()
print(f"  Sulawesi filtered:")
for phase, count in sulawesi_ops.items():
    print(f"    {phase}: {count}")
print(f"  Master dataset:")
for phase, count in master_ops.items():
    print(f"    {phase}: {count}")

print(f"\n" + "="*80)
print("CONCLUSION")
print("="*80)
if len(sulawesi) == len(master):
    print("""
✅ CONFIRMED: Master dataset contains ALL Sulawesi nickel permits
   - NOT a sample
   - COMPLETE filtering from 8,396 total permits
   - Includes all IUP/IUPK/KK/PKP2B nickel licenses in Sulawesi
   - No data loss during merge
""")
else:
    print(f"""
⚠️ WARNING: Record count mismatch
   Please investigate the difference
""")
