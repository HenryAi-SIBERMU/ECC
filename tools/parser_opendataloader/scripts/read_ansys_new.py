import opendataloader_pdf
import os

pdf_path = r'../inputs/Hasil Simulasi ansys perhitungan new.pdfr'
out_dir = r"../outputs"

opendataloader_pdf.convert(
    input_path=[pdf_path],
    output_dir=out_dir,
    format="markdown"
)
