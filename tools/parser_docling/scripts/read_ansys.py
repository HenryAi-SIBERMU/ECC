import os
from pathlib import Path
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
from docling_core.types.doc import ImageRefMode

pdf_path = r"../inputs/Hasil Simulasi ansys perhitungan.pdfr"
out_dir = Path(r"../outputs")

out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "Hasil_Simulasi_ansys.md"

print(f"Reading {pdf_path} using Docling with FULL FEATURES enabled...")

pipeline_options = PdfPipelineOptions()
pipeline_options.do_formula_enrichment = True
pipeline_options.generate_picture_images = True

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

result = converter.convert(pdf_path)

print("Saving markdown and extracting images to disk (NOT Base64)...")
result.document.save_as_markdown(out_path, image_mode=ImageRefMode.REFERENCED)

print(f"Successfully converted PDF and saved images to {out_dir}")
