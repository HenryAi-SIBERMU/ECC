# prepare_data.py — CELIOS ECC Data Pipeline
# Mengambil, membersihkan, dan mengekspor data ECC ke data/processed/
# Analog dengan prepare_data.py di proyek EBT
#
# Pipeline:
#   1. fetch_bps()      — ambil data populasi & konsumsi dari BPS WebAPI
#   2. fetch_klhk()     — ambil data tutupan lahan & kawasan lindung
#   3. calculate_cf()   — hitung Carbon Footprint per komponen (7 komponen)
#   4. calculate_bc()   — hitung Biocapacity per tipe lahan (5 tipe GFN)
#   5. calculate_ecc()  — hitung ECC status (deficit/reserve) per provinsi
#   6. export_csv()     — simpan ke data/processed/
#
# Output:
#   data/processed/nasional_summary.csv
#   data/processed/provinsi_ecc.csv
#
# Jalankan: python data/prepare_data.py
# Akan diisi implementasi lengkap setelah struktur selesai

import os
import pandas as pd

DATA_DIR = os.path.dirname(__file__)
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")


def main():
    print("ECC Data Pipeline — belum diimplementasikan.")
    print("Jalankan setelah BPS API key tersedia di .env")


if __name__ == "__main__":
    main()
