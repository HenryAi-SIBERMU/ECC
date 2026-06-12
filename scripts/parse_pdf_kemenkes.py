import pdfplumber
import pandas as pd
from pathlib import Path

def ekstrak_tabel(tahun, pdf_filename, target_tabel):
    BASE_DIR = Path(__file__).resolve().parent.parent
    pdf_path = BASE_DIR / 'data' / 'raw' / 'pdf_kemenkes' / pdf_filename
    
    print(f"[*] Membuka dokumen PDF: {pdf_path}")
    
    try:
        print(f"[*] Mengekstrak seluruh data penyakit dari Lampiran Tahun {tahun}...")
        with pdfplumber.open(pdf_path) as pdf:
            for penyakit, pages in target_tabel.items():
                print(f"\n[>] Sedang memproses {penyakit.upper()}...")
                all_data = []
                
                page_list = [int(p) for p in str(pages).split(',')] if isinstance(pages, (str, int)) else pages
                
                for page_idx in page_list:
                    if page_idx < len(pdf.pages):
                        page = pdf.pages[page_idx]
                        tables = page.extract_tables()
                        
                        if tables:
                            for table in tables:
                                for row in table:
                                    clean_row = [str(cell).replace('\n', ' ').strip() if cell else '' for cell in row]
                                    if any(clean_row):
                                        all_data.append(clean_row)
                
                if all_data:
                    df = pd.DataFrame(all_data)
                    output_csv = BASE_DIR / 'data' / 'raw' / f'raw_kemenkes_{penyakit}_{tahun}.csv'
                    df.to_csv(output_csv, index=False, header=False)
                    print(f"    [SUKSES] Tersimpan di: {output_csv.name}")
                else:
                    print(f"    [-] Gagal menemukan tabel {penyakit} di halaman tersebut.")
                    
            print("\n[V] Ekstraksi SELESAI!")
            return True
            
    except Exception as e:
        print(f"[!] Gagal memproses PDF: {e}")
        return False

if __name__ == "__main__":
    # Konfigurasi untuk Tahun 2015
    # Halaman asli: ISPA (373-374), Diare (375), Kusta (376-377), Malaria (386-387)
    target_config = {
        '2014': {'ispa': [351, 352], 'diare': [353], 'kusta': [354, 355], 'malaria': [364, 365]},
        '2015': {'ispa': [373, 374], 'diare': [375], 'kusta': [376, 377], 'malaria': [386, 387]},
        '2016': {'ispa': [390], 'diare': [392], 'kusta': [393], 'malaria': [403]},
        '2017': {'ispa': [445], 'kusta': [451], 'malaria': [462]},
        '2018': {'ispa': [498], 'diare': [502], 'kusta': [504], 'malaria': [515]},
        '2019': {'ispa': [426], 'diare': [435], 'kusta': [436], 'malaria': [459]},
        '2020': {'ispa': [422], 'diare': [434], 'kusta': [435], 'malaria': [454]},
        '2021': {'ispa': '203', 'diare': '206', 'kusta': '208', 'malaria': '213'},
        '2023': {
            'ispa': '483,484',
            'diare': '489,490',
            'kusta': '491,492',
            'malaria': '507,508'
        },
        '2024': {
            'ispa': '470,471',
            'diare': '476,477',
            'kusta': '478,479',
            'malaria': '494,495'
        }
    }
    
    import sys
    if len(sys.argv) > 1:
        year = sys.argv[1]
        if year in target_config:
            if year == '2024':
                ekstrak_tabel(year, "profil-kesehatan-indonesia-2024.pdf", target_config[year])
            elif year == '2023':
                ekstrak_tabel(year, "2023.pdf", target_config[year])
            elif year == '2016':
                ekstrak_tabel(year, "361185081-Profil-Kesehatan-Indonesia-2016-pdf.pdf", target_config[year])
            else:
                ekstrak_tabel(year, f"{year}.pdf", target_config[year])
        else:
            print(f"Tahun {year} belum ada di target_config.")
    else:
        print("Gunakan: python parse_pdf_kemenkes.py <tahun>")
