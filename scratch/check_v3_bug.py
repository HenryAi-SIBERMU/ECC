import pandas as pd
df = pd.read_csv('data/processed/sulawesi_gfw_master_1_dekade_2014_2023_v3.csv')
for i, row in df.head(5).iterrows():
    print(f"{row['Provinsi']} {row['Tahun']} - Total: {row['Total_Deforestasi_Ha']}, Primer: {row['Deforestasi_Hutan_Primer_Ha']}, Lindung: {row['Deforestasi_Kawasan_Lindung_Ha']}")
