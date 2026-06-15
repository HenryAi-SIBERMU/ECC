import os
import glob
import pandas as pd

def clean_loss_by_driver(input_dir, output_dir):
    pattern = os.path.join(input_dir, "land_api_fetch", "loss_by_driver_*.csv")
    files = glob.glob(pattern)
    if not files:
        print("File loss_by_driver tidak ditemukan.")
        return
        
    df = pd.read_csv(files[0])
    
    # Filter 1 dekade (2014-2023)
    df = df[(df['year'] >= 2014) & (df['year'] <= 2023)].copy()
    
    # Rename columns ke bahasa Indonesia
    df = df.rename(columns={
        'province': 'Provinsi',
        'year': 'Tahun',
        'driver': 'Faktor_Pendorong',
        'area_ha': 'Luas_Deforestasi_Ha',
        'co2_emissions_mg': 'Emisi_CO2_Megagram',
        'is_primary': 'Hutan_Primer'
    })
    
    # Fill NA untuk is_primary menjadi False/Tidak
    if 'Hutan_Primer' in df.columns:
        df['Hutan_Primer'] = df['Hutan_Primer'].fillna('Tidak/Tidak Diketahui')
        
    # Translate driver
    driver_map = {
        'Commodity driven deforestation': 'Deforestasi Komoditas (Tambang/Sawit)',
        'Forestry': 'Kehutanan',
        'Shifting agriculture': 'Pertanian Berpindah',
        'Urbanization': 'Urbanisasi',
        'Wildfire': 'Kebakaran Hutan',
        'Unknown': 'Tidak Diketahui'
    }
    if 'Faktor_Pendorong' in df.columns:
        df['Faktor_Pendorong'] = df['Faktor_Pendorong'].map(driver_map).fillna(df['Faktor_Pendorong'])
        
    out_path = os.path.join(output_dir, "sulawesi_gfw_loss_by_driver_2014_2023.csv")
    df.to_csv(out_path, index=False)
    print(f"Berhasil Disimpan: {out_path} ({len(df)} baris)")

def clean_primary_forest_loss(input_dir, output_dir):
    pattern = os.path.join(input_dir, "mega_fetch_v2", "primary_forest_loss_*.csv")
    files = glob.glob(pattern)
    if not files:
        print("File primary_forest_loss tidak ditemukan.")
        return
        
    df = pd.read_csv(files[0])
    
    # Cek ada kolom apa saja, biasnya province, year, area_ha
    if 'year' in df.columns:
        df = df[(df['year'] >= 2014) & (df['year'] <= 2023)].copy()
        
    rename_map = {
        'province': 'Provinsi',
        'year': 'Tahun',
        'area__ha': 'Luas_Hilang_Hutan_Primer_Ha',
        'area_ha': 'Luas_Hilang_Hutan_Primer_Ha',
        'loss_ha': 'Luas_Hilang_Hutan_Primer_Ha'
    }
    df = df.rename(columns={k:v for k,v in rename_map.items() if k in df.columns})
    
    out_path = os.path.join(output_dir, "sulawesi_gfw_hutan_primer_loss_2014_2023.csv")
    df.to_csv(out_path, index=False)
    print(f"Berhasil Disimpan: {out_path} ({len(df)} baris)")

def clean_protected_areas_loss(input_dir, output_dir):
    pattern = os.path.join(input_dir, "mega_fetch_v2", "loss_in_protected_areas_*.csv")
    files = glob.glob(pattern)
    if not files:
        print("File loss_in_protected_areas tidak ditemukan.")
        return
        
    df = pd.read_csv(files[0])
    
    if 'year' in df.columns:
        df = df[(df['year'] >= 2014) & (df['year'] <= 2023)].copy()
        
    rename_map = {
        'province': 'Provinsi',
        'year': 'Tahun',
        'area__ha': 'Luas_Hilang_Kawasan_Lindung_Ha',
        'area_ha': 'Luas_Hilang_Kawasan_Lindung_Ha',
        'loss_ha': 'Luas_Hilang_Kawasan_Lindung_Ha'
    }
    df = df.rename(columns={k:v for k,v in rename_map.items() if k in df.columns})
    
    out_path = os.path.join(output_dir, "sulawesi_gfw_kawasan_lindung_loss_2014_2023.csv")
    df.to_csv(out_path, index=False)
    print(f"Berhasil Disimpan: {out_path} ({len(df)} baris)")

def main():
    input_dir = "data/raw/klhk_gfw"
    output_dir = "data/processed"
    os.makedirs(output_dir, exist_ok=True)
    
    print("Memulai pembersihan data GFW (1 Dekade 2014-2023)...")
    clean_loss_by_driver(input_dir, output_dir)
    clean_primary_forest_loss(input_dir, output_dir)
    clean_protected_areas_loss(input_dir, output_dir)
    print("Semua data GFW berhasil di-clean dan dipindahkan ke processed!")

if __name__ == '__main__':
    main()
