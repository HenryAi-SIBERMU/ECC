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

RAW_DIR = r"data/raw/profil kesehatan_nasional_kemenkes"
OUT_PROCESSED = r"data/processed/sulawesi_faskes_agregat_v2.csv"
PROVINCES = ["Gorontalo", "Sulawesi Tengah", "Sulawesi Tenggara", "Sulawesi Selatan", "Sulawesi Utara", "Sulawesi Barat"]

def is_proxy_row(row):
    kutipan = str(row['sumber_kutipan']).strip().lower()
    if kutipan.startswith("berdasarkan tabel") or "tabel x" in kutipan:
        return True
    return False

def extract_chunks_from_md(filepath):
    chunks = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f: lines = f.readlines()
    except:
        with open(filepath, 'r', encoding='latin-1') as f: lines = f.readlines()
            
    chunk_size = 1500
    overlap = 200
    i = 0
    while i < len(lines):
        end = min(i + chunk_size, len(lines))
        chunk_lines = lines[i:end]
        chunk_text = "\n".join(chunk_lines).lower()
        
        has_prov = any(prov.lower() in chunk_text for prov in PROVINCES)
        has_kw = "puskesmas" in chunk_text or "rumah sakit" in chunk_text
        
        if has_prov and has_kw:
            context_lines = [f"[{j+1}] {lines[j].strip()}" for j in range(i, end) if lines[j].strip()]
            if context_lines:
                chunks.append({
                    "kalimat_asli": "\n".join(context_lines),
                    "start_baris": i + 1,
                    "sumber_file": os.path.basename(filepath)
                })
        i += (chunk_size - overlap)
    return chunks

def process_year(tahun, missing_combos):
    md_file = os.path.join(RAW_DIR, f"profil-kesehatan-indonesia-{tahun}.md")
    if not os.path.exists(md_file):
        # try without strict name
        possible_files = glob.glob(os.path.join(RAW_DIR, f"*{tahun}*.md"))
        if not possible_files: return []
        md_file = possible_files[0]
        
    print(f"Mengekstrak {tahun} dari {os.path.basename(md_file)}...")
    chunks = extract_chunks_from_md(md_file)
    extracted = []
    
    def analyze_chunk(chunk):
        context_text = chunk['kalimat_asli']
        missing_str = ", ".join([f"{p} ({j})" for p, j in missing_combos])
        prompt = f"""Anda adalah Data Scientist Senior.
Tugas: Temukan angka TOTAL JUMLAH PUSKESMAS dan TOTAL JUMLAH RUMAH SAKIT untuk provinsi yang datanya KOSONG berikut ini:
{missing_str}

ATURAN KETAT:
1. JANGAN mengambil angka persentase, rasio, atau jumlah kabupaten/kota. Hanya ambil angka JUMLAH ABSOLUT FASKES.
2. JANGAN ambil angka untuk Puskesmas Pembantu (Pustu).
3. SUMBER KUTIPAN SANGAT PENTING: Anda WAJIB menyalin teks asli beserta nomor barisnya (contoh: "[Baris 150] Sulawesi Selatan | 460 | ...") sebagai bukti forensik. Jangan pernah menjawab "Berdasarkan Tabel X". Kutipan harus berupa kalimat aktual atau potongan baris tabel aktual di mana angka tersebut berada.
4. Jika di dalam teks tidak ada tabel/kalimat yang menunjukkan angka absolut faskes untuk provinsi tersebut, kembalikan array kosong [].

Format JSON (WAJIB array):
[
  {{"provinsi": "Sulawesi Selatan", "jenis": "Puskesmas", "jumlah": 460, "baris_md": 150, "sumber_kutipan": "[149] Tabel 4.1 Jumlah Puskesmas\\n[150] Sulawesi Selatan | 460 | 120"}}
]

TEKS SUMBER (Profil Kesehatan Nasional {tahun}):
{context_text}"""
        try:
            res = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0, max_tokens=2000
            )
            raw = res.choices[0].message.content.strip()
            if raw.startswith('```json'): raw = raw[7:-3]
            elif raw.startswith('```'): raw = raw[3:-3]
            data = json.loads(raw)
            # filter only the ones we requested
            valid_res = []
            for d in data:
                prov = d.get('provinsi')
                jns = d.get('jenis')
                if (prov, jns) in missing_combos:
                    valid_res.append(d)
            return valid_res
        except Exception as e:
            return []

    with ThreadPoolExecutor(max_workers=10) as executor:
        for res in executor.map(analyze_chunk, chunks):
            if res: extracted.extend(res)
            
    # deduplicate
    final_for_year = []
    seen = set()
    for item in extracted:
        key = (item['provinsi'], item['jenis'])
        if key not in seen and item.get('jumlah') is not None:
            seen.add(key)
            item['tahun'] = tahun
            final_for_year.append(item)
    return final_for_year

def main():
    print("Membaca base data...")
    df = pd.read_csv(OUT_PROCESSED)
    
    # 1. Separate valid vs proxy
    valid_mask = ~df.apply(is_proxy_row, axis=1)
    df_valid = df[valid_mask].copy()
    print(f"Data valid provinsi: {len(df_valid)} baris. (Membuang {len(df) - len(df_valid)} baris proxy lama)")
    
    # 2. Find missing combinations per year (2014-2024)
    existing = set(zip(df_valid['tahun'].astype(int), df_valid['provinsi'], df_valid['jenis']))
    
    years = range(2014, 2025)
    jenis_faskes = ["Puskesmas", "Rumah Sakit"]
    missing_dict = {y: [] for y in years}
    
    for y in years:
        for p in PROVINCES:
            for j in jenis_faskes:
                if (y, p, j) not in existing:
                    missing_dict[y].append((p, j))
                    
    # 3. Process missing data from National PDFs
    new_records = []
    for y, combos in missing_dict.items():
        if combos:
            print(f"\nTahun {y}: {len(combos)} kombinasi kosong.")
            res = process_year(y, combos)
            new_records.extend(res)
            
    if new_records:
        df_new = pd.DataFrame(new_records)
        df_final = pd.concat([df_valid, df_new], ignore_index=True)
        df_final = df_final.sort_values(by=['provinsi', 'tahun', 'jenis']).reset_index(drop=True)
        df_final.to_csv(OUT_PROCESSED, index=False)
        print(f"\nBerhasil menambahkan {len(df_new)} baris proxy dengan kutipan forensik.")
    else:
        df_valid = df_valid.sort_values(by=['provinsi', 'tahun', 'jenis']).reset_index(drop=True)
        df_valid.to_csv(OUT_PROCESSED, index=False)
        print("\nTidak ada proxy yang berhasil ditemukan (misal 2024 kosong tabel absolut).")

if __name__ == "__main__":
    main()
