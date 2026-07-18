import pandas as pd
from pathlib import Path
import re

def clean_number(val):
    if pd.isna(val):
        return 0
    val = str(val).strip().replace('.', '')
    try:
        return int(val)
    except:
        return 0

def clean_provinsi(val):
    if pd.isna(val):
        return ""
    val = str(val).strip()
    # Menghilangkan angka jika ada (misal "1 Aceh" menjadi "Aceh")
    val = re.sub(r'^\d+\s*', '', val)
    return val

def process_table(filepath, tahun, col_idx, chunk_idx, indikator):
    print(f"Mencuci data {indikator} {tahun}...")
    try:
        df = pd.read_csv(filepath, header=None, dtype=str)
        df_valid = df[df[0].str.match(r'^\d+$', na=False)].copy()
        
        # Metode super presisi untuk memotong tabel: 
        # Setiap tabel baru selalu dimulai dari No '1'
        # Kita pisahkan mereka menjadi grup tabel (1, 2, 3, dst)
        if len(df_valid) > 0:
            tabel_group = (df_valid[0] == '1').cumsum()
            
            if chunk_idx == 0:
                df_valid = df_valid[tabel_group == 1]
            elif chunk_idx == 1:
                df_valid = df_valid[tabel_group == 2]
            elif chunk_idx == -1:
                df_valid = df_valid[tabel_group == tabel_group.max()]
            
        df_clean = df_valid[[1, col_idx]].copy()
        df_clean.columns = ['provinsi', 'nilai']
        df_clean['provinsi'] = df_clean['provinsi'].apply(clean_provinsi)
        df_clean['nilai'] = df_clean['nilai'].apply(clean_number)
        df_clean['indikator'] = indikator
        df_clean['tahun'] = tahun
        
        return df_clean
    except Exception as e:
        print(f"Error {indikator}: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    import sys
    BASE_DIR = Path(__file__).resolve().parent.parent
    raw_dir = BASE_DIR / 'data' / 'raw'
    
    # Format: { 'tahun': {'ispa': [idx, chunk], 'diare': [idx, chunk], 'kusta': [idx, chunk], 'malaria': [idx, chunk]} }
    # Mapping indeks kolom untuk nilai absolut per penyakit & tahun
    target_idx = {
        '2014_id': {'ispa': 8, 'diare': 4, 'kusta': 2, 'malaria': 6},
        '2015': {'ispa': 8, 'diare': 4, 'kusta': 2, 'malaria': 6},
        '2017': {'ispa': 9, 'kusta': 10, 'malaria': 8},
        '2022': {'ispa': 4, 'diare': 4, 'kusta': 2, 'malaria': 2}
    }
    
    # chunk: 0 = atas, 1 = tengah, -1 = bawah
    CONFIG = {
        '2022': {
            'ispa': [14, 0], 
            'diare': [4, -1], 
            'kusta': [10, 0], 
            'malaria': [10, 1]
        },
        '2014_id': {
            'ispa': [9, 0], 
            'diare': [3, 0], 
            'kusta': [10, 0], 
            'malaria': [7, 0]
        },
        '2015': {
            'ispa': [9, 0], 
            'diare': [3, 0], 
            'kusta': [10, 0], 
            'malaria': [7, 0]
        },
        '2016': {
            'ispa': [9, 0],
            'diare': [3, 0],
            'kusta': [10, 0],
            'malaria': [7, 0]
        },
        '2017': {
            'ispa': [9, 0],
            'kusta': [10, 0],
            'malaria': [8, 0]
        },
        '2018': {
            'ispa': [9, 0],
            'diare': [3, 0],
            'kusta': [10, 0],
            'malaria': [7, 0]
        },
        '2019': {
            'ispa': [15, 0],
            'diare': [4, 0],
            'kusta': [11, 0],
            'malaria': [10, 0]
        },
        '2020': {
            'ispa': [15, 0],
            'diare': [4, 0],
            'kusta': [11, 0],
            'malaria': [10, 0]
        },
        '2021': {
            'ispa': [15, 0],
            'diare': [4, 0],
            'kusta': [11, 0],
            'malaria': [10, 0]
        },
        '2023': {
            'ispa': [14, 0],
            'diare': [4, 0],
            'kusta': [11, 0],
            'malaria': [10, 0]
        },
        '2024': {
            'ispa': [14, 0],
            'diare': [2, 0],
            'kusta': [11, 0],
            'malaria': [10, 0]
        }
    }
    
    tahun = '2014_id'
    if len(sys.argv) > 1:
        tahun = sys.argv[1]
        
    if tahun not in CONFIG:
        print(f"Error: Konfigurasi kolom untuk tahun {tahun} belum ada.")
        sys.exit(1)
        
    cfg = CONFIG[tahun]
    t = tahun.split('_')[0]
    
    df_ispa = process_table(raw_dir / f'raw_kemenkes_ispa_{tahun}.csv', t, cfg['ispa'][0], cfg['ispa'][1], 'Kasus ISPA/Pneumonia')
    df_kusta = process_table(raw_dir / f'raw_kemenkes_kusta_{tahun}.csv', t, cfg['kusta'][0], cfg['kusta'][1], 'Kasus Kusta Baru')
    df_malaria = process_table(raw_dir / f'raw_kemenkes_malaria_{tahun}.csv', t, cfg['malaria'][0], cfg['malaria'][1], 'Kasus Malaria Positif')
    
    df_diare = pd.DataFrame()
    if 'diare' in cfg:
        df_diare = process_table(raw_dir / f'raw_kemenkes_diare_{tahun}.csv', t, cfg['diare'][0], cfg['diare'][1], 'Kasus Diare Dilayani')
    
    # Gabungkan semua
    frames = [df for df in [df_ispa, df_diare, df_kusta, df_malaria] if not df.empty]
    
    if frames:
        df_final = pd.concat(frames, ignore_index=True)
        df_final = df_final[['provinsi', 'tahun', 'indikator', 'nilai']]
        df_final = df_final.sort_values(by=['indikator', 'provinsi'])
        
        output_file = BASE_DIR / 'data' / 'processed' / f'kemenkes_bersih_{tahun}.csv'
        output_file.parent.mkdir(parents=True, exist_ok=True)
        df_final.to_csv(output_file, index=False)
        
        print(f"\n[SUKSES] Data berhasil dibersihkan dan digabung!")
        print(f"Tersimpan di: {output_file}")
        print("\nPreview Data Bersih:")
        print(df_final.head(10).to_string())
        print("...")
        print(df_final.tail(5).to_string())
    else:
        print("[!] Gagal memproses data apapun.")
