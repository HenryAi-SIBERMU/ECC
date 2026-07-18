import pdfplumber
import re

file_path = r'data\raw\pdf_kemenkes\pdf-profil-kesehatan-indonesia-2016pdf_compress.pdf'

def de_double(text):
    if not text: return ""
    # "PPnneeuummoonniiaa" -> "Pneumonia"
    # Sederhananya, ambil karakter ganjil saja:
    return text[::2]

try:
    with pdfplumber.open(file_path) as pdf:
        for i in range(130, 181):
            if i >= len(pdf.pages): break
            text = pdf.pages[i].extract_text()
            if not text: continue
            
            text_norm = text.lower()
            text_dedouble = de_double(text).lower()
            
            # Cari ISPA
            if 'pneumonia' in text_norm or 'ispa' in text_norm or 'pneumonia' in text_dedouble or 'ispa' in text_dedouble:
                print(f"ISPA found on page: {i}")
            # Cari Diare
            if 'diare' in text_norm or 'diare' in text_dedouble:
                print(f"Diare found on page: {i}")
            # Cari Kusta
            if 'kusta' in text_norm or 'kusta' in text_dedouble:
                print(f"Kusta found on page: {i}")
            # Cari Malaria
            if 'malaria' in text_norm or 'malaria' in text_dedouble:
                print(f"Malaria found on page: {i}")
except Exception as e:
    print(f"Error: {e}")
