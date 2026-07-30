import pandas as pd
import scipy.stats as scipy_stats
import numpy as np

df_ika = pd.read_csv('data/processed/sulawesi_ika_2016_2024.csv')
df_ika = df_ika.rename(columns={'Indeks Kualitas Air': 'IKA'})
df_kes = pd.read_csv('data/processed/sulawesi_kesehatan_detail_2014_2024.csv')

df_diare = df_kes[df_kes['indikator'] == 'Kasus Diare Dilayani'].groupby(['provinsi','tahun'])['nilai'].sum().reset_index()
df_diare.columns = ['Provinsi', 'Tahun', 'Total_Diare']

df = df_ika.merge(df_diare, on=['Provinsi','Tahun'], how='inner')
df = df.sort_values(['Provinsi','Tahun'])
df['delta_IKA'] = df.groupby('Provinsi')['IKA'].diff()
df['delta_Diare'] = df.groupby('Provinsi')['Total_Diare'].diff()
df_fe = df.dropna(subset=['delta_IKA','delta_Diare'])

slope, intercept, r, p, se = scipy_stats.linregress(df_fe['delta_IKA'].values, df_fe['delta_Diare'].values)
r2 = r**2
sig = "SIGNIFIKAN" if p < 0.05 else "TIDAK SIGNIFIKAN"
print(f"=== Fixed-Effects (DELTA) ===")
print(f"n={len(df_fe)}, slope={slope:.1f}, R2={r2:.4f}, P={p:.4f} => {sig}")

slope2, intercept2, r2v, p2, se2 = scipy_stats.linregress(df['IKA'].dropna().values, df.loc[df['IKA'].notna(),'Total_Diare'].values)
sig2 = "SIGNIFIKAN" if p2 < 0.05 else "TIDAK SIGNIFIKAN"
print(f"\n=== OLS Biasa (Cross-sectional) ===")
print(f"slope={slope2:.1f}, R2={r2v**2:.4f}, P={p2:.4f} => {sig2}")

print("\n=== Data per Provinsi ===")
print(df_fe.groupby('Provinsi')[['delta_IKA','delta_Diare']].mean().round(2).to_string())
