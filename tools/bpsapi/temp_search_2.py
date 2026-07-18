import stadata
import pandas as pd

API_KEY = '06fd644648629502353deaed29fc6383'
client = stadata.Client(API_KEY)

for dom in ['7200', '7400']:
    tables = client.list_dynamictable(domain=dom)
    res = tables[tables['title'].str.contains('PDRB', case=False, na=False) & 
                 tables['title'].str.contains('Lapangan Usaha', case=False, na=False) & 
                 tables['title'].str.contains('Berlaku', case=False, na=False)]
    print(f"\nMatches for {dom}:")
    print(res[['var_id', 'title', 'domain']].to_string())
