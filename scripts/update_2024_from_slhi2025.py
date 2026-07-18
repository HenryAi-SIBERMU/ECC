import pandas as pd
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

def update_2024_data():
    csv_path = BASE_DIR / 'data' / 'processed' / 'semua_sulawesi_ika_1_dekade_2016_2024.csv'
    df = pd.read_csv(csv_path)
    
    # Update data 2024 dari BPS SLHI 2025 (Page 134)
    data_2024_slhi2025 = {
        'Sulawesi Utara': 58.17,
        'Sulawesi Tengah': 62.07,
        'Sulawesi Selatan': 58.50,
        'Sulawesi Tenggara': 65.32,
        'Gorontalo': 58.14,
        'Sulawesi Barat': 55.93
    }
    
    for prov, val in data_2024_slhi2025.items():
        # Cari baris yang Tahun = 2024 dan Provinsi = prov
        idx = df[(df['Tahun'] == 2024) & (df['Provinsi'] == prov)].index
        if not idx.empty:
            df.loc[idx, 'Indeks Kualitas Air'] = val
            df.loc[idx, 'Sumber Data'] = 'BPS SLHI 2025'
            
    df.to_csv(csv_path, index=False)
    print("Data 2024 berhasil diperbarui dengan rilis SLHI 2025 terbaru!")
    print(df[df['Tahun'] == 2024])

if __name__ == "__main__":
    update_2024_data()
