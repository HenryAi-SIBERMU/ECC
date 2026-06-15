"""
Global Forest Watch (GFW) API Client
=====================================

Client untuk mengakses Global Forest Watch API untuk data deforestasi Indonesia.

API Documentation: https://data.globalforestwatch.org/documents
Data Source: Hansen et al. (2013) High-Resolution Global Maps of Forest Cover Change

Author: CELIOS Research Division
Date: 14 Juni 2026
"""

import requests
import pandas as pd
import time
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GFWAPIClient:
    """Client untuk Global Forest Watch API."""
    
    # API Base URLs (GFW Data API v2 - Updated 14 Juni 2026)
    BASE_URL = "https://data-api.globalforestwatch.org"
    DATASETS_URL = f"{BASE_URL}/dataset"
    
    # Key datasets
    TREE_COVER_LOSS = "umd_tree_cover_loss"
    TREE_COVER_GAIN = "umd_tree_cover_gain"
    TREE_COVER_DENSITY = "umd_tree_cover_density_2000"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize GFW API client.
        
        Args:
            api_key: API key (read from .env.gfw if not provided)
        """
        if api_key is None:
            # Try read from .env.gfw
            env_file = Path(__file__).parent.parent.parent / ".env.gfw"
            if env_file.exists():
                with open(env_file) as f:
                    for line in f:
                        if line.startswith("GFW_API_KEY="):
                            api_key = line.split("=")[1].strip()
                            break
        
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({'x-api-key': api_key})
            logger.info("GFW API Client initialized with API key")
        else:
            logger.warning("GFW API Client initialized WITHOUT API key - queries will fail")
        
        logger.info("GFW API Client initialized (Data API v2)")
    
    def download_tree_cover_loss_csv(
        self,
        sql_query: str,
        filename: str = "export.csv"
    ) -> str:
        """
        Download tree cover loss data as CSV (may not require API key).
        
        Args:
            sql_query: SQL query string
            filename: Output filename
        
        Returns:
            CSV content as string
        """
        endpoint = f"{self.DATASETS_URL}/{self.TREE_COVER_LOSS}/latest/download/csv"
        
        params = {
            'sql': sql_query,
            'filename': filename
        }
        
        try:
            logger.info(f"Downloading tree cover loss CSV...")
            logger.debug(f"SQL: {sql_query}")
            
            response = self.session.get(endpoint, params=params, timeout=120)
            response.raise_for_status()
            
            logger.info(f"Download successful: {len(response.text)} bytes")
            return response.text
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error downloading CSV: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response body: {e.response.text[:500]}")
            return ""
    
    def get_dataset_fields(self, dataset: str = None) -> List[Dict]:
        """
        Get available fields/columns for a dataset.
        
        Args:
            dataset: Dataset name (default: tree cover loss)
        
        Returns:
            List of field definitions
        """
        if dataset is None:
            dataset = self.TREE_COVER_LOSS
        
        endpoint = f"{self.DATASETS_URL}/{dataset}/latest/fields"
        
        try:
            logger.info(f"Fetching fields for dataset: {dataset}")
            response = self.session.get(endpoint, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            fields = data.get('data', [])
            logger.info(f"Found {len(fields)} fields")
            return fields
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching fields: {e}")
            return []
    
    def query_global_tree_loss(
        self,
        start_year: int = 2016,
        end_year: int = 2024,
        group_by_year: bool = True
    ) -> pd.DataFrame:
        """
        Query global tree cover loss data using download endpoint.
        
        Args:
            start_year: Start year
            end_year: End year
            group_by_year: Group results by year
        
        Returns:
            DataFrame with tree cover loss data
        """
        # Build SQL query
        select_fields = [
            "umd_tree_cover_loss__year",
            "SUM(area__ha) as total_loss_ha",
            "SUM(whrc_aboveground_co2_emissions__Mg) as co2_emissions_mg"
        ]
        
        sql = f"""
        SELECT {', '.join(select_fields)}
        FROM data
        WHERE umd_tree_cover_loss__year >= {start_year}
          AND umd_tree_cover_loss__year <= {end_year}
        """
        
        if group_by_year:
            sql += " GROUP BY umd_tree_cover_loss__year ORDER BY umd_tree_cover_loss__year"
        
        # Try download endpoint (may not require auth)
        csv_content = self.download_tree_cover_loss_csv(sql, filename="tree_loss_global.csv")
        
        if csv_content:
            from io import StringIO
            df = pd.read_csv(StringIO(csv_content))
            return df
        else:
            logger.error("Failed to download data via CSV endpoint")
            return pd.DataFrame()
    
    def _rate_limit_wait(self, wait_time: float = 1.0):
        """Wait between API calls to respect rate limits."""
        time.sleep(wait_time)


# Indonesia Admin Codes for Sulawesi Provinces
SULAWESI_PROVINCES = {
    'Sulawesi Utara': {
        'admin1_code': 'IDN.31',  # ISO admin code
        'bps_code': '71',
        'name_en': 'North Sulawesi'
    },
    'Sulawesi Tengah': {
        'admin1_code': 'IDN.29',
        'bps_code': '72',
        'name_en': 'Central Sulawesi'
    },
    'Sulawesi Selatan': {
        'admin1_code': 'IDN.30',
        'bps_code': '73',
        'name_en': 'South Sulawesi'
    },
    'Sulawesi Tenggara': {
        'admin1_code': 'IDN.32',
        'bps_code': '74',
        'name_en': 'Southeast Sulawesi'
    },
    'Gorontalo': {
        'admin1_code': 'IDN.11',
        'bps_code': '75',
        'name_en': 'Gorontalo'
    },
    'Sulawesi Barat': {
        'admin1_code': 'IDN.33',
        'bps_code': '76',
        'name_en': 'West Sulawesi'
    }
}


def fetch_sulawesi_deforestation(
    start_year: int = 2016,
    end_year: int = 2024,
    output_file: Optional[str] = None
) -> pd.DataFrame:
    """
    Fetch deforestasi data untuk semua provinsi Sulawesi dari GFW.
    
    Strategy: Query global tree cover loss, lalu simpen semua data.
    Filter provinsi akan dilakukan di consolidation script.
    
    Args:
        start_year: Start year (default: 2016)
        end_year: End year (default: 2024)
        output_file: Optional output CSV file path
    
    Returns:
        DataFrame dengan kolom: year, total_loss_ha, co2_emissions_mg, data_source
    """
    client = GFWAPIClient()
    
    logger.info(f"Fetching global tree cover loss data {start_year}-{end_year}...")
    logger.info("Note: GFW API tidak support filter by province via SQL")
    logger.info("Strategy: Download global/Indonesia data, filter locally")
    
    # Try fetching global data grouped by year
    df = client.query_global_tree_loss(
        start_year=start_year,
        end_year=end_year,
        group_by_year=True
    )
    
    if df.empty:
        logger.error("No data returned from GFW API")
        logger.error("This might be due to:")
        logger.error("1. API endpoint changes")
        logger.error("2. Query syntax errors")
        logger.error("3. Authentication required")
        return pd.DataFrame()
    
    # Add metadata
    df['data_source'] = 'GFW_Hansen_et_al_2013'
    df['confidence_level'] = 'High'
    df['extraction_date'] = datetime.now().strftime('%Y-%m-%d')
    df['notes'] = 'Global aggregate data - Indonesia-specific filtering required'
    
    # Rename columns untuk consistency
    if 'umd_tree_cover_loss__year' in df.columns:
        df = df.rename(columns={'umd_tree_cover_loss__year': 'year'})
    
    logger.info(f"✅ Successfully fetched {len(df)} annual data points")
    
    if output_file:
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        logger.info(f"✅ Data saved to {output_file}")
    
    return df


if __name__ == "__main__":
    # Test GFW API connection
    print("=" * 70)
    print("Testing GFW Data API v2 Client")
    print("=" * 70)
    
    client = GFWAPIClient()
    
    # Test 1: Get dataset fields
    print("\n[TEST 1] Fetching available fields...")
    fields = client.get_dataset_fields()
    if fields:
        print(f"✅ Found {len(fields)} fields")
        print("\nKey fields:")
        for field in fields[:10]:
            print(f"  - {field.get('name', 'N/A')}: {field.get('type', 'N/A')}")
    else:
        print("❌ Failed to fetch fields")
    
    # Test 2: Query global tree cover loss via download endpoint
    print("\n[TEST 2] Downloading tree cover loss 2020-2023 (CSV endpoint)...")
    sql = """
    SELECT umd_tree_cover_loss__year, SUM(area__ha) as total_loss_ha
    FROM data
    WHERE umd_tree_cover_loss__year >= 2020 AND umd_tree_cover_loss__year <= 2023
    GROUP BY umd_tree_cover_loss__year
    ORDER BY umd_tree_cover_loss__year
    """
    
    csv_content = client.download_tree_cover_loss_csv(sql, "test_tree_loss.csv")
    if csv_content:
        print("✅ Download successful!")
        print(f"CSV size: {len(csv_content)} bytes")
        print("\nFirst 500 chars:")
        print(csv_content[:500])
    else:
        print("❌ Download failed")
        print("Note: This endpoint may also require API key")
    
    # Test 3: Full Sulawesi fetch (commented untuk safety)
    print("\n[TEST 3] Full Sulawesi fetch (ready to run)...")
    print("Uncomment lines below to execute full data fetch")
    print("Expected: ~9 rows (2016-2024 global aggregate)")
    
    # df = fetch_sulawesi_deforestation(
    #     start_year=2016,
    #     end_year=2024,
    #     output_file='../../data/raw/gfw/sulawesi_deforestation_2016_2024.csv'
    # )
    # if not df.empty:
    #     print(f"\n✅ Fetched {len(df)} data points")
    #     print(df.to_string(index=False))
    # else:
    #     print("\n❌ Data fetch failed")
    
    print("\n" + "=" * 70)
    print("API client test completed")
    print("=" * 70)
