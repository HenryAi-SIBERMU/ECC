import sys
import pandas as pd
import os
sys.path.append('tools/bpsapi')
from bps_stadata_client import BPSStadataClient

def fetch_faskes_data():
    client = BPSStadataClient(api_key='06fd644648629502353deaed29fc6383')
    
    # We need to fetch var_id 232: "Jumlah Rumah Sakit Umum, Rumah Sakit Khusus, dan Puskesmas"
    # Max years per request is 3.
    year_chunks = ["2014:2016", "2017:2019", "2020:2022", "2023:2024"]
    
    all_dfs = []
    
    for chunk in year_chunks:
        print(f"Fetching data for years {chunk}...")
        try:
            df = client.get_dynamic_table(domain='0000', var_id='232', year=chunk)
            if not df.empty:
                all_dfs.append(df)
        except Exception as e:
            print(f"Failed chunk {chunk}: {e}")
            
    if not all_dfs:
        print("Failed to fetch any data.")
        return
        
    combined_df = pd.concat(all_dfs, ignore_index=True)
    
    # Let's see what columns we have and filter by Sulawesi
    print("Columns:", combined_df.columns)
    
    # We want to filter to only the 6 Sulawesi provinces:
    # 71 (Sulut), 72 (Sulteng), 73 (Sulsel), 74 (Sultra), 75 (Gorontalo), 76 (Sulbar)
    sulawesi_codes = ['7100', '7200', '7300', '7400', '7500', '7600']
    
    # The BPS dataframe structure usually has columns: vervar, turvar, tahun, nilai, dll
    # Let's save the raw output first to inspect it
    raw_out = "data/raw/bps_faskes/api_raw_faskes_2014_2024.csv"
    os.makedirs(os.path.dirname(raw_out), exist_ok=True)
    combined_df.to_csv(raw_out, index=False)
    print(f"Saved raw BPS API data to {raw_out}")
    
if __name__ == "__main__":
    fetch_faskes_data()
