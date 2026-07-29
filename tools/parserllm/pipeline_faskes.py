import os
import glob
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

RAW_DIR = "data/raw/profil kesehatan provinsi_kemenkes"
OUT_RAW = "data/raw/bps_faskes/faskes_raw_extracted.csv"
OUT_PROCESSED = "data/processed/sulawesi_faskes_agregat_v2.csv"

def extract_paragraphs_to_memory():
    """
    Step 1: Extract relevant paragraphs from Markdown files
    """
    print("=== TAHAP 1: EKSTRAKSI PARAGRAF DARI MARKDOWN ===")
    extracted_data = []
    md_files = glob.glob(os.path.join(RAW_DIR, "*.md"))
    
    if not md_files:
        print(f"Warning: No Markdown files found in {RAW_DIR}")
        return pd.DataFrame()
        
    for filepath in md_files:
        filename = os.path.basename(filepath)
        parts = filename.replace('.md', '').split('_')
        tahun = parts[-1] if parts[-1].isdigit() else "Unknown"
        
        provinsi = "Unknown"
        name_lower = filename.lower()
        if "gorontalo" in name_lower: provinsi = "Gorontalo"
        elif "sulteng" in name_lower: provinsi = "Sulawesi Tengah"
        elif "sulsel" in name_lower: provinsi = "Sulawesi Selatan"
        elif "sulut" in name_lower: provinsi = "Sulawesi Utara"
        elif "sultra" in name_lower: provinsi = "Sulawesi Tenggara"
        elif "sulbar" in name_lower: provinsi = "Sulawesi Barat"
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding='latin-1') as f:
                lines = f.readlines()
                
        seen_chunks = set()
                
        for i, line in enumerate(lines):
            line_lower = line.lower()
            has_count_word = any(w in line_lower for w in ["jumlah", "total", "banyaknya", "terdapat", "berjumlah"])
            has_pkm = "puskesmas" in line_lower
            has_rs = "rumah sakit" in line_lower
            
            if has_count_word and (has_pkm or has_rs):
                keyword = "Puskesmas" if has_pkm else "Rumah Sakit"
                if has_pkm and has_rs:
                    keyword = "Puskesmas & Rumah Sakit"
                
                start_idx = max(0, i - 2)
                end_idx = min(len(lines), i + 3)
                
                chunk_lines = [lines[j].strip() for j in range(start_idx, end_idx) if lines[j].strip()]
                paragraph = " ".join(chunk_lines)
                
                if paragraph not in seen_chunks:
                    seen_chunks.add(paragraph)
                    extracted_data.append({
                        "provinsi": provinsi,
                        "tahun": tahun,
                        "keyword": keyword,
                        "kalimat_asli": paragraph,
                        "baris_md": i + 1,
                        "sumber_file": filename
                    })
                    
    df_raw = pd.DataFrame(extracted_data)
    if not df_raw.empty:
        os.makedirs(os.path.dirname(OUT_RAW), exist_ok=True)
        df_raw.to_csv(OUT_RAW, index=False)
        print(f"-> Selesai: {len(df_raw)} paragraf relevan ditemukan dan dibackup ke {OUT_RAW}")
    
    return df_raw

def run_llm_validation(df_raw):
    """
    Step 2: Validate extracted paragraphs using GPT-4o
    """
    print("\n=== TAHAP 2: VALIDASI GPT-4O ===")
    if df_raw.empty:
        print("Data paragraf kosong. Proses dihentikan.")
        return
        
    aggregated_data = []
    grouped = df_raw.groupby(['provinsi', 'tahun'])
    
    for (provinsi, tahun), group in grouped:
        print(f"Menganalisis data {provinsi} {tahun}...")
        
        context_text = "\n".join([f"- [Baris {row['baris_md']}] {row['kalimat_asli']}" for _, row in group.iterrows()])
        
        prompt = f"""
        Anda adalah Data Scientist Senior di Kementerian Kesehatan.
        Tugas Anda adalah menentukan JUMLAH TOTAL PUSKESMAS dan JUMLAH TOTAL RUMAH SAKIT dari potongan teks laporan 'Profil Kesehatan {provinsi} Tahun {tahun}'.
        
        PERINGATAN KERAS (JANGAN SAMPAI SALAH):
        1. JANGAN ambil jumlah "Puskesmas Pembantu (Pustu)", "Puskesmas Keliling", atau "Posyandu". Cari total PUSKESMAS INDUK secara keseluruhan.
        2. JANGAN ambil jumlah "Puskesmas Rawat Inap" saja. Jika ada rincian rawat inap vs non rawat inap, jumlahkan atau cari kalimat yang menyebut TOTAL KESELURUHAN.
        3. JANGAN ambil jumlah Rumah Sakit "Tersertifikasi Akreditasi" jika ada kalimat yang menyebut total rumah sakit yang "Teregistrasi/Terdaftar". Total yang teregistrasi adalah angka yang benar.
        4. Jika sebuah kalimat hanya membahas "jejaring puskesmas", abaikan.
        
        Analisis dengan hati-hati seluruh teks di bawah ini (setiap baris diawali dengan nomor baris sumbernya).
        
        Jawab HANYA dengan JSON murni tanpa markdown formatter (```json):
        {{
          "puskesmas": {{"jumlah": <angka_total>, "bukti": "<kalimat utuh dari teks yang paling meyakinkan>", "baris_md": <angka_baris>}},
          "rumah_sakit": {{"jumlah": <angka_total>, "bukti": "<kalimat utuh dari teks yang paling meyakinkan>", "baris_md": <angka_baris>}}
        }}
        Jika sama sekali tidak ada informasi total keseluruhan yang meyakinkan, gunakan null.
        
        TEKS SUMBER:
        {context_text}
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=400
            )
            raw_json = response.choices[0].message.content.strip()
            if raw_json.startswith('```json'):
                raw_json = raw_json[7:-3]
            elif raw_json.startswith('```'):
                raw_json = raw_json[3:-3]
                
            res = json.loads(raw_json.strip())
            
            pkm = res.get("puskesmas")
            rs = res.get("rumah_sakit")
            
            if pkm and pkm.get("jumlah") is not None:
                aggregated_data.append({'tahun': int(tahun), 'provinsi': provinsi, 'jenis': 'Puskesmas', 'jumlah': int(pkm.get("jumlah")), 'baris_md': pkm.get('baris_md'), 'sumber_kutipan': pkm.get('bukti', '')})
            if rs and rs.get("jumlah") is not None:
                aggregated_data.append({'tahun': int(tahun), 'provinsi': provinsi, 'jenis': 'Rumah Sakit', 'jumlah': int(rs.get("jumlah")), 'baris_md': rs.get('baris_md'), 'sumber_kutipan': rs.get('bukti', '')})
                
        except Exception as e:
            print(f"Error pada GPT-4o untuk {provinsi} {tahun}: {e}")
            
    df_clean = pd.DataFrame(aggregated_data)
    os.makedirs(os.path.dirname(OUT_PROCESSED), exist_ok=True)
    df_clean.to_csv(OUT_PROCESSED, index=False)
    print(f"\n-> Selesai: Dataset agregat tervalidasi berhasil disimpan ke {OUT_PROCESSED}")

def main():
    print("=== MEMULAI 1-CLICK PIPELINE FASKES ===\n")
    df_raw = extract_paragraphs_to_memory()
    run_llm_validation(df_raw)
    print("\n=== SEMUA PROSES SELESAI ===")

if __name__ == "__main__":
    main()
