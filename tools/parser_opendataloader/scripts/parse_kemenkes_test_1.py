import opendataloader_pdf
import os

pdf_path = r"data/raw/profil kesehatan_kemenkes/Profil-Kesehatan-Indonesia-2017.pdf"
output_dir = r"data/raw/profil kesehatan_kemenkes"

print(f"Mulai mengekstrak {pdf_path} dengan OpenDataLoader...")
print("Proses ini memakan waktu karena file sangat besar. Mohon ditunggu...")

try:
    opendataloader_pdf.convert(
        input_path=[pdf_path],
        output_dir=output_dir,
        format="markdown",
        image_output="off" # <--- INI KUNCI AGAR TIDAK CRASH DI RAM 1.2 GB
    )
    print("Selesai! File markdown berhasil dibuat.")
except Exception as e:
    print(f"Terjadi error: {e}")
