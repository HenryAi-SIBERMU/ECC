import pdfplumber

file_path = r'data\raw\pdf_kemenkes\Profil-Kesehatan-Indonesia-2017.pdf'

try:
    with pdfplumber.open(file_path) as pdf:
        print("--- ISPA 445 ---")
        print(pdf.pages[445].extract_text()[:100])
        print("--- KUSTA 451 ---")
        print(pdf.pages[451].extract_text()[:100])
        print("--- MALARIA 462 ---")
        print(pdf.pages[462].extract_text()[:100])
except Exception as e:
    print(f"Error: {e}")
