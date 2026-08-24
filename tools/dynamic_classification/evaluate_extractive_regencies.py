import os
import pandas as pd

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_dir = os.path.join(base_dir, 'data', 'processed')
    izin_file = os.path.join(data_dir, 'sulawesi_izin_raw_details.csv')
    
    print("==========================================================")
    print(" ENGINE KLASIFIKASI KABUPATEN EKSTRAKTIF (DATA-DRIVEN) ")
    print("==========================================================\n")
    
    if not os.path.exists(izin_file):
        print(f"Error: File tidak ditemukan di {izin_file}")
        return

    df_izin = pd.read_csv(izin_file)
    
    # 1. Cleaning Kolom Lokasi
    # Data mentah ESDM mencatat "KAB. MOROWALI", kita bersihkan jadi "Morowali"
    df_izin['lokasi_clean'] = df_izin['lokasi_perizinan'].astype(str).str.replace('KAB. ', '', case=False)
    df_izin['lokasi_clean'] = df_izin['lokasi_clean'].str.replace('KOTA ', '', case=False)
    
    # Memisahkan area yang berada di lintas kabupaten (dipisah koma)
    df_izin['lokasi_clean'] = df_izin['lokasi_clean'].str.split(',')
    df_izin = df_izin.explode('lokasi_clean')
    df_izin['kabupaten'] = df_izin['lokasi_clean'].str.strip().str.title()
    
    # 2. Agregasi Total Luas Lahan Tambang (IUP) per Kabupaten
    df_agregat = df_izin.groupby('kabupaten')['luas_ha'].sum().reset_index()
    df_agregat = df_agregat.sort_values('luas_ha', ascending=False)
    
    # 3. Menerapkan Logika Data-Driven (Threshold)
    # Daripada hardcode nama kabupaten, kita definisikan threshold (misal > 25,000 Hektar)
    THRESHOLD_HA = 25000 
    
    df_agregat['is_ekstraktif_data_driven'] = df_agregat['luas_ha'] >= THRESHOLD_HA
    
    print(f"Batas Ambang (Threshold) Luas Konsesi : {THRESHOLD_HA:,} Hektar\n")
    
    print(f"{'KABUPATEN':<25} | {'TOTAL LUAS (HA)':<18} | {'STATUS BARU'}")
    print("-" * 65)
    
    ekstraktif_count = 0
    for idx, row in df_agregat.head(15).iterrows():
        status = "EKSTRAKTIF (Industri/Smelter)" if row['is_ekstraktif_data_driven'] else "Non-Ekstraktif"
        if row['is_ekstraktif_data_driven']:
            ekstraktif_count += 1
            
        print(f"{row['kabupaten']:<25} | {row['luas_ha']:<18,.2f} | {status}")
        
    print("-" * 65)
    print(f"\nKesimpulan: Secara otomatis (Data-Driven), algoritma menemukan {ekstraktif_count} Kabupaten yang")
    print(f"melewati batas ekstrem penguasaan lahan tambang di atas {THRESHOLD_HA:,} Ha.")
    print("Daftar kabupaten inilah yang seharusnya disuntikkan (inject) secara dinamis ke pipeline Demografi.")

if __name__ == "__main__":
    main()
