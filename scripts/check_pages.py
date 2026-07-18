import pandas as pd
df1 = pd.read_csv('data/processed/sulawesi_limbah_b3.csv')
print("--- LIMBAH B3 ---")
for idx, row in df1.iterrows():
    print(f"[{idx}] Halaman:{row.get('Halaman', 'NA')} | Catatan:{row.get('Catatan', '')}")
    
df2 = pd.read_csv('data/processed/sulawesi_limbah_b3_ngo_proxy.csv')
print("\n--- NGO PROXY ---")
for idx, row in df2.iterrows():
    print(f"[{idx}] Halaman:{row.get('Halaman', 'NA')} | Catatan:{row.get('Catatan', '')}")
