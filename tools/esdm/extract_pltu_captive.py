import os
import pandas as pd

def extract_pltu_captive():
    print("Mengekstrak data PLTU Captive di Sulawesi dari database GEM...")
    
    excel_path = 'data/raw/izin_ESDM/gem-data/Global-Coal-Plant-Tracker-January-2026.xlsx'
    if not os.path.exists(excel_path):
        print(f"File tidak ditemukan: {excel_path}")
        return
        
    df = pd.read_excel(excel_path, sheet_name='Units')
    
    # Filter for Indonesia
    indo_df = df[df['Country/Area'] == 'Indonesia'].copy()
    
    # Filter for Sulawesi Provinces (English names in GEM)
    provs = ['North Sulawesi', 'South Sulawesi', 'Southeast Sulawesi', 'Central Sulawesi', 'West Sulawesi', 'Gorontalo']
    pattern = '|'.join(provs)
    
    # Using Subnational unit (province, state)
    sulawesi_df = indo_df[indo_df['Subnational unit (province, state)'].str.contains(pattern, na=False, case=False)].copy()
    
    # Mapping nama provinsi kembali ke bahasa Indonesia
    prov_map = {
        'North Sulawesi': 'Sulawesi Utara',
        'South Sulawesi': 'Sulawesi Selatan',
        'Southeast Sulawesi': 'Sulawesi Tenggara',
        'Central Sulawesi': 'Sulawesi Tengah',
        'West Sulawesi': 'Sulawesi Barat',
        'Gorontalo': 'Gorontalo'
    }
    sulawesi_df['Subnational unit (province, state)'] = sulawesi_df['Subnational unit (province, state)'].map(lambda x: prov_map.get(x, x))
    
    # Filter for Captive Plants (kolom Captive berisi nama industri, bukan 'Yes')
    captive_df = sulawesi_df[sulawesi_df['Captive'].notna()].copy()
    
    # Fill NA for Start year
    captive_df['Start year'] = pd.to_numeric(captive_df['Start year'], errors='coerce')
    captive_df['Capacity (MW)'] = pd.to_numeric(captive_df['Capacity (MW)'], errors='coerce')
    
    # Sort by Start year
    captive_df = captive_df.sort_values(by=['Start year', 'Subnational unit (province, state)'], ascending=[False, True])
    
    # Select important columns
    out_cols = [
        'Plant name', 'Unit name', 'Owner', 'Parent', 
        'Capacity (MW)', 'Status', 'Start year', 
        'Subnational unit (province, state)', 'Local area (taluk, county)', 
        'Captive industry use'
    ]
    
    final_df = captive_df[out_cols].copy()
    
    # Rename columns to Indonesian
    final_df.columns = [
        'Nama PLTU', 'Unit', 'Pemilik', 'Induk Perusahaan', 
        'Kapasitas (MW)', 'Status', 'Tahun Beroperasi', 
        'Provinsi', 'Kabupaten/Kota', 
        'Disuplai ke Industri'
    ]
    
    out_dir = 'data/processed'
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'sulawesi_pltu_captive.csv')
    
    final_df.to_csv(out_path, index=False)
    print(f"Berhasil mengekstrak {len(final_df)} unit PLTU Captive ke {out_path}")

if __name__ == "__main__":
    extract_pltu_captive()
