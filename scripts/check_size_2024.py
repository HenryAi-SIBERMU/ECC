import pdfplumber

file_path = r'data\raw\pdf_kemenkes\profil-kesehatan-indonesia-2024.pdf'
with pdfplumber.open(file_path) as pdf:
    page = pdf.pages[469]
    print(f"Width: {page.width}, Height: {page.height}")
