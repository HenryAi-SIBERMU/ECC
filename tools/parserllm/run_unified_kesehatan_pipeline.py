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

RAW_PROV_DIR = "data/raw/profil kesehatan provinsi_kemenkes"
RAW_NAT_DIR = "data/raw/profil kesehatan_kemenkes"
OUT_V2 = "data/processed/sulawesi_kesehatan_detail_2014_2024_v2.csv"

PROVINCES = [
    "Sulawesi Utara", "Sulawesi Tengah", "Sulawesi Selatan", 
    "Sulawesi Tenggara", "Gorontalo", "Sulawesi Barat"
]

KEYWORDS = ["diare", "ispa", "pneumonia", "dbd", "dengue", "malaria"]

BAD_WORDS = [
    "gigi", "kusta", "tbc", "gizi", "ibu hamil", "sasaran program",
    "kematian bayi", "akb", "akba", "aki", "kematian ibu", "kematian balita",
    "penyebab kematian", "penyebab angka kematian",
    "cakupan", "persentase", "persen", "cfr", "api", "proporsi", "prevalensi", "incidence rate",
    "gambar :", "gambar", "grafik :", "grafik", "![image", "daftar isi", "table of content"
]

def extract_year_and_prov(filename):
    match_year = re.search(r'20\d{2}', filename)
    tahun = match_year.group(0) if match_year else "Unknown"
    
    lower_fname = filename.lower()
    if 'gorontalo' in lower_fname: prov = "Gorontalo"
    elif 'sulsel' in lower_fname or 'selatan' in lower_fname: prov = "Sulawesi Selatan"
    elif 'sulteng' in lower_fname or 'tengah' in lower_fname: prov = "Sulawesi Tengah"
    elif 'sultra' in lower_fname or 'tenggara' in lower_fname: prov = "Sulawesi Tenggara"
    elif 'sulut' in lower_fname or 'utara' in lower_fname: prov = "Sulawesi Utara"
    elif 'sulbar' in lower_fname or 'barat' in lower_fname: prov = "Sulawesi Barat"
    else: prov = "Sulawesi (Lainnya)"
        
    return tahun, prov

def is_valid_citation(indikator, bukti, context_text):
    bukti_lower = bukti.lower()
    context_lower = context_text.lower()
    ind_lower = indikator.lower()
    
    if any(bw in bukti_lower for bw in BAD_WORDS):
        return False
        
    is_valid = False
    if "diare" in ind_lower and "diare" in context_lower: is_valid = True
    elif "ispa" in ind_lower or "pneumonia" in ind_lower:
        if "ispa" in context_lower or "pneumonia" in context_lower: is_valid = True
    elif "dbd" in ind_lower or "dengue" in ind_lower:
        if "dbd" in context_lower or "dengue" in context_lower or "berdarah" in context_lower: is_valid = True
    elif "malaria" in ind_lower and "malaria" in context_lower: is_valid = True
    
    return is_valid

