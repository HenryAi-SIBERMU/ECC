import pdfplumber

file_path = r'data\raw\pdf_kemenkes\2023.pdf'

def search_pdf():
    try:
        with pdfplumber.open(file_path) as pdf:
            print("Searching for Diare...")
            for i in range(480, 520):
                text = pdf.pages[i].extract_text()
                if text:
                    text_upper = text.upper()
                    if 'DIARE' in text_upper:
                        clean_text = text[:100].replace('\n', ' ')
                        print(f"Diare found on page {i}: {clean_text}")
                    if 'KUSTA' in text_upper and 'BARU' in text_upper:
                        clean_text = text[:100].replace('\n', ' ')
                        print(f"Kusta found on page {i}: {clean_text}")
    except Exception as e:
        print(f"Error: {e}")

search_pdf()
