"""
Script to process PAD data with BREAKDOWN by component (Pajak, Retribusi, Hasil BUMD, Lain-lain)
for hierarchical treemap visualization.

Output: data/processed/sulawesi_pad_breakdown_2016_2024.csv
Columns: provinsi, tahun, jenis_pendapatan, nilai_juta_rupiah
"""

import pandas as pd
import os

# Province files mapping
PROVINCE_FILES = {
    'Sulawesi Utara': 'data/raw/bps_pad/padsulut.csv',
    'Sulawesi Selatan': 'data/raw/bps_pad/padsulsel.csv',
    'Sulawesi Tenggara': 'data/raw/bps_pad/padsultra.csv',  # Re-enabled with special handling
    'Gorontalo': 'data/raw/bps_pad/padgorontalo.csv',
    'Sulawesi Barat': 'data/raw/bps_pad/padsulbar.csv',
}

# ALL revenue component patterns to extract (not just PAD sub-components)
# Extract EVERYTHING from the raw data files
REVENUE_COMPONENTS = {
    # PAD sub-components (level 1.a, 1.b, etc)
    'Pajak Daerah': ['- Pajak Daerah', 'a. Pajak Daerah'],
    'Retribusi Daerah': ['- Restribusi Daerah', 'b. Retribusi Daerah'],
    'Hasil BUMD': [
        '- Hasil Perusahaan Milik Daerah dan Pengelolaan Kekayaan Daerah yang Dipisahkan',
        'c. Hasil BUMD dan Pengelolaan Kekayaan Daerah'
    ],
    'Lain-lain PAD Yang Sah': ['- Lain-lain PAD yang Sah', 'd. Lain-lain PAD Yang Sah'],
    
    # Dana Perimbangan (level 2)
    'Dana Perimbangan': ['2. Dana Perimbangan'],
    'Bagi Hasil Pajak dan Bukan Pajak': ['- Bagi Hasil Pajak', 'a. Bagi Hasil Pajak dan Bukan Pajak'],
    'Bagi Hasil Bukan Pajak/SDA': ['- Bagi Hasil Bukan Pajak/Sumber Daya Alam'],
    'Dana Alokasi Umum': ['- Dana Alokasi Umum', 'b. Dana Alokasi Umum'],
    'Dana Alokasi Khusus': ['- Dana Alokasi Khusus', 'c. Dana Alokasi Khusus'],
    
    # Lain-lain Pendapatan Yang Sah (level 3)
    'Lain-lain Pendapatan Yang Sah': ['3. Lain-lain Pendapatan Yang Sah'],
    'Dana Penguatan Infrastruktur': ['a. Dana Penguatan Infrastruktur dan Prasarana Daerah'],
    'Dana Penyesuaian & Otonomi Khusus': ['b. Dana Penyesuaian & Otonomi Khusus'],
    'Hibah': ['- Pendapatan Hibah', 'c. Hibah'],
    'Dana Darurat': ['- Dana Darurat'],
    'Dana Bagi Hasil Pajak Provinsi': ['- Dana Bagi Hasil Pajak dan Provinsi dan Pemerintah Daerah Lainnya'],
    'Dana Penyesuaian dan Otonomi Daerah': ['- Dana Penyesuaian dan Otonomi Daerah'],
    'Bantuan Keuangan dari Provinsi': ['- Bantuan Keuangan dari Provinsi'],
}


