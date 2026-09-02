import pandas as pd
df = pd.read_csv('data/processed/sulawesi_pltu_captive.csv')
print('KOLOM PENENTU:')
print('- Status Column:', 'Status')
print('- Capacity Column:', 'Capacity (MW)')
print('- Plant/Unit Column:', 'Plant', '/', 'Unit')
print('\nRINCIAN ROW BERDASARKAN STATUS:')
for status, group in df.groupby('Status'):
    print(f"=== Status: {status} ===")
    print(f"Total Kapasitas: {group['Capacity (MW)'].sum()} MW")
    print(f"Jumlah Unit/Baris: {len(group)}")
    print(f"Nomor Baris (Row Index 0-based di CSV):")
    # limit to max 10 to not overflow, or just print all if small
    print(list(group.index))
    print()
