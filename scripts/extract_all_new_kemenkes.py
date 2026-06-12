import pdfplumber
import pandas as pd
from pathlib import Path
import os
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = BASE_DIR / 'data' / 'raw' / 'pdf_kemenkes'

# Konfigurasi tahun ke file PDF (sesuai direktori yang ada)
FILE_MAP = {
    '2014': 'PROFIL_KESEHATAN_INDONESIA_TAHUN_2014.pdf',
    '2015': 'Profil-Kesehatan-Indonesia-Tahun_2015 (1).pdf',
    '2016': '361185081-Profil-Kesehatan-Indonesia-2016-pdf.pdf',
    '2017': 'Profil-Kesehatan-Indonesia-2017.pdf',
    '2018': 'profil-kesehatan-indonesia-2018.pdf',
    '2019': 'Profil-Kesehatan-Indonesia-2019.pdf',
    '2020': 'Profil-Kesehatan-Indonesia-2020.pdf',
    '2021': 'Profil-Kesehatan-Indonesia-2021.pdf',
    '2022': 'Profil_Kesehatan_Indonesia_2022.pdf',
    '2023': '2023.pdf',
    '2024': 'profil-kesehatan-indonesia-2024.pdf'
}

TARGET_KATEGORI = {
    'penyakit_kulit': ['penyakit kulit', 'dermatitis'],
    'gangguan_napas': ['gangguan napas', 'gangguan pernapasan', 'pernapasan'],
    'puskesmas': ['puskesmas', 'pusat kesehatan masyarakat'],
    'rumah_sakit': ['rumah sakit', 'hospital']
}

def extract_for_year(tahun, pdf_filename):
    pdf_path = PDF_DIR / pdf_filename
    if not pdf_path.exists():
        print(f"[-] File tidak ditemukan: {pdf_filename}")
        return

    print(f"\n[*] Memproses: {tahun} -> {pdf_filename}")
    found_data = {k: [] for k in TARGET_KATEGORI.keys()}
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            start_page = 100 if total_pages > 150 else 0
            
            for i in range(start_page, total_pages):
                page = pdf.pages[i]
                text = page.extract_text()
                if not text: continue
                
                text_lower = text.lower()
                is_table_page = any(k in text_lower for k in ['provinsi', 'tabel', 'lampiran', 'province'])
                
                if not is_table_page: continue
                
                # Cek halaman ini cocok ke kategori mana
                for kat, keywords in TARGET_KATEGORI.items():
                    if any(k in text_lower for k in keywords):
                        tables = page.extract_tables()
                        if tables:
                            for table in tables:
                                for row in table:
                                    clean_row = [str(cell).replace('\n', ' ').strip() if cell else '' for cell in row]
                                    if any(clean_row):
                                        found_data[kat].append(clean_row)
                                        
            # Simpan data yang ditemukan
            for kat, data_rows in found_data.items():
                if data_rows:
                    df = pd.DataFrame(data_rows)
                    out_csv = PDF_DIR.parent / f"raw_kemenkes_{kat}_{tahun}.csv"
                    df.to_csv(out_csv, index=False, header=False)
                    print(f"    [+] {kat}: Terekstrak {len(data_rows)} baris -> {out_csv.name}")
                else:
                    print(f"    [-] {kat}: Tidak ada tabel yang ditemukan.")
                    
    except Exception as e:
        print(f"[!] Gagal memproses {pdf_filename}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        th = sys.argv[1]
        if th in FILE_MAP:
            extract_for_year(th, FILE_MAP[th])
        else:
            print(f"Tahun {th} tidak ada di konfigurasi.")
    else:
        print("Mengekstrak untuk semua tahun...")
        for th, file in FILE_MAP.items():
            extract_for_year(th, file)
