#!/usr/bin/env python3
"""
Fetch National Ekspor Data from BPS API
CELIOS ECC Intelligence System

Fetch nilai ekspor nasional (breakdown per sektor/komoditas)
Note: Data regional per-provinsi tidak tersedia di BPS API
"""

import argparse
from datetime import datetime
from pathlib import Path
import pandas as pd

from bps_stadata_client import BPSStadataClient


# Variable IDs untuk ekspor (hasil deep search)
EKSPOR_VAR_IDS = {
    '196': 'Nilai Ekspor',
    '1753': 'Nilai Ekspor Migas-NonMigas',
    '1492': 'Volume Ekspor Menurut Golongan SITC',
    '1494': 'Nilai Ekspor Menurut Golongan SITC',
    '2172': 'Volume Ekspor Migas-NonMigas',
    '1261': 'Pertumbuhan Ekspor Produk Non Migas',
}


def fetch_ekspor_national(
    client: BPSStadataClient,
    tahun_awal: int = 2016,
    tahun_akhir: int = 2026,
    var_ids: list = None
) -> pd.DataFrame:
    """
    Fetch ekspor data nasional untuk rentang tahun tertentu
    
    Args:
        client: BPSStadataClient instance
        tahun_awal: Start year
        tahun_akhir: End year
        var_ids: List of variable IDs to fetch (default: semua)
        
    Returns:
        DataFrame with ekspor data
    """
    if var_ids is None:
        var_ids = list(EKSPOR_VAR_IDS.keys())
    
    all_data = []
    
    print(f"\n📊 Fetching national ekspor data ({tahun_awal}-{tahun_akhir})...")
    print(f"Target: {len(var_ids)} indicators\n")
    
    for var_id in var_ids:
        indicator_name = EKSPOR_VAR_IDS.get(var_id, f"Unknown (var_id: {var_id})")
        print(f"  📈 Fetching: {indicator_name} (var_id: {var_id})")
        
        indicator_data = []
        
        # Loop through each year (API requires year parameter)
        for tahun in range(tahun_awal, tahun_akhir + 1):
            try:
                df = client.get_dynamic_table(
                    domain='0000',  # National level
                    var_id=var_id,
                    year=str(tahun)
                )
                
                if not df.empty:
                    indicator_data.append(df)
                    
            except Exception as e:
                # Silent fail for individual years
                continue
        
        if indicator_data:
            # Combine all years for this indicator
            combined_indicator = pd.concat(indicator_data, ignore_index=True)
            
            # Add metadata
            combined_indicator['var_id'] = var_id
            combined_indicator['indicator_name'] = indicator_name
            combined_indicator['scraped_at'] = datetime.now().isoformat()
            
            print(f"     ✅ Retrieved {len(combined_indicator)} rows")
            all_data.append(combined_indicator)
        else:
            print(f"     ⚠️  No data available")
            continue
    
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        print(f"\n✅ Total data fetched: {len(combined)} rows from {len(all_data)} indicators")
        return combined
    else:
        print(f"\n❌ No data retrieved")
        return pd.DataFrame()


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Fetch ekspor data nasional dari BPS API"
    )
    parser.add_argument(
        "--tahun-awal",
        type=int,
        default=2016,
        help="Start year (default: 2016)"
    )
    parser.add_argument(
        "--tahun-akhir",
        type=int,
        default=2026,
        help="End year (default: 2026)"
    )
    parser.add_argument(
        "--var-ids",
        nargs="+",
        default=None,
        help="Specific variable IDs to fetch (default: all)"
    )
    parser.add_argument(
        "--output",
        default="output/ekspor_national.csv",
        help="Output file path"
    )
    parser.add_argument(
        "--format",
        choices=["csv", "json", "xlsx"],
        default="csv",
        help="Output format"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    print("="*80)
    print("BPS API - National Ekspor Data Fetcher")
    print("="*80)
    
    # Initialize client
    api_key = "06fd644648629502353deaed29fc6383"
    client = BPSStadataClient(api_key=api_key, verbose=args.verbose)
    
    # Fetch data
    data = fetch_ekspor_national(
        client,
        tahun_awal=args.tahun_awal,
        tahun_akhir=args.tahun_akhir,
        var_ids=args.var_ids
    )
    
    if data.empty:
        print("\n⚠️  No data retrieved")
        return
    
    # Export
    output_path = Path(args.output)
    
    print(f"\n💾 Exporting data...")
    if args.format == "csv":
        client.export_to_csv(data, str(output_path))
    elif args.format == "json":
        client.export_to_json(data, str(output_path.with_suffix('.json')))
    elif args.format == "xlsx":
        client.export_to_excel(data, str(output_path.with_suffix('.xlsx')))
    
    # Show summary
    print(f"\n" + "="*80)
    print("✅ SUCCESS!")
    print("="*80)
    print(f"📁 Output: {output_path}")
    print(f"📊 Total entries: {len(data)}")
    
    if 'tahun' in data.columns:
        years = data['tahun'].dropna().unique()
        print(f"📅 Year range: {int(years.min())} - {int(years.max())}")
    
    if 'indicator_name' in data.columns:
        print(f"📈 Indicators: {data['indicator_name'].nunique()}")
    
    print("\n⚠️  NOTE: Data ini adalah level NASIONAL (Indonesia)")
    print("   Breakdown per provinsi/regional tidak tersedia di BPS API")


if __name__ == "__main__":
    main()
