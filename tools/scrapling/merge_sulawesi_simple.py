"""
Simple CSV merger for MinerbaOne Sulawesi data (no pandas required)
"""
import csv
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output" / "full"
PROCESSED_DIR = BASE_DIR.parent.parent / "data" / "processed"

DETAILS_FILE = OUTPUT_DIR / "minerbaone_details.csv"
PERMITS_FILE = OUTPUT_DIR / "minerbaone_permits.csv"
OUTPUT_FILE = PROCESSED_DIR / "minerbaone_sulawesi_full.csv"

SULAWESI_KEYWORDS = [
    'BOLAANG MONGONDOW', 'MINAHASA', 'SANGIHE', 'TALAUD', 'MANADO', 'BITUNG', 'TOMOHON', 'KOTAMOBAGU',
    'BANGGAI', 'POSO', 'DONGGALA', 'TOLI TOLI', 'BUOL', 'MOROWALI', 'PARIGI MOUTONG', 'TOJO UNA UNA', 
    'SIGI', 'PALU',
    'SELAYAR', 'BULUKUMBA', 'BANTAENG', 'JENEPONTO', 'TAKALAR', 'GOWA', 'SINJAI', 'BONE', 'MAROS', 
    'PANGKAJENE', 'BARRU', 'SOPPENG', 'WAJO', 'SIDENRENG RAPPANG', 'PINRANG', 'ENREKANG', 'LUWU', 
    'TORAJA', 'MAKASSAR', 'PAREPARE', 'PALOPO',
    'KOLAKA', 'KONAWE', 'MUNA', 'BUTON', 'BOMBANA', 'WAKATOBI', 'KENDARI', 'BAU BAU',
    'GORONTALO', 'BOALEMO', 'BONE BOLANGO', 'POHUWATO',
    'PASANGKAYU', 'MAMUJU', 'MAMASA', 'POLEWALI MANDAR', 'MAJENE'
]

def is_sulawesi(text):
    if not text:
        return False
    text_upper = text.upper()
    if any(kw in text_upper for kw in ['SULAWESI', 'SULSEL', 'SULTENG', 'SULUT', 'SULTRA', 'SULBAR']):
        return True
    return any(kw in text_upper for kw in SULAWESI_KEYWORDS)

def extract_provinsi(text):
    if not text:
        return ''
    text_upper = text.upper()
    if 'SULAWESI UTARA' in text_upper or 'SULUT' in text_upper:
        return 'Sulawesi Utara'
    elif 'SULAWESI TENGAH' in text_upper or 'SULTENG' in text_upper:
        return 'Sulawesi Tengah'
    elif 'SULAWESI SELATAN' in text_upper or 'SULSEL' in text_upper:
        return 'Sulawesi Selatan'
    elif 'SULAWESI TENGGARA' in text_upper or 'SULTRA' in text_upper:
        return 'Sulawesi Tenggara'
    elif 'GORONTALO' in text_upper:
        return 'Gorontalo'
    elif 'SULAWESI BARAT' in text_upper or 'SULBAR' in text_upper:
        return 'Sulawesi Barat'
    return ''

print("="*70)
print("MINERBAONE SULAWESI MERGER (Simple CSV Version)")
print("="*70)

