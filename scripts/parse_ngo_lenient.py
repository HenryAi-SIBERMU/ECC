import os
import pdfplumber
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw' / 'ngo_reports'

def extract_lenient(filepath):
    print(f"\n--- Membaca Narasi {filepath.name} ---")
    
    try:
        with pdfplumber.open(filepath) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if not text:
                    continue
                    
                text_lower = text.lower()
                
                # Lenient search: any paragraph with ('slag' OR 'tailing') AND 'ton'
                if ('slag' in text_lower or 'tailing' in text_lower or 'limbah b3' in text_lower) and 'ton' in text_lower:
                    sentences = re.split(r'(?<=[.!?]) +', text)
                    for s in sentences:
                        s_low = s.lower()
                        if ('slag' in s_low or 'tailing' in s_low or 'limbah b3' in s_low) and 'ton' in s_low:
                            print(f"[Hal {page_num+1}] -> {s.strip().replace(chr(10), ' ')}")
                            
    except Exception as e:
        print(f"Error parsing {filepath.name}: {e}")

if __name__ == "__main__":
    if RAW_DIR.exists():
        for file in RAW_DIR.glob('*.pdf'):
            extract_lenient(file)
