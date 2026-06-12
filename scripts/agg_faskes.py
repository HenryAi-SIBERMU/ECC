import pandas as pd
import glob, os

SULAWESI = ['Sulawesi Utara', 'Sulawesi Tengah', 'Sulawesi Selatan', 'Sulawesi Tenggara', 'Gorontalo', 'Sulawesi Barat']

# 1. Rumah Sakit
rs_files = glob.glob('data/raw/profil kesehatan_kemenkes/raw_kemenkes_rumah_sakit_*.csv')
dfs = []
for f in rs_files:
    try:
        tahun = f.split('_sakit_')[1].split('.')[0].replace('_id', '')
        df = pd.read_csv(f)
        df['prov_lower'] = df.iloc[:, 1].astype(str).str.lower()
        sul = df[df['prov_lower'].str.contains('sulawesi|gorontalo', na=False)].copy()
        sul['tahun'] = int(tahun)
        sul['jenis'] = 'Rumah Sakit'
        sul['provinsi'] = sul.iloc[:, 1]
        sul['jumlah'] = pd.to_numeric(sul.iloc[:, 2], errors='coerce').fillna(0)
        dfs.append(sul[['tahun', 'provinsi', 'jenis', 'jumlah']])
    except Exception as e:
        print(f"Error rs {f}:", e)

# 2. Puskesmas
pusk_files = glob.glob('data/raw/profil kesehatan_kemenkes/raw_kemenkes_puskesmas_*.csv')
for f in pusk_files:
    try:
        tahun = f.split('_puskesmas_')[1].split('.')[0].replace('_id', '')
        df = pd.read_csv(f)
        df['prov_lower'] = df.iloc[:, 1].astype(str).str.lower()
        sul = df[df['prov_lower'].str.contains('sulawesi|gorontalo', na=False)].copy()
        sul['tahun'] = int(tahun)
        sul['jenis'] = 'Puskesmas'
        sul['provinsi'] = sul.iloc[:, 1]
        sul['jumlah'] = pd.to_numeric(sul.iloc[:, 2], errors='coerce').fillna(0)
        dfs.append(sul[['tahun', 'provinsi', 'jenis', 'jumlah']])
    except Exception as e:
        print(f"Error pusk {f}:", e)

if dfs:
    df_faskes = pd.concat(dfs)
    df_faskes.to_csv('data/processed/faskes_sulawesi_agg.csv', index=False)
    print("Faskes aggregated:", len(df_faskes))
else:
    print("dfs is empty")
