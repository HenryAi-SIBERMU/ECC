import pandas as pd
import numpy as pd_np # to use for nan

csv_path = r"C:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\data\processed\sulawesi_faskes_agregat_v3.csv"
df = pd.read_csv(csv_path)

def split_nilai(row):
    variabel = str(row['variabel']).lower()
    nilai = str(row['nilai']).strip()
    
    is_persen = '%' in variabel or 'persentase' in variabel or '%' in nilai
    
    if is_persen:
        return pd.Series([pd_np.nan, nilai])
    else:
        return pd.Series([nilai, pd_np.nan])

df[['nilai_absolut', 'nilai_persen']] = df.apply(split_nilai, axis=1)

# Drop old 'nilai' column
df = df.drop(columns=['nilai'])

# Reorder columns to put nilai_absolut and nilai_persen before sumber_file
cols = list(df.columns)
cols.remove('nilai_absolut')
cols.remove('nilai_persen')
cols.remove('sumber_file')

new_cols = cols + ['nilai_absolut', 'nilai_persen', 'sumber_file']
df = df[new_cols]

df.to_csv(csv_path, index=False)
print(f"Updated {csv_path} with split nilai_absolut and nilai_persen columns.")
