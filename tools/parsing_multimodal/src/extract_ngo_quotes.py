import os
import pandas as pd
import pdfplumber

# Use relative paths for better portability within the project
RAW_DIR = r"data/raw/ika_ngo"
CSV_PATH = r"data/processed/ika_ngo_cr6_gabungan.csv"

def extract_quotes():
    print("Loading CSV...")
    df = pd.read_csv(CSV_PATH)
    
    # Initialize new column
    df["Kutipan_Lengkap"] = "Kutipan tidak ditemukan."
    
    pdf_files = [f for f in os.listdir(RAW_DIR) if f.lower().endswith('.pdf')]
    
    print(f"Found {len(pdf_files)} PDFs. Extracting text...")
    
    pdf_texts = {}
    for pdf_file in pdf_files:
        pdf_path = os.path.join(RAW_DIR, pdf_file)
        text_pages = []
        print(f"Reading {pdf_file}...")
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    txt = page.extract_text()
                    if txt:
                        # Replace newlines with spaces to form proper continuous sentences
                        txt = txt.replace('\n', ' ')
                        text_pages.append(txt)
        except Exception as e:
            print(f"Error reading {pdf_file}: {e}")
            
        pdf_texts[pdf_file] = text_pages

    # Process each row
    for index, row in df.iterrows():
        titik = str(row["Titik Sampling"]).lower()
        # the titik might be "Titik 1 (IMIP)", in the text it might just be "Titik 1"
        titik_short = titik.split('(')[0].strip()
        val_str = str(row["Konsentrasi Cr6+ (mg/L)"])
        
        found_quote = None
        for pdf_file, pages in pdf_texts.items():
            for page_num, text in enumerate(pages):
                # Split into sentences roughly
                sentences = [s.strip() for s in text.split('. ') if len(s.strip()) > 10]
                for sentence in sentences:
                    s_lower = sentence.lower()
                    # Check if sentence contains the value
                    if val_str in s_lower:
                        # We found the exact value. Check if it's related to our metric or location.
                        if ("cr" in s_lower or "kromium" in s_lower or "heksavalen" in s_lower or 
                            titik_short in s_lower or "titik" in s_lower):
                            found_quote = sentence + "."
                            print(f"Found quote for {row['Titik Sampling']}: {found_quote}")
                            break
                if found_quote:
                    break
            if found_quote:
                break
                
        if found_quote:
            df.at[index, "Kutipan_Lengkap"] = found_quote
            
    print("Saving updated CSV...")
    df.to_csv(CSV_PATH, index=False)
    print("Done!")

if __name__ == "__main__":
    extract_quotes()
