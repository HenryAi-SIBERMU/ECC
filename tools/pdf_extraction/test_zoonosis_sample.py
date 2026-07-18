"""
TEST PARSER - 1 PDF SAJA (Sulteng 2022)
Jalankan: python tools/pdf_extraction/test_zoonosis_sample.py
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import re
from pathlib import Path
import pypdfium2 as pdfium

PDF_PATH = Path("data/raw/profil kesehatan provinsi_kemenkes/Profil_Kesehatan_Sulteng_2022.pdf")

KAB_SULTENG = [
    'banggai kepulauan', 'banggai laut', 'banggai',
    'morowali utara', 'morowali',
    'poso', 'donggala', 'toli-toli', 'tolitoli', 'buol',
    'parigi moutong', 'sigi', 'palu', 'touna', 'tojo una-una'
]

DISEASE_TABLE_MARKERS = {
    'dbd': ['demam berdarah dengue', 'kasus demam berdarah', 'kasus dbd'],
    'malaria': ['kasus malaria', 'penemuan kasus malaria', 'positif malaria', 'pemeriksaan darah malaria'],
    'rabies': ['pemberian var', 'gigitan hewan penular rabies', 'kasus ghpr', 'rabies'],
    'filariasis': ['kasus filariasis', 'kronis filariasis']
}

def normalize_kab(text):
    t = text.lower().strip()
    for kab in KAB_SULTENG:
        if kab in t:
            return kab.title()
    return None

def parse_numbers(row_text):
    # Hilangkan angka desimal/persen (2.9, 0.0, 1.1) sebelum parsing
    cleaned = re.sub(r'\d+[.,]\d+', '', row_text)
    cleaned = cleaned.replace(',', '').replace('.', '')
    nums = re.findall(r'\b(\d{1,6})\b', cleaned)
    return [int(n) for n in nums if 1 <= int(n) <= 99999]

pdf = pdfium.PdfDocument(str(PDF_PATH))
print(f"Total halaman: {len(pdf)}")
print("=" * 60)

current_disease = None

for pg_idx in range(len(pdf)):
    page = pdf[pg_idx]
    txt = page.get_textpage().get_text_range()
    txt_lower = txt.lower()

    # Deteksi halaman tabel penyakit
    detected = None
    for disease, markers in DISEASE_TABLE_MARKERS.items():
        if any(m in txt_lower for m in markers):
            has_kab = any(k in txt_lower for k in KAB_SULTENG)
            if has_kab:
                detected = disease
                break

    if detected:
        current_disease = detected
        print(f"\n>>> HALAMAN {pg_idx+1} — Tabel {detected.upper()} ditemukan!")
        print("-" * 60)
        # Print setiap baris yang ada nama kabupaten
        for line in txt.split('\n'):
            kab = normalize_kab(line)
            if kab:
                nums = parse_numbers(line)
                
                # Filter narasi paragraf (harus ada minimal 4 deret angka di tabel)
                if len(nums) < 4:
                    continue
                    
                if disease == 'dbd':
                    # Format DBD: No | Pusk | L | P | L+P | mati_L | mati_P | mati_L+P | CFR...
                    total_kasus = nums[4] if len(nums) >= 5 else (nums[-1] if nums else None)
                    meninggal = nums[7] if len(nums) >= 8 else None
                elif disease == 'malaria':
                    total_kasus = nums[9] if len(nums) >= 10 else (nums[-1] if nums else None)
                    meninggal = None
                elif disease == 'rabies':
                    total_kasus = nums[-1] if nums else None
                    meninggal = None
                elif disease == 'filariasis':
                    total_kasus = nums[-1] if nums else None
                    meninggal = None
                
                print(f"  KAB   : {kab}")
                print(f"  LINE  : {line.strip()[:120]}")
                print(f"  NUMS  : {nums}")
                print(f"  KASUS : {total_kasus}  |  MENINGGAL: {meninggal}")
                print()
