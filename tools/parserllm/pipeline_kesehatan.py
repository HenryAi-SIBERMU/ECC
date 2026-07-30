import os
import glob
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

RAW_DIR = "data/raw/profil kesehatan_kemenkes"
OUT_V3 = "data/processed/sulawesi_kesehatan_detail_2014_2024_v3.csv"
OUT_V2 = "data/processed/sulawesi_kesehatan_detail_2014_2024_v2.csv"

# Daftar target provinsi (hanya Sulawesi)
PROVINCES = [
    "Sulawesi Utara", "Sulawesi Tengah", "Sulawesi Selatan", 
    "Sulawesi Tenggara", "Gorontalo", "Sulawesi Barat"
]

KEYWORDS = ["diare", "ispa", "pneumonia", "dbd", "dengue", "malaria"]

def get_year_from_filename(filename):
    match = re.search(r'20\d{2}', filename)
    if match:
        return match.group(0)
    return "Unknown"

def extract_paragraphs_to_memory():
    """
    Step 1: Extract relevant chunks from National MD files in data/raw/profil kesehatan_kemenkes
    """
    print("=== TAHAP 1: EKSTRAKSI CHUNK DARI MARKDOWN NASIONAL ===")
    extracted_data = []
    
    md_files = glob.glob(os.path.join(RAW_DIR, "*.md"))
    if not md_files:
        md_files = glob.glob(os.path.join("../../", RAW_DIR, "*.md"))
        
    if not md_files:
        print(f"Warning: No Markdown files found in {RAW_DIR}")
        return pd.DataFrame()
        
    for filepath in md_files:
        filename = os.path.basename(filepath)
        tahun = get_year_from_filename(filename)
        print(f"Membaca {filename} (Tahun: {tahun})...")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding='latin-1') as f:
                lines = f.readlines()
                
        # Chunking: 1200 lines per chunk, 250 lines overlap
        chunk_size = 1200
        overlap = 250
        
        i = 0
        while i < len(lines):
            end = min(i + chunk_size, len(lines))
            chunk_lines = lines[i:end]
            chunk_text = "\n".join(chunk_lines).lower()
            
            # Cek apakah chunk ini memiliki provinsi sulawesi DAN keyword penyakit
            has_prov = any(prov.lower() in chunk_text for prov in PROVINCES)
            has_keyword = any(kw in chunk_text for kw in KEYWORDS)
            
            if has_prov and has_keyword:
                context_lines = []
                for j in range(i, end):
                    if lines[j].strip():
                        context_lines.append(f"[{j+1}] {lines[j].strip()}")
                        
                if context_lines:
                    extracted_data.append({
                        "tahun": tahun,
                        "kalimat_asli": "\n".join(context_lines),
                        "start_baris": i + 1,
                        "sumber_file": filename
                    })
            
            i += (chunk_size - overlap)
                    
    df_raw = pd.DataFrame(extracted_data)
    print(f"-> Selesai: {len(df_raw)} chunk masif relevan ditemukan untuk diproses GPT-5.4-mini.")
    return df_raw

