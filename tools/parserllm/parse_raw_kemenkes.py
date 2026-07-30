import os
import glob
import pandas as pd
import re

RAW_DIR = "data/raw/profil kesehatan_kemenkes"
OUT_V3 = "data/processed/sulawesi_kesehatan_detail_2014_2024_v3.csv"
OUT_V2 = "data/processed/sulawesi_kesehatan_detail_2014_2024_v2.csv"

# Mapping province names in English / Indonesian
PROV_MAP = {
    "north sulawesi": "Sulawesi Utara",
    "sulawesi utara": "Sulawesi Utara",
    "central sulawesi": "Sulawesi Tengah",
    "sulawesi tengah": "Sulawesi Tengah",
    "south sulawesi": "Sulawesi Selatan",
    "sulawesi selatan": "Sulawesi Selatan",
    "southeast sulawesi": "Sulawesi Tenggara",
    "sulawesi tenggara": "Sulawesi Tenggara",
    "gorontalo": "Gorontalo",
    "west sulawesi": "Sulawesi Barat",
    "sulawesi barat": "Sulawesi Barat"
}

def clean_val(v):
    if pd.isna(v) or v == '-' or v == '':
        return None
    s = str(v).replace(',', '').replace('.', '').strip()
    try:
        val = int(s)
        return val if val > 0 else None
    except ValueError:
        return None

def parse_national_csvs():
    records = []
    
    csv_files = glob.glob(os.path.join(RAW_DIR, "raw_kemenkes_*.csv"))
    print(f"Ditemukan {len(csv_files)} file CSV nasional Kemenkes di {RAW_DIR}")
    
    for filepath in csv_files:
        filename = os.path.basename(filepath)
        
        # Match disease and year
        # e.g., raw_kemenkes_diare_2014.csv
        m = re.search(r'raw_kemenkes_(diare|ispa|malaria)_(\d{4})', filename)
        if not m:
            continue
            
        disease_type = m.group(1)
        year = int(m.group(2))
        
        try:
            df = pd.read_csv(filepath)
        except Exception:
            try:
                df = pd.read_csv(filepath, encoding='latin-1')
            except Exception:
                continue
                
        # Find province column
        prov_col = None
        for col in df.columns:
            if 'prov' in str(col).lower():
                prov_col = col
                break
                
        if not prov_col:
            # Check first 3 columns
            for col in df.columns[:3]:
                if df[col].astype(str).str.lower().isin(PROV_MAP.keys()).any():
                    prov_col = col
                    break
                    
        if not prov_col:
            continue
            
        # Determine value column based on disease
        # Diare: Treated Cases / Diare Dilayani
        # ISPA: Pneumonia Total / Found / Pneumonia
        # Malaria: Positive / Positif
        for idx, row in df.iterrows():
            prov_name_raw = str(row[prov_col]).strip().lower()
            if prov_name_raw not in PROV_MAP:
                continue
                
            prov_std = PROV_MAP[prov_name_raw]
            
            # Find the best value column in this row
            val = None
            col_used = ""
            
            if disease_type == "diare":
                indikator = "Kasus Diare Dilayani"
                for c in df.columns:
                    cl = str(c).lower()
                    if 'treated' in cl or 'dilayani' in cl or 'ditangani' in cl:
                        if '%' not in cl and 'rate' not in cl:
                            parsed = clean_val(row[c])
                            if parsed:
                                val = parsed
                                col_used = c
                                break
            elif disease_type == "ispa":
                indikator = "Kasus ISPA/Pneumonia"
                for c in df.columns:
                    cl = str(c).lower()
                    if 'total' in cl or 'pneumonia' in cl or 'penderita' in cl:
                        if '%' not in cl and 'rate' not in cl and 'target' not in cl:
                            parsed = clean_val(row[c])
                            if parsed:
                                val = parsed
                                col_used = c
                                break
            elif disease_type == "malaria":
                indikator = "Kasus Malaria Positif"
                for c in df.columns:
                    cl = str(c).lower()
                    if 'positive' in cl or 'positif' in cl or 'kasus' in cl:
                        if '%' not in cl and 'api' in cl or 'positif' in cl:
                            if '%' not in cl and 'rate' not in cl:
                                parsed = clean_val(row[c])
                                if parsed:
                                    val = parsed
                                    col_used = c
                                    break
                                    
            if val is not None:
                records.append({
                    'tahun': year,
                    'provinsi': prov_std,
                    'kabupaten_kota': 'Total Provinsi',
                    'indikator': indikator,
                    'nilai': val,
                    'baris_md': 0,
                    'sumber_kutipan': f"Extracted from official Kemenkes Table ({filename}, col: {col_used})",
                    'sumber_file': filename
                })
                
    df_nat = pd.DataFrame(records)
    print(f"Data nasional berhasil diekstrak: {len(df_nat)} baris")
    
    # Merge with V3 (provincial profile clean data)
    if os.path.exists(OUT_V3):
        df_v3 = pd.read_csv(OUT_V3)
        print(f"Data provinsi V3 dibaca: {len(df_v3)} baris")
        
        df_merged = pd.concat([df_v3, df_nat], ignore_index=True)
        df_merged = df_merged.drop_duplicates(subset=['tahun', 'provinsi', 'kabupaten_kota', 'indikator'], keep='first')
        df_merged = df_merged.sort_values(by=['tahun', 'provinsi', 'kabupaten_kota'])
        
        df_merged.to_csv(OUT_V3, index=False)
        df_merged.to_csv(OUT_V2, index=False)
        print(f"[SUKSES GABUNGAN REKAP] Data bersih disimpan ke V3 & V2 (Total: {len(df_merged)} baris)")
    else:
        df_nat.to_csv(OUT_V3, index=False)
        df_nat.to_csv(OUT_V2, index=False)

if __name__ == "__main__":
    parse_national_csvs()
