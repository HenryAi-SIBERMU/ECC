import sys
sys.path.append('tools/bpsapi')
from bps_stadata_client import BPSStadataClient

client = BPSStadataClient(api_key="06fd644648629502353deaed29fc6383")
print('Searching for Puskesmas...')
try:
    df_puskesmas = client.list_dynamic_tables(domains=['0000', '7100', '7200', '7300', '7400', '7500', '7600'], keyword='puskesmas')
    if not df_puskesmas.empty:
        print('Found Variables:')
        print(df_puskesmas[['table_id', 'title', 'subj', 'domain']].head(10).to_string())
    else:
        print('No variables found for puskesmas.')
except Exception as e:
    print(f'Error: {e}')

print('\nSearching for Rumah Sakit...')
try:
    df_rs = client.list_dynamic_tables(domains=['0000', '7100', '7200', '7300', '7400', '7500', '7600'], keyword='rumah sakit')
    if not df_rs.empty:
        print('Found Variables:')
        print(df_rs[['table_id', 'title', 'subj', 'domain']].head(10).to_string())
    else:
        print('No variables found for rumah sakit.')
except Exception as e:
    print(f'Error: {e}')
