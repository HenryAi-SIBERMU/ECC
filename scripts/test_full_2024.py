import pdfplumber
import pandas as pd

file_path = r'data\raw\pdf_kemenkes\profil-kesehatan-indonesia-2024.pdf'

def test_full_extract(p):
    with pdfplumber.open(file_path) as pdf:
        page = pdf.pages[p]
        table = page.extract_table()
        if table:
            for i, row in enumerate(table[:10]):
                clean = [str(c).replace('\n', ' ') if c else '' for c in row]
                print(f"Row {i}: {clean}")

print("=== ISPA 469 ===")
test_full_extract(469)

print("\n=== MALARIA 493 ===")
test_full_extract(493)
