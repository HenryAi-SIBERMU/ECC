import pandas as pd

df_old = pd.read_csv('data/processed/sulawesi_gfw_master_1_dekade_2014_2023.csv')
df_new = pd.read_csv('data/processed/sulawesi_gfw_master_1_dekade_2014_2023_v3.csv')

# Sum up total values for key columns across all years (2014-2023) and all provinces
cols_to_compare = [
    'Total_Deforestasi_Ha', 
    'Deforestasi_Hutan_Primer_Ha', 
    'Deforestasi_Kawasan_Lindung_Ha'
]

print("=== COMPARISON REPORT (TOTAL SULAWESI 2014-2023) ===")
for col in cols_to_compare:
    old_sum = df_old[col].sum()
    new_sum = df_new[col].sum()
    diff = old_sum - new_sum
    pct_diff = (diff / new_sum * 100) if new_sum > 0 else 0
    print(f"{col}:")
    print(f"  Old (Kotak/BBox) : {old_sum:,.2f} Ha")
    print(f"  New (Admin Asli) : {new_sum:,.2f} Ha")
    print(f"  Selisih          : {diff:,.2f} Ha (Overestimasi {pct_diff:.1f}%)")

print("\n=== PER PROVINCE (Total Deforestasi Ha) ===")
old_prov = df_old.groupby('Provinsi')['Total_Deforestasi_Ha'].sum()
new_prov = df_new.groupby('Provinsi')['Total_Deforestasi_Ha'].sum()

for p in old_prov.index:
    o_val = old_prov[p]
    n_val = new_prov.get(p, 0)
    d = o_val - n_val
    p_diff = (d / n_val * 100) if n_val > 0 else 0
    print(f"{p}: Old={o_val:,.0f}, New={n_val:,.0f} -> Overestimasi {p_diff:.1f}%")

