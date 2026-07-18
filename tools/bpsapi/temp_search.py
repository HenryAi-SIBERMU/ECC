import stadata
import pandas as pd
import json

API_KEY = '06fd644648629502353deaed29fc6383'
client = stadata.Client(API_KEY)
tables = client.list_dynamictable(all=True)

# Search for PDRB Sektoral (Lapangan Usaha)
matches = tables[tables['title'].str.contains('PDRB', case=False, na=False) & tables['title'].str.contains('Lapangan Usaha', case=False, na=False)]

print(f"Found {len(matches)} matches.")
if not matches.empty:
    print(matches[['var_id', 'title', 'domain']].head(20).to_string())
