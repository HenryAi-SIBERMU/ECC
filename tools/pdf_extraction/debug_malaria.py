"""
DEBUG: Lihat teks mentah halaman Malaria Sulteng
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import re
from pathlib import Path
import pypdfium2 as pdfium

PDF_PATH = Path("data/raw/profil kesehatan provinsi_kemenkes/Profil_Kesehatan_Sulteng_2022.pdf")
TARGET_HALAMAN = [163, 164, 165, 166, 167]  # Halaman Malaria Sulteng dari log run

pdf = pdfium.PdfDocument(str(PDF_PATH))

for pg in TARGET_HALAMAN:
    idx = pg - 1
    if idx >= len(pdf):
        continue
    txt = pdf[idx].get_textpage().get_text_range()
    print(f"\n{'='*70}")
    print(f"HALAMAN {pg}")
    print(f"{'='*70}")
    # Print 40 baris pertama saja
    for i, line in enumerate(txt.split('\n')[:60]):
        line = line.strip()
        if line:
            print(f"  [{i:02d}] {line[:120]}")
