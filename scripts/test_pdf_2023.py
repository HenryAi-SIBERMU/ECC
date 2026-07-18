import pdfplumber

file_path = r'data\raw\pdf_kemenkes\2023.pdf'

try:
    with pdfplumber.open(file_path) as pdf:
        pages = [483, 484, 489, 490, 491, 492, 507, 508]
        for p in pages:
            print(f"--- PAGE {p} ---")
            print(pdf.pages[p].extract_text()[:250])
except Exception as e:
    print(f"Error: {e}")
