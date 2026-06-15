"""
Filter MinerbaOne data untuk region Sulawesi
Merge company details + permits + aggregate by company
Output: 1 clean CSV for dorking reference
"""
import csv
from collections import defaultdict

print("="*80)
print("FILTERING MINERBAONE DATA - SULAWESI REGION")
print("="*80)

# Step 1: Read company details
print("\n1. Reading company details...")
companies = {}
with open('tools/scrapling/output/full/minerbaone_details.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        companies[row['id_badan_usaha']] = {
            'id': row['id_badan_usaha'],
            'nama': row['nama_badan_usaha'],
            'nib': row.get('nib', ''),
            'npwp': row.get('npwp_badan_usaha', ''),
            'telp': row.get('no_telp', ''),
            'email': row.get('email', ''),
            'alamat': row.get('alamat', ''),
            'jenis_badan_usaha': row.get('jenis_badan_usaha', '')
        }

print(f"   Total companies in database: {len(companies):,}")

# Step 2: Read permits and filter Sulawesi
print("\n2. Filtering permits for Sulawesi region...")

# Sulawesi kabupaten keywords
sulawesi_keywords = [
    # Sulawesi Utara
    'MINAHASA', 'MANADO', 'BITUNG', 'TOMOHON', 'KOTAMOBAGU', 'BOLAANG MONGONDOW', 
    'SANGIHE', 'TALAUD', 'SIAU',
    
    # Sulawesi Tengah
    'POSO', 'MOROWALI', 'TOJO', 'BANGGAI', 'TOLI', 'BUOL', 'PARIGI', 'DONGGALA', 
    'SIGI', 'PALU',
    
    # Sulawesi Selatan
    'MAKASSAR', 'PAREPARE', 'PALOPO', 'GOWA', 'MAROS', 'PANGKEP', 'BARRU', 'BONE',
    'SOPPENG', 'WAJO', 'SIDRAP', 'PINRANG', 'ENREKANG', 'LUWU', 'TANA TORAJA',
    'SINJAI', 'BULUKUMBA', 'BANTAENG', 'JENEPONTO', 'TAKALAR', 'SELAYAR',
    
    # Sulawesi Tenggara
    'KENDARI', 'BAU-BAU', 'KOLAKA', 'KONAWE', 'MUNA', 'BUTON', 'WAKATOBI', 'BOMBANA',
    
    # Gorontalo
    'GORONTALO', 'POHUWATO', 'BOALEMO', 'BONE BOLANGO', 'GORONTALO UTARA',
    
    # Sulawesi Barat
    'MAMUJU', 'MAJENE', 'POLEWALI', 'MANDAR', 'MAMASA', 'PASANGKAYU'
]

sulawesi_permits = []
company_permits = defaultdict(list)

