import pdfplumber
import os

pdf_path = os.path.join("data", "raw", "kpa_ylbhi", "catahu-2016-liberalisasi-agraria-diperhebat-reforma-agraria-dibelokkan.pdf")
output_path = os.path.join("data", "raw", "kpa_ylbhi", "full_text_2016.txt")

with pdfplumber.open(pdf_path) as pdf:
    full_text = ""
    for page in pdf.pages:
        full_text += page.extract_text() + "\n"

with open(output_path, "w", encoding="utf-8") as f:
    f.write(full_text)

print(f"Full text extracted to {output_path}")
