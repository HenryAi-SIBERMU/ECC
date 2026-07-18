import stadata
import pandas as pd

pd.set_option('display.max_colwidth', 80)

client = stadata.Client('06fd644648629502353deaed29fc6383')

print('Fetching dynamic tables for Sulawesi Selatan (7300)...')
tables = client.list_dynamictable(all=False, domain=['7300'])

print(f'\nTotal tables: {len(tables)}')

if len(tables) > 0:
    # Search for PAD/Keuangan related tables
    pad_tables = tables[tables['title'].str.contains(
        'pendapatan|pemerintah|keuangan|realisasi', 
        case=False, 
        regex=True,
        na=False
    )]
    
    print(f'\nPAD/Keuangan related tables: {len(pad_tables)}')
    print('\nSample tables:')
    print(pad_tables[['var_id', 'title']].head(10).to_string())
    
    # Save full results
    pad_tables.to_csv('output/sulsel_pad_tables.csv', index=False, encoding='utf-8-sig')
    print(f'\n✅ Saved to: output/sulsel_pad_tables.csv')
else:
    print('\n❌ No tables found for domain 7300')
