import os
import pandas as pd

def extract_sulawesi_konflik():
    print("Mengekstrak data konflik sosial dan hukum di Sulawesi...")
    
    csv_path = 'data/raw/konflik_kpa_ylbhi_tanahkita/tanahkita_konflik.csv'
    if not os.path.exists(csv_path):
        print(f"File tidak ditemukan: {csv_path}")
        return
        
    df = pd.read_csv(csv_path)
    
    # Kata kunci wilayah Sulawesi
    keywords = ['Sulawesi', 'Kendari', 'Palu', 'Makassar', 'Morowali', 'Konawe', 'Sultra', 'Sulteng', 'Sulsel', 'Sulut', 'Sulbar', 'Gorontalo', 'Wawoni', 'Tinanggea', 'Mamuju', 'Bitung']
    pattern = '|'.join(keywords)
    
    # Filter judul atau deskripsi yang mengandung wilayah Sulawesi
    sulawesi_df = df[
        df['judul'].str.contains(pattern, na=False, case=False) | 
        df['deskripsi'].str.contains(pattern, na=False, case=False)
    ].copy()
    
    # Buat fungsi untuk menebak provinsi berdasarkan kata kunci
    def tebak_provinsi(text):
        text = str(text).upper()
        if 'SULTRA' in text or 'TENGGARA' in text or 'KENDARI' in text or 'KONAWE' in text or 'WAWONI' in text or 'TINANGGEA' in text:
            return 'Sulawesi Tenggara'
        elif 'SULTENG' in text or 'TENGAH' in text or 'PALU' in text or 'MOROWALI' in text:
            return 'Sulawesi Tengah'
        elif 'SULSEL' in text or 'SELATAN' in text or 'MAKASSAR' in text or 'MAROS' in text:
            return 'Sulawesi Selatan'
        elif 'SULUT' in text or 'UTARA' in text or 'BITUNG' in text or 'MANADO' in text:
            return 'Sulawesi Utara'
        elif 'SULBAR' in text or 'BARAT' in text or 'MAMUJU' in text:
            return 'Sulawesi Barat'
        elif 'GORONTALO' in text:
            return 'Gorontalo'
        return 'Sulawesi (Umum)'

    sulawesi_df['Provinsi'] = (sulawesi_df['judul'] + ' ' + sulawesi_df['deskripsi']).apply(tebak_provinsi)
    
    out_cols = ['nomor', 'Provinsi', 'judul', 'status', 'deskripsi', 'detail_url']
    final_df = sulawesi_df[out_cols].copy()
    final_df.columns = ['ID_Konflik', 'Provinsi', 'Judul_Kasus', 'Sektor', 'Deskripsi_Singkat', 'URL_Sumber']
    
    out_dir = 'data/processed'
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'sulawesi_konflik_hukum.csv')
    
    final_df.to_csv(out_path, index=False)
    print(f"Berhasil mengekstrak {len(final_df)} kasus pelanggaran/konflik ke {out_path}")

if __name__ == "__main__":
    extract_sulawesi_konflik()
