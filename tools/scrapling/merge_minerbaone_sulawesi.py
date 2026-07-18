"""
Script untuk merge dan filter data MinerbaOne untuk region Sulawesi
Output: CSV lengkap semua perusahaan tambang di Sulawesi dari MinerbaOne
"""

import pandas as pd
import re
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output" / "full"
PROCESSED_DIR = BASE_DIR.parent.parent / "data" / "processed"

# Files
DETAILS_FILE = OUTPUT_DIR / "minerbaone_details.csv"
PERMITS_FILE = OUTPUT_DIR / "minerbaone_permits.csv"
OUTPUT_FILE = PROCESSED_DIR / "minerbaone_sulawesi_full.csv"

# Sulawesi regions (kabupaten/kota keywords)
SULAWESI_KEYWORDS = [
    # Sulawesi Utara
    'BOLAANG MONGONDOW', 'MINAHASA', 'KEPULAUAN SANGIHE', 'KEPULAUAN TALAUD', 
    'MINAHASA SELATAN', 'MINAHASA UTARA', 'MINAHASA TENGGARA', 'BOLAANG MONGONDOW UTARA',
    'KEPULAUAN SIAU TAGULANDANG BIARO', 'BOLAANG MONGONDOW TIMUR', 'BOLAANG MONGONDOW SELATAN',
    'MANADO', 'BITUNG', 'TOMOHON', 'KOTAMOBAGU',
    
    # Sulawesi Tengah
    'BANGGAI', 'POSO', 'DONGGALA', 'TOLI TOLI', 'BUOL', 'MOROWALI', 'BANGGAI KEPULAUAN',
    'PARIGI MOUTONG', 'TOJO UNA UNA', 'SIGI', 'BANGGAI LAUT', 'MOROWALI UTARA',
    'PALU', 'MOROWALI TIMUR',
    
    # Sulawesi Selatan
    'KEPULAUAN SELAYAR', 'BULUKUMBA', 'BANTAENG', 'JENEPONTO', 'TAKALAR', 'GOWA', 'SINJAI',
    'BONE', 'MAROS', 'PANGKAJENE KEPULAUAN', 'BARRU', 'SOPPENG', 'WAJO', 'SIDENRENG RAPPANG',
    'PINRANG', 'ENREKANG', 'LUWU', 'TANA TORAJA', 'LUWU UTARA', 'LUWU TIMUR', 'TORAJA UTARA',
    'MAKASSAR', 'PAREPARE', 'PALOPO',
    
    # Sulawesi Tenggara
    'KOLAKA', 'KONAWE', 'MUNA', 'BUTON', 'KONAWE SELATAN', 'BOMBANA', 'WAKATOBI',
    'KOLAKA UTARA', 'KONAWE UTARA', 'BUTON UTARA', 'KOLAKA TIMUR', 'KONAWE KEPULAUAN',
    'MUNA BARAT', 'BUTON TENGAH', 'BUTON SELATAN', 'KENDARI', 'BAU BAU',
    
    # Gorontalo
    'GORONTALO', 'BOALEMO', 'BONE BOLANGO', 'POHUWATO', 'GORONTALO UTARA', 'KOTA GORONTALO',
    
    # Sulawesi Barat
    'PASANGKAYU', 'MAMUJU', 'MAMASA', 'POLEWALI MANDAR', 'MAJENE', 'MAMUJU TENGAH'
]

def is_sulawesi_location(text):
    """Check if location text contains Sulawesi region keywords"""
    if pd.isna(text) or not isinstance(text, str):
        return False
    
    text_upper = text.upper()
    
    # Check for direct Sulawesi mention
    if 'SULAWESI' in text_upper or 'SULSEL' in text_upper or 'SULTENG' in text_upper or \
       'SULUT' in text_upper or 'SULTRA' in text_upper or 'SULBAR' in text_upper:
        return True
    
    # Check for specific kabupaten/kota
    for keyword in SULAWESI_KEYWORDS:
        if keyword in text_upper:
            return True
    
    return False

