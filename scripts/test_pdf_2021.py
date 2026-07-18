import pdfplumber

file_path = r'data\raw\pdf_kemenkes\Profil-Kesehatan-Indonesia-2021.pdf'

try:
    with pdfplumber.open(file_path) as pdf:
        pages = [469, 470, 484, 485, 486, 487, 510, 511]
        for p in pages:
            print(f"--- PAGE {p} ---")
            print(pdf.pages[p].extract_text()[:250])
except Exception as e:
    print(f"Error: {e}")