def run_llm_validation(df_raw):
    """
    Step 2: Parse extracted chunks using GPT-5.4-mini with V8 Hard Filters
    """
    print("\n=== TAHAP 2: PARSING GPT-5.4-MINI (MARKDOWN NASIONAL) ===")
    if df_raw.empty:
        print("Data chunk kosong. Proses dihentikan.")
        return
        
    aggregated_data = []
    
    def process_chunk(idx, row, tahun):
        context_text = row['kalimat_asli']
        prompt = f"""
        Anda adalah Data Scientist Senior sekaligus Auditor Medis yang sangat teliti.
        Ini adalah potongan dokumen 'Profil Kesehatan Indonesia Tahun {tahun}'.
        
        Tugas Anda HANYA mengekstrak JUMLAH KASUS (tingkat 6 Provinsi Sulawesi: Sulawesi Utara, Sulawesi Tengah, Sulawesi Selatan, Sulawesi Tenggara, Gorontalo, Sulawesi Barat) untuk 4 indikator penyakit ini SAJA:
        1. Diare (atau Kasus Diare Dilayani / Diare Ditemukan)
        2. ISPA (atau Pneumonia)
        3. DBD (Demam Berdarah Dengue / Dengue Hemorrhagic Fever)
        4. Malaria (Malaria Positif)
        
        Setiap baris teks diawali dengan nomor baris sumbernya misalnya [1540].
        
        ATURAN SANGAT KETAT:
        1. ABAIKAN tabel/topik penyakit lain (Gigi, Kusta, TBC, Gizi, KIA, Kematian Bayi, AKB, AKI).
        2. ABAIKAN tabel yang HANYA berisi Persentase (%), Rate, CFR, API, IR, atau Daftar Isi.
        3. HANYA ambil JUMLAH KASUS ABSOLUT penderita/pasien.
        4. Bukti WAJIB menyertakan kutipan teks asli beserta nomor baris [nomor_baris].
        
        Format Output WAJIB JSON Array of Objects (atau [] jika tidak ada data valid):
        [
            {{
                "provinsi": "Sulawesi Selatan",
                "indikator": "Kasus Diare Dilayani",
                "jumlah": 146958,
                "bukti": "[1996] Tahun 2019 perkiraan diare sebanyak 236.099 kasus, adapun diare yang ditangani sebanyak 146.958kasus (62.24%).",
                "baris_md": 1996
            }}
        ]
        
        TEKS SUMBER:
        {context_text}
        """
        
        local_data = []
        try:
            response = client.chat.completions.create(
                model="gpt-5.4-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_completion_tokens=4096
            )
            raw_json = response.choices[0].message.content.strip()
            if raw_json.startswith('```json'):
                raw_json = raw_json[7:-3]
            elif raw_json.startswith('```'):
                raw_json = raw_json[3:-3]
                
            res = json.loads(raw_json.strip())
            
            if isinstance(res, list):
                for item in res:
                    if item.get("jumlah") is not None:
                        bukti = str(item.get("bukti", "")).lower()
                        indikator = str(item.get("indikator", "")).lower()
                        
                        # HARD FILTER: Drop rows quoting dental, leprosy, mortality causes, etc.
                        bad_words = [
                            "gigi", "kusta", "tbc", "gizi", "ibu hamil", "sasaran program",
                            "kematian bayi", "akb", "akba", "aki", "kematian ibu", "kematian balita",
                            "penyebab kematian", "penyebab angka kematian", "grafik : 5.", "grafik 5.",
                            "daftar isi", "table of content"
                        ]
                        if any(bad_word in bukti for bad_word in bad_words):
                            continue
                            
                        nilai_str = str(item.get('jumlah')).replace(',','').replace('.','')
                        try:
                            nilai = int(nilai_str)
                        except ValueError:
                            continue
                            
                        if nilai == 0:
                            continue
                            
                        if "tidak ditemukan" in bukti or "daftar isi" in bukti:
                            continue
                            
                        # Ensure the integer exists in the citation text
                        matches = re.finditer(r'([\d\.,]+)\s*(%?)', bukti)
                        found_valid_number = False
                        for m in matches:
                            num_str = m.group(1)
                            is_percent = m.group(2) == '%'
                            if is_percent:
                                continue
                            clean_num = num_str.replace('.', '').replace(',', '')
                            try:
                                if int(clean_num) == nilai:
                                    found_valid_number = True
                                    break
                            except Exception:
                                pass
                                
                        if not found_valid_number:
                            continue
                            
                        local_data.append({
                            'tahun': int(tahun),
                            'provinsi': item.get('provinsi'),
                            'kabupaten_kota': 'Total Provinsi',
                            'indikator': item.get('indikator'),
                            'nilai': nilai,
                            'baris_md': item.get('baris_md', row['start_baris']),
                            'sumber_kutipan': item.get('bukti', ''),
                            'sumber_file': row['sumber_file']
                        })
        except Exception as e:
            pass
        return local_data

    tasks = []
    for tahun, group in df_raw.groupby('tahun'):
        for idx, row in group.iterrows():
            tasks.append((idx, row, tahun))
            
    print(f"Memulai pemrosesan {len(tasks)} chunk secara paralel...")
    
    with ThreadPoolExecutor(max_workers=15) as executor:
        future_to_chunk = {executor.submit(process_chunk, t[0], t[1], t[2]): t for t in tasks}
        for future in as_completed(future_to_chunk):
            res = future.result()
            if res:
                aggregated_data.extend(res)
                
    if aggregated_data:
        df_national = pd.DataFrame(aggregated_data)
        
        # Load V3 (Provincial profile clean data) if exists
        if os.path.exists(OUT_V3):
            df_v3 = pd.read_csv(OUT_V3)
            # Combine V3 provincial data with National MD data
            df_merged = pd.concat([df_v3, df_national], ignore_index=True)
            df_merged = df_merged.drop_duplicates(subset=['tahun', 'provinsi', 'kabupaten_kota', 'indikator', 'nilai'], keep='first')
            df_merged = df_merged.sort_values(by=['tahun', 'provinsi', 'kabupaten_kota'])
            
            df_merged.to_csv(OUT_V3, index=False)
            df_merged.to_csv(OUT_V2, index=False)
            print(f"\n[SUKSES] Data gabungan MD Provinsi + MD Nasional disimpan ke V3 & V2 (Total: {len(df_merged)} baris)")
        else:
            df_national.to_csv(OUT_V3, index=False)
            df_national.to_csv(OUT_V2, index=False)
            print(f"\n[SUKSES] Data MD Nasional disimpan ke V3 & V2 (Total: {len(df_national)} baris)")
    else:
        print("\n[!] Tidak ada data tambahan diekstrak dari dokumen nasional MD.")

if __name__ == "__main__":
    df_raw = extract_paragraphs_to_memory()
    if not df_raw.empty:
        run_llm_validation(df_raw)
