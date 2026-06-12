import pdfplumber

file_path = r'data\raw\pdf_kemenkes\profil-kesehatan-indonesia-2024.pdf'

def check_pdf():
    try:
        with pdfplumber.open(file_path) as pdf:
            pages = [469, 470, 475, 476, 477, 478, 493, 494]
            for p in pages:
                print(f"--- PAGE {p} ---")
                text = pdf.pages[p].extract_text()
                if text:
                    print(text[:250].replace('\n', ' '))
                else:
                    print("(No text or CID encoded)")
    except Exception as e:
        print(f"Error: {e}")

check_pdf()
