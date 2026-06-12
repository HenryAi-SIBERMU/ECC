#!/usr/bin/env python3
"""Re-export CSV with proper quoting - load dengan error handling"""

import pandas as pd

# Load CSV dengan error handling
df = pd.read_csv(
    'output/tanahkita_konflik_FINAL.csv',
    encoding='utf-8-sig',
    on_bad_lines='skip',  # Skip bad lines
    engine='python'  # More robust parser
)

print(f"Loaded {len(df)} entries from CSV")
print(f"Duplicates: {df.duplicated().sum()}")

# Export dengan proper quoting
df.to_csv(
    'output/tanahkita_konflik_CLEAN.csv',
    index=False,
    encoding='utf-8-sig',
    quoting=1,  # QUOTE_ALL
)

print("✅ Exported to tanahkita_konflik_CLEAN.csv with proper quoting")

# Also export JSON
df.to_json(
    'output/tanahkita_konflik.json',
    orient='records',
    force_ascii=False,
    indent=2
)

print("✅ Exported to tanahkita_konflik.json")
