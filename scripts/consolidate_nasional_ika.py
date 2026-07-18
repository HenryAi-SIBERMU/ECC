import pandas as pd
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

def run_consolidation_nasional():
    print("Mengonsolidasikan data IKA Nasional (Indonesia) 2015-2024...")
    
    # Berdasarkan teks ekstraksi PDF SLHI sebelumnya:
    # SLHI 2021: Indonesia 2015=53,10 | 2016=50,20 | 2017=53,20 | 2018=51,01 | 2019=52,62 | 2020=53,53
    # SLHI 2024: Indonesia 2019=52,62 | 2020=53,53 | 2021=52,82 | 2022=53,88 | 2023=54,59
    # SLHI 2025: Indonesia 2020=53,53 | 2021=52,82 | 2022=53,88 | 2023=54,59 | 2024=54,78
    
    data = [
        {'Tahun': 2015, 'Wilayah': 'Indonesia (Nasional)', 'Indeks Kualitas Air': 53.10, 'Sumber Data': 'BPS SLHI 2021'},
        {'Tahun': 2016, 'Wilayah': 'Indonesia (Nasional)', 'Indeks Kualitas Air': 50.20, 'Sumber Data': 'BPS SLHI 2021'},
        {'Tahun': 2017, 'Wilayah': 'Indonesia (Nasional)', 'Indeks Kualitas Air': 53.20, 'Sumber Data': 'BPS SLHI 2021'},
        {'Tahun': 2018, 'Wilayah': 'Indonesia (Nasional)', 'Indeks Kualitas Air': 51.01, 'Sumber Data': 'BPS SLHI 2021'},
        {'Tahun': 2019, 'Wilayah': 'Indonesia (Nasional)', 'Indeks Kualitas Air': 52.62, 'Sumber Data': 'BPS SLHI 2024'},
        {'Tahun': 2020, 'Wilayah': 'Indonesia (Nasional)', 'Indeks Kualitas Air': 53.53, 'Sumber Data': 'BPS SLHI 2024'},
        {'Tahun': 2021, 'Wilayah': 'Indonesia (Nasional)', 'Indeks Kualitas Air': 52.82, 'Sumber Data': 'BPS SLHI 2024'},
        {'Tahun': 2022, 'Wilayah': 'Indonesia (Nasional)', 'Indeks Kualitas Air': 53.88, 'Sumber Data': 'BPS SLHI 2024'},
        {'Tahun': 2023, 'Wilayah': 'Indonesia (Nasional)', 'Indeks Kualitas Air': 54.59, 'Sumber Data': 'BPS SLHI 2024'},
        {'Tahun': 2024, 'Wilayah': 'Indonesia (Nasional)', 'Indeks Kualitas Air': 54.78, 'Sumber Data': 'BPS SLHI 2025'}
    ]
    
    df = pd.DataFrame(data)
    
    out_dir = BASE_DIR / 'data' / 'processed'
    os.makedirs(out_dir, exist_ok=True)
    
    out_path = out_dir / 'nasional_ika_1_dekade_2015_2024.csv'
    df.to_csv(out_path, index=False)
    
    print(f"Data IKA Nasional berhasil disimpan di:\n{out_path}")
    print("\nPreview:")
    print(df.to_string(index=False))

if __name__ == "__main__":
    run_consolidation_nasional()
