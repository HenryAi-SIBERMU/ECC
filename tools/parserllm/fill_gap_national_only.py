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

BASE_CSV = "data/processed/sulawesi_kesehatan_detail_2014_2024_v2.bak.csv"
RAW_NAT_DIR = "data/raw/profil kesehatan_kemenkes"
OUT_V2 = "data/processed/sulawesi_kesehatan_detail_2014_2024_v2.csv"

PROVINCES_KEYWORDS = [
    "sulawesi utara", "sulut", 
    "sulawesi tengah", "sulteng", 
    "sulawesi selatan", "sulsel", 
    "sulawesi tenggara", "sultra", 
    "gorontalo", 
    "sulawesi barat", "sulbar"
]

KEYWORDS = ["diare", "ispa", "pneumonia", "dbd", "dengue", "malaria", "kusta"]

BAD_WORDS = [
    "gigi", "tbc", "gizi", "ibu hamil", "sasaran program",
    "kematian bayi", "akb", "akba", "aki", "kematian ibu", "kematian balita",
    "penyebab kematian", "penyebab angka kematian",
    "gambar :", "gambar", "grafik :", "grafik", "![image", "daftar isi", "table of content"
]

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
    elif "kusta" in ind_lower and "kusta" in context_lower: is_valid = True
    
    return is_valid

