#!/usr/bin/env python3
"""Re-export CSV with proper quoting"""

import json
import pandas as pd

# Load from JSON (lebih reliable)
with open('output/tanahkita_konflik_FINAL.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

df = pd.DataFrame(data)

print(f"Loaded {len(df)} entries from JSON")

# Export dengan proper quoting
df.to_csv(
    'output/tanahkita_konflik_CLEAN.csv',
    index=False,
    encoding='utf-8-sig',
    quoting=1,  # QUOTE_ALL - quote semua field
)

print("✅ Exported to tanahkita_konflik_CLEAN.csv")
print(f"   Total: {len(df)} rows")
print(f"   Duplicates: {df.duplicated().sum()}")
