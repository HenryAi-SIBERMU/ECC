"""
FIX CGS PARSING & REBUILD EVERYTHING
Masalah: CGS CSV parsing berantakan karena embedded commas
Solution: Parse properly pake csv.DictReader
"""
import os
import csv

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, '..', '..')

print("="*100)
print("FIX CGS PARSING & REBUILD CLEAN DATASET")
print("="*100)

# Step 1: Parse CGS data PROPERLY
cgs_file = os.path.join(script_dir, 'output/cgs_dataset_extracted.csv')
cgs_sulawesi = []

with open(cgs_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if 'Sulawesi' in row.get('Province', ''):
            cgs_sulawesi.append({
                'smelter_name': row.get('Smelter Name', ''),
                'operating_owner': row.get('Operating Owner', ''),
                'province': row.get('Province', ''),
                'latitude': row.get('Latitude', ''),
                'longitude': row.get('Longitude', ''),
                'input_capacity': row.get('Input Capacity (Tonnes) ', ''),  # Note: space after Tonnes
                'output_product': row.get('Output Product ', ''),  # Note: space
                'output_capacity': row.get('Output Capacity (Tonnes)', ''),
                'metal': row.get('Metal', ''),
                'process': row.get('Process', '')
            })

print(f"\n📊 CGS Sulawesi smelters parsed: {len(cgs_sulawesi)}")

# Step 2: Re-run matching with CLEAN CGS data
minerbaone_file = os.path.join(script_dir, 'output/full/minerbaone_details.csv')
mb_names_upper = []
mb_names_orig = []

with open(minerbaone_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        if len(row) > 1:
            name = row[1]
            mb_names_upper.append(name.upper())
            mb_names_orig.append(name)

print(f"📊 MinerbaOne companies: {len(mb_names_upper):,}")

# Known aliases
known_aliases = {
    'ANEKA TAMBANG': ['ANTAM'],
    'VALE INDONESIA': ['VALE'],
    'CERIA KARYA ABADI': ['CORII', 'CERIA'],
    'CENTRAL OMEGA RESOURCES': ['CORII'],
    'ANG AND FANG BROTHER': ['ANG AND FANG'],
    'CAHAYA SULTRA INDONESIA': ['VIRTUE', 'VIRTU', 'DRAGON'],
    'DAMPALA SEJAHTERA BERSAMA': ['BAHODOPI'],
    'IFISHDECO': ['BINTANG SMELTER'],
    'ANUGRAH BATU SULAWESI RESOURCES': ['SULAWESI RESOURCES'],
}

def find_match(smelter_name, owner_name):
    """Match by smelter name or operating owner"""
    smelter_upper = smelter_name.upper()
    owner_upper = owner_name.upper()
    
    # 1. Exact match by owner
    for var in [owner_upper, f"PT {owner_upper}", owner_upper.replace("PT ", "")]:
        if var in mb_names_upper:
            idx = mb_names_upper.index(var)
            return (True, mb_names_orig[idx], 'EXACT_OPERATING_OWNER')
    
    # 2. Exact match by smelter
    for var in [smelter_upper, f"PT {smelter_upper}", smelter_upper.replace("PT ", "")]:
        if var in mb_names_upper:
            idx = mb_names_upper.index(var)
            return (True, mb_names_orig[idx], 'EXACT_SMELTER_NAME')
    
    # 3. Known aliases
    for mb_name, aliases in known_aliases.items():
        for alias in aliases:
            if alias in smelter_upper or alias in owner_upper:
                for i, mb_upper in enumerate(mb_names_upper):
                    if any(a in mb_upper for a in aliases) or mb_name.upper() == mb_upper:
                        return (True, mb_names_orig[i], 'KNOWN_ALIAS')
    
    return (False, None, 'NOT_FOUND')

# Perform matching
print("\n" + "="*100)
print("MATCHING RESULTS")
print("="*100)

matching_results = []
for smelter in cgs_sulawesi:
    found, mb_name, match_type = find_match(smelter['smelter_name'], smelter['operating_owner'])
    
    status = 'ADA IUP' if found else 'TIDAK ADA IUP'
    
    matching_results.append({
        'cgs_smelter_name': smelter['smelter_name'],
        'cgs_operating_owner': smelter['operating_owner'],
        'province': smelter['province'],
        'minerbaone_match': mb_name if found else 'TIDAK ADA IUP',
        'match_type': match_type,
        'status_izin': status,
        'latitude': smelter['latitude'],
        'longitude': smelter['longitude'],
        'kapasitas_input_ton': smelter['input_capacity'],
        'produk_output': smelter['output_product'],
        'kapasitas_output_ton': smelter['output_capacity'],
        'metal': smelter['metal'],
        'process': smelter['process']
    })
    
    if found:
        print(f"✅ {smelter['smelter_name']:50s} → {mb_name}")
    else:
        print(f"❌ {smelter['smelter_name']:50s} → TIDAK ADA IUP")

# Save cleaned matching
output_matching = os.path.join(project_root, 'data/processed/cgs_minerbaone_matching_FIXED.csv')
with open(output_matching, 'w', newline='', encoding='utf-8') as f:
    fieldnames = list(matching_results[0].keys())
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(matching_results)

print(f"\n💾 Fixed matching saved: {output_matching}")

# Step 3: Rebuild final dataset with CLEAN data
print("\n" + "="*100)
print("REBUILDING FINAL DATASET")
print("="*100)

# Read MinerbaOne permits
existing_file = os.path.join(project_root, 'data/processed/esdm_master_sulawesi_nikel_2016_2026_id.csv')
minerbaone_permits = []

with open(existing_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        minerbaone_permits.append(row)

# Group by company
mb_by_company = {}
for permit in minerbaone_permits:
    company = permit['nama_perusahaan_minerbaone'].upper()
    if company not in mb_by_company:
        mb_by_company[company] = []
    mb_by_company[company].append(permit)

# Build final rows
final_rows = []
matched_companies = set()

for match in matching_results:
    status = match['status_izin']
    is_illegal = 'TRUE' if status == 'TIDAK ADA IUP' else 'FALSE'
    
    if status == 'ADA IUP':
        mb_name_upper = match['minerbaone_match'].upper()
        
        if mb_name_upper in mb_by_company:
            for permit in mb_by_company[mb_name_upper]:
                row = permit.copy()
                
                # Add CLEAN CGS columns
                row['cgs_smelter_name'] = match['cgs_smelter_name']
                row['cgs_operating_owner'] = match['cgs_operating_owner']
                row['cgs_province'] = match['province']
                row['status_izin_iup'] = status
                row['match_type'] = match['match_type']
                row['is_illegal_smelter'] = is_illegal
                row['cgs_latitude'] = match['latitude']
                row['cgs_longitude'] = match['longitude']
                row['cgs_kapasitas_input_ton'] = match['kapasitas_input_ton']
                row['cgs_produk_output'] = match['produk_output']
                row['cgs_kapasitas_output_ton'] = match['kapasitas_output_ton']
                row['cgs_metal'] = match['metal']
                row['cgs_process'] = match['process']
                row['parent_company'] = ''
                row['parent_country'] = ''
                row['keterangan'] = f"Smelter: {match['cgs_smelter_name']} | Operator: {match['cgs_operating_owner']} | Process: {match['process']} | Status: ADA IUP di MinerbaOne"
                
                final_rows.append(row)
            
            matched_companies.add(mb_name_upper)
    
    else:
        # TIDAK ADA IUP - create clean row
        row = {
            'id_perusahaan': 'N/A - TIDAK ADA IUP',
            'id_izin': 'N/A',
            'nomor_izin': 'TIDAK ADA IUP',
            'nama_perusahaan_minerbaone': f'[ILLEGAL] {match["cgs_operating_owner"]}',
            'alamat': 'Data tidak tersedia - Smelter tidak terdaftar di MinerbaOne',
            'email': 'N/A',
            'telepon': 'N/A',
            'provinsi': match['province'],
            'lokasi_lengkap': f'Lat: {match["latitude"]}, Long: {match["longitude"]}',
            'jenis_izin': 'TIDAK ADA IUP',
            'komoditas': match['metal'],
            'fase_operasi': 'DIDUGA OPERASI TANPA IZIN',
            'status_cnc': 'N/A',
            'tahun_terbit': 'N/A',
            'tanggal_mulai_izin': 'N/A',
            'tanggal_berakhir_izin': 'N/A',
            'luas_hektar': 'N/A',
            'tanggal_scraping': 'N/A',
            'nama_perusahaan_cgs': '',
            'latitude': match['latitude'],
            'longitude': match['longitude'],
            'kapasitas_input_ton_tahun': match['kapasitas_input_ton'],
            'kapasitas_output_ton_tahun': match['kapasitas_output_ton'],
            'kapasitas_ni_ekuivalen_ton_tahun': '',
            'tipe_produk_output': match['produk_output'],
            'sumber_data': 'CGS only',
            'skor_kecocokan_cgs': '',
            'kepercayaan_kapasitas': 'CGS',
            'investasi_miliar_rp': '',
            'kepercayaan_investasi': 'none',
            'sumber_investasi': 'none',
            'metodologi_investasi': 'N/A',
            'cgs_smelter_name': match['cgs_smelter_name'],
            'cgs_operating_owner': match['cgs_operating_owner'],
            'cgs_province': match['province'],
            'status_izin_iup': status,
            'match_type': match['match_type'],
            'is_illegal_smelter': is_illegal,
            'cgs_latitude': match['latitude'],
            'cgs_longitude': match['longitude'],
            'cgs_kapasitas_input_ton': match['kapasitas_input_ton'],
            'cgs_produk_output': match['produk_output'],
            'cgs_kapasitas_output_ton': match['kapasitas_output_ton'],
            'cgs_metal': match['metal'],
            'cgs_process': match['process'],
            'parent_company': '',
            'parent_country': '',
            'keterangan': f"⚠️ SMELTER TANPA IUP | Operator: {match['cgs_operating_owner']} | Process: {match['process']} | TIDAK TERDAFTAR di MinerbaOne | Kemungkinan ILEGAL"
        }
        final_rows.append(row)

# Add MinerbaOne-only
for company, permits in mb_by_company.items():
    if company not in matched_companies:
        for permit in permits:
            row = permit.copy()
            row['cgs_smelter_name'] = ''
            row['cgs_operating_owner'] = ''
            row['cgs_province'] = ''
            row['status_izin_iup'] = 'IUP ONLY (No Smelter)'
            row['match_type'] = 'N/A'
            row['is_illegal_smelter'] = 'FALSE'
            row['cgs_latitude'] = ''
            row['cgs_longitude'] = ''
            row['cgs_kapasitas_input_ton'] = ''
            row['cgs_produk_output'] = ''
            row['cgs_kapasitas_output_ton'] = ''
            row['cgs_metal'] = ''
            row['cgs_process'] = ''
            row['parent_company'] = ''
            row['parent_country'] = ''
            row['keterangan'] = f"Perusahaan: {permit['nama_perusahaan_minerbaone']} | Ada IUP tapi tidak ada data smelter di CGS (mining only atau smelter belum operasi)"
            final_rows.append(row)

# Write final clean CSV
output_final = os.path.join(project_root, 'data/processed/esdm_master_sulawesi_nikel_FINAL_CLEAN.csv')
if final_rows:
    fieldnames = list(final_rows[0].keys())
    with open(output_final, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(final_rows)

print(f"\n✅ Final clean dataset: {output_final}")
print(f"📊 Total rows: {len(final_rows)}")
print(f"📐 Total columns: {len(fieldnames)}")

stats = {
    'ada_iup': len([r for r in final_rows if r['status_izin_iup'] == 'ADA IUP']),
    'tidak_ada': len([r for r in final_rows if r['status_izin_iup'] == 'TIDAK ADA IUP']),
    'iup_only': len([r for r in final_rows if r['status_izin_iup'] == 'IUP ONLY (No Smelter)'])
}

print(f"\n✅ Smelters dengan IUP: {stats['ada_iup']}")
print(f"❌ Smelters TANPA IUP: {stats['tidak_ada']} ⭐")
print(f"📋 IUP only: {stats['iup_only']}")

print("\n" + "="*100)
print("✅ DONE! DATA BERSIH & KOLOM NYAMBUNG!")
print("="*100)
