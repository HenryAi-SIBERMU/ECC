import pandas as pd

v2_loss = pd.read_csv('data/raw/klhk_gfw/mega_fetch_v2/tree_cover_loss_sulawesi_2001_2025.csv')
v3_loss = pd.read_csv('data/raw/klhk_gfw/mega_fetch_v3/tree_cover_loss_sulawesi_v3.csv')

v2_sum = v2_loss.groupby('province')['tree_cover_loss_ha'].sum()
v3_sum = v3_loss.groupby('province')['tree_cover_loss_ha'].sum()

df_comp = pd.DataFrame({'V2_ha': v2_sum, 'V3_ha': v3_sum})
df_comp['Diff_ha'] = df_comp['V3_ha'] - df_comp['V2_ha']
df_comp['Pct_Change'] = (df_comp['Diff_ha'] / df_comp['V2_ha']) * 100

print("="*75)
print("PERBANDINGAN DATASET MEGA FETCH V2 (Geostore Hash BBox) VS V3 (GADM Resmi)")
print("="*75)

for prov, row in df_comp.iterrows():
    print(f"\nPROVINSI: {prov}")
    print(f"   V2 (Geostore BBox) : {row['V2_ha']:>14,.2f} ha")
    print(f"   V3 (Resmi GADM)   : {row['V3_ha']:>14,.2f} ha")
    print(f"   Selisih Absolut   : {row['Diff_ha']:>14,.2f} ha")
    print(f"   Perubahan (%)     : {row['Pct_Change']:>+14.2f}%")

tot_v2 = v2_loss['tree_cover_loss_ha'].sum()
tot_v3 = v3_loss['tree_cover_loss_ha'].sum()
tot_diff = tot_v3 - tot_v2
tot_pct = (tot_diff / tot_v2) * 100

print("\n" + "="*75)
print("TOTAL KESELURUHAN SULAWESI (TREE COVER LOSS 2001-2025):")
print(f"   Total V2 (BBox)   : {tot_v2:>14,.2f} ha")
print(f"   Total V3 (Resmi)  : {tot_v3:>14,.2f} ha")
print(f"   Selisih Total     : {tot_diff:>14,.2f} ha ({tot_pct:+.2f}%)")
print("="*75)
