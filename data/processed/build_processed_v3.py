import pandas as pd
import numpy as np

raw_path = r"C:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\data\raw\profil kesehatan_nasional_kemenkes\raw_sulawesi_faskes_agregat_v3.csv"
out_path = r"C:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\data\processed\sulawesi_faskes_agregat_v3.csv"

df_raw = pd.read_csv(raw_path)

def to_num(val):
    if pd.isna(val): return 0
    try:
        return int(str(val).replace('.', '').replace(',', '').strip())
    except:
        return 0

results = []
provinces = df_raw['provinsi'].unique()
years = range(2014, 2025)

for year in years:
    for prov in provinces:
        # PUSKESMAS
        pkm_val = np.nan
        pkm_source = ""
        pkm_title = ""
        
        df_pkm = df_raw[(df_raw['provinsi'] == prov) & (df_raw['jenis_faskes'] == 'Puskesmas')]
        
        match1 = df_pkm[df_pkm['variabel'] == f'Jumlah Puskesmas {year}']
        if not match1.empty:
            pkm_val = to_num(match1.iloc[0]['nilai_absolut'])
            pkm_source = match1.iloc[0]['sumber_file']
            pkm_title = match1.iloc[0]['judul_tabel']
        else:
            match2 = df_pkm[(df_pkm['tahun'] == year) & (df_pkm['variabel'].str.contains('Total Puskesmas', case=False, na=False))]
            if not match2.empty:
                pkm_val = to_num(match2.iloc[0]['nilai_absolut'])
                pkm_source = match2.iloc[0]['sumber_file']
                pkm_title = match2.iloc[0]['judul_tabel']
            else:
                match3 = df_pkm[(df_pkm['tahun'] == year) & (df_pkm['variabel'] == 'Total') & (df_pkm['judul_tabel'].str.contains('KARAKTERISTIK WILAYAH', case=False, na=False))]
                if not match3.empty:
                    pkm_val = to_num(match3.iloc[0]['nilai_absolut'])
                    pkm_source = match3.iloc[0]['sumber_file']
                    pkm_title = match3.iloc[0]['judul_tabel']
                else:
                    v1 = df_pkm[(df_pkm['tahun'] == year) & (df_pkm['variabel'] == 'Jumlah Puskesmas Belum Memenuhi')]
                    v2 = df_pkm[(df_pkm['tahun'] == year) & (df_pkm['variabel'] == 'Jumlah Puskesmas Memenuhi')]
                    if not v1.empty and not v2.empty:
                        pkm_val = to_num(v1.iloc[0]['nilai_absolut']) + to_num(v2.iloc[0]['nilai_absolut'])
                        pkm_source = v1.iloc[0]['sumber_file']
                        pkm_title = v1.iloc[0]['judul_tabel']
                            
        if not pd.isna(pkm_val):
            results.append({
                'tahun': year,
                'provinsi': prov,
                'jenis_faskes': 'Puskesmas',
                'jumlah': int(pkm_val),
                'sumber_kutipan': pkm_title,
                'sumber_file': pkm_source
            })

        # RUMAH SAKIT
        rs_val = np.nan
        rs_source = ""
        rs_title = ""
        
        df_rs = df_raw[(df_raw['provinsi'] == prov) & (df_raw['jenis_faskes'] == 'Rumah Sakit') & (df_raw['tahun'] == year)]
        
        v1 = df_rs[df_rs['variabel'] == 'Jumlah RS Umum']
        v2 = df_rs[df_rs['variabel'] == 'Jumlah RS Khusus']
        if not v1.empty and not v2.empty:
            rs_val = to_num(v1.iloc[0]['nilai_absolut']) + to_num(v2.iloc[0]['nilai_absolut'])
            rs_source = v1.iloc[0]['sumber_file']
            rs_title = v1.iloc[0]['judul_tabel']
            
        if not pd.isna(rs_val):
            results.append({
                'tahun': year,
                'provinsi': prov,
                'jenis_faskes': 'Rumah Sakit',
                'jumlah': int(rs_val),
                'sumber_kutipan': rs_title,
                'sumber_file': rs_source
            })

df_res = pd.DataFrame(results)
df_res = df_res.sort_values(by=['tahun', 'provinsi', 'jenis_faskes'])
df_res.to_csv(out_path, index=False)
print(f"Generated clean processed dataset without imputation: {len(df_res)} rows.")
