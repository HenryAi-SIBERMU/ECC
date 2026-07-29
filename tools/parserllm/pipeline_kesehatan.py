import os
import glob
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import json
import re

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

RAW_DIR = "data/raw/profil kesehatan_kemenkes"
OUT_RAW = "data/raw/bps_kemenkesispadiaremalaria/kesehatan_raw_extracted.csv"
OUT_PROCESSED = "data/processed/sulawesi_kesehatan_detail_2014_2024_v2.csv"

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
    Step 1: Extract relevant chunks from Markdown files
    """
    print("=== TAHAP 1: EKSTRAKSI CHUNK DARI MARKDOWN ===")
    extracted_data = []
    
    # Path to the directory where kemenkes national md files are
    md_files = glob.glob(os.path.join("../../", RAW_DIR, "*.md"))
    
    if not md_files:
        # Fallback if run from root
        md_files = glob.glob(os.path.join(RAW_DIR, "*.md"))
        
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
                
        # Chunking: 50 lines per chunk, 20 lines overlap
        chunk_size = 60
        overlap = 20
        
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
    if not df_raw.empty:
        # Save relative to root
        out_raw_path = os.path.join("../../", OUT_RAW) if os.path.exists("../../data") else OUT_RAW
        os.makedirs(os.path.dirname(out_raw_path), exist_ok=True)
        df_raw.to_csv(out_raw_path, index=False)
        print(f"-> Selesai: {len(df_raw)} chunk relevan ditemukan dan dibackup.")
    
    return df_raw

def run_llm_validation(df_raw):
    """
    Step 2: Parse extracted chunks using GPT-4o
    """
    print("\n=== TAHAP 2: PARSING GPT-4O ===")
    if df_raw.empty:
        print("Data paragraf kosong. Proses dihentikan.")
        return
        
    aggregated_data = []
    
    # Kelompokkan by tahun
    grouped = df_raw.groupby('tahun')
    
    for tahun, group in grouped:
        print(f"Menganalisis chunk untuk tahun {tahun} (Total: {len(group)} chunk)...")
        
        for idx, row in group.iterrows():
            context_text = row['kalimat_asli']
            
            prompt = f"""
            Anda adalah Data Scientist Senior.
            Ekstrak JUMLAH KASUS dari potongan tabel 'Profil Kesehatan Indonesia {tahun}' berikut untuk:
            1. Diare (atau Kasus Diare Dilayani)
            2. ISPA (atau Pneumonia)
            3. DBD (Demam Berdarah Dengue / Dengue Hemorrhagic Fever)
            4. Malaria (Malaria Positif)
            
            HANYA untuk 6 Provinsi: Sulawesi Utara, Sulawesi Tengah, Sulawesi Selatan, Sulawesi Tenggara, Gorontalo, Sulawesi Barat.
            Setiap baris teks diawali dengan nomor baris sumbernya misalnya [450].
            
            ATURAN:
            - Ambil KASUS absolut (jumlah penderita/kasus), BUKAN persentase (%), rate per 10.000, target, atau jumlah penduduk.
            - Jika nilai tidak ada/tdk relevan, abaikan.
            
            Format Output WAJIB JSON Array of Objects:
            [
                {{
                    "provinsi": "Sulawesi Tengah",
                    "indikator": "Kasus Diare Dilayani",
                    "jumlah": 12345,
                    "bukti": "<satu kalimat/baris tabel utuh dari teks>",
                    "baris_md": 450
                }}
            ]
            
            TEKS SUMBER:
            {context_text}
            """
            
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0,
                    max_tokens=800
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
                            aggregated_data.append({
                                'tahun': int(tahun),
                                'provinsi': item.get('provinsi'),
                                'indikator': item.get('indikator'),
                                'nilai': int(str(item.get('jumlah')).replace(',','').replace('.','')),
                                'baris_md': item.get('baris_md'),
                                'sumber_kutipan': item.get('bukti', ''),
                                'sumber_file': row['sumber_file']
                            })
                            
            except Exception as e:
                pass 
                
    if aggregated_data:
        df_out = pd.DataFrame(aggregated_data)
        df_out = df_out.sort_values(by='baris_md').drop_duplicates(subset=['tahun', 'provinsi', 'indikator', 'nilai'], keep='first')
        
        out_processed_path = os.path.join("../../", OUT_PROCESSED) if os.path.exists("../../data") else OUT_PROCESSED
        df_out.to_csv(out_processed_path, index=False)
        print(f"\n[SUKSES] Data hasil LLM parser berhasil disimpan ke: {out_processed_path} (Total: {len(df_out)} baris)")
    else:
        print("\n[!] Tidak ada data berhasil diekstrak.")

if __name__ == "__main__":
    df_raw = extract_paragraphs_to_memory()
    run_llm_validation(df_raw)
