import pdfplumber

file_path = r'data\raw\pdf_kemenkes\Profil-Kesehatan-Indonesia-2019.pdf'

try:
    with pdfplumber.open(file_path) as pdf:
        pages = [458, 459]
        for p in pages:
            print(f"--- PAGE {p} ---")
            print(pdf.pages[p].extract_text()[:250])
except Exception as e:
    print(f"Error: {e}")
