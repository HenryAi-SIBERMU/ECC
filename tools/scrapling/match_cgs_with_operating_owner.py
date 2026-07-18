"""
COMPREHENSIVE MATCHING: CGS vs MinerbaOne
Match by:
1. Smelter Name
2. Operating Owner
3. Known aliases

Output: TIDAK ADA IUP for companies not found (ini EMAS NYA!)
"""

# Read CGS data (Sulawesi only)
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, '..', '..')
cgs_file = os.path.join(script_dir, "output/cgs_dataset_extracted.csv")
minerbaone_file = os.path.join(script_dir, "output/full/minerbaone_details.csv")
matching_file = os.path.join(project_root, "data/processed/cgs_minerbaone_manual_matching.csv")

print("="*100)
print("COMPREHENSIVE MATCHING: SMELTER NAME + OPERATING OWNER")
print("="*100)

# Read files
with open(cgs_file, 'r', encoding='utf-8') as f:
    cgs_lines = f.readlines()

with open(minerbaone_file, 'r', encoding='utf-8') as f:
    mb_lines = f.readlines()

# Parse CGS data
cgs_header = cgs_lines[0].strip().split(',')
smelter_idx = cgs_header.index('Smelter Name')
owner_idx = cgs_header.index('Operating Owner')
province_idx = cgs_header.index('Province')
lat_idx = cgs_header.index('Latitude')
lon_idx = cgs_header.index('Longitude')
input_cap_idx = cgs_header.index('Input Capacity (Tonnes) ')
output_product_idx = cgs_header.index('Output Product ')
output_cap_idx = cgs_header.index('Output Capacity (Tonnes)')

cgs_sulawesi = []
for line in cgs_lines[1:]:
    parts = line.strip().split(',')
    if len(parts) > province_idx:
        province = parts[province_idx]
        if 'Sulawesi' in province:
            smelter_name = parts[smelter_idx] if len(parts) > smelter_idx else ''
            owner = parts[owner_idx] if len(parts) > owner_idx else ''
            lat = parts[lat_idx] if len(parts) > lat_idx else ''
            lon = parts[lon_idx] if len(parts) > lon_idx else ''
            input_cap = parts[input_cap_idx] if len(parts) > input_cap_idx else ''
            output_product = parts[output_product_idx] if len(parts) > output_product_idx else ''
            output_cap = parts[output_cap_idx] if len(parts) > output_cap_idx else ''
            
            cgs_sulawesi.append({
                'smelter_name': smelter_name.strip('"'),
                'operating_owner': owner.strip('"'),
                'province': province.strip('"'),
                'latitude': lat.strip('"'),
                'longitude': lon.strip('"'),
                'input_capacity': input_cap.strip('"'),
                'output_product': output_product.strip('"'),
                'output_capacity': output_cap.strip('"')
            })

# Parse MinerbaOne data (just names for matching)
mb_names_upper = []
mb_names_orig = []
for line in mb_lines[1:]:
    parts = line.split(',')
    if len(parts) > 1:
        name = parts[1].strip('"')
        mb_names_upper.append(name.upper())
        mb_names_orig.append(name)

print(f"\n📊 Data Loaded:")
print(f"   CGS Sulawesi Smelters: {len(cgs_sulawesi)}")
print(f"   MinerbaOne Companies: {len(mb_names_upper):,}")

# Known aliases
known_aliases = {
    'PT ANEKA TAMBANG': ['ANEKA TAMBANG', 'ANTAM'],
    'VALE INDONESIA': ['VALE'],
    'CERIA KARYA ABADI': ['CORII', 'CERIA'],
    'ANG AND FANG BROTHER': ['ANG AND FANG'],
    'CAHAYA SULTRA INDONESIA': ['VIRTUE', 'VIRTU', 'DRAGON'],
    'DAMPALA SEJAHTERA BERSAMA': ['BAHODOPI'],
    'LABOTA BAHODOPI SORAJAI': ['BAHODOPI'],
}

def find_match(smelter_name, owner_name):
    """
    Search for match by smelter name or operating owner
    Returns: (found, matched_name, match_type)
    """
    # Normalize
    smelter_upper = smelter_name.upper()
    owner_upper = owner_name.upper()
    
    # 1. Exact match by smelter name
    variations = [
        smelter_upper,
        f"PT {smelter_upper}",
        smelter_upper.replace("PT ", ""),
    ]
    
    for var in variations:
        if var in mb_names_upper:
            idx = mb_names_upper.index(var)
            return (True, mb_names_orig[idx], 'EXACT_SMELTER_NAME')
    
    # 2. Exact match by operating owner
    owner_variations = [
        owner_upper,
        f"PT {owner_upper}",
        owner_upper.replace("PT ", ""),
    ]
    
    for var in owner_variations:
        if var in mb_names_upper:
            idx = mb_names_upper.index(var)
            return (True, mb_names_orig[idx], 'EXACT_OPERATING_OWNER')
    
    # 3. Known aliases
    for mb_name, aliases in known_aliases.items():
        for alias in aliases:
            if alias in smelter_upper or alias in owner_upper:
                # Find in MinerbaOne
                for i, mb_upper in enumerate(mb_names_upper):
                    if any(a in mb_upper for a in aliases) or mb_name.upper() == mb_upper:
                        return (True, mb_names_orig[i], 'KNOWN_ALIAS')
    
    # 4. Partial match (owner name in company name)
    if len(owner_upper) > 5:  # Minimum length to avoid false positives
        owner_clean = owner_upper.replace("PT ", "").replace("PT. ", "").strip()
        for i, mb_upper in enumerate(mb_names_upper):
            if owner_clean in mb_upper:
                return (True, mb_names_orig[i], 'PARTIAL_OWNER_MATCH')
    
    return (False, None, 'NOT_FOUND')

