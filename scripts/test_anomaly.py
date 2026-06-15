import pandas as pd

df = pd.read_csv('data/processed/sulawesi_konflik_agraria_tanahkita.csv')
df['dampak_masyarakat_jiwa'] = pd.to_numeric(df['dampak_masyarakat_jiwa'], errors='coerce').fillna(0)
df['luas_ha'] = pd.to_numeric(df['luas_ha'], errors='coerce').fillna(0)

def map_sektor(status):
    status = str(status).lower()
    if 'kebun' in status: return 'Perkebunan'
    if 'tambang' in status: return 'Pertambangan'
    if 'hutan' in status: return 'Kehutanan'
    if any(x in status for x in ['infrastruktur', 'bendungan', 'transmigrasi', 'energi', 'fasilitas', 'jalan', 'industri']): return 'Infrastruktur & PSN'
    if any(x in status for x in ['pariwisata', 'laut', 'pesisir']): return 'Pariwisata & Pesisir'
    return 'Lainnya'

df['Sektor_Grup'] = df['status'].apply(map_sektor)

with open('anomaly_report.txt', 'w', encoding='utf-8') as f:
    f.write('--- SPIKE JIWA 2012 (Pertambangan) ---\n')
    spike1 = df[(df['tahun'] == 2012) & (df['Sektor_Grup'] == 'Pertambangan')].nlargest(2, 'dampak_masyarakat_jiwa')
    for idx, r in spike1.iterrows():
        f.write(f"Judul: {r['judul']}\nPerusahaan: {r['keterlibatan_perusahaan']}\nPemerintah: {r['keterlibatan_pemerintah']}\nSumber: {r['sumber']}\nJiwa: {r['dampak_masyarakat_jiwa']}\nNarasi: {str(r['narasi'])[:400]}...\n\n")

    f.write('--- SPIKE JIWA 2019 (Kehutanan & PSN) ---\n')
    spike2 = df[(df['tahun'] == 2019)].nlargest(3, 'dampak_masyarakat_jiwa')
    for idx, r in spike2.iterrows():
        f.write(f"Judul: {r['judul']}\nSektor: {r['Sektor_Grup']}\nPerusahaan: {r['keterlibatan_perusahaan']}\nPemerintah: {r['keterlibatan_pemerintah']}\nSumber: {r['sumber']}\nJiwa: {r['dampak_masyarakat_jiwa']}\nNarasi: {str(r['narasi'])[:400]}...\n\n")

    f.write('--- SPIKE AREA 2010 (Pertambangan) ---\n')
    spike3 = df[(df['tahun'] == 2010)].nlargest(2, 'luas_ha')
    for idx, r in spike3.iterrows():
        f.write(f"Judul: {r['judul']}\nSektor: {r['Sektor_Grup']}\nPerusahaan: {r['keterlibatan_perusahaan']}\nPemerintah: {r['keterlibatan_pemerintah']}\nSumber: {r['sumber']}\nLuas: {r['luas_ha']}\nNarasi: {str(r['narasi'])[:400]}...\n\n")

    f.write('--- SPIKE AREA 2015 (Pertambangan & Kehutanan) ---\n')
    spike4 = df[(df['tahun'] == 2015)].nlargest(3, 'luas_ha')
    for idx, r in spike4.iterrows():
        f.write(f"Judul: {r['judul']}\nSektor: {r['Sektor_Grup']}\nPerusahaan: {r['keterlibatan_perusahaan']}\nPemerintah: {r['keterlibatan_pemerintah']}\nSumber: {r['sumber']}\nLuas: {r['luas_ha']}\nNarasi: {str(r['narasi'])[:400]}...\n\n")
