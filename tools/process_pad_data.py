"""
Script to process and consolidate PAD (Pendapatan Asli Daerah) data from individual province CSV files
into a clean format for dashboard visualization.

Input: Individual province CSV files in data/raw/bps_pad/
Output: Consolidated CSV in data/processed/sulawesi_pad_2016_2024.csv
"""

import pandas as pd
import os
import re

# Mapping of province files to province names
PROVINCE_FILES = {
    'Sulawesi Utara': 'data/raw/bps_pad/padsulut.csv',
    'Sulawesi Selatan': 'data/raw/bps_pad/padsulsel.csv',
    'Sulawesi Tenggara': 'data/raw/bps_pad/padsultra.csv',
    'Gorontalo': 'data/raw/bps_pad/padgorontalo.csv',
    'Sulawesi Barat': 'data/raw/bps_pad/padsulbar.csv',
}

def process_pad_file(filepath, province_name):
    """
    Process a single PAD CSV file and extract PAD values per year.
    
    Handles multiple formats:
    - Format A (Sulsel): "Pendapatan Asli Daerah (PAD)" in Ribu Rupiah
    - Format B (Gorontalo): "1.Pendapatan Asli Daerah (PAD)" in Juta Rupiah  
    - Format C (Sulut): Kabupaten-level with province name in first column
    - Format D (Sulbar): Kabupaten-level with "Provinsi" row at bottom, TWO header rows
    
    Returns: DataFrame with columns [provinsi, tahun, pad_ribu_rupiah]
    """
    try:
        # Special handling for Sulbar - has 2 header rows before years
        if province_name == 'Sulawesi Barat':
            df = pd.read_csv(filepath, skiprows=2)  # Skip title + "Pendapatan" row
        else:
            df = pd.read_csv(filepath, skiprows=1)
        
        # The first column is the category/region name
        first_col_name = df.columns[0]
        df.columns = ['Kategori'] + list(df.columns[1:])
        
        # Check if this is kabupaten-level data with province row at bottom (Sulbar format)
        for idx, cat in enumerate(df['Kategori']):
            if pd.notna(cat) and 'Provinsi' in str(cat) and province_name in str(cat):
                print(f"     Detected province total row at bottom (row {idx})")
                pad_row = df.iloc[[idx]]
                year_columns = [col for col in df.columns if col != 'Kategori']
                year_columns = [c for c in year_columns if str(c).strip().replace('.', '').isdigit()]
                
                records = []
                for year_col in year_columns:
                    try:
                        year = int(float(str(year_col).strip()))
                        value = pad_row[year_col].values[0]
                        
                        if pd.notna(value) and str(value).strip() not in ['-', '']:
                            pad_ribu_rp = float(str(value).replace(',', ''))
                            records.append({
                                'provinsi': province_name,
                                'tahun': year,
                                'pad_ribu_rupiah': pad_ribu_rp
                            })
                    except Exception as e:
                        pass
                
                if records:
                    print(f"   [OK] Successfully extracted {len(records)} records from province row")
                    return pd.DataFrame(records)
                else:
                    print(f"   [!] Province row found but no valid data extracted")
        
        # Check if this is kabupaten-level data (Sulut format) - sum all rows
        if province_name == 'Sulawesi Utara' and df['Kategori'].iloc[0] == province_name:
            print(f"     Detected kabupaten-level data, summing to province level")
            year_columns = [col for col in df.columns if col != 'Kategori']
            year_columns = [c for c in year_columns if str(c).strip().replace('.', '').isdigit()]
            
            records = []
            for year_col in year_columns:
                try:
                    year = int(float(str(year_col).strip()))
                    # Sum all kabupaten values for this year
                    total = 0
                    for idx, row in df.iterrows():
                        val = row[year_col]
                        if pd.notna(val) and str(val).strip() not in ['-', '']:
                            try:
                                total += float(str(val).replace(',', ''))
                            except:
                                pass
                    
                    if total > 0:
                        records.append({
                            'provinsi': province_name,
                            'tahun': year,
                            'pad_ribu_rupiah': total
                        })
                except:
                    pass
            
            if records:
                return pd.DataFrame(records)
        
        # Try different PAD row patterns (exact match)
        pad_patterns = [
            'Pendapatan Asli Daerah (PAD)',
            '1.Pendapatan Asli Daerah (PAD)',
            '1. Pendapatan Asli Daerah (PAD)',
        ]
        
        pad_row = None
        unit_multiplier = 1  # Default: Ribu Rupiah (no conversion needed)
        
        # Try to find PAD row with exact match
        for pattern in pad_patterns:
            pad_row = df[df['Kategori'] == pattern]
            if not pad_row.empty:
                # Check if unit is Juta Rupiah (need to multiply by 1000)
                header_text = str(df.iloc[0, 1]) if len(df.columns) > 1 else ""
                if 'Juta Rupiah' in header_text or 'juta rupiah' in first_col_name.lower():
                    unit_multiplier = 1000  # Convert Juta to Ribu
                    print(f"     Detected Juta Rupiah unit, will convert to Ribu Rupiah")
                break
        
        if pad_row is None or pad_row.empty:
            print(f"  PAD row not found with any known pattern in {filepath}")
            print(f"   Available categories: {df['Kategori'].head(5).tolist()}")
            return pd.DataFrame()
        
        # Extract year columns (skip first column which is category name)
        year_columns = [col for col in df.columns if col != 'Kategori']
        year_columns = [c for c in year_columns if str(c).strip().replace('.', '').isdigit()]
        
        # Reshape data to long format
        records = []
        for year_col in year_columns:
            try:
                year = int(float(str(year_col).strip()))
                value = pad_row[year_col].values[0]
                
                # Handle missing values (-, empty, or NaN)
                if pd.isna(value) or str(value).strip() in ['-', '']:
                    continue
                    
                # Convert to float
                pad_value = float(str(value).replace(',', ''))
                pad_ribu_rp = pad_value * unit_multiplier
                records.append({
                    'provinsi': province_name,
                    'tahun': year,
                    'pad_ribu_rupiah': pad_ribu_rp
                })
            except Exception as e:
                print(f"  Could not convert value for {province_name} year {year_col}: {e}")
                continue
        
        return pd.DataFrame(records)
        
    except Exception as e:
        print(f" Error processing {filepath}: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()


def main():
    """Main processing function"""
    print("="*80)
    print("PROCESSING PAD DATA FOR SULAWESI PROVINCES")
    print("="*80)
    
    all_data = []
    
    for province, filepath in PROVINCE_FILES.items():
        if not os.path.exists(filepath):
            print(f"[!] File not found: {filepath}")
            continue
            
        print(f"\n>> Processing: {province}")
        df = process_pad_file(filepath, province)
        
        if not df.empty:
            print(f"   [OK] Extracted {len(df)} records")
            print(f"   Years: {df['tahun'].min()} - {df['tahun'].max()}")
            print(f"   Total PAD: {df['pad_ribu_rupiah'].sum()/1e6:,.2f} Juta Rupiah")
            all_data.append(df)
        else:
            print(f"   [FAIL] No data extracted")
    
    # Concatenate all province data
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        
        # Sort by province and year
        final_df = final_df.sort_values(['provinsi', 'tahun'])
        
        # Convert to Juta Rupiah (divide by 1000)
        final_df['pad_juta_rupiah'] = final_df['pad_ribu_rupiah'] / 1_000
        
        # Select final columns
        final_df = final_df[['provinsi', 'tahun', 'pad_juta_rupiah']]
        
        # Save to processed folder
        output_path = 'data/processed/sulawesi_pad_2016_2024.csv'
        final_df.to_csv(output_path, index=False)
        
        print("\n" + "="*80)
        print("PROCESSING COMPLETE")
        print("="*80)
        print(f"Output: {output_path}")
        print(f"Total records: {len(final_df)}")
        print(f"Provinces: {final_df['provinsi'].nunique()}")
        print(f"Years: {final_df['tahun'].min()} - {final_df['tahun'].max()}")
        print(f"\nTotal PAD across all provinces:")
        print(f"   {final_df['pad_juta_rupiah'].sum():,.2f} Juta Rupiah")
        print(f"   {final_df['pad_juta_rupiah'].sum()/1e6:,.2f} Triliun Rupiah")
        
        print("\nPAD by Province (Total across all years):")
        prov_summary = final_df.groupby('provinsi')['pad_juta_rupiah'].sum().sort_values(ascending=False)
        for prov, total in prov_summary.items():
            print(f"   {prov:20s}: {total:>12,.2f} Juta Rp ({total/1e6:>8,.2f} Triliun)")
        
    else:
        print("\n[ERROR] No data to process!")


if __name__ == "__main__":
    main()