# 1. Load details
print("\n[1/4] Loading company details...")
details = {}
with open(DETAILS_FILE, 'r', encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        id_bu = row.get('id_badan_usaha', '')
        if id_bu and is_sulawesi(row.get('alamat', '')):
            row['provinsi'] = extract_provinsi(row.get('alamat', ''))
            details[id_bu] = row

print(f"  ✓ Found {len(details):,} Sulawesi companies")

# 2. Load permits and aggregate
print("\n[2/4] Loading and aggregating permits...")
permit_stats = defaultdict(lambda: {
    'total_izin': 0,
    'izin_nikel': 0,
    'has_iup': False,
    'total_luas_ha': 0.0,
    'komoditas': set(),
    'lokasi': set()
})

with open(PERMITS_FILE, 'r', encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        id_bu = row.get('id_badan_usaha', '')
        if not id_bu:
            continue
        
        # Check if permit location is Sulawesi
        if id_bu not in details and is_sulawesi(row.get('lokasi_perizinan', '')):
            # Add missing company from permit
            if id_bu not in details:
                details[id_bu] = {'id_badan_usaha': id_bu, 'provinsi': ''}
        
        if id_bu in details:
            stats = permit_stats[id_bu]
            stats['total_izin'] += 1
            
            komoditas = row.get('komoditas', '').strip()
            if komoditas and komoditas.upper() == 'NIKEL':
                stats['izin_nikel'] += 1
            if komoditas:
                stats['komoditas'].add(komoditas)
            
            jenis_izin = row.get('jenis_perizinan', '')
            if 'IUP' in jenis_izin:
                stats['has_iup'] = True
            
            try:
                luas = float(row.get('luas_ha', 0) or 0)
                stats['total_luas_ha'] += luas
            except:
                pass
            
            lokasi = row.get('lokasi_perizinan', '').strip()
            if lokasi:
                stats['lokasi'].add(lokasi)

print(f"  ✓ Processed permits for {len(permit_stats):,} companies")

# 3. Merge data
print("\n[3/4] Merging data...")
merged = []
for id_bu, company in details.items():
    stats = permit_stats.get(id_bu, {})
    
    row = {
        'id_badan_usaha': id_bu,
        'nama_badan_usaha': company.get('nama_badan_usaha', ''),
        'jenis_badan_usaha': company.get('jenis_badan_usaha', ''),
        'provinsi': company.get('provinsi', ''),
        'nib': company.get('nib', ''),
        'npwp_badan_usaha': company.get('npwp_badan_usaha', ''),
        'no_telp': company.get('no_telp', ''),
        'email': company.get('email', ''),
        'alamat': company.get('alamat', ''),
        'total_izin': stats.get('total_izin', 0),
        'izin_nikel': stats.get('izin_nikel', 0),
        'has_nickel_permit': 'YES' if stats.get('izin_nikel', 0) > 0 else 'NO',
        'has_iup': 'YES' if stats.get('has_iup', False) else 'NO',
        'komoditas_list': ', '.join(sorted(stats.get('komoditas', set()))),
        'lokasi_izin': ' | '.join(sorted(stats.get('lokasi', set()))),
        'total_luas_ha': f"{stats.get('total_luas_ha', 0.0):.2f}",
        # Placeholder columns for dorking
        'investment_value_usd_million': '',
        'investment_value_idr_billion': '',
        'investment_year': '',
        'production_capacity_ton_year': '',
        'capacity_type': '',
        'operational_status': '',
        'data_source_investment': '',
        'data_source_capacity': '',
        'notes': '',
        'scraped_at': company.get('scraped_at', '')
    }
    merged.append(row)

# Sort by total permits
merged.sort(key=lambda x: int(x['total_izin']), reverse=True)

# 4. Write output
print("\n[4/4] Writing output...")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

fieldnames = [
    'id_badan_usaha', 'nama_badan_usaha', 'jenis_badan_usaha', 'provinsi',
    'nib', 'npwp_badan_usaha', 'no_telp', 'email', 'alamat',
    'total_izin', 'izin_nikel', 'has_nickel_permit', 'has_iup',
    'komoditas_list', 'lokasi_izin', 'total_luas_ha',
    'investment_value_usd_million', 'investment_value_idr_billion', 'investment_year',
    'production_capacity_ton_year', 'capacity_type', 'operational_status',
    'data_source_investment', 'data_source_capacity', 'notes',
    'scraped_at'
]

with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(merged)

# Stats
total = len(merged)
with_permits = sum(1 for row in merged if int(row['total_izin']) > 0)
with_nickel = sum(1 for row in merged if row['has_nickel_permit'] == 'YES')
with_iup = sum(1 for row in merged if row['has_iup'] == 'YES')

print("\n" + "="*70)
print("RESULTS")
print("="*70)
print(f"Total Companies:        {total:,}")
print(f"Companies with Permits: {with_permits:,}")
print(f"Companies with IUP:     {with_iup:,}")
print(f"Companies with Nickel:  {with_nickel:,}")

# Province distribution
prov_count = {}
for row in merged:
    prov = row['provinsi'] or 'Unknown'
    prov_count[prov] = prov_count.get(prov, 0) + 1

print("\nDistribution by Province:")
for prov, count in sorted(prov_count.items(), key=lambda x: -x[1]):
    print(f"  {prov:25s} {count:4d}")

print(f"\n✓ Saved to: {OUTPUT_FILE}")
print("="*70)
