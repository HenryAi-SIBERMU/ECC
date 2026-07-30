import os
import re
import json
import shutil
import pdfplumber

def run_smart_filter(mode="provinsi", sample_only=True, golden_dir_name="golden_tables"):
    BASE_DIR = f"tools/parsing_multimodal/output/faskes/{mode}"
    if mode == "provinsi":
        RAW_DIR = r"data/raw/profil kesehatan provinsi_kemenkes"
        JSON_NAME = "index_emas_provinsi.json"
        REGION_KWS = ["kabupaten", "kota"]
    else:
        RAW_DIR = r"data/raw/profil kesehatan_nasional_kemenkes"
        JSON_NAME = "index_emas.json"
        REGION_KWS = ["provinsi"]

    GOLDEN_DIR = os.path.join(BASE_DIR, golden_dir_name)

    if not os.path.exists(GOLDEN_DIR):
        os.makedirs(GOLDEN_DIR)
        
    golden_index = []
    
    # Ambil semua folder di dalam BASE_DIR (kecuali folder golden_tables)
    folders = [f for f in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, f)) and not f.startswith("golden_tables")]
    
    if sample_only and len(folders) > 0:
        target = next((f for f in folders if "Gorontalo_2020" in f), folders[0])
        folders = [target]
        print(f"MODE SAMPEL FILTER: Hanya memproses 1 Folder: {folders[0]}\n")
        
    for folder_name in sorted(folders):
        if mode == "provinsi":
            pdf_file = folder_name + ".pdf"
        else:
            year = folder_name.split("_")[-1]
            pdf_file = next((f for f in os.listdir(RAW_DIR) if year in f and f.endswith(".pdf")), None)
            
        if not pdf_file:
            print(f"PDF tidak ditemukan untuk folder {folder_name}")
            continue
            
        pdf_path = os.path.join(RAW_DIR, pdf_file)
        
        if not os.path.exists(pdf_path):
            print(f"PDF tidak ada di raw dir: {pdf_path}")
            continue
            
        img_folder = os.path.join(BASE_DIR, folder_name)
        print(f"Memfilter Dokumen {folder_name}...")
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for img_name in sorted(os.listdir(img_folder)):
                    if not img_name.endswith(".png"): continue
                    
                    page_num = int(re.search(r'page_(\d+)', img_name).group(1))
                    page = pdf.pages[page_num - 1]
                    text = page.extract_text()
                    
                    if not text: continue
                    text_lower = text.lower()
                    
                    # Kita baca karakter pertama sbg header (Nasional butuh 600 untuk cari 'provinsi', Provinsi butuh 300 agar tdk kena body tabel)
                    header_len = 600 if mode == "nasional" else 300
                    header_text = text_lower[:header_len] 
                    
                    # SYARAT EMAS: "jumlah rumah sakit" atau "jumlah puskesmas" DAN kata regionalnya
                    has_region = any(kw in header_text for kw in REGION_KWS)
                    
                    if mode == "nasional":
                        is_rs = "jumlah rumah sakit" in header_text
                        is_pkm = "jumlah puskesmas" in header_text
                        
                        is_forbidden = any(f in header_text for f in [
                            "rawat inap", "khusus", "kelas", "tempat tidur", "rasio", "posyandu", "kunjungan"
                        ])
                        
                        if (is_rs or is_pkm) and not is_forbidden:
                            jenis = "Rumah Sakit" if is_rs else "Puskesmas"
                        else:
                            continue
                            
                    else:
                        is_rs = "jumlah rumah sakit" in header_text and has_region
                        is_pkm = "jumlah puskesmas" in header_text and has_region
                        is_gabungan = any(kw in header_text for kw in ["sarana kesehatan", "fasilitas kesehatan"]) and has_region
                        
                        is_forbidden = any(f in header_text for f in [
                            "kelas", "rasio", "posyandu", "kecamatan", 
                            "kunjungan", "kematian", "gizi", "tenaga", "obat", "vaksin", "ketersediaan",
                            "indikator", "kinerja"
                        ])
                        
                        if (is_rs or is_pkm or is_gabungan) and not is_forbidden:
                            if is_rs: jenis = "Rumah Sakit"
                            elif is_pkm: jenis = "Puskesmas"
                            else: jenis = "Faskes Gabungan"
                        else:
                            continue
                            
                    prefix = folder_name.split("_")[-1] if mode == "nasional" else folder_name
                    new_img_name = f"{prefix}_{jenis.replace(' ', '_')}_page_{page_num}.png"
                    src_path = os.path.join(img_folder, img_name)
                    dst_path = os.path.join(GOLDEN_DIR, new_img_name)
                    
                    shutil.copy(src_path, dst_path)
                    
                    golden_index.append({
                        "dokumen": folder_name,
                        "jenis": jenis,
                        "halaman_pdf": page_num,
                        "file_gambar": new_img_name,
                        "path": f"tools/parsing_multimodal/output/faskes/{mode}/{golden_dir_name}/{new_img_name}"
                    })
                    print(f"  [EMAS] Menemukan tabel {jenis} di Halaman {page_num}")
                        
        except Exception as e:
            print(f"Error processing {folder_name}: {e}")

    # Simpan ke JSON
    json_path = os.path.join(GOLDEN_DIR, JSON_NAME)
    if sample_only:
        json_path = os.path.join(GOLDEN_DIR, "index_emas_test.json")
        
    with open(json_path, "w") as f:
        json.dump(golden_index, f, indent=4)
        
    print(f"\nSelesai! Tersaring {len(golden_index)} gambar emas ke {GOLDEN_DIR}")
    print(f"File index JSON dibuat di: {json_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Smart Filter Faskes (Nasional & Provinsi)")
    parser.add_argument("--mode", type=str, choices=["nasional", "provinsi"], default="provinsi", help="Mode pemrosesan")
    parser.add_argument("--sample", action="store_true", help="Jalankan dalam mode sampel (1 PDF saja)")
    parser.add_argument("--golden_dir", type=str, default="golden_tables", help="Nama folder output emas")
    args = parser.parse_args()
    
    run_smart_filter(mode=args.mode, sample_only=args.sample, golden_dir_name=args.golden_dir)
