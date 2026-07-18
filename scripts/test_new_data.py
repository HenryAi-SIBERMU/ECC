import pandas as pd
SULAWESI = ['Sulawesi Utara', 'Sulawesi Tengah', 'Sulawesi Selatan', 'Sulawesi Tenggara', 'Gorontalo', 'Sulawesi Barat']

df_keluhan = pd.read_csv('data/raw/bps_keluhanumum/bps_kesehatan_provinsi_2014_2024.csv')
sul_keluhan = df_keluhan[df_keluhan['provinsi'].isin(SULAWESI)]
print("Keluhan rows:", len(sul_keluhan))

df_pad = pd.read_csv('data/raw/bps_pad/bps_pad_sulawesi_2016_2026.csv')
print("PAD rows:", len(df_pad))

df_pdrb = pd.read_csv('data/raw/bps_pdrb/bps_pdrb_sulawesi_2016_2026.csv')
print("PDRB rows:", len(df_pdrb))
