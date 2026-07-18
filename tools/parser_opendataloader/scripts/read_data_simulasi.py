import opendataloader_pdf
import os

pdf_path = r'../inputs/Data Hasil Simulasi.pdfr'
out_dir = r"../outputs"

opendataloader_pdf.convert(
    input_path=[pdf_path],
    output_dir=out_dir,
    format="markdown"
)
