"""
Update matching file dengan approved matches
Merge yang alamatnya sama / high confidence:
1. Virtue Dragon → Cahaya Sultra Indonesia (alamat: KAWASAN INDUSTRI VIRTU DRAGON)
2. Bahodopi → Dampala Sejahtera Bersama (alamat: Kecamatan Bahodopi)
3. Bahodopi → Labota Bahodopi Sorajai (nama perusahaan: BAHODOPI)
"""
import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, '..', '..')

print("="*100)
print("UPDATE MATCHING FILE DENGAN APPROVED MATCHES")
print("="*100)

# Load existing matching
df_matching = pd.read_csv(os.path.join(project_root, 'data/processed/cgs_minerbaone_manual_matching.csv'))

print(f"\n📊 Current Status:")
print(f"   Total: {len(df_matching)}")
print(f"   Found: {len(df_matching[df_matching['found_in_minerbaone'] == 'YES'])}")
print(f"   Not Found: {len(df_matching[df_matching['found_in_minerbaone'] == 'NO - TIDAK PUNYA IZIN'])}")

# Approved matches (alamat sama / high confidence)
approved_matches = {
    'Virtue Dragon Nickel Industry (VDNI)': {
        'minerbaone_name': 'CAHAYA SULTRA INDONESIA',
        'match_type': 'ADDRESS_MATCH',
        'note': 'Address: KAWASAN INDUSTRI VIRTU DRAGON'
    },
    'Bahodopi Nickel Smelting Indonesia': {
        'minerbaone_name': 'DAMPALA SEJAHTERA BERSAMA',
        'match_type': 'ADDRESS_MATCH',
        'note': 'Address: Kecamatan Bahodopi, Morowali'
    },
    # Note: Bahodopi bisa match ke 2 companies, tapi kita pilih Dampala karena lebih eksplisit di alamat
}

# Update matching
for cgs_name, match_info in approved_matches.items():
    idx = df_matching[df_matching['cgs_smelter_name'] == cgs_name].index
    if len(idx) > 0:
        df_matching.loc[idx, 'found_in_minerbaone'] = 'YES'
        df_matching.loc[idx, 'minerbaone_name'] = match_info['minerbaone_name']
        df_matching.loc[idx, 'match_type'] = match_info['match_type']
        df_matching.loc[idx, 'status'] = 'LEGAL (ADA IZIN)'
        print(f"\n✅ UPDATED: {cgs_name}")
        print(f"   → {match_info['minerbaone_name']}")
        print(f"   Note: {match_info['note']}")

# Save updated matching
output_file = os.path.join(project_root, 'data/processed/cgs_minerbaone_manual_matching.csv')
df_matching.to_csv(output_file, index=False)

print(f"\n" + "="*100)
print("UPDATED STATISTICS")
print("="*100)

found = df_matching[df_matching['found_in_minerbaone'] == 'YES']
not_found = df_matching[df_matching['found_in_minerbaone'] == 'NO - TIDAK PUNYA IZIN']

print(f"\n📊 NEW Status:")
print(f"   Total: {len(df_matching)}")
print(f"   ✅ Found (ADA IZIN): {len(found)} ({len(found)/len(df_matching)*100:.1f}%)")
print(f"   ❌ Not Found (ILEGAL): {len(not_found)} ({len(not_found)/len(df_matching)*100:.1f}%)")

print(f"\n📍 By Province:")
for province in df_matching['province'].unique():
    prov_data = df_matching[df_matching['province'] == province]
    prov_matched = prov_data[prov_data['found_in_minerbaone'] == 'YES']
    print(f"   {province:25s}: {len(prov_matched)}/{len(prov_data)} ada izin")

print(f"\n💾 Updated file saved to: {output_file}")

print(f"\n" + "="*100)
print("ALL COMPANIES WITH IZIN")
print("="*100)
for idx, row in found.iterrows():
    print(f"✅ {row['cgs_smelter_name']:60s} → {row['minerbaone_name']:40s} [{row['match_type']}]")
