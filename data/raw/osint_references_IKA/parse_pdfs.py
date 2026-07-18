import opendataloader_pdf
from pathlib import Path
import os

pdf_dir = Path(r"C:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\data\raw\osint_references_IKA")
out_dir = pdf_dir

print(f"Reading PDFs in {pdf_dir} using OpenDataLoader...")

for pdf_file in pdf_dir.glob("*.pdf"):
    print(f"Processing {pdf_file.name}...")
    try:
        opendataloader_pdf.convert(
            input_path=[str(pdf_file)],
            output_dir=str(out_dir),
            format="markdown"
        )
        print(f"Successfully converted {pdf_file.name}")
    except Exception as e:
        print(f"Error converting {pdf_file.name}: {e}")