with open('tools/scrapling/output/full/minerbaone_permits.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        lokasi = row.get('lokasi_perizinan', '').upper()
        
        # Check if location is in Sulawesi
        is_sulawesi = any(keyword in lokasi for keyword in sulawesi_keywords)
        
        if is_sulawesi:
            company_id = row['id_badan_usaha']
            
            permit_info = {
                'id_izin': row.get('id_perizinan', ''),
                'nomor_izin': row.get('nomor_izin', ''),
                'jenis_izin': row.get('jenis_perizinan', ''),
                'tahap_kegiatan': row.get('tahap_kegiatan', ''),
                'komoditas': row.get('komoditas', ''),
                'golongan': row.get('golongan', ''),
                'luas_ha': row.get('luas_ha', ''),
                'tanggal_berlaku': row.get('tanggal_berlaku', ''),
                'tanggal_berakhir': row.get('tanggal_berakhir', ''),
                'lokasi': row.get('lokasi_perizinan', ''),
                'status_cnc': row.get('status_cnc', ''),
                'scraped_at': row.get('scraped_at', '')
            }
            
            sulawesi_permits.append(permit_info)
            company_permits[company_id].append(permit_info)

print(f"   Sulawesi permits found: {len(sulawesi_permits):,}")
print(f"   Unique companies: {len(company_permits):,}")

# Step 3: Aggregate by company
print("\n3. Aggregating data by company...")

company_aggregates = []

for company_id, permits in company_permits.items():
    if company_id not in companies:
        print(f"   WARNING: Company ID {company_id} not found in details")
        continue
    
    company_info = companies[company_id]
    
    # Aggregate permit info
    komoditas_set = set()
    lokasi_set = set()
    golongan_set = set()
    total_luas = 0
    
    nikel_permits = []
    other_permits = []
    
    for permit in permits:
        komoditas = permit['komoditas']
        komoditas_set.add(komoditas)
        lokasi_set.add(permit['lokasi'])
        if permit['golongan']:
            golongan_set.add(permit['golongan'])
        
        # Sum luas
        try:
            luas = float(permit['luas_ha']) if permit['luas_ha'] else 0
            total_luas += luas
        except:
            pass
        
        # Separate nickel vs others
        if 'Nikel' in komoditas or 'Nikel' in permit['golongan']:
            nikel_permits.append(permit)
        else:
            other_permits.append(permit)
    
    # Determine province
    province = "Unknown"
    first_lokasi = permits[0]['lokasi'].upper()
    
    if any(k in first_lokasi for k in ['MINAHASA', 'MANADO', 'BITUNG', 'TOMOHON', 'KOTAMOBAGU', 'BOLAANG', 'SANGIHE', 'TALAUD']):
        province = "Sulawesi Utara"
    elif any(k in first_lokasi for k in ['POSO', 'MOROWALI', 'TOJO', 'BANGGAI', 'TOLI', 'BUOL', 'PARIGI', 'DONGGALA', 'SIGI', 'PALU']):
        province = "Sulawesi Tengah"
    elif any(k in first_lokasi for k in ['MAKASSAR', 'PAREPARE', 'PALOPO', 'GOWA', 'MAROS', 'PANGKEP', 'BARRU', 'BONE', 'SOPPENG', 'WAJO', 'SIDRAP', 'PINRANG', 'ENREKANG', 'LUWU', 'TANA TORAJA', 'SINJAI', 'BULUKUMBA', 'BANTAENG', 'JENEPONTO', 'TAKALAR', 'SELAYAR']):
        province = "Sulawesi Selatan"
    elif any(k in first_lokasi for k in ['KENDARI', 'BAU-BAU', 'KOLAKA', 'KONAWE', 'MUNA', 'BUTON', 'WAKATOBI', 'BOMBANA']):
        province = "Sulawesi Tenggara"
    elif any(k in first_lokasi for k in ['GORONTALO', 'POHUWATO', 'BOALEMO', 'BONE BOLANGO']):
        province = "Gorontalo"
    elif any(k in first_lokasi for k in ['MAMUJU', 'MAJENE', 'POLEWALI', 'MANDAR', 'MAMASA', 'PASANGKAYU']):
        province = "Sulawesi Barat"
    
    aggregate = {
        'id_badan_usaha': company_info['id'],
        'nama_perusahaan': company_info['nama'],
        'nib': company_info['nib'],
        'npwp': company_info['npwp'],
        'telepon': company_info['telp'],
        'email': company_info['email'],
        'alamat': company_info['alamat'],
        'jenis_badan_usaha': company_info['jenis_badan_usaha'],
        'provinsi': province,
        'total_izin': len(permits),
        'izin_nikel': len(nikel_permits),
        'izin_lainnya': len(other_permits),
        'komoditas': '; '.join(sorted(komoditas_set)),
        'golongan': '; '.join(sorted(golongan_set)) if golongan_set else '',
        'lokasi_izin': '; '.join(sorted(lokasi_set)),
        'total_luas_ha': f"{total_luas:.2f}" if total_luas > 0 else '',
        'has_nickel_permit': 'YES' if len(nikel_permits) > 0 else 'NO'
    }
    
    company_aggregates.append(aggregate)

print(f"   Companies aggregated: {len(company_aggregates):,}")

# Step 4: Sort and save
print("\n4. Sorting and saving...")

# Sort by: has nickel permit (YES first), then by province, then by name
company_aggregates.sort(key=lambda x: (
    0 if x['has_nickel_permit'] == 'YES' else 1,
    x['provinsi'],
    x['nama_perusahaan']
))

# Save to CSV
output_file = 'data/processed/minerbaone_sulawesi_companies.csv'
fieldnames = [
    'id_badan_usaha', 'nama_perusahaan', 'nib', 'npwp', 'telepon', 'email', 
    'alamat', 'jenis_badan_usaha', 'provinsi', 'total_izin', 'izin_nikel', 
    'izin_lainnya', 'komoditas', 'golongan', 'lokasi_izin', 'total_luas_ha', 
    'has_nickel_permit'
]

with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(company_aggregates)

print(f"   ✅ Saved to: {output_file}")

# Step 5: Summary statistics
print("\n" + "="*80)
print("SUMMARY STATISTICS")
print("="*80)

total_companies = len(company_aggregates)
nickel_companies = len([c for c in company_aggregates if c['has_nickel_permit'] == 'YES'])
non_nickel = total_companies - nickel_companies

print(f"\n📊 Total Companies: {total_companies:,}")
print(f"   With Nickel Permits: {nickel_companies:,} ({nickel_companies/total_companies*100:.1f}%)")
print(f"   Without Nickel: {non_nickel:,} ({non_nickel/total_companies*100:.1f}%)")

# By province
print(f"\n📍 By Province:")
by_province = defaultdict(int)
nickel_by_province = defaultdict(int)

for company in company_aggregates:
    by_province[company['provinsi']] += 1
    if company['has_nickel_permit'] == 'YES':
        nickel_by_province[company['provinsi']] += 1

for prov in sorted(by_province.keys()):
    nickel_count = nickel_by_province[prov]
    total_count = by_province[prov]
    print(f"   {prov:25s}: {total_count:4d} companies ({nickel_count:3d} with nickel)")

print(f"\n🔥 Top 20 Companies by Number of Permits:")
sorted_by_permits = sorted(company_aggregates, key=lambda x: x['total_izin'], reverse=True)

for i, company in enumerate(sorted_by_permits[:20], 1):
    nickel_flag = "🟢" if company['has_nickel_permit'] == 'YES' else "⚪"
    print(f"   {i:2d}. {nickel_flag} {company['nama_perusahaan']:50s} | {company['total_izin']:3d} permits | {company['provinsi']}")

print(f"\n" + "="*80)
print("✅ COMPLETE - Ready for investment dorking!")
print("="*80)
print(f"\nNext step: Use company list from {output_file} for Google dorking")
