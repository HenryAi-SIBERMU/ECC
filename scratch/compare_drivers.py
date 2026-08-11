import pandas as pd

v1 = pd.read_csv('data/raw/klhk_gfw/land_api_fetch/loss_by_driver_sulawesi_2001_2025.csv')
v3 = pd.read_csv('data/raw/klhk_gfw/land_api_fetch/loss_by_driver_sulawesi_2001_2025_v3.csv')

v1_sum = v1.groupby('province')['area_ha'].sum()
v3_sum = v3.groupby('province')['area_ha'].sum()

df_comp = pd.DataFrame({'V1_ha': v1_sum, 'V3_ha': v3_sum})
df_comp['Diff_ha'] = df_comp['V3_ha'] - df_comp['V1_ha']
df_comp['Pct_Change'] = (df_comp['Diff_ha'] / df_comp['V1_ha']) * 100

print("="*60)
print("PERBANDINGAN SEBERAPA PARAH KESALAHAN DATA V1 VS V3 RESMI")
print("="*60)

for prov, row in df_comp.iterrows():
    print(f"\nPROVINSI: {prov}")
    print(f"   V1 (Salah ID) : {row['V1_ha']:>12,.2f} ha")
    print(f"   V3 (Resmi GADM): {row['V3_ha']:>12,.2f} ha")
    print(f"   Selisih Absolut: {row['Diff_ha']:>12,.2f} ha")
    print(f"   Perubahan (%)  : {row['Pct_Change']:>+12.2f}%")

tot_v1 = v1['area_ha'].sum()
tot_v3 = v3['area_ha'].sum()
tot_diff = tot_v3 - tot_v1
tot_pct = (tot_diff / tot_v1) * 100

print("\n" + "="*60)
print("TOTAL KELURUHULAN SULAWESI:")
print(f"   Total V1 (Lama) : {tot_v1:>12,.2f} ha")
print(f"   Total V3 (Resmi): {tot_v3:>12,.2f} ha")
print(f"   Selisih Total   : {tot_diff:>12,.2f} ha ({tot_pct:+.2f}%)")
print("="*60)
