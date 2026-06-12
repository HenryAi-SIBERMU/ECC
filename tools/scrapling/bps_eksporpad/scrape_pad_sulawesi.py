#!/usr/bin/env python3
"""
BPS PAD Data Scraper - Sulawesi Provinces
CELIOS ECC Intelligence System

Scrape Realisasi Pendapatan dan Belanja Pemerintah Kabupaten/Kota
dari BPS provincial websites menggunakan Scrapling
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
import time
import logging

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scrapling import Fetcher

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Sulawesi BPS URLs
SULAWESI_PROVINCES = {
    "73": {
        "name": "Sulawesi Selatan",
        "url": "https://sulsel.bps.go.id",
        "query_builder": "https://sulsel.bps.go.id/id/query-builder"
    },
    "71": {
        "name": "Sulawesi Utara",
        "url": "https://sulut.bps.go.id",
        "query_builder": "https://sulut.bps.go.id/id/query-builder"
    },
    "72": {
        "name": "Sulawesi Tengah",
        "url": "https://sulteng.bps.go.id",
        "query_builder": "https://sulteng.bps.go.id/id/query-builder"
    },
    "74": {
        "name": "Sulawesi Tenggara",
        "url": "https://sultra.bps.go.id",
        "query_builder": "https://sultra.bps.go.id/id/query-builder"
    },
    "75": {
        "name": "Gorontalo",
        "url": "https://gorontalo.bps.go.id",
        "query_builder": "https://gorontalo.bps.go.id/id/query-builder"
    },
    "76": {
        "name": "Sulawesi Barat",
        "url": "https://sulbar.bps.go.id",
        "query_builder": "https://sulbar.bps.go.id/id/query-builder"
    }
}


def scrape_query_builder_page(url: str, province_name: str) -> dict:
    """
    Scrape query builder page to find PAD-related tables
    
    Args:
        url: Query builder URL
        province_name: Province name
        
    Returns:
        Dict with table information
    """
    logger.info(f"🔍 Scraping query builder: {province_name}")
    
    try:
        # Use Scrapling Fetcher
        response = Fetcher.get(url, timeout=30)
        
        if response.status_code != 200:
            logger.error(f"  ❌ Failed to fetch {url}: Status {response.status_code}")
            return None
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find tables or form elements related to PAD
        # Look for keywords in the page
        page_text = soup.get_text().lower()
        
        pad_indicators = [
            'pendapatan asli daerah',
            'realisasi pendapatan',
            'realisasi pemerintah',
            'belanja pemerintah',
            'keuangan daerah'
        ]
        
        found_keywords = [kw for kw in pad_indicators if kw in page_text]
        
        if found_keywords:
            logger.info(f"  ✅ Found PAD keywords: {', '.join(found_keywords)}")
            
            # Look for table selectors or dropdowns
            selects = soup.find_all('select')
            tables_list = soup.find_all(['div', 'ul'], class_=lambda x: x and ('table' in x.lower() or 'list' in x.lower()))
            
            result = {
                'province': province_name,
                'url': url,
                'found_keywords': found_keywords,
                'selects_count': len(selects),
                'tables_list_count': len(tables_list),
                'scraped_at': datetime.now().isoformat()
            }
            
            # Try to extract table titles
            table_titles = []
            for elem in soup.find_all(['li', 'option', 'div']):
                text = elem.get_text(strip=True)
                if any(kw in text.lower() for kw in pad_indicators):
                    table_titles.append(text)
            
            result['table_titles'] = table_titles[:20]  # First 20 matches
            
            return result
        else:
            logger.warning(f"  ⚠️  No PAD keywords found in {province_name}")
            return None
            
    except Exception as e:
        logger.error(f"  ❌ Error scraping {province_name}: {e}")
        return None


def scrape_pad_table_direct(province_code: str, province_url: str, province_name: str) -> pd.DataFrame:
    """
    Try to scrape PAD table directly from common URLs
    
    Args:
        province_code: Province code
        province_url: Base URL
        province_name: Province name
        
    Returns:
        DataFrame with scraped data
    """
    logger.info(f"📊 Trying direct table scrape: {province_name}")
    
    # Common URL patterns for BPS tables
    url_patterns = [
        f"{province_url}/indicator/13/169/1/realisasi-pendapatan-dan-belanja-pemerintah.html",
        f"{province_url}/statictable/keuangan-daerah.html",
        f"{province_url}/subject/169/keuangan-daerah.html",
        f"{province_url}/dynamictable",
    ]
    
    for url in url_patterns:
        try:
            logger.info(f"  Testing: {url}")
            response = Fetcher.get(url, timeout=15)
            
            if response.status_code == 200:
                # Try to parse tables
                tables = pd.read_html(response.text)
                
                if tables:
                    logger.info(f"  ✅ Found {len(tables)} tables")
                    
                    # Take the largest table (usually the data table)
                    largest_table = max(tables, key=len)
                    
                    # Add metadata
                    largest_table['province_code'] = province_code
                    largest_table['province'] = province_name
                    largest_table['source_url'] = url
                    largest_table['scraped_at'] = datetime.now().isoformat()
                    
                    return largest_table
                    
        except Exception as e:
            continue
    
    logger.warning(f"  ⚠️  No direct tables found for {province_name}")
    return pd.DataFrame()


def main():
    """Main scraping function"""
    print("="*80)
    print("BPS PAD Data Scraper - Sulawesi Provinces")
    print("Using Scrapling Framework")
    print("="*80)
    
    query_builder_results = []
    direct_scrape_results = []
    
    for prov_code, prov_info in SULAWESI_PROVINCES.items():
        print(f"\n{'='*80}")
        print(f"PROVINCE: {prov_info['name']}")
        print(f"{'='*80}")
        
        # 1. Scrape query builder page
        qb_result = scrape_query_builder_page(
            prov_info['query_builder'],
            prov_info['name']
        )
        
        if qb_result:
            query_builder_results.append(qb_result)
        
        # 2. Try direct table scrape
        direct_data = scrape_pad_table_direct(
            prov_code,
            prov_info['url'],
            prov_info['name']
        )
        
        if not direct_data.empty:
            direct_scrape_results.append(direct_data)
        
        # Rate limiting
        time.sleep(3)
    
    # Save results
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Save query builder discoveries
    if query_builder_results:
        qb_df = pd.DataFrame(query_builder_results)
        qb_output = output_dir / "query_builder_discoveries.csv"
        qb_df.to_csv(qb_output, index=False, encoding='utf-8-sig')
        logger.info(f"\n✅ Saved query builder discoveries: {qb_output}")
    
    # Save direct scrape data
    if direct_scrape_results:
        combined = pd.concat(direct_scrape_results, ignore_index=True)
        data_output = output_dir / "pad_sulawesi_scraped.csv"
        combined.to_csv(data_output, index=False, encoding='utf-8-sig')
        
        print(f"\n{'='*80}")
        print("✅ SUCCESS!")
        print(f"{'='*80}")
        print(f"📁 Direct data: {data_output}")
        print(f"📊 Total rows: {len(combined)}")
        print(f"🏝️  Provinces with data: {combined['province'].nunique()}")
    else:
        print(f"\n{'='*80}")
        print("⚠️  NO DIRECT DATA FOUND")
        print(f"{'='*80}")
        print("\n💡 NEXT STEPS:")
        print("1. Check query_builder_discoveries.csv for available tables")
        print("2. Manually visit the URLs and note the exact table URLs")
        print("3. Update this script with correct URLs")
        print("\nOR use browser automation (Selenium/Playwright) to:")
        print("- Click table options")
        print("- Submit forms")
        print("- Download Excel/CSV files")


if __name__ == "__main__":
    main()
