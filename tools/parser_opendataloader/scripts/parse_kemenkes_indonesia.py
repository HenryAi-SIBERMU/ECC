import opendataloader_pdf
from pathlib import Path
import os
import glob

input_dir = r"data/raw/profil kesehatan_kemenkes"
output_dir = r"data/raw/profil kesehatan_kemenkes"

os.makedirs(output_dir, exist_ok=True)

# Find all PDF files in the directory
pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))

if not pdf_files:
    print(f"No PDF files found in {input_dir}")
else:
    for pdf_path in pdf_files:
        md_path = pdf_path.replace(".pdf", ".md")
        if os.path.exists(md_path):
            print(f"Skipping {os.path.basename(pdf_path)}, markdown already exists.")
            continue
            
        print(f"Processing: {pdf_path}")
        try:
            opendataloader_pdf.convert(
                input_path=[pdf_path],
                output_dir=output_dir,
                format="markdown",
                image_output="off"
            )
            print(f"Successfully converted {os.path.basename(pdf_path)}")
        except Exception as e:
            print(f"Error during OpenDataLoader conversion for {pdf_path}: {e}")

print("All conversions finished.")
