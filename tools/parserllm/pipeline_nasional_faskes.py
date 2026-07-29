import os
import glob
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

RAW_DIR = r"data/raw/profil kesehatan_kemenkes"
OUT_PROCESSED = r"data/processed/sulawesi_faskes_agregat_v2.csv"
PROVINCES = ["Gorontalo", "Sulawesi Tengah", "Sulawesi Tenggara", "Sulawesi Selatan", "Sulawesi Utara", "Sulawesi Barat"]

def extract_tables_from_md(filepath):
    tables = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except:
        with open(filepath, 'r', encoding='latin-1') as f:
            lines = f.readlines()
            
    in_table = False
    current_table = []
    title_context = []
    
    for i, line in enumerate(lines):
        if line.strip().startswith('|'):
            if not in_table:
                in_table = True
                title_context = lines[max(0, i-7):i]
            current_table.append((i, line))
        else:
            if in_table:
                # Table ended
                tables.append({"title": title_context, "rows": current_table})
                in_table = False
                current_table = []
                title_context = []
    
    # Check if file ends with table
    if in_table:
        tables.append({"title": title_context, "rows": current_table})
        
    return tables

def process_national_data():
    print("=== TAHAP 1: EKSTRAKSI TABEL DARI PROFIL KESEHATAN NASIONAL ===")
    md_files = glob.glob(os.path.join(RAW_DIR, "*.md"))
    
    # Load existing data to see what we need to fill
    existing_df = pd.read_csv(OUT_PROCESSED) if os.path.exists(OUT_PROCESSED) else pd.DataFrame(columns=['tahun', 'provinsi', 'jenis', 'jumlah'])
    existing_records = set()
    for _, row in existing_df.iterrows():
        existing_records.add((str(row['tahun']), row['provinsi'], row['jenis']))
        
    new_data = []
    
    for filepath in md_files:
        filename = os.path.basename(filepath)
        import re
        match = re.search(r'20\d{2}', filename)
        if not match: continue
        tahun = match.group(0)
        
        tables = extract_tables_from_md(filepath)
        relevant_blocks = []
        
        for table in tables:
            title_text = "".join(table['title']).lower()
            # We only care about tables mentioning puskesmas or rumah sakit in title/header
            header_text = "".join([r[1] for r in table['rows'][:3]]).lower()
            full_text = title_text + header_text
            
            if "puskesmas" in full_text or "rumah sakit" in full_text:
                # filter the rows: keep headers (first 3 rows), and rows mentioning our provinces
                filtered_rows = []
                for idx, row in enumerate(table['rows']):
                    if idx < 4: 
                        filtered_rows.append(f"[Baris {row[0] + 1}] {row[1]}")
                    else:
                        row_lower = row[1].lower()
                        if any(p.lower() in row_lower for p in PROVINCES):
                            filtered_rows.append(f"[Baris {row[0] + 1}] {row[1]}")
                
                # Only keep if we actually found data for our provinces
                if len(filtered_rows) > 4:
                    block = "".join(table['title']) + "".join(filtered_rows)
                    relevant_blocks.append(block)
        
        if not relevant_blocks:
            continue
            
        print(f"Mengirim {len(relevant_blocks)} blok tabel relevan tahun {tahun} ke GPT-4o...")
        
        context_text = "\n\n=== TABEL SELANJUTNYA ===\n\n".join(relevant_blocks)
        
        prompt = f"""
        Anda adalah Data Scientist Senior di Kementerian Kesehatan.
        Tugas Anda adalah mengekstrak JUMLAH TOTAL PUSKESMAS dan JUMLAH TOTAL RUMAH SAKIT untuk 6 provinsi di Sulawesi 
        berdasarkan potongan tabel Markdown dari "Profil Kesehatan Indonesia Tahun {tahun}".
        
        Provinsi Target: Gorontalo, Sulawesi Tengah, Sulawesi Tenggara, Sulawesi Selatan, Sulawesi Utara, Sulawesi Barat.
        
        ATURAN PENTING:
        1. Anda hanya boleh mengambil angka total Puskesmas secara keseluruhan dan total Rumah Sakit secara keseluruhan.
        2. Abaikan data Puskesmas Pembantu (Pustu) atau data spesifik lainnya jika ada total utamanya.
        3. Jika data tidak ada untuk sebuah provinsi di teks, abaikan provinsi tersebut.
        4. Wajib sertakan nomor baris (baris_md) dari baris tabel tempat Anda mengambil angka tersebut.
        
        Jawab HANYA dengan JSON murni dalam bentuk list of objects, tanpa markdown formatter (```json):
        [
          {{"tahun": {tahun}, "provinsi": "Nama Provinsi", "jenis": "Puskesmas", "jumlah": <angka>, "baris_md": <angka baris tabel provinsinya>, "sumber_kutipan": "Berdasarkan Tabel X..."}},
          {{"tahun": {tahun}, "provinsi": "Nama Provinsi", "jenis": "Rumah Sakit", "jumlah": <angka>, "baris_md": <angka baris tabel provinsinya>, "sumber_kutipan": "Berdasarkan Tabel Y..."}}
        ]
        
        TEKS SUMBER (sudah disaring hanya untuk baris provinsi target):
        {context_text}
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=1500
            )
            raw_json = response.choices[0].message.content.strip()
            if raw_json.startswith('```json'): raw_json = raw_json[7:-3]
            elif raw_json.startswith('```'): raw_json = raw_json[3:-3]
                
            res = json.loads(raw_json.strip())
            
            for item in res:
                # Check if it already exists in the original data (from provincial PDFs)
                # Only add if it's missing (bolong)
                key = (str(item['tahun']), item['provinsi'], item['jenis'])
                if key not in existing_records:
                    # ensure baris_md is captured
                    baris = item.get('baris_md', '')
                    new_item = {
                        'tahun': int(item['tahun']),
                        'provinsi': item['provinsi'],
                        'jenis': item['jenis'],
                        'jumlah': int(item['jumlah']),
                        'baris_md': baris,
                        'sumber_kutipan': item.get('sumber_kutipan', '')
                    }
                    new_data.append(new_item)
                    existing_records.add(key)
                    print(f"-> [NEW GAP FILLED] {item['provinsi']} {tahun} - {item['jenis']}: {item['jumlah']} (Baris MD: {baris})")
                else:
                    print(f"-> [SKIP] {item['provinsi']} {tahun} - {item['jenis']} sudah ada dari data Provinsi.")
                    
        except Exception as e:
            print(f"Error pada GPT-4o untuk tahun {tahun}: {e}")
            
    if new_data:
        df_new = pd.DataFrame(new_data)
        # Combine with existing
        df_combined = pd.concat([existing_df, df_new], ignore_index=True)
        # Sort for neatness
        df_combined = df_combined.sort_values(by=['provinsi', 'tahun', 'jenis']).reset_index(drop=True)
        df_combined.to_csv(OUT_PROCESSED, index=False)
        print(f"\nSelesai! {len(new_data)} data baru berhasil ditambahkan untuk mengisi yang bolong di {OUT_PROCESSED}")
    else:
        print("\nTidak ada data baru yang ditambahkan. Mungkin semua gap sudah terisi atau data tidak ditemukan di PDF nasional.")

if __name__ == "__main__":
    process_national_data()
