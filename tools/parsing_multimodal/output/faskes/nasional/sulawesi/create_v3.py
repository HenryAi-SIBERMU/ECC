import pandas as pd
import glob
import os
import re

v2_path = r"C:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\data\processed\sulawesi_faskes_agregat_v2.csv"
v3_path = r"C:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\data\processed\sulawesi_faskes_agregat_v3.csv"
md_dir = r"C:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\tools\parsing_multimodal\output\faskes\nasional\sulawesi"

df = pd.read_csv(v2_path)

# Prepare a dict to store the updates
# updates[(tahun, provinsi, jenis)] = (jumlah, filename, title)
updates = {}

def read_md_table(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    title = ""
    for line in lines:
        if line.startswith('#'):
            title = line.strip().replace('#', '').strip()
            break
            
    header = []
    data_rows = []
    
    in_table = False
    for line in lines:
        if line.strip().startswith('|'):
            row = [x.strip() for x in line.split('|')[1:-1]]
            
            # Check for separator
            chars_in_line = set(line.strip().replace('|', '').replace('-', '').replace(':', '').replace(' ', ''))
            
            if len(chars_in_line) == 0:
                in_table = True
            elif not in_table:
                header = row
            else:
                data_rows.append(row)
    return title, header, data_rows, os.path.basename(filepath)

def safe_int(val):
    if not val:
        return 0
    return int(val.replace('.', '').replace(',', ''))

# 1. PUSKESMAS 2014-2018
title, header, data_rows, fname = read_md_table(os.path.join(md_dir, 'sulawesi_2018_Puskesmas_page_393.md'))
for row in data_rows:
    prov = row[1]
    updates[(2014, prov, 'Puskesmas')] = (safe_int(row[2]), fname, title)
    updates[(2015, prov, 'Puskesmas')] = (safe_int(row[3]), fname, title)
    updates[(2016, prov, 'Puskesmas')] = (safe_int(row[4]), fname, title)
    updates[(2017, prov, 'Puskesmas')] = (safe_int(row[5]), fname, title)
    updates[(2018, prov, 'Puskesmas')] = (safe_int(row[6]), fname, title)

# 2. PUSKESMAS 2015-2019 (overwrites 2015-2018 if different)
title, header, data_rows, fname = read_md_table(os.path.join(md_dir, 'sulawesi_2019_Puskesmas_page_321.md'))
for row in data_rows:
    prov = row[1]
    updates[(2019, prov, 'Puskesmas')] = (safe_int(row[6]), fname, title)
    
# 3. PUSKESMAS 2020
title, header, data_rows, fname = read_md_table(os.path.join(md_dir, 'sulawesi_2020_Puskesmas_page_309.md'))
for row in data_rows:
    prov = row[1]
    updates[(2020, prov, 'Puskesmas')] = (safe_int(row[5]), fname, title)
    
# 4. PUSKESMAS 2021
title, header, data_rows, fname = read_md_table(os.path.join(md_dir, 'sulawesi_2021_Puskesmas_page_357.md'))
for row in data_rows:
    prov = row[1]
    updates[(2021, prov, 'Puskesmas')] = (safe_int(row[4]), fname, title)
    
# 5. PUSKESMAS 2022
title, header, data_rows, fname = read_md_table(os.path.join(md_dir, 'sulawesi_2022_Puskesmas_page_366.md'))
for row in data_rows:
    prov = row[1]
    # Column 2 + Column 3 (0-indexed: Belum Memenuhi, Memenuhi)
    tot = safe_int(row[2]) + safe_int(row[3])
    updates[(2022, prov, 'Puskesmas')] = (tot, fname, title)

# 6. PUSKESMAS 2023
title, header, data_rows, fname = read_md_table(os.path.join(md_dir, 'sulawesi_2023_Puskesmas_page_370.md'))
for row in data_rows:
    prov = row[1]
    updates[(2023, prov, 'Puskesmas')] = (safe_int(row[4]), fname, title)
    
# 7. PUSKESMAS 2024
title, header, data_rows, fname = read_md_table(os.path.join(md_dir, 'sulawesi_2024_Puskesmas_page_356.md'))
for row in data_rows:
    prov = row[1]
    updates[(2024, prov, 'Puskesmas')] = (safe_int(row[4]), fname, title)
    
# 8. RUMAH SAKIT 2022
title, header, data_rows, fname = read_md_table(os.path.join(md_dir, 'sulawesi_2022_Rumah_Sakit_page_373.md'))
for row in data_rows:
    prov = row[1]
    # RS Umum + RS Khusus (Column 14 + Column 15)
    tot = safe_int(row[14]) + safe_int(row[15])
    updates[(2022, prov, 'Rumah Sakit')] = (tot, fname, title)
    
# 9. RUMAH SAKIT 2023
title, header, data_rows, fname = read_md_table(os.path.join(md_dir, 'sulawesi_2023_Rumah_Sakit_page_377.md'))
for row in data_rows:
    prov = row[1]
    tot = safe_int(row[14]) + safe_int(row[15])
    updates[(2023, prov, 'Rumah Sakit')] = (tot, fname, title)
    
# 10. RUMAH SAKIT 2024
title, header, data_rows, fname = read_md_table(os.path.join(md_dir, 'sulawesi_2024_Rumah_Sakit_page_363.md'))
for row in data_rows:
    prov = row[1]
    tot = safe_int(row[14]) + safe_int(row[15])
    updates[(2024, prov, 'Rumah Sakit')] = (tot, fname, title)

# Function to normalize province name
def norm_prov(p):
    return p.lower().strip()

# Create a normalized updates dict
norm_updates = {}
for k, v in updates.items():
    year, prov, jenis = k
    norm_updates[(int(year), norm_prov(prov), jenis)] = v

# Update DataFrame
changes_made = 0
for idx, row in df.iterrows():
    year = int(row['tahun'])
    prov = norm_prov(row['provinsi'])
    jenis = row['jenis']
    key = (year, prov, jenis)
    
    if key in norm_updates:
        new_val, fname, title = norm_updates[key]
        df.at[idx, 'jumlah'] = new_val
        df.at[idx, 'sumber_kutipan'] = f"Tabel Ekstraksi MD: {title}"
        df.at[idx, 'sumber_file'] = f"nasional/sulawesi/{fname}"
        # Set baris_md to empty as this is from a specific table, not a generic raw text.
        df.at[idx, 'baris_md'] = pd.NA
        changes_made += 1

print(f"Updated {changes_made} rows based on new markdown tables.")

# Save v3
df.to_csv(v3_path, index=False)
print(f"Saved to {v3_path}")
