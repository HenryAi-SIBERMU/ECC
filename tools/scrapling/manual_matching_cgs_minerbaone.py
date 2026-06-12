"""
Manual Matching CGS dengan MinerbaOne
Berdasarkan pengetahuan + logika nama perusahaan
Yang ga ada di MinerbaOne = TIDAK PUNYA IZIN (ILEGAL)
"""
import pandas as pd
import numpy as np
import os

print("="*100)
print("MANUAL MATCHING CGS SMELTERS DENGAN MINERBAONE")
print("="*100)

# Load data
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, '..', '..')

df_cgs = pd.read_excel(os.path.join(project_root, 'data/raw/ESDM/CGS_Nickel_Smelter_Dataset_V1.xlsx'))
df_minerbaone = pd.read_csv(os.path.join(script_dir, 'output/full/minerbaone_details.csv'))

# Filter Sulawesi
df_cgs_sulawesi = df_cgs[df_cgs['Province'].str.contains('Sulawesi', case=False, na=False)].copy()

print(f"\nTotal CGS Smelters di Sulawesi: {len(df_cgs_sulawesi)}")
print(f"Total Companies di MinerbaOne: {len(df_minerbaone):,}")

# Prepare MinerbaOne names (uppercase for matching)
minerbaone_names = df_minerbaone['nama_badan_usaha'].str.upper().tolist()

# Manual matching rules berdasarkan pengetahuan
def manual_match(cgs_name):
    """
    Manual matching berdasarkan pengetahuan nama perusahaan Indonesia
    Return: (found, minerbaone_name, match_type)
    """
    cgs_upper = cgs_name.upper()
    
    # Direct exact match (with PT prefix variations)
    variations = [
        cgs_upper,
        f"PT {cgs_upper}",
        cgs_upper.replace("PT ", ""),
        cgs_upper.replace("PT. ", ""),
    ]
    
    for var in variations:
        if var in minerbaone_names:
            idx = minerbaone_names.index(var)
            return (True, df_minerbaone.iloc[idx]['nama_badan_usaha'], 'EXACT')
    
    # Check if any MinerbaOne name contains the CGS name (for subsidiaries/longer names)
    for mb_name in minerbaone_names:
        # Remove common prefixes for comparison
        cgs_clean = cgs_upper.replace("PT ", "").replace("PT. ", "").strip()
        mb_clean = mb_name.replace("PT ", "").replace("PT. ", "").strip()
        
        # Exact match after cleaning
        if cgs_clean == mb_clean and len(cgs_clean) > 5:  # Min 5 chars to avoid false positives
            idx = minerbaone_names.index(mb_name)
            return (True, df_minerbaone.iloc[idx]['nama_badan_usaha'], 'EXACT_CLEAN')
    
    # Known aliases/variations (based on domain knowledge)
    # Format: CGS_name_pattern -> MinerbaOne_name_pattern
    known_mappings = {
        'ANTAM': 'ANEKA TAMBANG',
        'VALE INDONESIA': 'VALE',
        'CORII': 'CERIA',  # CORII is CERIA
        'TSINGSHAN': 'TSINGSHAN',
        'HUAYOU': 'HUAYUE',  # Huayou = Huayue
    }
    
    for cgs_pattern, mb_pattern in known_mappings.items():
        if cgs_pattern in cgs_upper:
            # Find matching MinerbaOne name
            for mb_name in minerbaone_names:
                if mb_pattern in mb_name:
                    idx = minerbaone_names.index(mb_name)
                    return (True, df_minerbaone.iloc[idx]['nama_badan_usaha'], 'KNOWN_ALIAS')
    
    return (False, None, 'NOT_FOUND')

# Perform matching
print("\n" + "="*100)
print("MATCHING RESULTS")
print("="*100)

results = []
matched_count = 0
not_found_count = 0

for idx, row in df_cgs_sulawesi.iterrows():
    cgs_name = row['Smelter Name']
    province = row['Province']
    
    found, mb_name, match_type = manual_match(cgs_name)
    
    results.append({
        'cgs_smelter_name': cgs_name,
        'province': province,
        'found_in_minerbaone': 'YES' if found else 'NO - TIDAK PUNYA IZIN',
        'minerbaone_name': mb_name if found else '-',
        'match_type': match_type,
        'status': 'LEGAL (ADA IZIN)' if found else '⚠️ ILEGAL / TIDAK ADA IZIN'
    })
    
    if found:
        matched_count += 1
        print(f"✅ {cgs_name:60s} → {mb_name} ({match_type})")
    else:
        not_found_count += 1
        print(f"❌ {cgs_name:60s} → TIDAK ADA IZIN DI MINERBAONE")

df_results = pd.DataFrame(results)

# Save results
output_file = os.path.join(project_root, 'data/processed/cgs_minerbaone_manual_matching.csv')
df_results.to_csv(output_file, index=False)

# Statistics
print("\n" + "="*100)
print("STATISTIK MATCHING")
print("="*100)

print(f"\n📊 OVERALL:")
print(f"   Total CGS Smelters: {len(df_cgs_sulawesi)}")
print(f"   Found in MinerbaOne (ADA IZIN): {matched_count} ({matched_count/len(df_cgs_sulawesi)*100:.1f}%)")
print(f"   NOT Found (TIDAK ADA IZIN): {not_found_count} ({not_found_count/len(df_cgs_sulawesi)*100:.1f}%)")

print(f"\n📍 By Province:")
for province in df_results['province'].unique():
    prov_data = df_results[df_results['province'] == province]
    prov_matched = prov_data[prov_data['found_in_minerbaone'] == 'YES']
    print(f"   {province:25s}: {len(prov_matched)}/{len(prov_data)} ada izin")

print(f"\n⚠️  SMELTERS TANPA IZIN (ILEGAL):")
illegal = df_results[df_results['found_in_minerbaone'] != 'YES']
for idx, row in illegal.iterrows():
    print(f"   - {row['cgs_smelter_name']} ({row['province']})")

print(f"\n💾 Results saved to: {output_file}")

print("\n" + "="*100)
print("KESIMPULAN")
print("="*100)
print(f"""
Dari {len(df_cgs_sulawesi)} CGS smelters di Sulawesi:
- {matched_count} smelters ADA IZIN di MinerbaOne ({matched_count/len(df_cgs_sulawesi)*100:.1f}%)
- {not_found_count} smelters TIDAK ADA IZIN / ILEGAL ({not_found_count/len(df_cgs_sulawesi)*100:.1f}%)

CATATAN:
- MinerbaOne sudah di-scrape FULL (8,396 permits nasional)
- Yang tidak ada di MinerbaOne = TIDAK PUNYA IZIN
- Matching menggunakan exact match + known aliases
""")
