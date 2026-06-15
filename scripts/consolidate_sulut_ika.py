import pandas as pd
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

def run_consolidation():
    print("Mengonsolidasikan data IKA Sulawesi Utara 2016-2024...")
    
    # Data historis yang sudah di-cross-check dari BPS SLHI 2019, 2021, dan 2024
    # serta Open Data Sulut 2024.
    data = [
        {'Tahun': 2016, 'Provinsi': 'Sulawesi Utara', 'Indeks Kualitas Air': 49.52, 'Sumber Data': 'BPS SLHI 2019'},
        {'Tahun': 2017, 'Provinsi': 'Sulawesi Utara', 'Indeks Kualitas Air': 54.62, 'Sumber Data': 'BPS SLHI 2019'},
        {'Tahun': 2018, 'Provinsi': 'Sulawesi Utara', 'Indeks Kualitas Air': 54.10, 'Sumber Data': 'BPS SLHI 2019'},
        {'Tahun': 2019, 'Provinsi': 'Sulawesi Utara', 'Indeks Kualitas Air': 45.48, 'Sumber Data': 'BPS SLHI 2024'},
        {'Tahun': 2020, 'Provinsi': 'Sulawesi Utara', 'Indeks Kualitas Air': 50.53, 'Sumber Data': 'BPS SLHI 2024'},
        {'Tahun': 2021, 'Provinsi': 'Sulawesi Utara', 'Indeks Kualitas Air': 49.69, 'Sumber Data': 'BPS SLHI 2024'},
        {'Tahun': 2022, 'Provinsi': 'Sulawesi Utara', 'Indeks Kualitas Air': 48.24, 'Sumber Data': 'BPS SLHI 2024'},
        {'Tahun': 2023, 'Provinsi': 'Sulawesi Utara', 'Indeks Kualitas Air': 52.12, 'Sumber Data': 'BPS SLHI 2024'},
        {'Tahun': 2024, 'Provinsi': 'Sulawesi Utara', 'Indeks Kualitas Air': 58.17, 'Sumber Data': 'Open Data Sulawesi Utara 2024'}
    ]
    
    df = pd.DataFrame(data)
    
    # Pastikan direktori processed ada
    out_dir = BASE_DIR / 'data' / 'processed'
    os.makedirs(out_dir, exist_ok=True)
    
    out_path = out_dir / 'sulut_ika_1_dekade_2016_2024.csv'
    df.to_csv(out_path, index=False)
    
    print(f"Data 1 Dekade berhasil dikonsolidasi dan disimpan di:\n{out_path}")
    print("\nPreview Data:")
    print(df.to_string(index=False))

if __name__ == "__main__":
    run_consolidation()
