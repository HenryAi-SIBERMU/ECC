import os
import glob
import pandas as pd
import numpy as np

def get_file(folder, pattern):
    files = glob.glob(os.path.join("data/raw/klhk_gfw", folder, pattern))
    return files[0] if files else None

def main():
    print("Memulai konsolidasi Master Dataset GFW (2014-2023)...")
    
    # Base DataFrame (Provinsi x Tahun 2014-2023)
    provinces = ["Sulawesi Utara", "Sulawesi Tengah", "Sulawesi Selatan", "Sulawesi Tenggara", "Gorontalo", "Sulawesi Barat"]
    years = list(range(2014, 2024))
    
    master = pd.DataFrame([(p, y) for p in provinces for y in years], columns=["Provinsi", "Tahun"])
    
    # 1. Tree Cover Loss
    f_loss = get_file("mega_fetch_v2", "tree_cover_loss_*.csv")
    if f_loss:
        df = pd.read_csv(f_loss)
        if 'tree_cover_loss_ha' in df.columns:
            df = df.rename(columns={'province': 'Provinsi', 'year': 'Tahun', 'tree_cover_loss_ha': 'Total_Deforestasi_Ha'})
            master = master.merge(df[['Provinsi', 'Tahun', 'Total_Deforestasi_Ha']], on=['Provinsi', 'Tahun'], how='left')

    # 2. Primary Forest Loss
    f_primary = get_file("mega_fetch_v2", "primary_forest_loss_*.csv")
    if f_primary:
        df = pd.read_csv(f_primary)
        df = df.rename(columns={'province': 'Provinsi', 'year': 'Tahun', 'area__ha': 'Deforestasi_Hutan_Primer_Ha', 'area_ha': 'Deforestasi_Hutan_Primer_Ha', 'loss_ha': 'Deforestasi_Hutan_Primer_Ha'})
        df = df.groupby(['Provinsi', 'Tahun'])['Deforestasi_Hutan_Primer_Ha'].sum().reset_index()
        master = master.merge(df, on=['Provinsi', 'Tahun'], how='left')

    # 3. Protected Areas Loss
    f_pa = get_file("mega_fetch_v2", "loss_in_protected_areas_*.csv")
    if f_pa:
        df = pd.read_csv(f_pa)
        df = df.rename(columns={'province': 'Provinsi', 'year': 'Tahun', 'area__ha': 'Deforestasi_Kawasan_Lindung_Ha', 'area_ha': 'Deforestasi_Kawasan_Lindung_Ha'})
        df = df.groupby(['Provinsi', 'Tahun'])['Deforestasi_Kawasan_Lindung_Ha'].sum().reset_index()
        master = master.merge(df, on=['Provinsi', 'Tahun'], how='left')

    # 4. Loss by Driver (THE GOLDEN FILE) & CO2
    f_driver = get_file("land_api_fetch", "loss_by_driver_*.csv")
    if f_driver:
        df = pd.read_csv(f_driver)
        df = df.rename(columns={'province': 'Provinsi', 'year': 'Tahun'})
        
        # Pivot drivers
        driver_map = {
            'Commodity driven deforestation': 'Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha',
            'Forestry': 'Deforestasi_Driver_Kehutanan_Ha',
            'Shifting agriculture': 'Deforestasi_Driver_Pertanian_Berpindah_Ha',
            'Urbanization': 'Deforestasi_Driver_Urbanisasi_Ha'
        }
        
        for en, id_col in driver_map.items():
            sub = df[df['driver'] == en].groupby(['Provinsi', 'Tahun'])['area_ha'].sum().reset_index()
            sub = sub.rename(columns={'area_ha': id_col})
            master = master.merge(sub, on=['Provinsi', 'Tahun'], how='left')
            
        # CO2 Total
        co2 = df.groupby(['Provinsi', 'Tahun'])['co2_emissions_mg'].sum().reset_index()
        co2 = co2.rename(columns={'co2_emissions_mg': 'Total_Emisi_CO2_Megagram'})
        master = master.merge(co2, on=['Provinsi', 'Tahun'], how='left')
        
    # 5. Deforestation Rate
    f_rate = get_file("complete_fetch", "deforestation_rate_*.csv")
    if f_rate:
        df = pd.read_csv(f_rate)
        df = df.rename(columns={'province': 'Provinsi', 'year': 'Tahun', 'loss_ha': 'Laju_Deforestasi_Ha'})
        master = master.merge(df[['Provinsi', 'Tahun', 'Laju_Deforestasi_Ha']], on=['Provinsi', 'Tahun'], how='left')

    # 6. Tree Cover Extent 2000 (Static Baseline)
    f_extent = get_file("complete_fetch", "tree_cover_extent_*.csv")
    if f_extent:
        df = pd.read_csv(f_extent)
        df = df.rename(columns={'province': 'Provinsi', 'tree_cover_2000_ha': 'Baseline_Tutupan_Hutan_2000_Ha'})
        df = df.groupby('Provinsi')['Baseline_Tutupan_Hutan_2000_Ha'].max().reset_index()
        master = master.merge(df, on=['Provinsi'], how='left')

    # Fill NA untuk kolom numerik dengan 0
    num_cols = master.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        if col != 'Tahun':
            master[col] = master[col].fillna(0)

    # Reorder columns
    cols = ['Provinsi', 'Tahun', 'Total_Deforestasi_Ha', 'Deforestasi_Hutan_Primer_Ha', 
            'Deforestasi_Kawasan_Lindung_Ha', 'Laju_Deforestasi_Ha',
            'Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha', 'Deforestasi_Driver_Kehutanan_Ha',
            'Total_Emisi_CO2_Megagram', 'Baseline_Tutupan_Hutan_2000_Ha']
            
    # Pastikan hanya kolom yang ada di dataframe yang diurutkan
    final_cols = [c for c in cols if c in master.columns]
    
    # Tambahkan sisa kolom yang mungkin terlewat
    for c in master.columns:
        if c not in final_cols:
            final_cols.append(c)
            
    master = master[final_cols]

    # Save to processed
    out_dir = 'data/processed'
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'sulawesi_gfw_master_1_dekade_2014_2023.csv')
    
    master.to_csv(out_path, index=False)
    print(f"Berhasil! Master dataset tersimpan di: {out_path} ({len(master)} baris, {len(master.columns)} kolom)")

if __name__ == '__main__':
    main()
