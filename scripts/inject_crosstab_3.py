import pandas as pd

with open('crosstab_snippet.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace variables
code = code.replace('df_gfw, df_izin', 'df_iku, df_kes_ispa')
code = code.replace('Total_Deforestasi_Ha', 'Total_ISPA')
code = code.replace('Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha', 'Total_Diare')
code = code.replace('Jumlah_Izin_Baru', 'IKU_Point')
code = code.replace('Total_Luas_Konsesi_Baru_Ha', 'IKU_Point_Alt')
code = code.replace("df_panel = pd.merge(df_iku, df_kes_ispa, on=['Provinsi', 'Tahun'], how='left').fillna({'IKU_Point': 0, 'IKU_Point_Alt': 0})", """
import scipy.stats as stats

df_kes_ispa = df_kes[df_kes['indikator'] == 'Kasus ISPA/Pneumonia'][['provinsi', 'tahun', 'nilai']].rename(columns={'nilai': 'Total_ISPA', 'provinsi': 'Provinsi', 'tahun': 'Tahun'})
df_kes_diare = df_kes[df_kes['indikator'] == 'Kasus Diare Dilayani'][['provinsi', 'tahun', 'nilai']].rename(columns={'nilai': 'Total_Diare', 'provinsi': 'Provinsi', 'tahun': 'Tahun'})
df_panel = pd.merge(df_kes_ispa, df_iku, on=['Provinsi', 'Tahun'], how='inner')
df_panel = pd.merge(df_panel, df_kes_diare, on=['Provinsi', 'Tahun'], how='inner')
df_panel['IKU_Point'] = df_panel['IKU']
df_panel['IKU_Point_Alt'] = df_panel['IKU']
""")

code = code.replace('"Jumlah Izin Baru (IUP)"', '"Skor Indeks Kualitas Udara (IKU)"')
code = code.replace('"Luas Konsesi Baru (Hektar)"', '"Skor IKU (Alternatif)"')
code = code.replace('"Total Deforestasi Alam (Hektar)"', '"Total Kasus ISPA/Pneumonia"')
code = code.replace('"Deforestasi Komoditas Tambang/Sawit (Hektar)"', '"Total Kasus Diare"')

code = code.replace('Intensitas Ekspansi vs Deforestasi', 'Penurunan Kualitas Udara vs Ledakan Penyakit')
code = code.replace('lonjakan ekspansi ekstraktif', 'penurunan kualitas udara (IKU)')
code = code.replace('kebangkrutan ekologis (deforestasi)', 'ledakan penyakit pernapasan dan lingkungan')
code = code.replace('Tekanan Ekspansi', 'Faktor Lingkungan')
code = code.replace('Indikator Ekspansi', 'Indikator Lingkungan')

code = code.replace('Pilih Indikator Dampak', 'Pilih Indikator Penyakit')
code = code.replace('Dampak Ekologis', 'Dampak Kesehatan')

# Save to append
with open('pages/3_Beban_Kesehatan.py', 'a', encoding='utf-8') as f:
    f.write('\\n\\n')
    f.write(code)
