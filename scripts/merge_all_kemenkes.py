import pandas as pd
import glob

# Cari semua file kemenkes_bersih_*.csv
files = glob.glob('data/processed/kemenkes_bersih_*.csv')

all_dfs = []
for f in files:
    if 'kemenkes_bersih_all.csv' in f:
        continue
    df = pd.read_csv(f)
    all_dfs.append(df)

# Gabung semuanya
master_df = pd.concat(all_dfs, ignore_index=True)

# Hapus duplikat barangkali ada (opsional)
master_df = master_df.drop_duplicates()

# Sort berdasarkan provinsi, lalu tahun, lalu indikator
master_df = master_df.sort_values(by=['provinsi', 'tahun', 'indikator']).reset_index(drop=True)

output_path = 'data/processed/kemenkes_bersih_all.csv'
master_df.to_csv(output_path, index=False)
print(f"Berhasil menggabungkan {len(files)} file!")
print(f"Total baris: {len(master_df)}")
print(f"Tersimpan di: {output_path}")
