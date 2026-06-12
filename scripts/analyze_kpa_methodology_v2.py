import os
import pdfplumber
import re

pdf_dir = os.path.join("data", "raw", "kpa_ylbhi")
output_file = "kpa_methodology_extract_v2.txt"

ignore_files = ["361185081-Profil-Kesehatan-Indonesia-2016-pdf.pdf"]

# Urutkan berdasarkan tahun
files_to_process = sorted([f for f in os.listdir(pdf_dir) if f.endswith(".pdf") and f not in ignore_files])

results = []

for filename in files_to_process:
    pdf_path = os.path.join(pdf_dir, filename)
    print(f"Memproses {filename}...")
    
    full_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + " "
                    
        # Clean text
        full_text_clean = re.sub(r'\s+', ' ', full_text)
        
        # Cari keyword
        keywords = ["metode pengumpulan data", "metode pemantauan", "sumber data dalam perekaman"]
        found = False
        for kw in keywords:
            idx = full_text_clean.lower().find(kw)
            if idx != -1:
                # Ambil 2500 karakter setelah keyword ditemukan agar pasti lengkap
                chunk = full_text_clean[idx:idx+2500]
                results.append(f"========== {filename} ==========\n{chunk}\n")
                found = True
                break
                
        if not found:
            results.append(f"========== {filename} ==========\nTidak ditemukan keyword.\n")
            
    except Exception as e:
        print(f"Gagal: {e}")

with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(results))
