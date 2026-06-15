import os
import requests
import pandas as pd
import urllib3
urllib3.disable_warnings()

url = "https://footprint.info.yorku.ca/files/2026/04/NEFBA_Data_global_national_ecological_footprint_biocapacity.xlsx"
dest = "data/raw/gfn/NEFBA_Data.xlsx"
os.makedirs(os.path.dirname(dest), exist_ok=True)

if not os.path.exists(dest):
    print(f"Downloading {url} ...")
    r = requests.get(url, verify=False)
    with open(dest, 'wb') as f:
        f.write(r.content)
    print("Download selesai.")

print("Membaca Excel...")
xl = pd.ExcelFile(dest)
print("Sheet Names:", xl.sheet_names)

for sheet in xl.sheet_names:
    print(f"\n--- Sheet: {sheet} ---")
    df = xl.parse(sheet, nrows=5)
    print(df.head())

