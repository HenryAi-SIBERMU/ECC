import pdfplumber
import pandas as pd

file_path = r'data\raw\pdf_kemenkes\profil-kesehatan-indonesia-2024.pdf'

def extract_table(page_indices, output_csv):
    all_rows = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for p in page_indices:
                page = pdf.pages[p]
                
                table = page.extract_table()
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

# ISPA
extract_table([469, 470], 'data/raw/raw_kemenkes_ispa_2024.csv')

# Malaria
extract_table([493, 494], 'data/raw/raw_kemenkes_malaria_2024.csv')