def parse_md_files(md_dir, is_provincial=True):
    search_path = os.path.join(md_dir, "**", "*.md")
    md_files = glob.glob(search_path, recursive=True)
    
    if not md_files:
        search_path = os.path.join("../../", md_dir, "**", "*.md")
        md_files = glob.glob(search_path, recursive=True)
        
    print(f"\n=== PROSES PAKAI GPT-5.4-MINI V9: {md_dir} ({len(md_files)} file) ===")
    
    chunks = []
    for filepath in md_files:
        filename = os.path.basename(filepath)
        match_year = re.search(r'20\d{2}', filename)
        tahun = match_year.group(0) if match_year else "Unknown"
        
        _, prov_detected = extract_year_and_prov(filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f: lines = f.readlines()
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding='latin-1') as f: lines = f.readlines()
            
        chunk_size = 1500
        overlap = 200
        i = 0
        while i < len(lines):
            end = min(i + chunk_size, len(lines))
            chunk_lines = lines[i:end]
            chunk_text = "\n".join(chunk_lines).lower()
            
            has_prov = any(prov.lower() in chunk_text for prov in PROVINCES) if not is_provincial else True
            has_kw = any(kw in chunk_text for kw in KEYWORDS)
            
            if has_prov and has_kw:
                context_lines = [f"[{j+1}] {lines[j].strip()}" for j in range(i, end) if lines[j].strip()]
                if context_lines:
                    chunks.append({
                        "tahun": tahun,
                        "provinsi_default": prov_detected if is_provincial else "Sulawesi",
                        "kalimat_asli": "\n".join(context_lines),
                        "start_baris": i + 1,
                        "sumber_file": filename
                    })
            i += (chunk_size - overlap)
            
    print(f"-> {len(chunks)} chunk masif siap diproses LLM parser.")
    
    extracted_records = []
    
    def process_one_chunk(c):
        context_text = c['kalimat_asli']
        tahun = c['tahun']
        sumber_file = c['sumber_file']
        
        prompt = f"""
        Anda adalah Data Scientist Senior sekaligus Auditor Medis yang sangat teliti.
        Ini adalah potongan dokumen 'Profil Kesehatan {sumber_file} Tahun {tahun}'.
        
        Tugas Anda HANYA mengekstrak JUMLAH KASUS (tingkat 6 Provinsi Sulawesi: Sulawesi Utara, Sulawesi Tengah, Sulawesi Selatan, Sulawesi Tenggara, Gorontalo, Sulawesi Barat) untuk 4 indikator penyakit ini SAJA:
        1. Diare (atau Kasus Diare Dilayani / Diare Ditemukan)
        2. ISPA (atau Pneumonia)
        3. DBD (Demam Berdarah Dengue)
        4. Malaria (Malaria Positif)
        
        ATURAN KETAT V9:
        1. JANGAN PERNAH mengekstrak angka dari Gambar / Grafik / Chart OCR (misal 'Gambar 6.12', '![image]'). ABAIKAN!
        2. JANGAN PERNAH mengambil angka dari Tabel Cakupan (Coverage %), Persentase (%), Rate, CFR, API, Kematian Bayi (AKB), Kusta, Gigi, TBC.
        3. HANYA ambil JUMLAH KASUS ABSOLUT penderita dari TABEL DATA UTUH atau NARASI TEKS RESMI.
        4. Wajib menyertakan kutipan teks asli dengan tag baris [nomor_baris].
        
        Format Output WAJIB JSON Array of Objects (atau [] jika tidak ada data valid):
        [
            {{
                "provinsi": "Gorontalo",
                "kabupaten_kota": "Total Provinsi",
                "indikator": "Kasus Diare Dilayani",
                "jumlah": 19118,
                "bukti": "[3685] |JUMLAH (KAB/KOTA)| |95|1,245,978|33,641|19,118|...",
                "baris_md": 3685
            }}
        ]
        
        TEKS SUMBER:
        {context_text}
        """
        
        out_list = []
        try:
            response = client.chat.completions.create(
                model="gpt-5.4-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_completion_tokens=4096
            )
            raw = response.choices[0].message.content.strip()
            if raw.startswith('```json'): raw = raw[7:-3]
            elif raw.startswith('```'): raw = raw[3:-3]
            
            res = json.loads(raw.strip())
            if isinstance(res, list):
                for item in res:
                    if item.get("jumlah") is not None:
                        bukti = str(item.get("bukti", ""))
                        indikator = str(item.get("indikator", ""))
                        
                        if not is_valid_citation(indikator, bukti, context_text):
                            continue
                            
                        nilai_str = str(item.get('jumlah')).replace(',','').replace('.','')
                        try: nilai = int(nilai_str)
                        except ValueError: continue
                        
                        if nilai == 0: continue
                        
                        # Number match check
                        matches = re.finditer(r'([\d\.,]+)\s*(%?)', bukti)
                        valid_num = False
                        for m in matches:
                            if m.group(2) == '%': continue
                            num_clean = m.group(1).replace('.', '').replace(',', '')
                            try:
                                if int(num_clean) == nilai:
                                    valid_num = True
                                    break
                            except Exception: pass
                            
                        if not valid_num: continue
                        
                        prov_out = item.get('provinsi', c['provinsi_default'])
                        if not any(p.lower() in prov_out.lower() for p in PROVINCES):
                            continue
                            
                        out_list.append({
                            'tahun': int(tahun),
                            'provinsi': prov_out,
                            'kabupaten_kota': item.get('kabupaten_kota', 'Total Provinsi'),
                            'indikator': item.get('indikator'),
                            'nilai': nilai,
                            'baris_md': item.get('baris_md', c['start_baris']),
                            'sumber_kutipan': bukti,
                            'sumber_file': sumber_file
                        })
        except Exception as e: pass
        return out_list

    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = [executor.submit(process_one_chunk, c) for c in chunks]
        for f in as_completed(futures):
            res = f.result()
            if res:
                extracted_records.extend(res)
                
    return pd.DataFrame(extracted_records)

def main():
    # 1. Parse Provincial Profile MDs (Priority 1)
    df_prov = parse_md_files(RAW_PROV_DIR, is_provincial=True)
    print(f"\n-> Extracted {len(df_prov)} clean rows from Provincial Profiles.")
    
    # 2. Parse National Profile MDs (Priority 2 - Gap Filling)
    df_nat = parse_md_files(RAW_NAT_DIR, is_provincial=False)
    print(f"\n-> Extracted {len(df_nat)} clean rows from National Profiles.")
    
    # Combine both datasets with deduplication prioritizing provincial profiles
    if not df_prov.empty and not df_nat.empty:
        df_combined = pd.concat([df_prov, df_nat], ignore_index=True)
    elif not df_prov.empty:
        df_combined = df_prov
    else:
        df_combined = df_nat
        
    if not df_combined.empty:
        df_combined = df_combined.sort_values(by=['tahun', 'provinsi', 'kabupaten_kota']).drop_duplicates(
            subset=['tahun', 'provinsi', 'kabupaten_kota', 'indikator', 'nilai'], keep='first'
        )
        
        out_v2_path = os.path.abspath(OUT_V2)
        os.makedirs(os.path.dirname(out_v2_path), exist_ok=True)
        try:
            df_combined.to_csv(out_v2_path, index=False)
            print(f"\n[SUKSES LENGKAP V9] Data gabungan bersih disimpan KE HANYA {out_v2_path} (Total: {len(df_combined)} baris)")
        except PermissionError:
            out_alt_path = os.path.abspath("data/processed/sulawesi_kesehatan_detail_2014_2024_v2_new.csv")
            df_combined.to_csv(out_alt_path, index=False)
            print(f"\n[PERINGATAN] File v2.csv sedang dibuka di Excel. Data berhasil disimpan ke: {out_alt_path} (Total: {len(df_combined)} baris)")
    else:
        print("\n[!] Tidak ada data berhasil diekstrak.")

if __name__ == "__main__":
    main()
