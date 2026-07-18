import pandas as pd
df_konflik = pd.read_csv('data/processed/sulawesi_konflik_agraria_tanahkita.csv')
keywords = r'\b(sulawesi|sulsel|sulteng|sultra|sulut|sulbar|gorontalo|morowali|konawe|kolaka|bombana|poso|donggala|makassar|manado|minahasa|sangihe|mamuju|majene|polewali|halmahera|maluku utara|weda|obi|soroako|luwu|bantaeng|buton|muna|wakatobi|banggai|buol|toli-toli|parigi|luwuk|kendari|baubau|palu|bitung|tomohon|kotamobagu|gowa|takalar|jeneponto|bulukumba|sinjai|bone|maros|pangkep|barru|pinrang|enrekang|toraja|palopo)\b'
mask = df_konflik['judul'].str.contains(keywords, case=False, na=False, regex=True) | \
       df_konflik['deskripsi'].str.contains(keywords, case=False, na=False, regex=True) | \
       df_konflik['narasi'].str.contains(keywords, case=False, na=False, regex=True) | \
       df_konflik['lokasi'].str.contains(keywords, case=False, na=False, regex=True)
df_konflik = df_konflik[mask].copy()

def extract_actors(column):
    actors = []
    for val in column.dropna():
        parts = [x.strip() for x in str(val).split('|') if x.strip()]
        actors.extend(parts)
    return pd.Series(actors).value_counts().reset_index()

df_aktor_masyarakat = extract_actors(df_konflik['keterlibatan_masyarakat'])
df_aktor_masyarakat.columns = ['Aktor', 'Frekuensi']
df_aktor_perusahaan = extract_actors(df_konflik['keterlibatan_perusahaan'])
df_aktor_perusahaan.columns = ['Aktor', 'Frekuensi']

print("Top 10 Korporasi:")
print(df_aktor_perusahaan.head(10).to_markdown())
print("\nTop 10 Masyarakat/Sipil:")
print(df_aktor_masyarakat[~df_aktor_masyarakat['Aktor'].str.contains('Masyarakat Desa|Masyarakat Kabupaten|Warga|Petani', case=False, na=False)].head(10).to_markdown())
