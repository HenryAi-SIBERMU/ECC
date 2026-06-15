import os
import pdfplumber
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw' / 'klhk_ngo_reports'

def extract_lenient(filepath):
    print(f"\n{'='*50}\n--- Membaca Narasi: {filepath.name} ---\n{'='*50}")
    
    found_any = False
    try:
        with pdfplumber.open(filepath) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if not text:
                    continue
                    
                text_lower = text.lower()
                
                # Keyword fokus untuk limbah smelter
                if any(k in text_lower for k in ['slag', 'tailing', 'limbah b3', 'b3']) and any(k in text_lower for k in ['ton', 'juta']):
                    # Pisahkan berdasarkan kalimat untuk ekstraksi konteks
                    sentences = re.split(r'(?<=[.!?]) +', text.replace('\n', ' '))
                    for s in sentences:
                        s_low = s.lower()
                        if any(k in s_low for k in ['slag', 'tailing', 'limbah', 'b3']) and any(k in s_low for k in ['ton', 'juta']):
                            print(f"[Hal {page_num+1}] -> {s.strip()}")
                            found_any = True
                            
            if not found_any:
                print("Tidak ada temuan kalimat relevan (Slag/Tailing + Ton/Juta) pada dokumen ini.")
                
    except Exception as e:
        print(f"Error parsing {filepath.name}: {e}")

if __name__ == "__main__":
    if RAW_DIR.exists():
        files_to_parse = [
            'Arinto-Sangadji-HPAL-dalam-Industri-Nikel-Nov-2024_compressed.pdf',
            'Riset-Final-WALHI-SULTRA.pdf',
            'buku-arkl-morowali-summary.pdf'
        ]
        for f in files_to_parse:
            file_path = RAW_DIR / f
            if file_path.exists():
                extract_lenient(file_path)
            else:
                print(f"\nFile tidak ditemukan: {f}")
    else:
        print(f"Folder tidak ditemukan: {RAW_DIR}")
