import os
import pandas as pd
import numpy as np

def classify_province(lokasi):
    if pd.isna(lokasi):
        return None
        
    lokasi = str(lokasi).upper()
    
    sulut = ['MINAHASA', 'MANADO', 'BITUNG', 'TOMOHON', 'KOTAMOBAGU', 'BOLAANG', 'SANGIHE', 'TALAUD', 'SITARO']
    sulteng = ['DONGGALA', 'MOROWALI', 'POSO', 'PALU', 'BANGGAI', 'BUOL', 'TOLI', 'PARIGI', 'TOJO', 'SIGI']
    sulsel = ['MAKASSAR', 'GOWA', 'TAKALAR', 'JENEPONTO', 'BANTAENG', 'BULUKUMBA', 'SINJAI', 'BONE', 'MAROS', 'PANGKA', 'BARRU', 'SOPPENG', 'WAJO', 'SIDENRENG', 'PINRANG', 'ENREKANG', 'LUWU', 'TORAJA', 'PAREPARE', 'PALOPO']
    sultra = ['KENDARI', 'BAUBAU', 'KONAWE', 'KOLAKA', 'MUNA', 'BUTON', 'BOMBANA', 'WAKATOBI', 'KENDARI']
    gorontalo = ['GORONTALO', 'BOALEMO', 'POHUWATO', 'BONE BOLANGO']
    sulbar = ['MAMUJU', 'MAJENE', 'POLEWALI', 'MAMASA', 'PASANGKAYU', 'MATENG']

    # Jika langsung menyebut provinsi
    if 'SULAWESI UTARA' in lokasi: return 'Sulawesi Utara'
    if 'SULAWESI TENGAH' in lokasi: return 'Sulawesi Tengah'
    if 'SULAWESI SELATAN' in lokasi: return 'Sulawesi Selatan'
    if 'SULAWESI TENGGARA' in lokasi: return 'Sulawesi Tenggara'
    if 'SULAWESI BARAT' in lokasi: return 'Sulawesi Barat'
    if 'GORONTALO' in lokasi and 'KAB.' not in lokasi and 'KOTA' not in lokasi: return 'Gorontalo'

    for k in sulut:
        if k in lokasi: return 'Sulawesi Utara'
    for k in sulteng:
        if k in lokasi: return 'Sulawesi Tengah'
    for k in sulsel:
        if k in lokasi: return 'Sulawesi Selatan'
    for k in sultra:
        if k in lokasi: return 'Sulawesi Tenggara'
    for k in gorontalo:
        if k in lokasi: return 'Gorontalo'
    for k in sulbar:
        if k in lokasi: return 'Sulawesi Barat'
        
    return None

def main():
    print("Mengekstrak timeline izin baru untuk Sulawesi (2014-2024)...")
    
    file_path = 'data/raw/izin_ESDM/minerbaone_permits.csv'
    if not os.path.exists(file_path):
        print(f"File tidak ditemukan: {file_path}")
        return
        
    df = pd.read_csv(file_path, dtype=str)
    print(f"Total data izin nasional: {len(df)}")
    
    # Extract tahun
    df['Tahun'] = pd.to_datetime(df['tanggal_berlaku'], errors='coerce').dt.year
    
    # Classify province
    df['Provinsi'] = df['lokasi_perizinan'].apply(classify_province)
    
    # Filter only Sulawesi
    df_sulawesi = df.dropna(subset=['Provinsi', 'Tahun']).copy()
    df_sulawesi['Tahun'] = df_sulawesi['Tahun'].astype(int)
    
    # Filter 1 dekade (2014-2024)
    df_sulawesi = df_sulawesi[(df_sulawesi['Tahun'] >= 2014) & (df_sulawesi['Tahun'] <= 2024)]
    print(f"Total izin ditemukan di Sulawesi (2014-2024): {len(df_sulawesi)}")
    
    # Aggregate
    agg = df_sulawesi.groupby(['Provinsi', 'Tahun']).size().reset_index(name='Jumlah_Izin_Baru')
    
    # Ensure all province/year combinations exist (even 0)
    provinces = ["Sulawesi Utara", "Sulawesi Tengah", "Sulawesi Selatan", "Sulawesi Tenggara", "Gorontalo", "Sulawesi Barat"]
    years = list(range(2014, 2025))
    master = pd.DataFrame([(p, y) for p in provinces for y in years], columns=["Provinsi", "Tahun"])
    
    final_df = master.merge(agg, on=['Provinsi', 'Tahun'], how='left').fillna(0)
    final_df['Jumlah_Izin_Baru'] = final_df['Jumlah_Izin_Baru'].astype(int)
    
    # Tambahan: kita juga hitung kumulatif atau luas_ha (kalau ada)
    # Roll-up luas area per provinsi/tahun
    df_sulawesi['luas_ha'] = pd.to_numeric(df_sulawesi['luas_ha'], errors='coerce').fillna(0)
    luas_agg = df_sulawesi.groupby(['Provinsi', 'Tahun'])['luas_ha'].sum().reset_index(name='Total_Luas_Konsesi_Baru_Ha')
    
    final_df = final_df.merge(luas_agg, on=['Provinsi', 'Tahun'], how='left').fillna(0)
    
    out_path = 'data/processed/sulawesi_izin_baru_per_tahun.csv'
    final_df.to_csv(out_path, index=False)
    print(f"Berhasil disimpan: {out_path} ({len(final_df)} baris)")

if __name__ == '__main__':
    main()
