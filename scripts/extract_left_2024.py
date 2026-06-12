import pdfplumber
import pandas as pd
import re

file_path = r'data\raw\pdf_kemenkes\profil-kesehatan-indonesia-2024.pdf'

def extract_left_table(page_indices, output_csv):
    all_rows = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for p in page_indices:
                page = pdf.pages[p]
                # Crop left half of the page
                width = page.width
                height = page.height
                left_half = page.crop((0, 0, 520, height))
                
                # Extract table from the cropped region
                table = left_half.extract_table()
                if table:
                    for row in table:
                        clean_row = [str(cell).replace('\n', ' ').strip() if cell else '' for cell in row]
                        if any(clean_row):
                            all_rows.append(clean_row)
                            
        if all_rows:
            df = pd.DataFrame(all_rows)
            df.to_csv(output_csv, index=False, header=False)
            print(f"Sukses menyimpan: {output_csv}")
        else:
            print(f"Gagal ekstrak tabel untuk {output_csv}")
            
    except Exception as e:
        print(f"Error: {e}")

# ISPA is on pages 469, 470 (0-indexed)
extract_left_table([469, 470], 'data/raw/raw_kemenkes_ispa_2024.csv')

# Malaria is on pages 493, 494 (0-indexed)
extract_left_table([493, 494], 'data/raw/raw_kemenkes_malaria_2024.csv')
