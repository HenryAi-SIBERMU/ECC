import opendataloader_pdf
import os
import sys

pdf_path = r"C:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\data\raw\regulasi\Udara_NO2_China_TROPOMI_Arxiv.pdf"
out_dir = r"C:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\data\raw\regulasi"

if not os.path.exists(pdf_path):
    print(f"Error: {pdf_path} does not exist.")
    sys.exit(1)

print(f"Reading {pdf_path} using OpenDataLoader...")

try:
    opendataloader_pdf.convert(
        input_path=[pdf_path],
        output_dir=out_dir,
        format="markdown"
    )
    print(f"Successfully converted PDF to {out_dir}")
except Exception as e:
    print(f"Error during OpenDataLoader conversion: {e}")
