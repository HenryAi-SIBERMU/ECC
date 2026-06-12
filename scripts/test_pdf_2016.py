import pdfplumber

file_path = r'data\raw\pdf_kemenkes\361185081-Profil-Kesehatan-Indonesia-2016-pdf.pdf'

def check_pdf():
    try:
        with pdfplumber.open(file_path) as pdf:
            pages = [390, 391, 392, 393, 394, 395, 403, 404, 405]
            for p in pages:
                print(f"--- PAGE {p} ---")
                text = pdf.pages[p].extract_text()
                if text:
                    print(text[:250].replace('\n', ' '))
                else:
                    print("(No text)")
    except Exception as e:
        print(f"Error: {e}")

check_pdf()
