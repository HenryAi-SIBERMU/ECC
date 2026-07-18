import os
import pandas as pd

def classify_province(lokasi):
    if pd.isna(lokasi):
        return None
        
    lokasi = str(lokasi).upper()
    
    sulut = ['MINAHASA', 'MANADO', 'BITUNG', 'TOMOHON', 'KOTAMOBAGU', 'BOLAANG', 'SANGIHE', 'TALAUD', 'SITARO']
    sulteng = ['DONGGALA', 'MOROWALI', 'POSO', 'PALU', 'BANGGAI', 'BUOL', 'TOLI', 'PARIGI', 'TOJO', 'SIGI']
    sulsel = ['MAKASSAR', 'GOWA', 'TAKALAR', 'JENEPONTO', 'BANTAENG', 'BULUKUMBA', 'SINJAI', 'BONE', 'MAROS', 'PANGKA', 'BARRU', 'SOPPENG', 'WAJO', 'SIDENRENG', 'PINRANG', 'ENREKANG', 'LUWU', 'TORAJA', 'PAREPARE', 'PALOPO']
    sultra = ['KENDARI', 'BAUBAU', 'KONAWE', 'KOLAKA', 'MUNA', 'BUTON', 'BOMBANA', 'WAKATOBI'] # Removed duplicated KENDARI
    gorontalo = ['GORONTALO', 'BOALEMO', 'POHUWATO', 'BONE BOLANGO']
    sulbar = ['MAMUJU', 'MAJENE', 'POLEWALI', 'MAMASA', 'PASANGKAYU', 'MATENG']

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
    permits_path = 'data/raw/izin_ESDM/minerbaone_permits.csv'
    companies_path = 'data/raw/izin_ESDM/IUP1_minerbaone_companies.csv'
    
    df_p = pd.read_csv(permits_path, dtype=str)
    df_c = pd.read_csv(companies_path, dtype=str)
    
    # Extract tahun
    df_p['Tahun'] = pd.to_datetime(df_p['tanggal_berlaku'], errors='coerce').dt.year
    df_p['Provinsi'] = df_p['lokasi_perizinan'].apply(classify_province)
    
    # Join with companies to get company names
    df = df_p.merge(df_c[['id_badan_usaha', 'nama_badan_usaha', 'jenis_badan_usaha']], on='id_badan_usaha', how='left')
    
    df_sulawesi = df.dropna(subset=['Provinsi', 'Tahun']).copy()
    df_sulawesi['Tahun'] = df_sulawesi['Tahun'].astype(int)
    
    # Filter 1 dekade (2014-2024)
    df_sulawesi = df_sulawesi[(df_sulawesi['Tahun'] >= 2014) & (df_sulawesi['Tahun'] <= 2024)]
    
    # Format Luas
    df_sulawesi['luas_ha'] = pd.to_numeric(df_sulawesi['luas_ha'], errors='coerce').fillna(0)
    
    out_cols = ['nama_badan_usaha', 'nomor_izin', 'jenis_badan_usaha', 'komoditas', 'tahap_kegiatan', 'Provinsi', 'lokasi_perizinan', 'Tahun', 'luas_ha']
    final_df = df_sulawesi[out_cols].copy()
    
    out_path = 'data/processed/sulawesi_izin_raw_details.csv'
    final_df.to_csv(out_path, index=False)
    print(f"Berhasil disimpan: {out_path} ({len(final_df)} baris)")

if __name__ == '__main__':
    main()
