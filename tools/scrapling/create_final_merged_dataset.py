"""
CREATE FINAL MERGED DATASET
Combine ALL findings:
1. MinerbaOne permits (Sulawesi nickel)
2. CGS smelter data
3. Comprehensive matching (smelter name + operating owner)
4. Status IUP flags ("ADA IUP" / "TIDAK ADA IUP")
"""
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, '..', '..')

print("="*100)
print("CREATING FINAL MERGED DATASET")
print("="*100)

# Read comprehensive matching
matching_file = os.path.join(project_root, 'data/processed/cgs_minerbaone_comprehensive_matching.csv')
with open(matching_file, 'r', encoding='utf-8') as f:
    matching_lines = f.readlines()

matching_header = matching_lines[0].strip().split(',')
matching_data = []
for line in matching_lines[1:]:
    parts = line.strip().split('","')
    if len(parts) >= 6:
        # Clean quotes
        parts = [p.strip('"') for p in parts]
        matching_data.append({
            'cgs_smelter_name': parts[0] if len(parts) > 0 else '',
            'cgs_operating_owner': parts[1] if len(parts) > 1 else '',
            'province': parts[2] if len(parts) > 2 else '',
            'minerbaone_match': parts[3] if len(parts) > 3 else '',
            'match_type': parts[4] if len(parts) > 4 else '',
            'status_izin': parts[5] if len(parts) > 5 else '',
            'latitude': parts[6] if len(parts) > 6 else '',
            'longitude': parts[7] if len(parts) > 7 else '',
            'kapasitas_input_ton': parts[8] if len(parts) > 8 else '',
            'produk_output': parts[9] if len(parts) > 9 else '',
            'kapasitas_output_ton': parts[10] if len(parts) > 10 else '',
        })

print(f"\n📊 Data Loaded:")
print(f"   CGS Comprehensive Matching: {len(matching_data)} smelters")

# Read existing MinerbaOne final dataset
existing_file = os.path.join(project_root, 'data/processed/esdm_master_sulawesi_nikel_2016_2026_id.csv')
with open(existing_file, 'r', encoding='utf-8') as f:
    existing_lines = f.readlines()

existing_header = existing_lines[0].strip()
existing_data = existing_lines[1:]

print(f"   MinerbaOne Sulawesi Permits: {len(existing_data)} permits")

# Create mapping: MinerbaOne company name -> list of permits
minerbaone_companies = {}
for line in existing_data:
    parts = line.split(',')
    if len(parts) > 3:
        company_name = parts[3].strip('"').upper()
        if company_name not in minerbaone_companies:
            minerbaone_companies[company_name] = []
        minerbaone_companies[company_name].append(line)

print(f"   Unique MinerbaOne Companies: {len(minerbaone_companies)}")

# Create final merged dataset
print("\n" + "="*100)
print("MERGING DATA")
print("="*100)

# New columns to add
new_columns = [
    'cgs_smelter_name',
    'cgs_operating_owner',
    'status_izin_iup',
    'match_type',
    'is_illegal_smelter',
    'cgs_latitude',
    'cgs_longitude',
    'cgs_kapasitas_input_ton',
    'cgs_produk_output',
    'cgs_kapasitas_output_ton'
]

output_header = existing_header + ',' + ','.join(new_columns) + '\n'
output_lines = [output_header]

matched_companies = set()

