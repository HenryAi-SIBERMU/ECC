import os
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
from docling_core.types.doc import ImageRefMode

# 1. Extract Pages 30 to 60 (which contains Bab 4 / Hasil Simulasi)
input_pdf = r"../inputs/Laporan Tugas Akhir_M. Muamar Kadafi.pdfr"
subset_pdf = r"../inputs/Bab4_Skripsi.pdfr"
out_dir = Path(r"../outputs")
out_dir.mkdir(parents=True, exist_ok=True)

print("Extracting pages 30 to 65 for Bab 4...")
reader = PdfReader(input_pdf)
writer = PdfWriter()

# Pages are 0-indexed in PyPDF2.
start_page = 30
end_page = min(65, len(reader.pages))

for i in range(start_page, end_page):
    writer.add_page(reader.pages[i])

with open(subset_pdf, "wb") as f:
    writer.write(f)

print(f"Subset PDF created: {subset_pdf} ({end_page - start_page} pages)")

# 2. Run Docling on the subset
print("Running Docling V2 (Vision AI) on the extracted Bab 4 to fix the graphs...")
out_path = out_dir / "Bab4_Hasil_Simulasi.md"

pipeline_options = PdfPipelineOptions()
pipeline_options.do_formula_enrichment = True
pipeline_options.generate_picture_images = True

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

result = converter.convert(subset_pdf)

print("Saving markdown and extracting images to disk...")
result.document.save_as_markdown(out_path, image_mode=ImageRefMode.REFERENCED)

print(f"Successfully converted Bab 4 and saved proper images to {out_dir}")
