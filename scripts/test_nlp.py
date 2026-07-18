import pandas as pd
import re

df = pd.read_csv('data/processed/sulawesi_konflik_agraria_tanahkita.csv')
keywords = r'\b(sulawesi|sulsel|sulteng|sultra|sulut|sulbar|gorontalo|morowali|konawe|kolaka|bombana|poso|donggala|makassar|manado|minahasa|sangihe|mamuju|majene|polewali|halmahera|maluku utara|weda|obi|soroako|luwu|bantaeng|buton|muna|wakatobi|banggai|buol|toli-toli|parigi|luwuk|kendari|baubau|palu|bitung|tomohon|kotamobagu|gowa|takalar|jeneponto|bulukumba|sinjai|bone|maros|pangkep|barru|pinrang|enrekang|toraja|palopo)\b'
df_sul = df[df['judul'].str.contains(keywords, case=False, na=False, regex=True) | 
            df['deskripsi'].str.contains(keywords, case=False, na=False, regex=True) | 
            df['narasi'].str.contains(keywords, case=False, na=False, regex=True) | 
            df['lokasi'].str.contains(keywords, case=False, na=False, regex=True)]

# NLP Extraction (Regex) for Corporate Actors
text_corpus = " ".join((df_sul['judul'].fillna('') + " " + df_sul['deskripsi'].fillna('') + " " + df_sul['narasi'].fillna('')).tolist())

pts = re.findall(r'\b(?:PT|CV)\.?\s*[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*){0,3}\b', text_corpus)
# Clean up extra spaces
pts = [" ".join(pt.split()) for pt in pts]
print('Extracted Corporations:\n', pd.Series(pts).value_counts().head(15))

# Also extract Civil Society Actors using similar regex:
# Keywords like: JATAM, Walhi, AMAN, LBH, Konsorsium, Aliansi, Masyarakat Adat, Desa, Serikat
civils = re.findall(r'\b(?:Walhi|WALHI|Jatam|JATAM|AMAN|LBH|Aliansi|Serikat|Konsorsium|Masyarakat Adat|Warga Desa)\s*[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*){0,3}\b', text_corpus)
civils = [" ".join(cv.split()) for cv in civils]
print('\nExtracted Civils:\n', pd.Series(civils).value_counts().head(15))
