import pandas as pd
import os

def clean_bnpb_data():
    raw_path = os.path.join("data", "raw", "bnpb", "20260626_200458.csv")
    out_path = os.path.join("data", "processed", "bnpb_ekologis_sulawesi_2014_2024.csv")
    
    print(f"Membaca data raw dari {raw_path}...")
    df = pd.read_csv(raw_path)
    
    # 1. Filter Tahun 2014 - 2024
    df_filtered = df[(df['Tahun'] >= 2014) & (df['Tahun'] <= 2024)].copy()
    
    # 2. Filter Khusus Provinsi Sulawesi
    # Kode Provinsi Sulawesi di BPS/BNPB: 71 (Sulut), 72 (Sulteng), 73 (Sulsel), 74 (Sultra), 75 (Gorontalo), 76 (Sulbar)
    sulawesi_codes = [71, 72, 73, 74, 75, 76]
    df_filtered = df_filtered[df_filtered['Kode Provinsi'].isin(sulawesi_codes)]
    
    # 3. Filter Jenis Bencana Ekologis (Banjir, Longsor, Cuaca Ekstrem/Banjir Bandang, Karhutla)
    ekologis_keywords = ['Banjir', 'Longsor', 'Cuaca Ekstrem', 'Kebakaran Hutan', 'Kekeringan']
    
    def is_ekologis(bencana):
        if pd.isna(bencana): return False
        return any(k in str(bencana) for k in ekologis_keywords)
        
    df_filtered = df_filtered[df_filtered['Jenis Bencana'].apply(is_ekologis)]
    
    # 4. Agregasi data per Kabupaten dan Tahun
    # Kita butuh menjumlahkan kejadian dan dampak
    agg_cols = {
        'Jumlah Kejadian': 'sum',
        'Meninggal': 'sum',
        'Luka / Sakit': 'sum',
        'menderita_mengungsi': 'sum',
        'Rumah Rusak Berat': 'sum',
        'Rumah Rusak Sedang': 'sum',
        'Rumah Rusak Ringan': 'sum',
        'Rumah Terendam': 'sum'
    }
    
    df_grouped = df_filtered.groupby(['Tahun', 'Kode Provinsi', 'Provinsi', 'Kode Kabupaten', 'Kabupaten', 'Jenis Bencana'], as_index=False).agg(agg_cols)
    
    # Simpan hasil
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df_grouped.to_csv(out_path, index=False)
    
    print(f"Data BNPB berhasil dibersihkan! Tersisa {len(df_grouped)} baris data bencana ekologis di Sulawesi.")
    print(f"Disimpan ke: {out_path}")

if __name__ == "__main__":
    clean_bnpb_data()