def parse_national_gap():
    search_path = os.path.join(RAW_NAT_DIR, "**", "*.md")
    md_files = glob.glob(search_path, recursive=True)
    
    print(f"\n=== PARSING PARALEL GPT-5.4-MINI V9: {RAW_NAT_DIR} ({len(md_files)} file) ===")
    
    chunks = []
    for filepath in md_files:
        filename = os.path.basename(filepath)
        match_year = re.search(r'20\d{2}', filename)
        tahun = match_year.group(0) if match_year else "Unknown"
        
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
            
            has_prov = any(prov in chunk_text for prov in PROVINCES_KEYWORDS)
            has_kw = any(kw in chunk_text for kw in KEYWORDS)
            
            if has_prov and has_kw:
                context_lines = [f"[{j+1}] {lines[j].strip()}" for j in range(i, end) if lines[j].strip()]
                if context_lines:
                    chunks.append({
                        "tahun": tahun,
                        "kalimat_asli": "\n".join(context_lines),
                        "start_baris": i + 1,
                        "sumber_file": filename
                    })
            i += (chunk_size - overlap)
            
    print(f"-> {len(chunks)} chunk relevan ditemukan untuk diekstrak.")
    
    extracted_records = []
    
    def process_one_chunk(c):
        context_text = c['kalimat_asli']
        tahun = c['tahun']
        sumber_file = c['sumber_file']
        
        prompt = f"""
        Anda adalah Data Scientist Senior & Auditor Medis.
        Ini adalah potongan dokumen 'Profil Kesehatan Indonesia {sumber_file} Tahun {tahun}'.
        
        Tugas Anda HANYA mengekstrak JUMLAH KASUS ABSOLUT (tingkat 6 Provinsi Sulawesi: Sulawesi Utara, Sulawesi Tengah, Sulawesi Selatan, Sulawesi Tenggara, Gorontalo, Sulawesi Barat) untuk 5 indikator penyakit ini:
        1. Diare (Kasus Diare Dilayani)
        2. ISPA / Pneumonia (Penemuan Pneumonia Balita)
        3. DBD (Demam Berdarah Dengue)
        4. Malaria (Malaria Positif)
        5. Kusta (Kasus Kusta Baru)
        
        ATURAN PENTING:
        1. DILARANG KERAS MENGAMBIL ANGKA PECAHAN (KOMA) ATAU PERSENTASE. Jika data memiliki koma (seperti 22,3), itu adalah Cakupan/Persentase. JANGAN diambil!
        2. Cari data untuk 6 provinsi (Sulawesi Utara, Tengah, Selatan, Tenggara, Barat, Gorontalo). Nama provinsi bisa saja disingkat (Sulut, Sulteng, Sulsel, Sultra, Sulbar).
        3. DILARANG AMBIL DARI GAMBAR / GRAFIK / CHART OCR ('Gambar :', '![image]', 'CAKUPAN', 'PERSENTASE'). DIBUANG!
        4. BUKTI FORENSIK (SANGAT PENTING): Anda WAJIB menyertakan 'judul_tabel'.
           Dan untuk 'bukti', salin KONTEKS TEKS YANG LUAS (minimal 3-4 baris di atas dan di bawah angka tersebut) agar pengguna dapat melakukan audit forensik dengan jelas. Jangan dipotong-potong jadi sangat singkat!
        
        Format JSON:
        [
            {{
                "provinsi": "Sulawesi Selatan",
                "kabupaten_kota": "Total Provinsi",
                "indikator": "Penemuan Pneumonia Balita",
                "jumlah": 99999,
                "judul_tabel": "Lampiran X.X JUDUL TABEL DUMMY",
                "bukti": "[997] Sulawesi Tengah 1234\n[998] Sulawesi Selatan 99999\n[999] Sulawesi Barat 5678",
                "baris_md": 998
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
                            num_str = m.group(1)
                            # In Indonesian, ',' is the decimal separator. 
                            # If it contains a comma, it is a fraction/percentage (e.g. 22,3), not an absolute count!
                            if ',' in num_str: continue
                            
                            num_clean = num_str.replace('.', '')
                            try:
                                if int(num_clean) == nilai:
                                    valid_num = True
                                    break
                            except Exception: pass
                            
                        if not valid_num: continue
                        
                        prov_out = item.get('provinsi', 'Sulawesi').lower()
                        matched_prov = None
                        if 'utara' in prov_out or 'sulut' in prov_out: matched_prov = 'Sulawesi Utara'
                        elif 'tengah' in prov_out or 'sulteng' in prov_out: matched_prov = 'Sulawesi Tengah'
                        elif 'selatan' in prov_out or 'sulsel' in prov_out: matched_prov = 'Sulawesi Selatan'
                        elif 'tenggara' in prov_out or 'sultra' in prov_out: matched_prov = 'Sulawesi Tenggara'
                        elif 'barat' in prov_out or 'sulbar' in prov_out: matched_prov = 'Sulawesi Barat'
                        elif 'gorontalo' in prov_out: matched_prov = 'Gorontalo'
                        if not matched_prov: continue
                        
                        bukti_str = item.get("bukti", "").replace('\n', ' ').strip()
                        judul = item.get("judul_tabel", "")
                        if judul and judul not in bukti_str:
                            bukti_str = f"[{judul}] {bukti_str}"
                        
                        out_list.append({
                            'tahun': int(tahun),
                            'provinsi': matched_prov,
                            'kabupaten_kota': item.get('kabupaten_kota', 'Total Provinsi'),
                            'indikator': item.get('indikator'),
                            'nilai': nilai,
                            'baris_md': item.get('baris_md', c['start_baris']),
                            'sumber_kutipan': bukti_str,
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
    base_path = os.path.abspath(BASE_CSV)
    print(f"1. Membaca data dasar murni dari: {base_path}")
    df_base = pd.read_csv(base_path)
    print(f"-> Base file v2.bak.csv memuat {len(df_base)} baris murni provinsi.")
    
    print("\n2. Ekstraksi proxy gap dari profil kesehatan nasional...")
    df_nat_gap = parse_national_gap()
    print(f"-> Berhasil mengekstrak {len(df_nat_gap)} baris gap nasional.")
    
    if not df_nat_gap.empty:
        # Combined base and gap
        df_combined = pd.concat([df_base, df_nat_gap], ignore_index=True)
        df_combined['tahun'] = pd.to_numeric(df_combined['tahun'], errors='coerce')
        df_combined = df_combined.sort_values(by=['tahun', 'provinsi', 'kabupaten_kota'], ascending=[True, True, True]).drop_duplicates(
            subset=['tahun', 'provinsi', 'kabupaten_kota', 'indikator', 'nilai'], keep='first'
        )
    else:
        df_combined = df_base
        
    out_v2_path = os.path.abspath(OUT_V2)
    try:
        df_combined.to_csv(out_v2_path, index=False)
        print(f"\n[SUKSES LENGKAP] Data v2.bak.csv + gap nasional berhasil disimpan ke: {out_v2_path} (Total: {len(df_combined)} baris)")
    except PermissionError:
        out_alt = os.path.abspath("data/processed/sulawesi_kesehatan_detail_2014_2024_v2_new.csv")
        df_combined.to_csv(out_alt, index=False)
        print(f"\n[PERINGATAN] File v2.csv sedang dibuka di Excel. Hasil disimpan ke: {out_alt}")

if __name__ == "__main__":
    main()
