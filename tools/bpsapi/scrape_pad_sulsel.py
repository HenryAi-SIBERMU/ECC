#!/usr/bin/env python3
"""
Scrape PAD Data from BPS Sulawesi Selatan Website
CELIOS ECC Intelligence System

Target: sulsel.bps.go.id - Tabel Dinamis PAD per Kabupaten/Kota
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from pathlib import Path
import time
import logging


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Base URL dari screenshot yang Anda berikan
BASE_URL = "https://sulsel.bps.go.id"

# Sulawesi provinces URLs
SULAWESI_BPS_URLS = {
    "7300": {
        "name": "Sulawesi Selatan",
        "url": "https://sulsel.bps.go.id",
        "code": "73"
    },
    "7100": {
        "name": "Sulawesi Utara",
        "url": "https://sulut.bps.go.id",
        "code": "71"
    },
    "7200": {
        "name": "Sulawesi Tengah",
        "url": "https://sulteng.bps.go.id",
        "code": "72"
    },
    "7400": {
        "name": "Sulawesi Tenggara",
        "url": "https://sultra.bps.go.id",
        "code": "74"
    },
    "7500": {
        "name": "Gorontalo",
        "url": "https://gorontalo.bps.go.id",
        "code": "75"
    },
    "7600": {
        "name": "Sulawesi Barat",
        "url": "https://sulbar.bps.go.id",
        "code": "76"
    }
}


def scrape_pad_table(province_url: str, province_name: str) -> pd.DataFrame:
    """
    Scrape PAD data from BPS provincial website
    
    Args:
        province_url: Base URL of BPS provincial website
        province_name: Province name
        
    Returns:
        DataFrame with PAD data
    """
    logger.info(f"Scraping PAD data from {province_name}...")
    
    # Construct dynamic table URL (need to find the correct endpoint)
    # This is a placeholder - actual URL needs to be discovered from the website
    search_url = f"{province_url}/subject/169/keuangan-daerah.html"
    
    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Get the page
        response = session.get(search_url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the PAD table (struktur HTML perlu di-adjust berdasarkan actual website)
        tables = soup.find_all('table')
        
        if not tables:
            logger.warning(f"No tables found for {province_name}")
            return pd.DataFrame()
        
        # Parse tables into DataFrame
        dfs = []
        for table in tables:
            try:
                df = pd.read_html(str(table))[0]
                dfs.append(df)
            except:
                continue
        
        if dfs:
            combined = pd.concat(dfs, ignore_index=True)
            combined['province'] = province_name
            combined['scraped_at'] = datetime.now().isoformat()
            logger.info(f"  ✅ Scraped {len(combined)} rows from {province_name}")
            return combined
        else:
            logger.warning(f"No data extracted from {province_name}")
            return pd.DataFrame()
            
    except Exception as e:
        logger.error(f"Failed to scrape {province_name}: {e}")
        return pd.DataFrame()


def discover_pad_url(province_url: str, province_name: str) -> str:
    """
    Discover the correct URL for PAD dynamic table
    
    Args:
        province_url: Base URL
        province_name: Province name
        
    Returns:
        URL of PAD table
    """
    logger.info(f"🔍 Discovering PAD table URL for {province_name}...")
    
    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Try common paths
        common_paths = [
            "/subject/169/keuangan-daerah.html",
            "/dynamictable",
            "/subject/13/keuangan.html",
            "/indicator/169",
            "/statictable/2023/01/15/1234/realisasi-pendapatan-daerah.html"
        ]
        
        for path in common_paths:
            test_url = f"{province_url}{path}"
            logger.info(f"  Testing: {test_url}")
            
            try:
                response = session.get(test_url, timeout=10)
                if response.status_code == 200:
                    # Check if page contains PAD-related keywords
                    content = response.text.lower()
                    if any(kw in content for kw in ['pendapatan asli daerah', 'pad', 'realisasi pendapatan']):
                        logger.info(f"  ✅ Found! {test_url}")
                        return test_url
            except:
                continue
        
        logger.warning(f"  ⚠️  No PAD URL found for {province_name}")
        return None
        
    except Exception as e:
        logger.error(f"Error discovering URL: {e}")
        return None


def main():
    """Main scraping function"""
    print("="*80)
    print("BPS PAD Data Scraper - Sulawesi Provinces")
    print("="*80)
    
    all_data = []
    
    # Start with Sulawesi Selatan (yang Anda tunjukkan di screenshot)
    for prov_code, prov_info in SULAWESI_BPS_URLS.items():
        prov_name = prov_info['name']
        prov_url = prov_info['url']
        
        print(f"\n📊 Processing: {prov_name}")
        print(f"   URL: {prov_url}")
        
        # Discover the correct URL first
        pad_url = discover_pad_url(prov_url, prov_name)
        
        if pad_url:
            # Scrape the data
            data = scrape_pad_table(prov_url, prov_name)
            if not data.empty:
                all_data.append(data)
        
        # Rate limiting
        time.sleep(2)
    
    # Combine all data
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        
        # Export
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        output_path = output_dir / "pad_sulawesi_scraped.csv"
        combined.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        print(f"\n" + "="*80)
        print("✅ SUCCESS!")
        print("="*80)
        print(f"📁 Output: {output_path}")
        print(f"📊 Total rows: {len(combined)}")
        print(f"🏝️  Provinces: {combined['province'].nunique()}")
        
    else:
        print(f"\n❌ No data scraped")
        print("\n💡 MANUAL ACTION NEEDED:")
        print("   1. Visit: https://sulsel.bps.go.id")
        print("   2. Navigate to: Produk > Tabel Dinamis > Keuangan Daerah")
        print("   3. Find the exact URL of the PAD table")
        print("   4. Update this script with the correct URL")


if __name__ == "__main__":
    main()
