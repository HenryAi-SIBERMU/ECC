import pandas as pd

df = pd.read_csv('data/processed/amdal_parsed_limbah_b3.csv')
found = df[df['status'] == 'DITEMUKAN']

print(f"Total baris  : {len(df)}")
print(f"Baris temuan : {len(found)}")
print(f"Jumlah PDF   : {df['file'].nunique()}")

print("\n=== TOP TEMUAN DENGAN DATA VOLUME ===")
with_vol = found[found['volume_temuan'].str.len() > 1].drop_duplicates(subset=['file','volume_temuan'])
for _, r in with_vol[['file','volume_temuan','keyword_hit']].head(20).iterrows():
    fname = str(r['file'])[:45]
    vol   = str(r['volume_temuan'])[:80]
    kw    = str(r['keyword_hit'])
    print(f"  [{kw}] {fname}")
    print(f"        VOLUME: {vol}")