# Perform comprehensive matching
print("\n" + "="*100)
print("MATCHING RESULTS")
print("="*100)

results = []
matched_count = 0
not_found_count = 0

for smelter in cgs_sulawesi:
    smelter_name = smelter['smelter_name']
    owner = smelter['operating_owner']
    province = smelter['province']
    
    found, mb_name, match_type = find_match(smelter_name, owner)
    
    if found:
        matched_count += 1
        status = 'ADA IUP'
        print(f"✅ {smelter_name:50s} / Owner: {owner:30s} → {mb_name} [{match_type}]")
    else:
        not_found_count += 1
        mb_name = '-'
        status = 'TIDAK ADA IUP'
        print(f"❌ {smelter_name:50s} / Owner: {owner:30s} → TIDAK ADA IUP")
    
    results.append({
        'cgs_smelter_name': smelter_name,
        'cgs_operating_owner': owner,
        'province': province,
        'minerbaone_match': mb_name if found else 'TIDAK ADA IUP',
        'match_type': match_type,
        'status_izin': status,
        'latitude': smelter['latitude'],
        'longitude': smelter['longitude'],
        'kapasitas_input_ton': smelter['input_capacity'],
        'produk_output': smelter['output_product'],
        'kapasitas_output_ton': smelter['output_capacity']
    })

# Save results
output = "cgs_smelter_name,cgs_operating_owner,province,minerbaone_match,match_type,status_izin,latitude,longitude,kapasitas_input_ton,produk_output,kapasitas_output_ton\n"
for r in results:
    output += f'"{r["cgs_smelter_name"]}","{r["cgs_operating_owner"]}","{r["province"]}","{r["minerbaone_match"]}","{r["match_type"]}","{r["status_izin"]}","{r["latitude"]}","{r["longitude"]}","{r["kapasitas_input_ton"]}","{r["produk_output"]}","{r["kapasitas_output_ton"]}"\n'

output_file = os.path.join(project_root, 'data/processed/cgs_minerbaone_comprehensive_matching.csv')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(output)

# Statistics
print("\n" + "="*100)
print("STATISTIK FINAL")
print("="*100)

print(f"\n📊 OVERALL:")
print(f"   Total CGS Smelters Sulawesi: {len(results)}")
print(f"   ✅ ADA IUP: {matched_count} ({matched_count/len(results)*100:.1f}%)")
print(f"   ❌ TIDAK ADA IUP: {not_found_count} ({not_found_count/len(results)*100:.1f}%)")

print(f"\n📍 By Province:")
provinces = {}
for r in results:
    prov = r['province']
    if prov not in provinces:
        provinces[prov] = {'total': 0, 'ada_iup': 0, 'tidak_ada_iup': 0}
    provinces[prov]['total'] += 1
    if r['status_izin'] == 'ADA IUP':
        provinces[prov]['ada_iup'] += 1
    else:
        provinces[prov]['tidak_ada_iup'] += 1

for prov, stats in provinces.items():
    print(f"   {prov:25s}: {stats['ada_iup']}/{stats['total']} ada IUP ({stats['tidak_ada_iup']} TIDAK ADA IUP)")

print(f"\n🎯 INI EMAS NYA:")
print(f"   {not_found_count} smelters TIDAK ADA IUP di MinerbaOne!")
print(f"   = Potentially ILLEGAL / OPERATING WITHOUT PERMIT")

print(f"\n💾 Results saved to: {output_file}")

print("\n" + "="*100)
print("TOP 10 SMELTERS TANPA IUP (by Output Capacity)")
print("="*100)

# Sort by output capacity (TIDAK ADA IUP only)
no_iup = [r for r in results if r['status_izin'] == 'TIDAK ADA IUP']
no_iup_sorted = sorted(no_iup, key=lambda x: float(x['kapasitas_output_ton']) if x['kapasitas_output_ton'] and x['kapasitas_output_ton'] != '' else 0, reverse=True)

for i, r in enumerate(no_iup_sorted[:10], 1):
    cap = f"{float(r['kapasitas_output_ton']):,.0f}" if r['kapasitas_output_ton'] and r['kapasitas_output_ton'] != '' else 'N/A'
    print(f"{i:2d}. {r['cgs_smelter_name']:50s} {cap:>15s} tons/year")
