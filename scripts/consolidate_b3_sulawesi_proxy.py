import pandas as pd
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

def generate_ngo_proxy_b3():
    print("Mengonsolidasikan data Proksi Limbah B3 Sulawesi (Estimasi NGO/Kajian)...")
    
    # Data diekstrak dari kajian WALHI, AEER, JATAM, dan pemberitaan (Dorking OSINT)
    # Karena ini data proksi, rentang tahun lebih fleksibel (kisaran 2020-2024)
    data = [
        # Sulawesi Tengah (IMIP Morowali)
        {
            'Provinsi': 'Sulawesi Tengah', 
            'Kawasan/Perusahaan': 'IMIP (Morowali)', 
            'Jenis Limbah B3': 'Slag & Tailing HPAL',
            'Estimasi Timbulan (Ton/Tahun)': 12000000, 
            'Sumber Referensi': 'Temuan KLH/BPLH & Laporan AEER (2024-2025)',
            'Catatan': 'Timbunan tanpa izin mencapai >12 juta ton. Sebagian dimanfaatkan jadi batako (40.000 unit/hari).'
        },
        # Sulawesi Tenggara (VDNI Konawe)
        {
            'Provinsi': 'Sulawesi Tenggara', 
            'Kawasan/Perusahaan': 'VDNI (Konawe) & Sekitarnya', 
            'Jenis Limbah B3': 'Slag Feronikel',
            'Estimasi Timbulan (Ton/Tahun)': 6500000, # Estimasi 90% dari 7.28jt ton bijih olahan
            'Sumber Referensi': 'Data Produksi VDNI & Kajian WALHI',
            'Catatan': 'Tahun 2020 mengolah 7,28 juta ton bijih nikel. Mayoritas industri nikel nasional (13 juta ton slag) berada di wilayah ini.'
        },
        # Sulawesi Selatan (Huadi Bantaeng)
        {
            'Provinsi': 'Sulawesi Selatan', 
            'Kawasan/Perusahaan': 'Huadi Nickel Alloy (Bantaeng)', 
            'Jenis Limbah B3': 'Slag EAF',
            'Estimasi Timbulan (Ton/Tahun)': 1000000, # Estimasi konservatif
            'Sumber Referensi': 'Kajian JATAM & Akademis (Unhas/BRIN)',
            'Catatan': 'Volume slag mencapai 90% dari total bahan baku yang diproses di tungku EAF. Dimanfaatkan untuk penahan abrasi.'
        }
    ]
    
    df = pd.DataFrame(data)
    
    out_dir = BASE_DIR / 'data' / 'processed'
    os.makedirs(out_dir, exist_ok=True)
    
    out_path = out_dir / 'sulawesi_limbah_b3_ngo_proxy.csv'
    df.to_csv(out_path, index=False)
    
    print(f"Data Proksi Limbah B3 Sulawesi berhasil disimpan di:\n{out_path}")
    print("\nPreview Dataset:")
    print(df[['Provinsi', 'Kawasan/Perusahaan', 'Estimasi Timbulan (Ton/Tahun)']])

if __name__ == "__main__":
    generate_ngo_proxy_b3()
