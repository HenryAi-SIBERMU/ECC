import os
import re
import pdfplumber

RAW_DIR_PROVINSI = r"data/raw/profil kesehatan provinsi_kemenkes"
RAW_DIR_NASIONAL = r"data/raw/profil kesehatan_nasional_kemenkes"
OUTPUT_BASE = r"tools/parsing_multimodal/output/penyakit"

# Kita definisikan list penyakit sebagai sub-kategori
DISEASES = [
    "ispa",
    "pneumonia",
    "diare",
    "demam berdarah",
    "dbd",
    "malaria",
    "kusta"
]

TABLE_KEYWORDS = [
    "jumlah kasus",
    "angka kesakitan",
    "tabel",
    "dilayani",
    "kabupaten",
    "kota",
    "provinsi",
    "laki-laki",
    "perempuan"
]

def capture_pages(mode="provinsi", sample_only=True):
    if mode == "provinsi":
        input_dir = RAW_DIR_PROVINSI
        output_dir_mode = os.path.join(OUTPUT_BASE, "provinsi")
    else:
        input_dir = RAW_DIR_NASIONAL
        output_dir_mode = os.path.join(OUTPUT_BASE, "nasional")
        
    print(f"\n========================================")
    print(f"MEMULAI PROSES UNTUK DATA: {mode.upper()}")
    print(f"========================================\n")

    if not os.path.exists(input_dir):
        print(f"Folder {input_dir} tidak ditemukan!")
        return

    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    
    if sample_only and len(pdf_files) > 0:
        target = next((f for f in pdf_files if "Gorontalo_2020" in f), pdf_files[0])
        pdf_files = [target]
        print(f"MODE SAMPEL: Hanya memproses 1 PDF: {pdf_files[0]}\n")
    
    total_captured = 0
    for pdf_file in pdf_files:
        filename_without_ext = os.path.splitext(pdf_file)[0]
        pdf_path = os.path.join(input_dir, pdf_file)
        
        print(f"Membuka dokumen: {pdf_file}...")
        
        captured_count = 0
        try:
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                print(f"  Total Halaman: {total_pages}")
                
                for i in range(total_pages):
                    page = pdf.pages[i]
                    text = page.extract_text()
                    
                    if not text:
                        continue
                        
                    text_lower = text.lower()
                    
                    # Cek indikator tabel
                    has_table_indicator = any(kw in text_lower for kw in TABLE_KEYWORDS)
                    if not has_table_indicator:
                        continue
                    
                    # Cek penyakit apa saja yang ada di halaman ini
                    found_diseases = [disease for disease in DISEASES if disease in text_lower]
                    
                    if found_diseases:
                        print(f"  --> Menangkap Halaman {i+1} (Penyakit: {', '.join(found_diseases)})")
                        im = page.to_image(resolution=300)
                        
                        output_folder = os.path.join(output_dir_mode, filename_without_ext)
                        if not os.path.exists(output_folder):
                            os.makedirs(output_folder)
                            
                        img_path = os.path.join(output_folder, f"page_{i+1}.png")
                        im.save(img_path, format="PNG")
                            
                        captured_count += 1
                        total_captured += 1
                        
        except Exception as e:
            print(f"  Error memproses {pdf_file}: {e}")
            
        print(f"  Selesai: {captured_count} halaman unik ditangkap untuk {filename_without_ext}\n")
        
    print(f"PROSES SELESAI! Total {total_captured} gambar halaman unik ditangkap.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Capture Screenshots Penyakit (Nasional & Provinsi)")
    parser.add_argument("--mode", type=str, choices=["nasional", "provinsi"], default="provinsi", help="Mode pemrosesan")
    parser.add_argument("--sample", action="store_true", help="Jalankan dalam mode sampel (1 PDF saja)")
    args = parser.parse_args()
    
    capture_pages(mode=args.mode, sample_only=args.sample)