# Process each CGS smelter
for smelter in matching_data:
    status_izin = smelter['status_izin']
    is_illegal = 'TRUE' if status_izin == 'TIDAK ADA IUP' else 'FALSE'
    
    if status_izin == 'ADA IUP':
        # Find matching MinerbaOne permits
        mb_name_upper = smelter['minerbaone_match'].upper()
        
        if mb_name_upper in minerbaone_companies:
            # Add CGS data to each MinerbaOne permit for this company
            for permit_line in minerbaone_companies[mb_name_upper]:
                new_data = [
                    f'"{smelter["cgs_smelter_name"]}"',
                    f'"{smelter["cgs_operating_owner"]}"',
                    status_izin,
                    smelter['match_type'],
                    is_illegal,
                    smelter['latitude'],
                    smelter['longitude'],
                    smelter['kapasitas_input_ton'],
                    smelter['produk_output'],
                    smelter['kapasitas_output_ton']
                ]
                output_line = permit_line.strip() + ',' + ','.join(new_data) + '\n'
                output_lines.append(output_line)
            
            matched_companies.add(mb_name_upper)
            print(f"✅ {smelter['cgs_smelter_name']:50s} → {len(minerbaone_companies[mb_name_upper])} permits")
        else:
            print(f"⚠️  {smelter['cgs_smelter_name']:50s} → Match declared but no permits found")
    else:
        # TIDAK ADA IUP - create new row without MinerbaOne permit data
        # Use empty values for MinerbaOne columns
        empty_minerbaone = [''] * (len(existing_header.split(',')) - 1)
        
        new_data = [
            f'"{smelter["cgs_smelter_name"]}"',
            f'"{smelter["cgs_operating_owner"]}"',
            status_izin,
            smelter['match_type'],
            is_illegal,
            smelter['latitude'],
            smelter['longitude'],
            smelter['kapasitas_input_ton'],
            smelter['produk_output'],
            smelter['kapasitas_output_ton']
        ]
        
        # Create row for ILLEGAL smelter
        output_line = ',' + ','.join(empty_minerbaone) + ',' + ','.join(new_data) + '\n'
        output_lines.append(output_line)
        print(f"❌ {smelter['cgs_smelter_name']:50s} → TIDAK ADA IUP (no permit)")

# Add MinerbaOne permits that don't have CGS match
print("\n📝 Adding MinerbaOne permits without CGS match...")
for company_name, permits in minerbaone_companies.items():
    if company_name not in matched_companies:
        for permit_line in permits:
            # Add empty CGS columns
            empty_cgs = [''] * len(new_columns)
            output_line = permit_line.strip() + ',' + ','.join(empty_cgs) + '\n'
            output_lines.append(output_line)

# Save final dataset
output_file = os.path.join(project_root, 'data/processed/esdm_master_sulawesi_nikel_2016_2026_FINAL.csv')
with open(output_file, 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

print("\n" + "="*100)
print("FINAL STATISTICS")
print("="*100)

total_rows = len(output_lines) - 1  # Exclude header
cgs_matched = len([s for s in matching_data if s['status_izin'] == 'ADA IUP'])
cgs_illegal = len([s for s in matching_data if s['status_izin'] == 'TIDAK ADA IUP'])

print(f"\n📊 FINAL DATASET:")
print(f"   Total Rows: {total_rows:,}")
print(f"   CGS Smelters ADA IUP: {cgs_matched}")
print(f"   CGS Smelters TIDAK ADA IUP: {cgs_illegal} ⭐ EMAS!")
print(f"   MinerbaOne-only permits: {total_rows - cgs_matched - cgs_illegal}")

print(f"\n💾 Final dataset saved to:")
print(f"   {output_file}")

print("\n" + "="*100)
print("DATASET STRUCTURE")
print("="*100)
print(f"""
ORIGINAL MINERBAONE COLUMNS (32):
- id_perusahaan, id_izin, nomor_izin, nama_perusahaan_minerbaone
- alamat, email, telepon, provinsi, lokasi_lengkap
- jenis_izin, komoditas, fase_operasi, status_cnc
- tahun_terbit, tanggal_mulai_izin, tanggal_berakhir_izin, luas_hektar
- tanggal_scraping, nama_perusahaan_cgs, latitude, longitude
- kapasitas_input_ton_tahun, kapasitas_output_ton_tahun
- kapasitas_ni_ekuivalen_ton_tahun, tipe_produk_output
- sumber_data, skor_kecocokan_cgs, kepercayaan_kapasitas
- investasi_miliar_rp, kepercayaan_investasi, sumber_investasi, metodologi_investasi

NEW CGS COLUMNS ({len(new_columns)}):
- cgs_smelter_name         : Nama smelter dari CGS
- cgs_operating_owner      : Operating owner dari CGS
- status_izin_iup          : "ADA IUP" atau "TIDAK ADA IUP" ⭐
- match_type               : Tipe matching (EXACT, ALIAS, ADDRESS_MATCH, dll)
- is_illegal_smelter       : TRUE/FALSE flag untuk analisis
- cgs_latitude             : Koordinat dari CGS
- cgs_longitude            : Koordinat dari CGS
- cgs_kapasitas_input_ton  : Kapasitas input dari CGS
- cgs_produk_output        : Produk output (FeNi, NPI, MHP, dll)
- cgs_kapasitas_output_ton : Kapasitas output dari CGS

TOTAL COLUMNS: {len(existing_header.split(',')) + len(new_columns)}
""")

print("="*100)
print("✅ FINAL MERGED DATASET CREATED!")
print("="*100)
