import pandas as pd
df = pd.read_csv('data/processed/kemenkes_bersih_2021.csv')
zeros = df[df['nilai'] == 0]
if len(zeros) > 0:
    print("Ada nilai 0:")
    print(zeros)
else:
    print("Tidak ada nilai 0. Aman!")
