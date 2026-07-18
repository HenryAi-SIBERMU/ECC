import os
import pdfplumber
import pandas as pd
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw' / 'ngo_reports'

def parse_pdf(filepath):
    print(f"\n--- Parsing {filepath.name} ---")
    extracted_data = []
    
    # Keywords for limbah
    keywords = ['slag', 'tailing', 'limbah', 'b3', 'ton', 'juta']
    
    try:
        with pdfplumber.open(filepath) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if not text:
                    continue
                    
                text_lower = text.lower()
                
                # Check if page has relevant keywords
                if any(kw in text_lower for kw in ['slag', 'tailing']) and any(kw in text_lower for kw in ['ton', 'juta']):
                    
                    # Try to extract tables first
                    tables = page.extract_tables()
                    for i, table in enumerate(tables):
                        # Filter empty rows/cells
                        clean_table = [[str(cell).strip().replace('\n', ' ') for cell in row if cell is not None] for row in table]
                        # Flatten to text to check relevance
                        table_text = " ".join([" ".join(row) for row in clean_table]).lower()
                        
                        if any(kw in table_text for kw in ['slag', 'tailing', 'b3', 'ton', 'kapasitas', 'produksi']):
                            print(f"[Page {page_num+1}] Ditemukan Tabel Potensial:")
                            for row in clean_table:
                                if len(row) > 1:
                                    print(" | ".join(row))
                                    
                    # Search text for numeric patterns related to tons
                    # Look for things like "12 juta ton", "1,5 juta ton", "450.000 ton"
                    pattern = r'(\d+[\.,]?\d*)\s*(juta)?\s*ton\s*(?:per\s*tahun|/tahun)?.*?((?:slag|tailing|limbah\s*b3|feronikel|nikel))'
                    matches = re.finditer(pattern, text_lower)
                    for match in matches:
                        snippet_start = max(0, match.start() - 60)
                        snippet_end = min(len(text_lower), match.end() + 60)
                        snippet = text[snippet_start:snippet_end].replace('\n', ' ')
                        print(f"[Page {page_num+1}] Ekstrak Teks: ...{snippet}...")
                        extracted_data.append({
                            'Dokumen': filepath.name,
                            'Halaman': page_num + 1,
                            'Teks Konteks': snippet
                        })
    except Exception as e:
        print(f"Error parsing {filepath.name}: {e}")
        
    return extracted_data

def main():
    all_data = []
    if not RAW_DIR.exists():
        print("Folder raw/ngo_reports belum ada.")
        return
        
    for file in RAW_DIR.glob('*.pdf'):
        data = parse_pdf(file)
        all_data.extend(data)
        
    if all_data:
        df = pd.DataFrame(all_data)
        out_path = BASE_DIR / 'data' / 'processed' / 'ngo_parsed_raw_context.csv'
        df.to_csv(out_path, index=False)
        print(f"\nRaw context tersimpan di {out_path}")
    else:
        print("\nTidak ada data yang berhasil diekstrak.")

if __name__ == "__main__":
    main()
