import os
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'

PARSED_CSV = PROCESSED_DIR / 'amdal_parsed_limbah_b3_v2.csv'
EXISTING_SULAWESI_CSV = PROCESSED_DIR / 'sulawesi_limbah_b3.csv'
ESDM_CSV = PROCESSED_DIR / 'sulawesi_esdm_nikel.csv'

# 1. Map Perusahaan ke Provinsi dari ESDM
perusahaan_to_provinsi = {}
if ESDM_CSV.exists():
    with open(ESDM_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            nama = row.get('nama_perusahaan', '').upper()
            prov = row.get('provinsi', 'Sulawesi (Unknown)')
            perusahaan_to_provinsi[nama] = prov

# 2. Baca file sulawesi_limbah_b3 yang ada
existing_rows = []
fieldnames = []
if EXISTING_SULAWESI_CSV.exists():
    with open(EXISTING_SULAWESI_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            existing_rows.append(row)

if not fieldnames:
    fieldnames = ['Provinsi', 'Kawasan/Perusahaan', 'Jenis Limbah B3', 'Estimasi Timbulan (Ton/Tahun)', 'Sumber Referensi', 'Catatan']

# 3. Baca data parsed amdal v2 dan mapping ke format Sulawesi
new_rows = []
if PARSED_CSV.exists():
    with open(PARSED_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            perusahaan = row.get('perusahaan', '')
            # Coba cari provinsi, pakai pencocokan substring jika tidak sama persis
            prov = 'Sulawesi (Unknown)'
            for key, val in perusahaan_to_provinsi.items():
                if key in perusahaan or perusahaan in key:
                    prov = val
                    break
            
            jenis_limbah = row.get('keyword_konteks', '').title()
            
            # Kolom timbulan di sulawesi_limbah_b3 mintanya Ton/Tahun
            nilai = row.get('nilai', '')
            satuan = row.get('satuan_kode', '')
            jenis_besaran = row.get('jenis_besaran', '')
            
            estimasi_timbulan = ''
            catatan_tambahan = ''
            
            if satuan.lower() in ['ton', 'juta ton', 'mt', 'ton/tahun', 'kg', 'ribu ton']:
                estimasi_timbulan = nilai
                if satuan.lower() != 'ton':
                    catatan_tambahan = f"[{satuan}] "
            else:
                # Kalau bukan ton (misal Ha, mg/L, m3), masukkan ke catatan
                catatan_tambahan = f"[Nilai asli: {nilai} {satuan} ({jenis_besaran})] "
                
            sumber = f"{row.get('kategori_sumber', 'Unknown')} ({row.get('file', '')})"
            catatan_full = catatan_tambahan + "Teks: " + row.get('snippet', '').strip()
            
            new_row = {
                'Provinsi': prov,
                'Kawasan/Perusahaan': perusahaan,
                'Jenis Limbah B3': jenis_limbah,
                'Estimasi Timbulan (Ton/Tahun)': estimasi_timbulan,
                'Sumber Referensi': sumber,
                'Catatan': catatan_full
            }
            new_rows.append(new_row)

# 4. Gabungkan dan simpan kembali ke sulawesi_limbah_b3.csv
all_rows = existing_rows + new_rows

with open(EXISTING_SULAWESI_CSV, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_rows)

print(f"[*] Berhasil menambahkan {len(new_rows)} baris data baru ke {EXISTING_SULAWESI_CSV.name}")

# Hapus file intermediate yang membingungkan agar rapi
import glob
for f in glob.glob(str(PROCESSED_DIR / 'amdal_parsed_limbah_b3*.csv')):
    try:
        os.remove(f)
        print(f"[*] Menghapus file sementara: {os.path.basename(f)}")
    except:
        pass
