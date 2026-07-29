import pandas as pd
from pathlib import Path

def main():
    # Load the research grade CSV
    input_file = Path("../../data/processed/gfw/papua_deforestation_research_grade_2016_2026.csv")
    if not input_file.exists():
        print(f"Error: Could not find {input_file}")
        return
        
    df = pd.read_csv(input_file)
    
    # Prepare the output Excel file
    output_dir = Path("../../data/processed/gfw")
    output_file = output_dir / "Papua_Deforestation_Data_2016_2026.xlsx"
    
    # We will use ExcelWriter to write multiple sheets
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        
        # 1. Sheet: Ringkasan Total (All Papua)
        # Aggregate the data across both provinces
        df_total = df.groupby(['year', 'indicator_name'])['value'].sum().reset_index()
        # Pivot table: rows = year, cols = indicator
        pivot_total = df_total.pivot(index='year', columns='indicator_name', values='value').reset_index()
        # Rename columns to remove name axis
        pivot_total.columns.name = None
        pivot_total.to_excel(writer, sheet_name='Total Seluruh Papua', index=False)
        
        # 2. Sheet per Province
        provinces = df['province'].unique()
        for prov in provinces:
            df_prov = df[df['province'] == prov]
            # Pivot table
            pivot_prov = df_prov.pivot(index='year', columns='indicator_name', values='value').reset_index()
            pivot_prov.columns.name = None
            
            # Shorten sheet name if needed (Excel max 31 chars)
            sheet_name = prov[:31]
            pivot_prov.to_excel(writer, sheet_name=sheet_name, index=False)
            
        # 3. Sheet: Data Mentah (Raw Data Table) for completeness
        df.to_excel(writer, sheet_name='Master Data (Tidy)', index=False)
        
    print(f"\nSUCCESS! Excel file created at: {output_file.resolve()}")

if __name__ == "__main__":
    main()
