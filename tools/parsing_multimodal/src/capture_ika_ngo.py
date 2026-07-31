import os
import pdfplumber

RAW_DIR = r"data/raw/ika_ngo"
OUTPUT_DIR = r"tools/parsing_multimodal/output/ika_ngo"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# The values we are looking for (as strings, dot and comma separated)
TARGET_VALUES = ["0.004", "0,004", "0.028", "0,028", "0.070", "0,070", "0.010", "0,010", 
                 "0.021", "0,021", "0.023", "0,023", "0.100", "0,100", "0.050", "0,050", 
                 "Kromium", "Cr6+", "Heksavalen"]

pdf_files = [f for f in os.listdir(RAW_DIR) if f.lower().endswith('.pdf')]

print("Mulai mencari dan mengambil screenshot (capture) halaman sumber...")

for pdf_file in pdf_files:
    pdf_path = os.path.join(RAW_DIR, pdf_file)
    pdf_name = os.path.splitext(pdf_file)[0]
    
    out_pdf_folder = os.path.join(OUTPUT_DIR, pdf_name)
    
    print(f"\nMemproses {pdf_file}...")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if not text:
                    continue
                
                text_lower = text.lower()
                
                # Cek apakah ada angka spesifik dari data kita
                found_values = [v for v in TARGET_VALUES if v.lower() in text_lower]
                
                # Khusus untuk mencari halaman relevan, kita butuh kombinasi nilai atau kata kunci
                # Jika ada nilai desimal yang sangat spesifik seperti 0.028 atau 0.070
                is_highly_relevant = any(v in text_lower for v in ["0.028", "0,028", "0.070", "0,070", "0.021", "0,021", "0.023", "0,023", "0.100", "0,100"])
                has_chromium_keyword = any(k in text_lower for k in ["cr6+", "kromium", "heksavalen"])
                
                if is_highly_relevant or has_chromium_keyword:
                    print(f"  -> Menemukan kecocokan di Halaman {i+1} ({', '.join(found_values)})")
                    
                    if not os.path.exists(out_pdf_folder):
                        os.makedirs(out_pdf_folder)
                        
                    # Capture screenshot
                    im = page.to_image(resolution=300)
                    img_path = os.path.join(out_pdf_folder, f"page_{i+1}_evidence.png")
                    im.save(img_path, format="PNG")
                    print(f"     [Tersimpan] {img_path}")
                    
    except Exception as e:
        print(f"Error memproses {pdf_file}: {e}")

print("\nSelesai! Seluruh screenshot bukti fisik telah disimpan di folder output.")
