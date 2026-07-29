import pandas as pd
import scipy.stats as scipy_stats
import numpy as np

# Load data
df_ika = pd.read_csv('data/processed/sulawesi_ika_2016_2024.csv')
df_ika = df_ika.rename(columns={'Indeks Kualitas Air': 'IKA'})

df_kes = pd.read_csv('data/processed/sulawesi_kesehatan_detail_2014_2024.csv')
df_diare = df_kes[df_kes['indikator'] == 'Kasus Diare Dilayani'].groupby(['provinsi','tahun'])['nilai'].sum().reset_index()
df_diare.columns = ['Provinsi', 'Tahun', 'Total_Diare']

# Merge
df = df_ika.merge(df_diare, on=['Provinsi','Tahun'], how='inner')

# Chi-Square Crosstab
ika_median = df['IKA'].median()
diare_median = df['Total_Diare'].median()

df['Kategori_IKA'] = np.where(df['IKA'] < ika_median, 'Buruk', 'Baik')
df['Kategori_Diare'] = np.where(df['Total_Diare'] > diare_median, 'Tinggi', 'Rendah')

crosstab = pd.crosstab(df['Kategori_IKA'], df['Kategori_Diare'])
chi2, p_crosstab, dof, expected = scipy_stats.chi2_contingency(crosstab)

print("CROSSTAB (Total Diare):")
print(crosstab)
print(f"Chi2 P-value = {p_crosstab:.4f}")

# Normalized Crosstab
df_pop = pd.read_csv('data/processed/sulawesi_demografi_master_fase4.csv')
df_pop_prov = df_pop.groupby(['provinsi','tahun'])['jumlah_penduduk_rb'].sum().reset_index()
df_pop_prov.columns = ['Provinsi', 'Tahun', 'Pop_rb']
df_pop_prov['Provinsi'] = df_pop_prov['Provinsi'].replace({'Sulawesi Tengah': 'Sulawesi Tengah', 'Sulawesi Tenggara': 'Sulawesi Tenggara', 'Sulawesi Selatan': 'Sulawesi Selatan', 'Sulawesi Utara': 'Sulawesi Utara', 'Sulawesi Barat': 'Sulawesi Barat', 'Gorontalo': 'Gorontalo'})

df = df.merge(df_pop_prov, on=['Provinsi','Tahun'], how='inner')
df['Diare_IR'] = (df['Total_Diare'] / (df['Pop_rb'] * 1000)) * 100000

ir_median = df['Diare_IR'].median()
df['Kategori_Diare_IR'] = np.where(df['Diare_IR'] > ir_median, 'Tinggi', 'Rendah')

crosstab_ir = pd.crosstab(df['Kategori_IKA'], df['Kategori_Diare_IR'])
chi2_ir, p_crosstab_ir, dof, expected = scipy_stats.chi2_contingency(crosstab_ir)

print("\nCROSSTAB (Diare Incidence Rate):")
print(crosstab_ir)
print(f"Chi2 P-value = {p_crosstab_ir:.4f}")

# Also try splitting by Sentra vs Non-Sentra and doing Crosstab there?
sentra = ["Sulawesi Tengah", "Sulawesi Tenggara"]
df['is_sentra'] = df['Provinsi'].isin(sentra)
crosstab_sentra = pd.crosstab(df['is_sentra'], df['Kategori_Diare_IR'])
chi2_s, p_s, dof, ex = scipy_stats.chi2_contingency(crosstab_sentra)
print("\nCROSSTAB (Sentra Tambang vs Diare IR Tinggi):")
print(crosstab_sentra)
print(f"Chi2 P-value = {p_s:.4f}")

