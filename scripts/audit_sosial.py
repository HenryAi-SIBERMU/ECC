import pandas as pd

# ====================================================
# AUDIT FORENSIK: MATRIKS DAYA DUKUNG SOSIAL
# ====================================================

print("=" * 60)
print("AUDIT 1: ANGKA AKTUAL DATASET KONFLIK")
print("=" * 60)

df = pd.read_csv('data/processed/sulawesi_konflik_agraria_tanahkita.csv')
df_fpic = pd.read_csv('data/processed/sulawesi_konflik_tambang_fpic.csv')

# Konversi numerik
for col in ['jumlah_ditangkap', 'jumlah_tewas', 'jumlah_luka', 'luas_ha', 'dampak_masyarakat_jiwa']:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# Filter sektor tambang
df_tambang = df[df['sektor'].str.contains('ambang|nikel|mineral|Tambang|Pertambangan', case=False, na=False)]

print(f"Total kasus konflik Sulawesi: {len(df)}")
print(f"Kasus sektor TAMBANG (nikel/mineral): {len(df_tambang)}")
print(f"FPIC konflik dataset: {len(df_fpic)}")
print()
print("--- ANGKA TAMBANG SAJA ---")
print(f"Warga ditangkap (kriminalisasi): {df_tambang['jumlah_ditangkap'].sum():.0f}")
print(f"Warga tewas: {df_tambang['jumlah_tewas'].sum():.0f}")
print(f"Warga luka-luka: {df_tambang['jumlah_luka'].sum():.0f}")
print(f"Jiwa terdampak: {df_tambang['dampak_masyarakat_jiwa'].sum():,.0f}")
print(f"Luas Ha dikonflikkan: {df_tambang['luas_ha'].sum():,.0f}")
print(f"Indikasi kriminalisasi: {df_tambang['indikasi_kriminalisasi'].sum():.0f}")
print()
print("--- BREAKDOWN SEKTOR ---")
print(df['sektor'].value_counts().head(10))

print()
print("=" * 60)
print("AUDIT 2: EVALUASI MODEL SKORING SOSIAL SAAT INI")
print("=" * 60)

# Replika kalkulasi skor yang ada di page 6
kasus_fpic = len(df_fpic)
jiwa_terdampak = df_tambang['dampak_masyarakat_jiwa'].sum()
insiden_krim = df_tambang['indikasi_kriminalisasi'].sum()

skor_sosial_1 = min(10.0, (kasus_fpic / 5) * 10)
skor_sosial_2 = min(10.0, (jiwa_terdampak / 100_000) * 10)
skor_sosial_3 = min(10.0, (insiden_krim / 50) * 10)
skor_akumulasi_sosial = (skor_sosial_1 + skor_sosial_2 + skor_sosial_3) / 3

print(f"kasus_fpic: {kasus_fpic} | skor_1: {skor_sosial_1:.1f}")
print(f"jiwa_terdampak: {jiwa_terdampak:,.0f} | skor_2: {skor_sosial_2:.1f}")
print(f"insiden_krim: {insiden_krim:.0f} | skor_3: {skor_sosial_3:.1f}")
print(f"SKOR AKUMULASI SOSIAL: {skor_akumulasi_sosial:.2f} / 10")
print()
print("=== VERDICT BIAS ===")
for label, val, threshold in [
    ("FPIC (kasus/5)", kasus_fpic, 5),
    ("Jiwa terdampak (jiwa/100k)", jiwa_terdampak, 100_000),
    ("Kriminalisasi (kasus/50)", insiden_krim, 50),
]:
    rasio = val / threshold
    bias = "SANGAT MUDAH DILAMPAUI" if rasio > 5 else ("OK" if rasio >= 0.8 else "PERLU REVISI (TERLALU LONGGAR)")
    print(f"  {label}: {val:,.0f} / {threshold:,} = {rasio:.1f}x → {bias}")

print()
print("=" * 60)
print("AUDIT 3: PAGE 1-5 YANG ADA DATASET SOSIAL YANG BISA DIPINDAH")
print("=" * 60)

# Page 4 - Konflik Sosial
df_konflik_all = pd.read_csv('data/processed/sulawesi_konflik_agraria_tanahkita.csv')
print(f"Page 4 sudah ada: {len(df_konflik_all)} kasus konflik Sulawesi")
print("Kolom berharga:", ['sektor', 'jumlah_ditangkap', 'jumlah_tewas', 'luas_ha', 'dampak_masyarakat_jiwa', 'indikasi_kriminalisasi'])

# Faskes - belum terpakai di sosial
df_faskes = pd.read_csv('data/processed/sulawesi_faskes_agregat.csv')
print()
print(f"Dataset FASKES: {len(df_faskes)} baris, {df_faskes['tahun'].unique()}")
print(f"Jenis faskes: {df_faskes['jenis'].unique()}")
faskes_tren = df_faskes.groupby(['tahun','provinsi'])['jumlah'].sum()
print(f"Total faskes Sulteng 2024: {df_faskes[(df_faskes['tahun']==2024) & (df_faskes['provinsi']=='Sulawesi Tengah')]['jumlah'].sum()}")

print()
print("=== POTENSI TAB BARU ORGANIK ===")
print("Tab 4 POTENSIAL: Defisit Layanan Kesehatan")
print("  - Dataset: sulawesi_faskes_agregat.csv")
print("  - Narasi: Pertambangan masif tp rasio RS/Puskesmas/Nakes per 100k penduduk justru stagnasi")
print("  - Dataset kesehatan: sulawesi_kesehatan_detail_2014_2024.csv (cek konfirmasi)")
