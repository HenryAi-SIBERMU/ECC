"""
Check if CGS company names exist in MinerbaOne with exact/similar match
Untuk cek apakah CGS names sebenarnya ada di MinerbaOne
"""
import pandas as pd
from fuzzywuzzy import fuzz

print("="*100)
print("CEK: APAKAH NAMA CGS ADA DI MINERBAONE?")
print("="*100)

# Load split report (CGS names yang salah match)
df_split = pd.read_csv('../../data/processed/esdm_split_report.csv')
print(f"\nTotal CGS yang salah match: {len(df_split)}")

# Get unique CGS names
cgs_names = df_split['cgs_name'].unique()
print(f"Unique CGS companies: {len(cgs_names)}")

# Load MinerbaOne companies
df_companies = pd.read_csv('output/minerbaone_companies.csv')
print(f"Total MinerbaOne companies: {len(df_companies):,}")

# Load details for better matching
df_details = pd.read_csv('output/full/minerbaone_details.csv')
print(f"Total MinerbaOne details: {len(df_details):,}")

print("\n" + "="*100)
print("HASIL CEK PER CGS COMPANY")
print("="*100)

results = []

for cgs_name in sorted(cgs_names):
    print(f"\n🔍 CGS: {cgs_name}")
    
    # Check exact match (case insensitive)
    exact_match = df_details[df_details['nama_badan_usaha'].str.upper() == cgs_name.upper()]
    
    if len(exact_match) > 0:
        print(f"   ✅ EXACT MATCH FOUND in MinerbaOne!")
        print(f"      Company ID: {exact_match.iloc[0]['id_badan_usaha']}")
        print(f"      Name: {exact_match.iloc[0]['nama_badan_usaha']}")
        results.append({
            'cgs_name': cgs_name,
            'found_in_minerbaone': 'YES - EXACT',
            'minerbaone_name': exact_match.iloc[0]['nama_badan_usaha'],
            'company_id': exact_match.iloc[0]['id_badan_usaha'],
            'match_score': 100
        })
    else:
        # Check fuzzy match (>90% similarity)
        best_match = None
        best_score = 0
        
        for idx, company in df_details.iterrows():
            score = fuzz.token_sort_ratio(cgs_name.upper(), str(company['nama_badan_usaha']).upper())
            if score > best_score:
                best_score = score
                best_match = company
        
        if best_score >= 90:
            print(f"   ⚠️  HIGH SIMILARITY MATCH (score: {best_score})")
            print(f"      MinerbaOne: {best_match['nama_badan_usaha']}")
            print(f"      Company ID: {best_match['id_badan_usaha']}")
            results.append({
                'cgs_name': cgs_name,
                'found_in_minerbaone': 'YES - SIMILAR',
                'minerbaone_name': best_match['nama_badan_usaha'],
                'company_id': best_match['id_badan_usaha'],
                'match_score': best_score
            })
        elif best_score >= 80:
            print(f"   🟡 MEDIUM SIMILARITY (score: {best_score})")
            print(f"      MinerbaOne: {best_match['nama_badan_usaha']}")
            results.append({
                'cgs_name': cgs_name,
                'found_in_minerbaone': 'MAYBE',
                'minerbaone_name': best_match['nama_badan_usaha'],
                'company_id': best_match['id_badan_usaha'],
                'match_score': best_score
            })
        else:
            print(f"   ❌ NOT FOUND (best match: {best_score})")
            print(f"      Closest: {best_match['nama_badan_usaha']}")
            results.append({
                'cgs_name': cgs_name,
                'found_in_minerbaone': 'NO',
                'minerbaone_name': best_match['nama_badan_usaha'] if best_match is not None else '',
                'company_id': best_match['id_badan_usaha'] if best_match is not None else '',
                'match_score': best_score
            })

# Save results
df_results = pd.DataFrame(results)
output_file = '../../data/processed/cgs_in_minerbaone_check.csv'
df_results.to_csv(output_file, index=False)

print("\n" + "="*100)
print("SUMMARY")
print("="*100)

exact_found = (df_results['found_in_minerbaone'] == 'YES - EXACT').sum()
similar_found = (df_results['found_in_minerbaone'] == 'YES - SIMILAR').sum()
maybe_found = (df_results['found_in_minerbaone'] == 'MAYBE').sum()
not_found = (df_results['found_in_minerbaone'] == 'NO').sum()

print(f"\n📊 HASIL:")
print(f"  ✅ Exact match: {exact_found}/{len(cgs_names)}")
print(f"  ⚠️  High similarity (90+): {similar_found}/{len(cgs_names)}")
print(f"  🟡 Medium similarity (80-89): {maybe_found}/{len(cgs_names)}")
print(f"  ❌ Not found: {not_found}/{len(cgs_names)}")

print(f"\n💾 SAVED: {output_file}")

print(f"\n" + "="*100)
print("KESIMPULAN")
print("="*100)

if exact_found > 0 or similar_found > 0:
    print(f"""
⚠️  ADA {exact_found + similar_found} CGS COMPANIES YANG SEBENARNYA ADA DI MINERBAONE!

Ini berarti:
1. Fuzzy matching GAGAL menemukan mereka karena threshold atau logic yang salah
2. Perusahaan ini SEHARUSNYA di-match, BUKAN dipisah
3. Perlu RE-MATCH dengan algorithm yang lebih baik

REKOMENDASI:
- Review {exact_found + similar_found} companies ini secara manual
- Gunakan exact name matching dulu sebelum fuzzy matching
- Pertimbangkan matching by company ID (NPWP/NIB) jika ada
""")
else:
    print(f"""
✅ SEMUA CGS COMPANIES MEMANG TIDAK ADA DI MINERBAONE

Ini berarti:
- CGS dataset punya perusahaan yang berbeda dari MinerbaOne
- Split decision sudah BENAR
- Kedua dataset melacak entitas yang berbeda (mines vs smelters)
""")
