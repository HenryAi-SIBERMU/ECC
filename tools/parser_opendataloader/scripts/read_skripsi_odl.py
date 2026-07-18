import os
import sys
from pathlib import Path
from docx2pdf import convert as docx_to_pdf
import opendataloader_pdf

docx_path = r"../inputs/Laporan Tugas Akhir_M. Muamar Kadafi.docxr"
pdf_path = r"../inputs/Laporan Tugas Akhir_M. Muamar Kadafi.pdfr"
out_dir = r"../outputs"

os.makedirs(out_dir, exist_ok=True)

print("1. Converting DOCX to PDF using Word COM via docx2pdf...")
try:
    docx_to_pdf(docx_path, pdf_path)
    print("PDF Conversion successful!")
except Exception as e:
    print(f"Error during DOCX to PDF conversion: {e}")
    sys.exit(1)

print("\n2. Parsing PDF using OpenDataLoader...")
try:
    opendataloader_pdf.convert(
        input_path=[pdf_path],
        output_dir=out_dir,
        format="markdown,json,html"
    )
    print(f"Successfully converted PDF and extracted images to {out_dir}")
except Exception as e:
    print(f"Error during OpenDataLoader parsing: {e}")
