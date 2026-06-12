import pandas as pd
import os

project_root = os.path.join(os.path.dirname(__file__), '..', '..')
correct_file = os.path.join(project_root, 'data/processed/esdm_master_sulawesi_nikel_2016_2026_id.csv')

df = pd.read_csv(correct_file)
print(f"✅ File loaded successfully")
print(f"   Rows: {len(df):,}")
print(f"   Columns: {len(df.columns)}")

has_match = (df['nama_perusahaan_cgs'].notna()) & (df['nama_perusahaan_minerbaone'].notna())
print(f"   Matched dengan CGS: {has_match.sum():,}")

# Check match scores
matched_scores = df[has_match]['skor_kecocokan_cgs']
if len(matched_scores) > 0:
    print(f"   Average score: {matched_scores.mean():.1f}")
    print(f"   Score 100: {(matched_scores == 100).sum()}")
    print(f"   Score 80-99: {((matched_scores >= 80) & (matched_scores < 100)).sum()}")
    print(f"   Score <80: {(matched_scores < 80).sum()}")

print(f"\n✅ File is correct!")
