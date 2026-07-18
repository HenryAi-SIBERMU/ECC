import pandas as pd
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

def generate_b3_nasional():
    print("Mengonsolidasikan data Timbulan Limbah B3 Nasional (2020-2024) per Sektor...")
    
    # Data diekstrak dari BPS SLHI 2025 (Halaman 211)
    # Satuan: Ton
    data = [
        # 2020
        {'Tahun': 2020, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Manufaktur', 'Timbulan Limbah B3 (Ton)': 15868574, 'Sumber Data': 'BPS SLHI 2025'},
        {'Tahun': 2020, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Agroindustri', 'Timbulan Limbah B3 (Ton)': 2901881, 'Sumber Data': 'BPS SLHI 2025'},
        {'Tahun': 2020, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Pertambangan, Energi, dan Migas', 'Timbulan Limbah B3 (Ton)': 310657793, 'Sumber Data': 'BPS SLHI 2025'},
        {'Tahun': 2020, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Prasarana', 'Timbulan Limbah B3 (Ton)': 203520, 'Sumber Data': 'BPS SLHI 2025'},
        {'Tahun': 2020, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Jasa', 'Timbulan Limbah B3 (Ton)': 8072500, 'Sumber Data': 'BPS SLHI 2025'},
        {'Tahun': 2020, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Fasilitas Pelayanan Kesehatan', 'Timbulan Limbah B3 (Ton)': 396979, 'Sumber Data': 'BPS SLHI 2025'},
        
        # 2021
        {'Tahun': 2021, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Manufaktur', 'Timbulan Limbah B3 (Ton)': 21266539, 'Sumber Data': 'BPS SLHI 2025'},
        {'Tahun': 2021, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Agroindustri', 'Timbulan Limbah B3 (Ton)': 3654645, 'Sumber Data': 'BPS SLHI 2025'},
        {'Tahun': 2021, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Pertambangan, Energi, dan Migas', 'Timbulan Limbah B3 (Ton)': 54093048, 'Sumber Data': 'BPS SLHI 2025'},
        {'Tahun': 2021, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Prasarana', 'Timbulan Limbah B3 (Ton)': 245259, 'Sumber Data': 'BPS SLHI 2025'},
        {'Tahun': 2021, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Jasa', 'Timbulan Limbah B3 (Ton)': 5851762, 'Sumber Data': 'BPS SLHI 2025'},
        {'Tahun': 2021, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Fasilitas Pelayanan Kesehatan', 'Timbulan Limbah B3 (Ton)': 107826, 'Sumber Data': 'BPS SLHI 2025'},
        
        # 2022
        {'Tahun': 2022, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Manufaktur', 'Timbulan Limbah B3 (Ton)': 38663883, 'Sumber Data': 'BPS SLHI 2025'},
        {'Tahun': 2022, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Agroindustri', 'Timbulan Limbah B3 (Ton)': 3498959, 'Sumber Data': 'BPS SLHI 2025'},
        {'Tahun': 2022, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Pertambangan, Energi, dan Migas', 'Timbulan Limbah B3 (Ton)': 60133158, 'Sumber Data': 'BPS SLHI 2025'},
        {'Tahun': 2022, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Prasarana', 'Timbulan Limbah B3 (Ton)': 260430, 'Sumber Data': 'BPS SLHI 2025'},
        {'Tahun': 2022, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Jasa', 'Timbulan Limbah B3 (Ton)': 5732465, 'Sumber Data': 'BPS SLHI 2025'},
        {'Tahun': 2022, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Fasilitas Pelayanan Kesehatan', 'Timbulan Limbah B3 (Ton)': 726817, 'Sumber Data': 'BPS SLHI 2025'},
        
        # 2023
        {'Tahun': 2023, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Manufaktur', 'Timbulan Limbah B3 (Ton)': 14751640, 'Sumber Data': 'BPS SLHI 2025'},
        {'Tahun': 2023, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Agroindustri', 'Timbulan Limbah B3 (Ton)': 3008362, 'Sumber Data': 'BPS SLHI 2025'},
        {'Tahun': 2023, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Pertambangan, Energi, dan Migas', 'Timbulan Limbah B3 (Ton)': 58525950, 'Sumber Data': 'BPS SLHI 2025'},
        {'Tahun': 2023, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Prasarana', 'Timbulan Limbah B3 (Ton)': 376416, 'Sumber Data': 'BPS SLHI 2025'},
        {'Tahun': 2023, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Jasa', 'Timbulan Limbah B3 (Ton)': 4738330, 'Sumber Data': 'BPS SLHI 2025'},
        {'Tahun': 2023, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Fasilitas Pelayanan Kesehatan', 'Timbulan Limbah B3 (Ton)': 573896, 'Sumber Data': 'BPS SLHI 2025'},
        
        # 2024
        {'Tahun': 2024, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Manufaktur', 'Timbulan Limbah B3 (Ton)': 17576073, 'Sumber Data': 'BPS SLHI 2025'},
        {'Tahun': 2024, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Agroindustri', 'Timbulan Limbah B3 (Ton)': 3757321, 'Sumber Data': 'BPS SLHI 2025'},
        {'Tahun': 2024, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Pertambangan, Energi, dan Migas', 'Timbulan Limbah B3 (Ton)': 81894584, 'Sumber Data': 'BPS SLHI 2025'},
        {'Tahun': 2024, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Prasarana', 'Timbulan Limbah B3 (Ton)': 152740, 'Sumber Data': 'BPS SLHI 2025'},
        {'Tahun': 2024, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Jasa', 'Timbulan Limbah B3 (Ton)': 583200, 'Sumber Data': 'BPS SLHI 2025'},
        {'Tahun': 2024, 'Wilayah': 'Indonesia (Nasional)', 'Sektor': 'Fasilitas Pelayanan Kesehatan', 'Timbulan Limbah B3 (Ton)': 456579, 'Sumber Data': 'BPS SLHI 2025'},
    ]
    
    df = pd.DataFrame(data)
    
    out_dir = BASE_DIR / 'data' / 'processed'
    os.makedirs(out_dir, exist_ok=True)
    
    out_path = out_dir / 'nasional_limbah_b3_per_sektor_2020_2024.csv'
    df.to_csv(out_path, index=False)
    
    print(f"Data Timbulan Limbah B3 Nasional berhasil disimpan di:\n{out_path}")
    
    # Hitung total per tahun
    total_df = df.groupby('Tahun')['Timbulan Limbah B3 (Ton)'].sum().reset_index()
    print("\nTotal Timbulan Limbah B3 Nasional per Tahun:")
    print(total_df)

if __name__ == "__main__":
    generate_b3_nasional()
