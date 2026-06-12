"""
Tambah kolom investasi & status IUP ke minerbaone_sulawesi_companies.csv
Semua kolom pakai Bahasa Indonesia
"""
import csv
from pathlib import Path

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR.parent.parent / "data" / "processed" / "minerbaone_sulawesi_companies.csv"
OUTPUT_FILE = BASE_DIR.parent.parent / "data" / "processed" / "minerbaone_sulawesi_lengkap.csv"
PERMITS_FILE = BASE_DIR / "output" / "full" / "minerbaone_permits.csv"

print("="*70)
print("TAMBAH KOLOM INVESTASI & STATUS IUP")
print("="*70)

# Load permits untuk cek status IUP
print("\n[1/2] Loading data izin untuk cek status IUP...")
iup_companies = set()
with open(PERMITS_FILE, 'r', encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        jenis_izin = row.get('jenis_perizinan', '')
        if 'IUP' in jenis_izin:
            iup_companies.add(row.get('id_badan_usaha', ''))

print(f"  ✓ Ditemukan {len(iup_companies):,} perusahaan dengan IUP")

# Load CSV existing dan rename + tambah kolom
print("\n[2/2] Rename kolom & tambah kolom investasi...")
rows = []

# Mapping nama kolom English -> Indonesia
column_mapping = {
    'id_badan_usaha': 'id_perusahaan',
    'nama_perusahaan': 'nama_perusahaan',
    'nib': 'nib',
    'npwp': 'npwp',
    'telepon': 'telepon',
    'email': 'email',
    'alamat': 'alamat',
    'jenis_badan_usaha': 'jenis_badan_usaha',
    'provinsi': 'provinsi',
    'total_izin': 'jumlah_izin',
    'izin_nikel': 'jumlah_izin_nikel',
    'izin_lainnya': 'jumlah_izin_lainnya',
    'komoditas': 'komoditas',
    'golongan': 'golongan',
    'lokasi_izin': 'lokasi_izin',
    'total_luas_ha': 'total_luas_ha'
}

with open(INPUT_FILE, 'r', encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        # Rename kolom existing
        new_row = {}
        for old_key, new_key in column_mapping.items():
            if old_key in row:
                new_row[new_key] = row[old_key]
        
        # Tambah kolom baru
        id_bu = row.get('id_badan_usaha', '')
        
        # Status IUP (Legal/Ilegal)
        new_row['status_iup'] = 'LEGAL' if id_bu in iup_companies else 'ILEGAL'
        
        # Kolom investasi (kosong untuk dorking)
        new_row['nilai_investasi_usd_juta'] = ''
        new_row['nilai_investasi_idr_miliar'] = ''
        new_row['tahun_investasi'] = ''
        
        # Kolom kapasitas produksi (kosong untuk dorking)
        new_row['kapasitas_produksi_ton_tahun'] = ''
        new_row['jenis_kapasitas'] = ''  # bijih/feronikel/NPI/RKEF/dll
        
        # Status operasional
        new_row['status_operasional'] = ''  # operasional/konstruksi/planned
        
        # Sumber data (untuk tracking)
        new_row['sumber_data_investasi'] = ''
        new_row['sumber_data_kapasitas'] = ''
        
        # Catatan tambahan
        new_row['catatan'] = ''
        
        rows.append(new_row)

# Urutan kolom final (Bahasa Indonesia) - tanpa id_perusahaan
final_fieldnames = [
    'nama_perusahaan',
    'jenis_badan_usaha',
    'provinsi',
    'nib',
    'npwp',
    'telepon',
    'email',
    'alamat',
    'jumlah_izin',
    'jumlah_izin_nikel',
    'jumlah_izin_lainnya',
    'status_iup',
    'komoditas',
    'golongan',
    'lokasi_izin',
    'total_luas_ha',
    'nilai_investasi_usd_juta',
    'nilai_investasi_idr_miliar',
    'tahun_investasi',
    'kapasitas_produksi_ton_tahun',
    'jenis_kapasitas',
    'status_operasional',
    'sumber_data_investasi',
    'sumber_data_kapasitas',
    'catatan'
]

# Write output
with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=final_fieldnames, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(rows)

# Statistik
total = len(rows)
legal = sum(1 for row in rows if row['status_iup'] == 'LEGAL')
ilegal = total - legal
izin_nikel = sum(1 for row in rows if row.get('jumlah_izin_nikel', '0') != '0' and row.get('jumlah_izin_nikel', '0') != '')

print("\n" + "="*70)
print("HASIL")
print("="*70)
print(f"Total Perusahaan:          {total:,}")
print(f"Status LEGAL (punya IUP):  {legal:,} ({100*legal/total:.1f}%)")
print(f"Status ILEGAL (no IUP):    {ilegal:,} ({100*ilegal/total:.1f}%)")
print(f"Perusahaan ada izin nikel: {izin_nikel:,} ({100*izin_nikel/total:.1f}%)")

# Breakdown per provinsi
print("\nPer Provinsi:")
prov_count = {}
for row in rows:
    prov = row.get('provinsi', 'Unknown')
    prov_count[prov] = prov_count.get(prov, 0) + 1

for prov in sorted(prov_count.keys()):
    print(f"  {prov:25s} {prov_count[prov]:4d}")

print(f"\n✓ File disimpan: {OUTPUT_FILE}")
print("\nLangkah Berikutnya:")
print("  1. Jalankan Google dorking untuk isi kolom investasi")
print("  2. Lihat panduan: docs/DORKING_PLAN_MINING_INVESTMENT.md")
print("="*70)
