import opendataloader_pdf
import glob
import os
import sys

pdf_dir = r'c:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\data\raw\osint_references_IKA'
pdfs = glob.glob(os.path.join(pdf_dir, '*.pdf'))

for p in pdfs:
    print(f"Processing: {os.path.basename(p)}")
    try:
        opendataloader_pdf.convert(
            input_path=[p],
            output_dir=pdf_dir,
            format='markdown'
        )
        print(f"Success: {os.path.basename(p)}")
    except Exception as e:
        print(f"Failed: {os.path.basename(p)} -> {e}")