def process_pad_breakdown(filepath, province_name):
    """
    Extract PAD breakdown by component from a single province file.
    
    Returns: DataFrame with columns [provinsi, tahun, jenis_pendapatan, nilai_ribu_rupiah]
    """
    try:
        # Special handling for Sulawesi Tenggara - has different structure
        if province_name == 'Sulawesi Tenggara':
            df = pd.read_csv(filepath, skiprows=1)
            df.columns = ['Kategori'] + list(df.columns[1:])
            
            # Extract "Pendapatan" row as total (row 4 in the file)
            pendapatan_row = df[df['Kategori'] == 'Pendapatan']
            
            if pendapatan_row.empty:
                print(f"   [SKIP] Pendapatan row not found")
                return pd.DataFrame()
            
            # Get year columns - extract year from column names like "Realisasi 2022"
            records = []
            for col in df.columns:
                if col == 'Kategori':
                    continue
                
                # Extract year from column name (e.g., "Realisasi 2022" -> 2022)
                import re
                year_match = re.search(r'(\d{4})', str(col))
                if not year_match:
                    continue
                
                try:
                    year = int(year_match.group(1))
                    value = pendapatan_row[col].values[0]
                    
                    if pd.notna(value) and str(value).strip() not in ['-', '']:
                        nilai_ribu = float(str(value).replace(',', ''))
                        records.append({
                            'provinsi': province_name,
                            'tahun': year,
                            'jenis_pendapatan': 'Total Pendapatan',
                            'nilai_ribu_rupiah': nilai_ribu
                        })
                except Exception as e:
                    pass
            
            if records:
                print(f"   [OK] Extracted as Total Pendapatan (no breakdown available)")
                return pd.DataFrame(records)
            else:
                print(f"   [SKIP] No valid data")
                return pd.DataFrame()
        
        # Special handling for Sulbar
        if province_name == 'Sulawesi Barat':
            print(f"   [SKIP] {province_name} - File format doesn't have PAD breakdown")
            return pd.DataFrame()
        
        # For Sulut - skip because it's kabupaten-level aggregated data
        if province_name == 'Sulawesi Utara':
            print(f"   [SKIP] {province_name} - Kabupaten-level data without breakdown")
            return pd.DataFrame()
        
        # Read file
        df = pd.read_csv(filepath, skiprows=1)
        df.columns = ['Kategori'] + list(df.columns[1:])
        
        # Check if unit is Juta Rupiah (Gorontalo)
        unit_multiplier = 1  # Default: Ribu Rupiah
        if 'Juta Rupiah' in str(df.iloc[0, 1]):
            unit_multiplier = 1000  # Convert Juta to Ribu
            print(f"   [INFO] Unit is Juta Rupiah, will convert to Ribu")
        
        # Extract year columns
        year_columns = [col for col in df.columns if col != 'Kategori']
        year_columns = [c for c in year_columns if str(c).strip().replace('.', '').isdigit()]
        
        records = []
        
        # Extract each revenue component (ALL, not just PAD sub-components)
        for component_name, patterns in REVENUE_COMPONENTS.items():
            for pattern in patterns:
                component_row = df[df['Kategori'] == pattern]
                
                if not component_row.empty:
                    print(f"   [OK] Found: {component_name}")
                    
                    for year_col in year_columns:
                        try:
                            year = int(float(str(year_col).strip()))
                            value = component_row[year_col].values[0]
                            
                            if pd.notna(value) and str(value).strip() not in ['-', '']:
                                nilai_ribu = float(str(value).replace(',', '')) * unit_multiplier
                                records.append({
                                    'provinsi': province_name,
                                    'tahun': year,
                                    'jenis_pendapatan': component_name,
                                    'nilai_ribu_rupiah': nilai_ribu
                                })
                        except Exception as e:
                            pass
                    
                    break  # Found this component, move to next
        
        return pd.DataFrame(records)
        
    except Exception as e:
        print(f"   [ERROR] {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()


def main():
    print("="*80)
    print("PROCESSING PAD BREAKDOWN DATA FOR SULAWESI")
    print("="*80)
    
    all_data = []
    
    for province, filepath in PROVINCE_FILES.items():
        if not os.path.exists(filepath):
            print(f"\n[!] File not found: {filepath}")
            continue
        
        print(f"\n>> Processing: {province}")
        df = process_pad_breakdown(filepath, province)
        
        if not df.empty:
            print(f"   [SUCCESS] Extracted {len(df)} records")
            print(f"   Years: {df['tahun'].min()} - {df['tahun'].max()}")
            print(f"   Components: {df['jenis_pendapatan'].nunique()}")
            all_data.append(df)
        else:
            print(f"   [SKIP] No breakdown data")
    
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df = final_df.sort_values(['provinsi', 'tahun', 'jenis_pendapatan'])
        
        # Convert to Juta Rupiah
        final_df['nilai_juta_rupiah'] = final_df['nilai_ribu_rupiah'] / 1_000
        final_df = final_df[['provinsi', 'tahun', 'jenis_pendapatan', 'nilai_juta_rupiah']]
        
        # Save
        output_path = 'data/processed/sulawesi_pad_breakdown_2016_2024.csv'
        final_df.to_csv(output_path, index=False)
        
        print("\n" + "="*80)
        print("PROCESSING COMPLETE")
        print("="*80)
        print(f"Output: {output_path}")
        print(f"Total records: {len(final_df)}")
        print(f"Provinces: {final_df['provinsi'].nunique()}")
        print(f"Components: {sorted(final_df['jenis_pendapatan'].unique())}")
        print(f"Years: {final_df['tahun'].min()} - {final_df['tahun'].max()}")
        
        print(f"\nTotal PAD (all components): {final_df['nilai_juta_rupiah'].sum():,.2f} Juta Rp")
        
        print("\nBreakdown by Component:")
        comp_summary = final_df.groupby('jenis_pendapatan')['nilai_juta_rupiah'].sum().sort_values(ascending=False)
        for comp, total in comp_summary.items():
            pct = (total / final_df['nilai_juta_rupiah'].sum()) * 100
            print(f"   {comp:30s}: {total:>15,.2f} Juta Rp ({pct:>5.1f}%)")
        
        print("\nBreakdown by Province:")
        prov_summary = final_df.groupby('provinsi')['nilai_juta_rupiah'].sum().sort_values(ascending=False)
        for prov, total in prov_summary.items():
            print(f"   {prov:20s}: {total:>15,.2f} Juta Rp")
    else:
        print("\n[ERROR] No data to process!")


if __name__ == "__main__":
    main()
