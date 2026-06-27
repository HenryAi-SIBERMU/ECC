#!/usr/bin/env python3
"""
Extract Zoonosis Data (Malaria, DBD, Rabies, Filariasis) dari Profil Kesehatan Kemenkes
========================================================================================
Pendekatan Final: Scan teks per halaman dengan pypdfium2, filter tabel lampiran, 
lalu ekstrak array angka berderet per Kabupaten/Kota.

Output: data/raw/profil kesehatan provinsi_kemenkes/zoonosis_raw_extracted.csv

Author: CELIOS Research Division
Date: 26 Juni 2026
"""
import sys
import re
from pathlib import Path
import pandas as pd
import pypdfium2 as pdfium

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).parent.parent.parent
INPUT_DIR = PROJECT_ROOT / 'data' / 'raw' / 'profil kesehatan provinsi_kemenkes'
OUTPUT_FILE = INPUT_DIR / 'zoonosis_raw_extracted.csv'

REGION_MAP = {
    'Sulteng': [
        'banggai kepulauan', 'banggai laut', 'banggai',
        'morowali utara', 'morowali',
        'poso', 'donggala', 'toli-toli', 'tolitoli', 'buol',
        'parigi moutong', 'sigi', 'palu', 'touna', 'tojo una-una'
    ],
    'Gorontalo': [
        'boalemo', 'gorontalo', 'pohuwato', 'bone bolango', 'gorontalo utara'
    ],
    'Sulsel': [
        'makassar', 'parepare', 'palopo', 'bulukumba', 'bantaeng', 'jeneponto', 
        'takalar', 'gowa', 'sinjai', 'bone', 'maros', 'pangkajene', 'pangkep', 
        'barru', 'soppeng', 'wajo', 'sidrap', 'sidenreng', 'pinrang', 'enrekang', 
        'luwu', 'luwu utara', 'luwu timur', 'tana toraja', 'toraja utara', 'selayar'
    ],
    'Sulut': [
        'manado', 'bitung', 'tomohon', 'kotamobagu', 'bolaang mongondow', 
        'minahasa', 'sangihe', 'talaud', 'sitaro', 'minahasa utara', 
        'minahasa selatan', 'minahasa tenggara', 'mongondow utara', 
        'mongondow selatan', 'mongondow timur'
    ]
}

def get_kab_list(province: str) -> list[str]:
    # Sesuaikan keyword provinsi dengan list kabupatennya
    for key, kab_list in REGION_MAP.items():
        if key.lower() in province.lower():
            return kab_list
    return []

def normalize_kab(text: str, kab_list: list[str]) -> str | None:
    t = text.lower().strip()
    for kab in kab_list:
        if kab in t:
            return kab.title()
    return None

def parse_numbers(row_text: str) -> list[int]:
    # Hilangkan persentase dan desimal (misal 2.5 atau 0,0) agar angka murni tidak tercampur
    cleaned = re.sub(r'\d+[.,]\d+', '', row_text)
    cleaned = cleaned.replace(',', '').replace('.', '')
    nums = re.findall(r'\b(\d{1,6})\b', cleaned)
    # Abaikan angka 0 agar tidak merusak urutan array utama
    return [int(n) for n in nums if 1 <= int(n) <= 99999]

DISEASE_TABLE_MARKERS = {
    'dbd': ['demam berdarah dengue', 'kasus demam berdarah', 'kasus dbd'],
    'malaria': ['kasus malaria', 'penemuan kasus malaria', 'positif malaria', 'pemeriksaan darah malaria'],
    'rabies': ['pemberian var', 'gigitan hewan penular rabies', 'kasus ghpr', 'rabies'],
    'filariasis': ['kasus filariasis', 'kronis filariasis']
}

