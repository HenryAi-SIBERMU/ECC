import pdfplumber
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

if len(sys.argv) > 1:
    pdf_filename = sys.argv[1]
else:
    pdf_filename = 'Profil_Kesehatan_Indonesia_2022.pdf'

pdf_path = BASE_DIR / 'data' / 'raw' / 'pdf_kemenkes' / pdf_filename

try:
    print(f"[*] Menjalankan Scanner untuk file: {pdf_filename} ...")
    with pdfplumber.open(pdf_path) as pdf:
        total_halaman = len(pdf.pages)
        
        halaman_ispa = []
        halaman_kulit = []
        halaman_puskesmas = []
        halaman_rs = []
        
        start_page = 100 if total_halaman > 150 else 0
        for i in range(start_page, total_halaman):
            page = pdf.pages[i]
            text = page.extract_text()
            if text:
                text_lower = text.lower()
                
                is_table = any(k in text_lower for k in ['provinsi', 'tabel', 'lampiran', 'province', 'table', 'appendix'])
                
                # Penyakit Kulit / Skin disease / dermatitis
                if ('penyakit kulit' in text_lower or 'dermatitis' in text_lower) and is_table:
                    halaman_kulit.append(i + 1)

                # Puskesmas / Pusat Kesehatan Masyarakat
                if ('puskesmas' in text_lower) and is_table:
                    halaman_puskesmas.append(i + 1)
                    
                # Rumah Sakit / Hospital
                if ('rumah sakit' in text_lower or 'hospital' in text_lower) and is_table:
                    halaman_rs.append(i + 1)
                    
                # ISPA / Pneumonia / Gangguan pernapasan
                if ('ispa' in text_lower or 'pneumonia' in text_lower or 'pernapasan' in text_lower or 'napas' in text_lower) and is_table:
                    halaman_ispa.append(i + 1)
                        
        print("\n=== HASIL SCAN ===")
        print(f"ISPA/Gangguan Pernapasan: {halaman_ispa}")
        print(f"Penyakit Kulit: {halaman_kulit}")
        print(f"Puskesmas: {halaman_puskesmas}")
        print(f"Rumah Sakit: {halaman_rs}")
        
except Exception as e:
    print(f"Error: {e}")
