import pandas as pd
df = pd.read_csv('data/processed/kemenkes_bersih_all.csv')
print("Tahun yang berhasil diekstrak:")
print(sorted(df['tahun'].unique()))
