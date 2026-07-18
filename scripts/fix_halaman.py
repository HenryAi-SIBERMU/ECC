import pandas as pd
import re

# Fix NGO Proxy dataset
df_ngo = pd.read_csv('data/processed/sulawesi_limbah_b3_ngo_proxy.csv')
if 'Halaman' not in df_ngo.columns:
    df_ngo['Halaman'] = df_ngo['Catatan'].str.extract(r'\((?:Hlm\.|Halaman)\s*([^)]+)\)')

# Manual overrides for the rows that might have failed regex
# Row with Huadi
mask_huadi = df_ngo['Kawasan/Perusahaan'].str.contains('Huadi', na=False)
df_ngo.loc[mask_huadi, 'Halaman'] = 'II-29, AMDAL PT Huadi'

# Row with Inalum
mask_inalum = df_ngo['Kawasan/Perusahaan'].str.contains('Inalum', na=False)
df_ngo.loc[mask_inalum, 'Halaman'] = '101, Laporan Tahunan 2020'

# Row with Ecoton/WALHI
mask_walhi = df_ngo['Catatan'].str.contains('Ecoton', na=False)
df_ngo.loc[mask_walhi, 'Halaman'] = '12-14, Riset WALHI & Ecoton'

df_ngo['Halaman'] = df_ngo['Halaman'].fillna('-')
df_ngo.to_csv('data/processed/sulawesi_limbah_b3_ngo_proxy.csv', index=False)

# Fix Limbah B3 dataset
df_limbah = pd.read_csv('data/processed/sulawesi_limbah_b3.csv')
if 'Halaman' not in df_limbah.columns:
    df_limbah['Halaman'] = df_limbah['Catatan'].str.extract(r'\((?:Hlm\.|Halaman)\s*([^)]+)\)')
df_limbah['Halaman'] = df_limbah['Halaman'].fillna('Tersebar di Dokumen (Ekstraksi Otomatis)')
df_limbah.to_csv('data/processed/sulawesi_limbah_b3.csv', index=False)
