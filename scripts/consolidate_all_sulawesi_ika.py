import pandas as pd
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

def run_consolidation_all_sulawesi():
    print("Mengonsolidasikan data IKA seluruh Sulawesi 2016-2024...")
    
    # Load data BPS 2016-2018
    df2019 = pd.read_csv(BASE_DIR / 'data' / 'raw' / 'sulut_kualitas_air' / 'raw_slhi_ika_2019.csv', header=None, names=['Provinsi', '2016', '2017', '2018'])
    # Load data BPS 2019-2023
    df2024 = pd.read_csv(BASE_DIR / 'data' / 'raw' / 'sulut_kualitas_air' / 'raw_slhi_ika_2024.csv', header=None, names=['Provinsi', '2019', '2020', '2021', '2022', '2023'])

    sulawesi = [
        'Sulawesi Utara', 'Sulawesi Tengah', 'Sulawesi Selatan', 
        'Sulawesi Tenggara', 'Gorontalo', 'Sulawesi Barat'
    ]

    all_data = []

    for prov in sulawesi:
        row_16_18 = df2019[df2019['Provinsi'] == prov]
        row_19_23 = df2024[df2024['Provinsi'] == prov]
        
        # Ekstrak nilai
        val_2016 = row_16_18['2016'].values[0] if not row_16_18.empty else None
        val_2017 = row_16_18['2017'].values[0] if not row_16_18.empty else None
        val_2018 = row_16_18['2018'].values[0] if not row_16_18.empty else None
        
        val_2019 = row_19_23['2019'].values[0] if not row_19_23.empty else None
        val_2020 = row_19_23['2020'].values[0] if not row_19_23.empty else None
        val_2021 = row_19_23['2021'].values[0] if not row_19_23.empty else None
        val_2022 = row_19_23['2022'].values[0] if not row_19_23.empty else None
        val_2023 = row_19_23['2023'].values[0] if not row_19_23.empty else None
        
        # Khusus Sulawesi Utara, kita ambil nilai yang sudah di-edit user dari CSV sebelumnya
        if prov == 'Sulawesi Utara':
            try:
                df_sulut = pd.read_csv(BASE_DIR / 'data' / 'processed' / 'sulut_ika_1_dekade_2016_2024.csv')
                val_2020 = df_sulut[df_sulut['Tahun'] == 2020]['Indeks Kualitas Air'].values[0]
                val_2021 = df_sulut[df_sulut['Tahun'] == 2021]['Indeks Kualitas Air'].values[0]
                val_2022 = df_sulut[df_sulut['Tahun'] == 2022]['Indeks Kualitas Air'].values[0]
                val_2024 = df_sulut[df_sulut['Tahun'] == 2024]['Indeks Kualitas Air'].values[0]
            except Exception as e:
                val_2024 = 58.17 # Fallback Open Data Sulut
        else:
            val_2024 = None # Data 2024 untuk 5 provinsi lain belum tersedia (Portal Open Data mati)

        data_prov = [
            {'Tahun': 2016, 'Provinsi': prov, 'Indeks Kualitas Air': val_2016, 'Sumber Data': 'BPS SLHI 2019'},
            {'Tahun': 2017, 'Provinsi': prov, 'Indeks Kualitas Air': val_2017, 'Sumber Data': 'BPS SLHI 2019'},
            {'Tahun': 2018, 'Provinsi': prov, 'Indeks Kualitas Air': val_2018, 'Sumber Data': 'BPS SLHI 2019'},
            {'Tahun': 2019, 'Provinsi': prov, 'Indeks Kualitas Air': val_2019, 'Sumber Data': 'BPS SLHI 2024'},
            {'Tahun': 2020, 'Provinsi': prov, 'Indeks Kualitas Air': val_2020, 'Sumber Data': 'BPS SLHI 2024' if prov != 'Sulawesi Utara' else 'Manual Edit / BPS'},
            {'Tahun': 2021, 'Provinsi': prov, 'Indeks Kualitas Air': val_2021, 'Sumber Data': 'BPS SLHI 2024' if prov != 'Sulawesi Utara' else 'Manual Edit / BPS'},
            {'Tahun': 2022, 'Provinsi': prov, 'Indeks Kualitas Air': val_2022, 'Sumber Data': 'BPS SLHI 2024' if prov != 'Sulawesi Utara' else 'Manual Edit / BPS'},
            {'Tahun': 2023, 'Provinsi': prov, 'Indeks Kualitas Air': val_2023, 'Sumber Data': 'BPS SLHI 2024'},
            {'Tahun': 2024, 'Provinsi': prov, 'Indeks Kualitas Air': val_2024, 'Sumber Data': 'Open Data Sulawesi Utara 2024' if prov == 'Sulawesi Utara' else 'TBD (Butuh Input Manual / KemenLHK)'}
        ]
        all_data.extend(data_prov)
    
    df_final = pd.DataFrame(all_data)
    
    out_dir = BASE_DIR / 'data' / 'processed'
    os.makedirs(out_dir, exist_ok=True)
    
    out_path = out_dir / 'semua_sulawesi_ika_1_dekade_2016_2024.csv'
    df_final.to_csv(out_path, index=False)
    
    print(f"Data 1 Dekade (Seluruh Sulawesi) berhasil dikonsolidasi dan disimpan di:\n{out_path}")

if __name__ == "__main__":
    run_consolidation_all_sulawesi()