def main():
    print("=" * 70)
    print("MINERBAONE SULAWESI DATA MERGER")
    print("=" * 70)
    
    # 1. Load data
    print("\n[1/5] Loading data...")
    df_details = pd.read_csv(DETAILS_FILE)
    df_permits = pd.read_csv(PERMITS_FILE)
    
    print(f"  ✓ Loaded {len(df_details):,} companies")
    print(f"  ✓ Loaded {len(df_permits):,} permits")
    
    # 2. Filter Sulawesi companies by address
    print("\n[2/5] Filtering Sulawesi companies...")
    df_details['is_sulawesi'] = df_details['alamat'].apply(is_sulawesi_location)
    
    # Add provinsi column based on address
    def extract_provinsi(text):
        if pd.isna(text):
            return None
        text_upper = text.upper()
        if 'SULAWESI UTARA' in text_upper or 'SULUT' in text_upper:
            return 'Sulawesi Utara'
        elif 'SULAWESI TENGAH' in text_upper or 'SULTENG' in text_upper:
            return 'Sulawesi Tengah'
        elif 'SULAWESI SELATAN' in text_upper or 'SULSEL' in text_upper:
            return 'Sulawesi Selatan'
        elif 'SULAWESI TENGGARA' in text_upper or 'SULTRA' in text_upper:
            return 'Sulawesi Tenggara'
        elif 'GORONTALO' in text_upper:
            return 'Gorontalo'
        elif 'SULAWESI BARAT' in text_upper or 'SULBAR' in text_upper:
            return 'Sulawesi Barat'
        return None
    
    df_details['provinsi'] = df_details['alamat'].apply(extract_provinsi)
    df_sulawesi = df_details[df_details['is_sulawesi']].copy()
    
    print(f"  ✓ Found {len(df_sulawesi):,} Sulawesi companies from address")
    
    # 3. Get Sulawesi companies from permit locations
    print("\n[3/5] Cross-checking with permit locations...")
    df_permits['is_sulawesi_loc'] = df_permits['lokasi_perizinan'].apply(is_sulawesi_location)
    sulawesi_company_ids_from_permits = df_permits[df_permits['is_sulawesi_loc']]['id_badan_usaha'].unique()
    
    # Add companies found in permits but not in address
    additional_companies = df_details[
        (~df_details['is_sulawesi']) & 
        (df_details['id_badan_usaha'].isin(sulawesi_company_ids_from_permits))
    ]
    
    df_sulawesi = pd.concat([df_sulawesi, additional_companies], ignore_index=True)
    print(f"  ✓ Added {len(additional_companies):,} companies from permit locations")
    print(f"  ✓ Total Sulawesi companies: {len(df_sulawesi):,}")
    
    # 4. Aggregate permits data
    print("\n[4/5] Aggregating permit data...")
    
    # Filter permits for Sulawesi companies
    df_permits_sulawesi = df_permits[df_permits['id_badan_usaha'].isin(df_sulawesi['id_badan_usaha'])].copy()
    print(f"  ✓ Found {len(df_permits_sulawesi):,} permits for Sulawesi companies")
    
    # Count permits per company
    permit_counts = df_permits_sulawesi.groupby('id_badan_usaha').agg(
        total_izin=('id_perizinan', 'count'),
        izin_nikel=('komoditas', lambda x: (x == 'Nikel').sum()),
        total_luas_ha=('luas_ha', 'sum')
    ).reset_index()
    
    # Get komoditas list and lokasi list
    komoditas_list = df_permits_sulawesi.groupby('id_badan_usaha')['komoditas'].apply(
        lambda x: ', '.join(sorted(set([k for k in x.dropna() if k != ''])))
    ).reset_index()
    
    lokasi_list = df_permits_sulawesi.groupby('id_badan_usaha')['lokasi_perizinan'].apply(
        lambda x: ' | '.join(sorted(set([loc for loc in x.dropna() if loc != ''])))
    ).reset_index()
    
    # 5. Merge everything
    print("\n[5/5] Merging and finalizing...")
    
    df_final = df_sulawesi.merge(permit_counts, on='id_badan_usaha', how='left')
    df_final = df_final.merge(komoditas_list, on='id_badan_usaha', how='left')
    df_final = df_final.merge(lokasi_list, on='id_badan_usaha', how='left')
    
    # Rename columns
    df_final = df_final.rename(columns={
        'komoditas': 'komoditas_list',
        'lokasi_perizinan': 'lokasi_izin'
    })
    
    # Add has_nickel_permit flag
    df_final['has_nickel_permit'] = df_final['izin_nikel'].fillna(0) > 0
    
    # Fill NaN for companies without permits
    df_final['total_izin'] = df_final['total_izin'].fillna(0).astype(int)
    df_final['izin_nikel'] = df_final['izin_nikel'].fillna(0).astype(int)
    df_final['total_luas_ha'] = df_final['total_luas_ha'].fillna(0).round(2)
    df_final['komoditas_list'] = df_final['komoditas_list'].fillna('')
    df_final['lokasi_izin'] = df_final['lokasi_izin'].fillna('')
    
    # Get IUP status (legal mining permit)
    iup_permits = df_permits_sulawesi[df_permits_sulawesi['jenis_perizinan'].str.contains('IUP', na=False)]
    companies_with_iup = iup_permits['id_badan_usaha'].unique()
    df_final['has_iup'] = df_final['id_badan_usaha'].isin(companies_with_iup)
    
    # Add placeholder columns for dorking data (investment & production capacity)
    df_final['investment_value_usd_million'] = None  # To be filled via dorking
    df_final['investment_value_idr_billion'] = None  # To be filled via dorking
    df_final['investment_year'] = None  # Year of investment
    df_final['production_capacity_ton_year'] = None  # Annual production capacity
    df_final['capacity_type'] = None  # ore/ferronickel/NPI/RKEF
    df_final['operational_status'] = None  # operational/construction/planned
    df_final['data_source_investment'] = None  # Source of investment data
    df_final['data_source_capacity'] = None  # Source of capacity data
    df_final['notes'] = None  # Additional notes
    
    # Select final columns
    final_columns = [
        'id_badan_usaha', 'nama_badan_usaha', 'jenis_badan_usaha', 'provinsi',
        'nib', 'npwp_badan_usaha', 'no_telp', 'email', 'alamat',
        'total_izin', 'izin_nikel', 'has_nickel_permit', 'has_iup',
        'komoditas_list', 'lokasi_izin', 'total_luas_ha',
        'investment_value_usd_million', 'investment_value_idr_billion', 'investment_year',
        'production_capacity_ton_year', 'capacity_type', 'operational_status',
        'data_source_investment', 'data_source_capacity', 'notes',
        'scraped_at'
    ]
    
    df_final = df_final[final_columns]
    
    # Sort by total permits descending
    df_final = df_final.sort_values('total_izin', ascending=False).reset_index(drop=True)
    
    # Save
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df_final.to_csv(OUTPUT_FILE, index=False)
    
    # Statistics
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"Total Companies:        {len(df_final):,}")
    print(f"Companies with Permits: {(df_final['total_izin'] > 0).sum():,}")
    print(f"Companies with IUP:     {df_final['has_iup'].sum():,}")
    print(f"Companies with Nickel:  {df_final['has_nickel_permit'].sum():,}")
    print(f"Total Permits:          {df_final['total_izin'].sum():,}")
    print(f"Total Nickel Permits:   {df_final['izin_nikel'].sum():,}")
    print(f"Total Area (ha):        {df_final['total_luas_ha'].sum():,.2f}")
    
    print("\nDistribution by Province:")
    print(df_final['provinsi'].value_counts())
    
    print("\nTop 5 Companies by Permits:")
    print(df_final[['nama_badan_usaha', 'provinsi', 'total_izin', 'izin_nikel', 'has_iup', 'total_luas_ha']].head())
    print(f"\n✓ Saved to: {OUTPUT_FILE}")
    print("=" * 70)

if __name__ == "__main__":
    main()
