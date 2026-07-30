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

RAW_DIR = "data/raw/profil kesehatan provinsi_kemenkes"
OUT_PROCESSED = "data/processed/sulawesi_kesehatan_detail_2014_2024_v2.bak.csv"

KEYWORDS = ["diare", "ispa", "pneumonia", "dbd", "dengue", "malaria"]

def extract_metadata(filename):
    # Cari tahun
    match_year = re.search(r'20\d{2}', filename)
    tahun = match_year.group(0) if match_year else "Unknown"
    
    # Cari provinsi
    lower_fname = filename.lower()
    if 'gorontalo' in lower_fname: prov = "Gorontalo"
    elif 'sulsel' in lower_fname or 'selatan' in lower_fname: prov = "Sulawesi Selatan"
    elif 'sulteng' in lower_fname or 'tengah' in lower_fname: prov = "Sulawesi Tengah"
    elif 'sultra' in lower_fname or 'tenggara' in lower_fname: prov = "Sulawesi Tenggara"
    elif 'sulut' in lower_fname or 'utara' in lower_fname: prov = "Sulawesi Utara"
    elif 'sulbar' in lower_fname or 'barat' in lower_fname: prov = "Sulawesi Barat"
    else: prov = "Sulawesi (Lainnya)"
        
    return tahun, prov

def extract_paragraphs_to_memory():
    print("=== TAHAP 1: EKSTRAKSI CHUNK DARI PROFIL PROVINSI ===")
    extracted_data = []
    
    # Path to directory
    md_files = []
    search_path = os.path.join("../../", RAW_DIR, "**", "*.md")
    md_files = glob.glob(search_path, recursive=True)
    
    if not md_files:
        search_path = os.path.join(RAW_DIR, "**", "*.md")
        md_files = glob.glob(search_path, recursive=True)
        
    for filepath in md_files:
        filename = os.path.basename(filepath)
        tahun, provinsi = extract_metadata(filename)
        print(f"Membaca {filename} (Tahun: {tahun}, Prov: {provinsi})...")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding='latin-1') as f:
                lines = f.readlines()
                
        # Konteks masif: 2000 baris per chunk, 200 overlap
        chunk_size = 2000
        overlap = 200
        
        i = 0
        while i < len(lines):
            end = min(i + chunk_size, len(lines))
            chunk_lines = lines[i:end]
            chunk_text = "\n".join(chunk_lines).lower()
            
            # Karena ini profil provinsi, kita cek saja apakah ada kata kunci penyakit
            if any(kw in chunk_text for kw in KEYWORDS):
                context_lines = []
                for j in range(i, end):
                    if lines[j].strip():
                        context_lines.append(f"[{j+1}] {lines[j].strip()}")
                        
                if context_lines:
                    extracted_data.append({
                        "tahun": tahun,
                        "provinsi": provinsi,
                        "kalimat_asli": "\n".join(context_lines),
                        "start_baris": i + 1,
                        "sumber_file": filename
                    })
            
            i += (chunk_size - overlap)
                    
    df_raw = pd.DataFrame(extracted_data)
    if not df_raw.empty:
        print(f"-> Selesai: {len(df_raw)} chunk masif relevan ditemukan untuk diproses GPT-5.4-mini.")
    return df_raw

