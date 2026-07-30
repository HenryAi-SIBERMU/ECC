import pdfplumber
import glob

pdf_path = glob.glob("data/raw/profil kesehatan_nasional_kemenkes/*2022*.pdf")[0]
try:
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text and "Sulawesi Tengah" in text and "Puskesmas" in text:
                print(f"--- PAGE {i+1} ---")
                layout_text = page.extract_text(layout=True)
                print(layout_text[:1000])
                break
except Exception as e:
    print(e)
