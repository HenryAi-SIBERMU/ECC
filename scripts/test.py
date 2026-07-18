import pandas as pd
df = pd.read_csv('data/processed/sulawesi_limbah_b3.csv')
print(df.groupby('Provinsi')['Estimasi Timbulan (Ton/Tahun)'].sum())
