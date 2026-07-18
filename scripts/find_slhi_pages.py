import pdfplumber
import os

pdf_dir = r'c:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\data\raw\sulut_kualitas_air'
pdfs = ['SLHI_2017.pdf', 'SLHI_2018.pdf', 'SLHI_2019.pdf']
keyword = 'indeks kualitas air'

for pdf_name in pdfs:
    pdf_path = os.path.join(pdf_dir, pdf_name)
    if not os.path.exists(pdf_path):
        print(f"Missing: {pdf_path}")
        continue
        
    print(f"\n--- Scanning {pdf_name} for '{keyword}' ---")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text and keyword in text.lower():
                    # check if it looks like a table page (has numbers/provinsi names)
                    if 'sulawesi' in text.lower() or 'tabel' in text.lower():
                        print(f"[{pdf_name}] Page {i} (0-indexed) seems to have IKA table.")
                        # Check if it has a table
                        tables = page.extract_tables()
                        if tables:
                            print(f"  -> Has {len(tables)} tables")
                            for row in tables[0][:3]:
                                print(f"    {row[:5]}")
    except Exception as e:
        print(f"Error reading {pdf_name}: {e}")
