import os
import pdfplumber
import re

pdf_dir = os.path.join("data", "raw", "kpa_ylbhi")
output_file = "kpa_methodology_extract.txt"

# File yang diabaikan (karena salah masuk, file kemenkes)
ignore_files = ["361185081-Profil-Kesehatan-Indonesia-2016-pdf.pdf"]

keywords = ["metode pengumpulan data", "sumber data", "metodologi", "data ini bersumber", "pengumpulan data"]

results = []

for filename in os.listdir(pdf_dir):
    if filename.endswith(".pdf") and filename not in ignore_files:
        pdf_path = os.path.join(pdf_dir, filename)
        print(f"Memproses {filename}...")
        
        found_texts = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        text_lower = text.lower()
                        for kw in keywords:
                            if kw in text_lower:
                                # Cari index kw
                                start_idx = text_lower.find(kw)
                                # Ekstrak ~1000 karakter setelah keyword
                                chunk = text[max(0, start_idx-50):min(len(text), start_idx+1500)]
                                chunk = re.sub(r'\s+', ' ', chunk).strip()
                                found_texts.append(f"--- Halaman {i+1} ---\n{chunk}...\n")
                                break # Lanjut ke halaman berikutnya agar tidak duplikat di halaman yang sama
        except Exception as e:
            print(f"Gagal membaca {filename}: {e}")
            
        if found_texts:
            results.append(f"========== {filename} ==========\n" + "\n".join(found_texts) + "\n")
        else:
            results.append(f"========== {filename} ==========\nTidak ditemukan keyword metodologi secara eksplisit.\n")

with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(results))

print("Selesai! Hasil ekstraksi disimpan di", output_file)
