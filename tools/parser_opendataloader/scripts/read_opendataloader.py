import opendataloader_pdf
from pathlib import Path
import os

pdf_path = r"../inputs/Hasil Simulasi ansys perhitungan.pdfr"
out_dir = r"../outputs"

os.makedirs(out_dir, exist_ok=True)

print(f"Reading {pdf_path} using OpenDataLoader...")

try:
    opendataloader_pdf.convert(
        input_path=[pdf_path],
        output_dir=out_dir,
        format="markdown,json,html"
    )
    print(f"Successfully converted PDF to {out_dir}")
except Exception as e:
    print(f"Error during OpenDataLoader conversion: {e}")