def process_chunk(idx, row):
    context_text = row['kalimat_asli']
    tahun = row['tahun']
    prov = row['provinsi']
    
    prompt = f"""
    Anda adalah Data Scientist Senior sekaligus Auditor Medis yang sangat teliti.
    Ini adalah potongan besar dokumen 'Profil Kesehatan Provinsi {prov} Tahun {tahun}'.
    
    Tugas Anda HANYA mengekstrak JUMLAH KASUS secara detail (level Provinsi / Kabupaten / Kota) untuk 4 indikator penyakit ini SAJA:
    1. Diare (atau Kasus Diare Dilayani / Diare Ditemukan)
    2. ISPA (atau Pneumonia)
    3. DBD (Demam Berdarah Dengue / Dengue Hemorrhagic Fever)
    4. Malaria (Malaria Positif)
    
    Setiap baris teks diawali dengan nomor baris sumbernya misalnya [1540].
    
    ATURAN SANGAT KETAT (WAJIB DIPATUHI):
    1. JANGAN PERNAH mengambil angka dari tabel penyakit/topik lain (misal: Kesehatan Gigi, Kusta, TBC, Gizi, KIA, dll) lalu menganggapnya sebagai Diare/ISPA/DBD/Malaria. Jika tabelnya tentang Gigi, abaikan!
    2. JANGAN PERNAH mengambil angka dari Daftar Isi (Table of Contents) atau Narasi kosong. Harus berupa angka real dari laporan/tabel riil.
    3. JIKA di dalam potongan teks ini TIDAK ADA tabel atau narasi angka aktual yang SECARA EKSPLISIT membahas Diare, ISPA, Pneumonia, DBD, atau Malaria, maka WAJIB kembalikan array kosong: []
    4. Ambil KASUS absolut (jumlah penderita/kasus), BUKAN persentase (%), rate, target, atau populasi.
    
    Format Output WAJIB JSON Array of Objects (atau [] jika tidak ada data valid):
    [
        {{
            "provinsi": "{prov}",
            "kabupaten_kota": "Nama Kabupaten (isi 'Total Provinsi' jika itu baris total)",
            "indikator": "Kasus Diare Dilayani",
            "jumlah": 1234,
            "bukti": "<Sertakan 2-3 baris lengkap yang memiliki header tabel dan angkanya untuk konteks utuh pembuktian. Ini wajib akurat>",
            "baris_md": 1540
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
            max_completion_tokens=15000
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
                    
                    # HARD FILTER: Drop rows quoting dental, leprosy, mortality causes, coverage percentages, and OCR charts (gambar/grafik)
                    bad_words = [
                        "gigi", "kusta", "tbc", "gizi", "ibu hamil", "sasaran program",
                        "kematian bayi", "akb", "akba", "aki", "kematian ibu", "kematian balita",
                        "penyebab kematian", "penyebab angka kematian",
                        "cakupan", "persentase", "persen", "cfr", "api", "proporsi", "prevalensi", "incidence rate",
                        "gambar :", "gambar", "grafik :", "grafik", "![image"
                    ]
                    if any(bad_word in bukti for bad_word in bad_words):
                        continue
                        
                    # HARD FILTER: Ensure the disease is actually mentioned in the citation!
                    is_valid = False
                    if "diare" in indikator and "diare" in bukti: is_valid = True
                    elif "ispa" in indikator or "pneumonia" in indikator:
                        if "ispa" in bukti or "pneumonia" in bukti: is_valid = True
                    elif "dbd" in indikator or "dengue" in indikator:
                        if "dbd" in bukti or "dengue" in bukti or "berdarah" in bukti: is_valid = True
                    elif "malaria" in indikator and "malaria" in bukti: is_valid = True
                    
                    if not is_valid:
                        continue
                        
                    nilai_str = str(item.get('jumlah')).replace(',','').replace('.','')
                    try:
                        nilai = int(nilai_str)
                    except ValueError:
                        continue
                        
                    if nilai == 0:
                        continue # Drop zero cases (usually means not found or hallucinated)
                        
                    if "tidak ditemukan" in bukti or "daftar isi" in bukti or "table of content" in bukti:
                        continue # Drop rows where AI explicitly admits data is not found
                        
                    # HARD FILTER 3: Number must exist as an independent integer, not a percentage!
                    # Often the AI hallucinates 426 from 42,6%.
                    # We regex all numbers from the 'bukti' text.
                    matches = re.finditer(r'([\d\.,]+)\s*(%?)', bukti)
                    found_valid_number = False
                    for m in matches:
                        num_str = m.group(1)
                        is_percent = m.group(2) == '%'
                        
                        if is_percent:
                            continue # Ignore numbers that are percentages in the text!
                            
                        # Try to parse the text number to match our target integer
                        clean_num = num_str.replace('.', '').replace(',', '')
                        try:
                            if int(clean_num) == nilai:
                                found_valid_number = True
                                break
                        except Exception:
                            pass
                            
                    if not found_valid_number:
                        continue # AI hallucinated a number not in the text, or derived it from a percentage!
                        
                    local_data.append({
                        'tahun': int(tahun),
                        'provinsi': item.get('provinsi', prov),
                        'kabupaten_kota': item.get('kabupaten_kota', 'Tidak Diketahui'),
                        'indikator': item.get('indikator'),
                        'nilai': nilai,
                        'baris_md': item.get('baris_md'),
                        'sumber_kutipan': item.get('bukti', ''),
                        'sumber_file': row['sumber_file']
                    })
    except Exception as e:
        print(f"Error pada chunk baris {row['start_baris']} di {row['sumber_file']}: {str(e)}")
    return local_data

def run_llm_validation(df_raw):
    print("\n=== TAHAP 2: PARSING GPT-5.4-MINI ===")
    if df_raw.empty:
        print("Data paragraf kosong. Proses dihentikan.")
        return
        
    aggregated_data = []
    tasks = []
    
    for idx, row in df_raw.iterrows():
        tasks.append((idx, row))
            
    print(f"Memulai pemrosesan {len(tasks)} chunk berukuran raksasa secara paralel...")
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_chunk = {executor.submit(process_chunk, t[0], t[1]): t for t in tasks}
        for future in as_completed(future_to_chunk):
            res = future.result()
            if res:
                aggregated_data.extend(res)
                
    if aggregated_data:
        df_out = pd.DataFrame(aggregated_data)
        df_out = df_out.sort_values(by='baris_md').drop_duplicates(subset=['tahun', 'provinsi', 'kabupaten_kota', 'indikator', 'nilai'], keep='first')
        
        out_v2 = os.path.abspath("data/processed/sulawesi_kesehatan_detail_2014_2024_v2.csv")
        os.makedirs(os.path.dirname(out_v2), exist_ok=True)
        df_out.to_csv(out_v2, index=False)
        print(f"\n[SUKSES] Data murni V8 berhasil disimpan ke: {out_v2} (Total: {len(df_out)} baris)")
    else:
        print("\n[!] Tidak ada data berhasil diekstrak.")

if __name__ == "__main__":
    df_raw = extract_paragraphs_to_memory()
    run_llm_validation(df_raw)
