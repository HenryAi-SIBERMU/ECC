import pandas as pd
import os

md_path = 'docs/GFW_ALL_DATASETS_RAW.md'
excel_path = 'docs/GFW_ALL_DATASETS.xlsx'

data = []
with open(md_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line.startswith('|') and not line.startswith('| No') and not line.startswith('|---'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3 and parts[1].isdigit():
                data.append({'No': int(parts[1]), 'Dataset ID (Layer GFW)': parts[2]})

if data:
    df = pd.DataFrame(data)
    df.to_excel(excel_path, index=False)
    print(f"Successfully converted {len(data)} rows to {excel_path}")
else:
    print("No data found to convert.")
