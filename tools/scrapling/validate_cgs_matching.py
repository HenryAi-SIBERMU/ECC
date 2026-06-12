"""
Validasi Manual Matching CGS dengan MinerbaOne
Mencari kemungkinan ada smelter yang miss karena nama berbeda
"""
import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, '..', '..')

# Load data
df_matching = pd.read_csv(os.path.join(project_root, 'data/processed/cgs_minerbaone_manual_matching.csv'))
df_minerbaone = pd.read_csv(os.path.join(script_dir, 'output/full/minerbaone_details.csv'))

print("="*100)
print("VALIDASI MANUAL MATCHING - MENCARI KEMUNGKINAN MISSED MATCHES")
print("="*100)

# Get list of "illegal" smelters
illegal_smelters = df_matching[df_matching['found_in_minerbaone'] == 'NO - TIDAK PUNYA IZIN']

print(f"\n📊 Total CGS Smelters: {len(df_matching)}")
print(f"✅ Found (ADA IZIN): {len(df_matching) - len(illegal_smelters)}")
print(f"❌ NOT Found (POTENTIALLY ILEGAL): {len(illegal_smelters)}")

# Prepare MinerbaOne names for searching
mb_names_upper = df_minerbaone['nama_badan_usaha'].str.upper().tolist()
mb_names_orig = df_minerbaone['nama_badan_usaha'].tolist()

print("\n" + "="*100)
print("SEARCH FOR POTENTIAL MATCHES DALAM MINERBAONE")
print("="*100)

# Known patterns untuk smelter besar
search_patterns = {
    'Walsin Nickel Industrial Indonesia': ['WALSIN'],
    'Indonesia Tsingshan Stainless Steel': ['TSINGSHAN', 'STAINLESS'],
    'Tsingshan Steel Indonesia': ['TSINGSHAN'],
    'Indonesia Guang Ching Nickel and SSI': ['GUANG', 'CHING'],
    'Indonesia Ruipu Nickel and Chrome Alloy': ['RUIPU'],
    'Wanxiang Nickel Indonesia': ['WANXIANG'],
    'QMB New Energy Materials Indonesia': ['QMB'],
    'Ranger Nickel Industry': ['RANGER'],
    'Gunbuster Nickel Industry': ['GUNBUSTER'],
    'Hengjaya Nickel Industry': ['HENGJAYA'],
    'Huadi Nickel-Alloy Indonesia': ['HUADI'],
    'Huayue Nickel Cobalt': ['HUAYUE', 'HUAYOU'],
    'Bahodopi Nickel Smelting Indonesia': ['BAHODOPI'],
    'Bintang Smelter Indonesia': ['BINTANG SMELTER'],
    'Bukit Smelter Indonesia': ['BUKIT SMELTER'],
    'Cahaya Smelter Indonesia': ['CAHAYA SMELTER'],
    'Fajar Metal Industry Excelsior Nickel Cobalt Project': ['FAJAR METAL', 'EXCELSIOR'],
    'Teluk Metal Industry': ['TELUK METAL'],
    'Lestari Smelter Indonesia': ['LESTARI SMELTER'],
    'Obsidian Stainless Steel': ['OBSIDIAN'],
    'Kolaka Nickel Indonesia': ['KOLAKA NICKEL'],
    'Macika Mineral Industri': ['MACIKA'],
    'Titan Mineral Utama': ['TITAN MINERAL'],
    'Virtue Dragon Nickel Industry (VDNI)': ['VIRTUE', 'DRAGON', 'VDNI'],
    'Ocean Sky Metal Industry': ['OCEAN SKY'],
    'Zhao Hui Nickel': ['ZHAO HUI', 'ZHAOHUI'],
    'Kinlin Nickel Industri': ['KINLIN'],
    'Mahkota Konaweeha': ['MAHKOTA', 'KONAWEEHA'],
    'Sinar Deli Bantaeng': ['SINAR DELI'],
    'Nadesico Nickel Industry': ['NADESICO'],
    'Zhongtsing New Energy': ['ZHONGTSING', 'ZHONG TSING'],
    'Dingxing New Energy': ['DINGXING'],
}

found_potential_matches = []

for cgs_name, patterns in search_patterns.items():
    # Check if this CGS smelter is in the illegal list
    if cgs_name not in illegal_smelters['cgs_smelter_name'].values:
        continue
    
    print(f"\n🔍 Searching for: {cgs_name}")
    print(f"   Patterns: {patterns}")
    
    # Search for each pattern
    matches = []
    for pattern in patterns:
        for idx, mb_name_upper in enumerate(mb_names_upper):
            if pattern in mb_name_upper:
                mb_name = mb_names_orig[idx]
                if mb_name not in matches:
                    matches.append(mb_name)
    
    if matches:
        print(f"   ✅ POTENTIAL MATCHES FOUND:")
        for match in matches:
            print(f"      - {match}")
            found_potential_matches.append({
                'cgs_name': cgs_name,
                'minerbaone_name': match,
                'confidence': 'medium'
            })
    else:
        print(f"   ❌ NO MATCHES FOUND")

print("\n" + "="*100)
print("SUMMARY - POTENTIAL MISSED MATCHES")
print("="*100)

if found_potential_matches:
    df_potential = pd.DataFrame(found_potential_matches)
    print(f"\n📋 Found {len(df_potential)} potential matches:")
    print(df_potential.to_string(index=False))
    
    # Save to CSV
    output_file = os.path.join(project_root, 'data/processed/cgs_minerbaone_potential_matches.csv')
    df_potential.to_csv(output_file, index=False)
    print(f"\n💾 Saved to: {output_file}")
else:
    print("\n❌ No additional potential matches found")

print("\n" + "="*100)
print("SPECIAL CASE: SUBSIDIARY/HOLDING COMPANIES")
print("="*100)
print("""
CATATAN PENTING:
Banyak smelter besar (terutama China) menggunakan struktur holding company:
- Smelter CGS name = Operating name (e.g., "Indonesia Tsingshan Stainless Steel")
- MinerbaOne name = Legal entity name yang bisa berbeda

Contoh yang sudah ditemukan:
- CORII (operating) = CERIA KARYA ABADI (legal entity)
- ANTAM Pomalaa RKEF = ANEKA TAMBANG
- Vale Indonesia (Sorowako) = VALE INDONESIA

Yang masih perlu VALIDASI INTERNET untuk smelter besar:
1. Indonesia Tsingshan - kemungkinan ada di BINTANGDELAPAN atau subsidiary lain
2. Wanxiang Nickel - ditemukan "INDONESIA WANXIANG NEW ENERGY TRADING"
3. Walsin Nickel - ditemukan "WALSIN RESEARCH INNOVATION INDONESIA"
4. Hengjaya Nickel - ditemukan "HENGJAYA MINERALINDO"

REKOMENDASI:
User perlu validasi manual via internet untuk smelter-smelter besar ini.
""")

print("\n" + "="*100)
print("NEXT STEPS")
print("="*100)
print("""
1. Review potential matches di atas
2. Untuk smelter besar China (Tsingshan, Wanxiang, dll):
   - Search internet untuk legal entity name
   - Cross-reference dengan MinerbaOne data
3. Untuk smelter yang benar-benar tidak ada:
   - Kemungkinan ILEGAL / belum punya izin
   - Atau masih dalam proses perizinan
""")
