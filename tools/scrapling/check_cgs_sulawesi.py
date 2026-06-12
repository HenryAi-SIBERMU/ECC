import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, '..', '..')
excel_path = os.path.join(project_root, 'data/raw/ESDM/CGS_Nickel_Smelter_Dataset_V1.xlsx')

df = pd.read_excel(excel_path)
sulawesi = df[df['Province'].str.contains('Sulawesi', case=False, na=False)]

print(f'Total CGS smelters di Sulawesi: {len(sulawesi)}')
print(f'\nBreakdown by Province:')
print(sulawesi['Province'].value_counts())
print(f'\nSmelter names:')
for name in sulawesi['Smelter Name'].sort_values():
    print(f'  - {name}')