def extract_disease_page(page_text: str, disease: str, year: int, province: str, page_num: int, kab_list: list[str]) -> list[dict]:
    records = []
    lines = page_text.split('\n')

    for line in lines:
        kab = normalize_kab(line, kab_list)
        if not kab:
            continue

        nums = parse_numbers(line)
        
        filtered_nums = [n for n in nums if not (1990 <= n <= 2030)]
        
        if len(filtered_nums) < 3:
            continue

        total_kasus = None
        meninggal = None

        if disease == 'dbd':
            total_kasus = filtered_nums[4] if len(filtered_nums) >= 5 else (filtered_nums[-1] if filtered_nums else None)
            meninggal = filtered_nums[7] if len(filtered_nums) >= 8 else None
        elif disease == 'malaria':
            total_kasus = filtered_nums[4] if len(filtered_nums) >= 5 else filtered_nums[-1]
        elif disease in ['rabies', 'filariasis']:
            total_kasus = filtered_nums[-1] if filtered_nums else None
            
        if total_kasus is not None:
            records.append({
                'provinsi': province,
                'kabupaten_kota': kab,
                'tahun': year,
                'jenis_penyakit': disease.upper(),
                'total_kasus': total_kasus,
                'meninggal': meninggal,
                'halaman_pdf': page_num,
                'raw_nums': str(nums) 
            })

    return records

def scan_pdf(pdf_path: Path, province: str, year: int) -> list[dict]:
    print(f"\n[MEMPROSES] {pdf_path.name}")
    
    kab_list = get_kab_list(province)
    if not kab_list:
        print(f"  --> SKIP: Daftar kabupaten untuk provinsi '{province}' tidak ditemukan di mapping.")
        return []

    pdf = pdfium.PdfDocument(str(pdf_path))
    total_pages = len(pdf)
    
    unique_records = {}
    current_disease = None
    in_data_table = False

    for pg_idx in range(total_pages):
        page = pdf[pg_idx]
        page_text = page.get_textpage().get_text_range()
        page_lower = page_text.lower()

        detected_disease = None
        for disease, markers in DISEASE_TABLE_MARKERS.items():
            if any(m in page_lower for m in markers):
                has_kab = any(kab in page_lower for kab in kab_list)
                if has_kab:
                    detected_disease = disease
                    break

        if detected_disease:
            current_disease = detected_disease
            in_data_table = True
            print(f"  --> Tabel {detected_disease.upper()} ditemukan di Halaman {pg_idx + 1}")
            records = extract_disease_page(page_text, current_disease, year, province, pg_idx + 1, kab_list)
            for r in records:
                unique_records[(r['provinsi'], r['tahun'], r['kabupaten_kota'], r['jenis_penyakit'])] = r
                
        elif in_data_table and current_disease:
            has_kab = any(kab in page_lower for kab in kab_list)
            if has_kab and 'tabel' not in page_lower[:50]:
                records = extract_disease_page(page_text, current_disease, year, province, pg_idx + 1, kab_list)
                for r in records:
                    unique_records[(r['provinsi'], r['tahun'], r['kabupaten_kota'], r['jenis_penyakit'])] = r
            else:
                in_data_table = False
                current_disease = None

    final_records = list(unique_records.values())
    print(f"  => {len(final_records)} baris data unik berhasil diekstrak.")
    return final_records

def main():
    print("=" * 70)
    print("CELIOS ZOONOSIS PDF EXTRACTOR (MASS SCAN)")
    print("=" * 70)

    pdf_files = sorted(INPUT_DIR.glob("Profil_Kesehatan_*.pdf"))
    if not pdf_files:
        print(f"ERROR: Tidak ada PDF di {INPUT_DIR}")
        return

    all_records = []
    for pdf_path in pdf_files:
        m = re.search(r'Profil_Kesehatan_([A-Za-z]+)_(\d{4})\.pdf', pdf_path.name)
        if not m:
            continue
        province = m.group(1)
        year = int(m.group(2))
        
        records = scan_pdf(pdf_path, province, year)
        all_records.extend(records)

    if all_records:
        df = pd.DataFrame(all_records)
        df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
        print("\n" + "=" * 70)
        print("EXTRACTION COMPLETE! 🚀")
        print("=" * 70)
        print(f"Total baris data : {len(df)}")
        print(f"Penyakit         : {df['jenis_penyakit'].unique()}")
        print(f"Output disimpan  : {OUTPUT_FILE}")
    else:
        print("\nGagal mengekstrak data dari PDF.")

if __name__ == "__main__":
    main()
