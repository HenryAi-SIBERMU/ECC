import pdfplumber

file_path = r'data\raw\pdf_kemenkes\profil-kesehatan-indonesia-2018.pdf'

try:
    with pdfplumber.open(file_path) as pdf:
        pages = [498, 502, 504, 515]
        for p in pages:
            print(f"--- PAGE {p} ---")
            print(pdf.pages[p].extract_text()[:250])
except Exception as e:
    print(f"Error: {e}")
