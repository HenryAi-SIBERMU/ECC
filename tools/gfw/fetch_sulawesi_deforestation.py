"""
Fetch Sulawesi Deforestation Data dari Global Forest Watch
===========================================================

Script untuk download data deforestasi Sulawesi 2016-2024 menggunakan GFW API.

Usage:
    python fetch_sulawesi_deforestation.py

Output:
    data/raw/gfw/sulawesi_deforestation_2016_2024.csv

Author: CELIOS Research Division
Date: 14 Juni 2026
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.gfw.gfw_api_client import GFWAPIClient, SULAWESI_PROVINCES, fetch_sulawesi_deforestation
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main execution function."""
    
    logger.info("=" * 60)
    logger.info("FETCHING SULAWESI DEFORESTATION DATA FROM GFW")
    logger.info("=" * 60)
    
    # Define output paths
    output_dir = project_root / 'data' / 'raw' / 'gfw'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / 'sulawesi_deforestation_2016_2024.csv'
    
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Output file: {output_file}")
    
    # Fetch data
    logger.info("\nStarting data fetch...")
    logger.info(f"Target: {len(SULAWESI_PROVINCES)} provinces")
    logger.info(f"Time range: 2016-2024 (9 years)")
    logger.info(f"Expected data points: {len(SULAWESI_PROVINCES) * 9} rows\n")
    
    try:
        df = fetch_sulawesi_deforestation(
            start_year=2016,
            end_year=2024,
            output_file=str(output_file)
        )
        
        logger.info("\n" + "=" * 60)
        logger.info("DATA FETCH COMPLETED")
        logger.info("=" * 60)
        logger.info(f"Total rows fetched: {len(df)}")
        logger.info(f"Provinces covered: {df['province'].nunique()}")
        logger.info(f"Years covered: {sorted(df['year'].unique())}")
        
        # Display sample
        logger.info("\nSample data (first 10 rows):")
        print(df.head(10).to_string(index=False))
        
        # Data quality check
        logger.info("\n" + "=" * 60)
        logger.info("DATA QUALITY CHECK")
        logger.info("=" * 60)
        
        missing_data = df[df['tree_cover_loss_ha'].isna()]
        if len(missing_data) > 0:
            logger.warning(f"Missing data: {len(missing_data)} rows")
            logger.warning("This is expected if GFW API structure needs adjustment")
        else:
            logger.info("✅ All data points populated")
        
        # Per-province summary
        logger.info("\nPer-province data coverage:")
        province_summary = df.groupby('province').agg({
            'year': ['count', 'min', 'max'],
            'tree_cover_loss_ha': 'count'
        })
        print(province_summary)
        
        logger.info(f"\n✅ Data successfully saved to: {output_file}")
        logger.info("\nNext steps:")
        logger.info("1. Inspect GFW API response structure")
        logger.info("2. Adjust parsing logic in gfw_api_client.py if needed")
        logger.info("3. Run SLHI extraction for cross-validation")
        logger.info("4. Consolidate both sources with scripts/consolidate_deforestasi.py")
        
    except Exception as e:
        logger.error(f"\n❌ Error during data fetch: {e}")
        logger.error("Please check:")
        logger.error("1. Internet connection")
        logger.error("2. GFW API endpoint availability")
        logger.error("3. API response structure changes")
        raise


if __name__ == "__main__":
    main()
