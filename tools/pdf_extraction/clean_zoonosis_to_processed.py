#!/usr/bin/env python3
"""
CELIOS Zoonosis Data Cleaner & Processor
=========================================
Membersihkan raw extracted CSV dan menyimpannya ke folder processed/.

Langkah cleaning:
1. Drop kolom raw_nums (tidak diperlukan di processed)
2. Hapus baris dengan total_kasus yang tidak masuk akal
   - total_kasus <= 0
   - total_kasus > 50000 (tidak realistis untuk satu kabupaten)
   - Baris Sulsel yang kode_wilayah (7xxx) terselip di kolom kasus
3. Normalisasi nama kabupaten (Toli-Toli / Tolitoli -> Tolitoli)
4. Tambah kolom 'catatan_data' untuk flagging anomali
5. Output: data/processed/zoonosis_kab_kota_2015_2024.csv

Author: CELIOS Research Division
Date: 26 Juni 2026
"""
import sys
import re
import pandas as pd
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).parent.parent.parent
INPUT_FILE  = PROJECT_ROOT / 'data' / 'raw' / 'profil kesehatan provinsi_kemenkes' / 'zoonosis_raw_extracted.csv'
OUTPUT_DIR  = PROJECT_ROOT / 'data' / 'processed'
OUTPUT_FILE = OUTPUT_DIR / 'zoonosis_kab_kota_2015_2024.csv'

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ─── LOAD ────────────────────────────────────────────────────────────────────
print("="*60)
print("CELIOS ZOONOSIS DATA CLEANER")
print("="*60)

df = pd.read_csv(INPUT_FILE, encoding='utf-8-sig')
print(f"[INPUT]  {len(df)} baris dimuat dari {INPUT_FILE.name}")
print(f"         Provinsi  : {sorted(df['provinsi'].unique())}")
print(f"         Penyakit  : {sorted(df['jenis_penyakit'].unique())}")
print(f"         Tahun     : {sorted(df['tahun'].unique())}")

# ─── STEP 1: Drop kolom debug ─────────────────────────────────────────────
df.drop(columns=['raw_nums'], inplace=True, errors='ignore')
print(f"\n[STEP 1] Kolom 'raw_nums' dihapus (debug only)")

# ─── STEP 2: Filter total_kasus tidak masuk akal ─────────────────────────
sebelum = len(df)
df['total_kasus'] = pd.to_numeric(df['total_kasus'], errors='coerce')

# Baris dengan kode wilayah 4-5 digit (7xxx) yang nyasar jadi total_kasus
mask_kode_wilayah = df['total_kasus'] >= 5000
# Baris yang jelas salah (nol atau negatif setelah coerce)
mask_invalid = df['total_kasus'].isna() | (df['total_kasus'] <= 0)

n_kode = mask_kode_wilayah.sum()
n_invalid = mask_invalid.sum()
df = df[~mask_kode_wilayah & ~mask_invalid].copy()
print(f"\n[STEP 2] Filter anomali:")
print(f"         - {n_kode} baris dengan kode wilayah nyasar (>=5000) → HAPUS")
print(f"         - {n_invalid} baris total_kasus null/nol → HAPUS")
print(f"         Sisa: {len(df)} baris (dari {sebelum})")

# ─── STEP 3: Normalisasi nama kabupaten ──────────────────────────────────
NORM_MAP = {
    'Toli-Toli'      : 'Tolitoli',
    'Tolitoli'       : 'Tolitoli',
    'Pangkajene'     : 'Pangkep',
    'Sidenreng'      : 'Sidrap',
}
df['kabupaten_kota'] = df['kabupaten_kota'].replace(NORM_MAP)
print(f"\n[STEP 3] Normalisasi nama kabupaten selesai ({len(NORM_MAP)} mapping)")

# ─── STEP 4: Flagging anomali dengan catatan_data ─────────────────────────
# Flag data yang total_kasus-nya terlihat masih aneh (terlalu besar untuk
# sebuah kabupaten tapi tidak sampai 5000)
df['catatan_data'] = ''

# Sulsel 2017-2018 Rabies: baris yang masih punya angka kecil tapi raw_nums
# kompleks -- kita flag saja, tidak hapus
mask_sulsel_rabies_suspect = (
    (df['provinsi'] == 'Sulsel') &
    (df['jenis_penyakit'] == 'RABIES') &
    (df['total_kasus'] <= 5)
)
df.loc[mask_sulsel_rabies_suspect, 'catatan_data'] = 'PERLU_VALIDASI_MANUAL'

# Malaria Sulteng: tidak ada data per kab (format PDF narasi, bukan tabel)
# Tidak perlu menambah baris kosong, cukup dokumentasikan di README

n_flagged = (df['catatan_data'] != '').sum()
print(f"\n[STEP 4] {n_flagged} baris di-flag 'PERLU_VALIDASI_MANUAL' (Sulsel Rabies angka kecil)")

# ─── STEP 5: Urutkan & simpan ─────────────────────────────────────────────
df['total_kasus'] = df['total_kasus'].astype(int)
df['meninggal'] = pd.to_numeric(df['meninggal'], errors='coerce').fillna(0).astype(int)
df = df.sort_values(['provinsi', 'jenis_penyakit', 'kabupaten_kota', 'tahun']).reset_index(drop=True)

df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')

# ─── SUMMARY ─────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print("OUTPUT SUMMARY")
print(f"{'='*60}")
print(f"Total baris bersih : {len(df)}")
print(f"Output             : {OUTPUT_FILE}")
print()

# Pivot ringkasan per provinsi-penyakit-tahun
pivot = df.groupby(['provinsi', 'jenis_penyakit'])['tahun'].apply(
    lambda x: f"{x.min()}-{x.max()} ({x.nunique()} thn)"
).reset_index()
pivot.columns = ['Provinsi', 'Penyakit', 'Rentang Tahun']
print(pivot.to_string(index=False))

print()
print(f"\n⚠️  CATATAN GAP DATA:")
print(f"   - MALARIA Sulteng: Data hanya tersedia dalam narasi (tidak ada tabel per kab)")
print(f"   - MALARIA Sulsel : Tidak tersedia di PDF 2015-2018 (format berbeda)")
print(f"   - Sultra, Sulbar, Sulut: PDF tidak tersedia (akses terbatas)")
print(f"\n✅  File siap digunakan untuk analisis Fase 2.")
