import os
import pdfplumber

RAW_DIR = r"data/raw/ika_ngo"
pdf_files = ["AEER_Risiko_Laut_IMIP_Cr6.pdf", "WALHI_Sulsel_Lumbung_Polusi.pdf"]

values_to_find = ["0.004", "0,004", "0.028", "0,028", "0.070", "0,070", "0.010", "0,010", "0.005", "0,005", "0.021", "0,021", "0.023", "0,023", "0.100", "0,100", "0.050", "0,050"]

for pdf_file in pdf_files:
    pdf_path = os.path.join(RAW_DIR, pdf_file)
    if not os.path.exists(pdf_path): continue
    print(f"\n--- Searching in {pdf_file} ---")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if not text: continue
                text_lower = text.lower()
                
                # We just want to see if the page has "kromium" or "cr6" and any value
                has_kromium = "cr6" in text_lower or "kromium" in text_lower or "heksavalen" in text_lower
                has_value = any(v in text_lower for v in values_to_find)
                
                if has_kromium and has_value:
                    print(f"\nPage {i+1} has Kromium/Cr6+ AND a target value!")
                    lines = text.split('\n')
                    for line in lines:
                        if any(v in line for v in values_to_find):
                            print(f"  > {line.strip()}")
                            
    except Exception as e:
        print(f"Error: {e}")
