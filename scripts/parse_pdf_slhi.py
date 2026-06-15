import pdfplumber
import pandas as pd
from pathlib import Path
import sys

def ekstrak_tabel_slhi(tahun, pdf_filename, target_tabel):
    BASE_DIR = Path(__file__).resolve().parent.parent
    pdf_path = BASE_DIR / 'data' / 'raw' / 'sulut_kualitas_air' / pdf_filename
    
    print(f"[*] Membuka dokumen PDF: {pdf_path}")
    
    try:
        print(f"[*] Mengekstrak teks IKA tahun {tahun}...")
        with pdfplumber.open(pdf_path) as pdf:
            for metrik, pages in target_tabel.items():
                print(f"\n[>] Sedang memproses {metrik.upper()}...")
                all_data = []
                
                page_list = [int(p) for p in str(pages).split(',')] if isinstance(pages, (str, int)) else pages
                
                for page_idx in page_list:
                    if page_idx < len(pdf.pages):
                        page = pdf.pages[page_idx]
                        text = page.extract_text()
                        if not text:
                            continue
                            
                        # Parse baris per baris menggunakan Regex manual
                        import re
                        for line in text.split('\n'):
                            # Cari baris yang diawali nama provinsi, misal: "Sulawesi Utara 49,52 54,62 54,10"
                            if re.match(r'^(Aceh|Sumatera|Riau|Jambi|Bengkulu|Lampung|Kepulauan|DKI|Jawa|DI Yogyakarta|Banten|Bali|Nusa|Kalimantan|Sulawesi|Gorontalo|Maluku|Papua|Indonesia)\b', line):
                                parts = line.replace(',', '.').split() # Ganti koma desimal indo jadi titik
                                if len(parts) >= 3: # minimal ada nama provinsi dan 1 angka
                                    # Kumpulkan bagian string jadi nama, sisanya angka
                                    nama = []
                                    angka = []
                                    for p in parts:
                                        if re.match(r'^[\d\.]+$', p) or p == '-':
                                            angka.append(p)
                                        else:
                                            # Skip char aneh dari OCR yang nempel
                                            clean_p = re.sub(r'[^A-Za-z]', '', p)
                                            if clean_p:
                                                nama.append(clean_p)
                                    
                                    if angka:
                                        prov_name = ' '.join(nama)
                                        all_data.append([prov_name] + angka)
                
                if all_data:
                    df = pd.DataFrame(all_data)
                    output_csv = BASE_DIR / 'data' / 'raw' / 'sulut_kualitas_air' / f'raw_slhi_{metrik}_{tahun}.csv'
                    df.to_csv(output_csv, index=False, header=False)
                    print(f"    [SUKSES] Tersimpan di: {output_csv.name}")
                else:
                    print(f"    [-] Gagal menemukan data {metrik} di halaman tersebut.")
                    
            print("\n[V] Ekstraksi SELESAI!")
            return True
            
    except Exception as e:
        print(f"[!] Gagal memproses PDF: {e}")
        return False

if __name__ == "__main__":
    # Konfigurasi halaman tabel IKA (0-indexed based on pdfplumber output)
    target_config = {
        '2017': {'ika': [70]},
        '2018': {'ika': [139]},
        '2019': {'ika': [277]},
        '2020': {'ika': [219]},
        '2024': {'ika': [153]}
    }
    
    if len(sys.argv) > 1:
        year = sys.argv[1]
        if year in target_config:
            ekstrak_tabel_slhi(year, f"SLHI_{year}.pdf", target_config[year])
        else:
            print(f"Tahun {year} belum ada di target_config.")
    else:
        print("Gunakan: python parse_pdf_slhi.py <tahun>")
