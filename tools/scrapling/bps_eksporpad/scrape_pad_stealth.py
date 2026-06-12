#!/usr/bin/env python3
"""
BPS PAD Data Scraper with Stealth Mode
CELIOS ECC Intelligence System

Uses Scrapling StealthyFetcher to bypass Cloudflare protection
"""

import sys
from pathlib import Path
from datetime import datetime
import pandas as pd
import time
import logging
import json
from scrapling.fetchers import StealthyFetcher
from bs4 import BeautifulSoup

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Sulawesi BPS URLs
SULAWESI_PROVINCES = {
    "7300": {
        "name": "Sulawesi Selatan",
        "url": "https://sulsel.bps.go.id",
        "query_builder": "https://sulsel.bps.go.id/id/query-builder"
    },
    "7100": {
        "name": "Sulawesi Utara",
        "url": "https://sulut.bps.go.id",
        "query_builder": "https://sulut.bps.go.id/id/query-builder"
    },
    "7200": {
        "name": "Sulawesi Tengah",
        "url": "https://sulteng.bps.go.id",
        "query_builder": "https://sulteng.bps.go.id/id/query-builder"
    },
    "7400": {
        "name": "Sulawesi Tenggara",
        "url": "https://sultra.bps.go.id",
        "query_builder": "https://sultra.bps.go.id/id/query-builder"
    },
    "7500": {
        "name": "Gorontalo",
        "url": "https://gorontalo.bps.go.id",
        "query_builder": "https://gorontalo.bps.go.id/id/query-builder"
    },
    "7600": {
        "name": "Sulawesi Barat",
        "url": "https://sulbar.bps.go.id",
        "query_builder": "https://sulbar.bps.go.id/id/query-builder"
    }
}


def test_stealth_fetch(url: str, province_name: str) -> dict:
    """
    Test StealthyFetcher to bypass Cloudflare
    
    Args:
        url: Query builder URL
        province_name: Province name
        
    Returns:
        Dict with page info
    """
    logger.info(f"🕵️  Stealth mode: {province_name}")
    
    try:
        # Use StealthyFetcher to bypass Cloudflare
        logger.info(f"  📄 Fetching: {url}")
        page = StealthyFetcher.fetch(
            url,
            headless=False,  # Show browser
            network_idle=True,
            wait_selector='form',  # Wait for form element
            wait_selector_state='attached'
        )
        
        logger.info(f"  ✅ Page fetched: {page.status}")
        logger.info(f"  ⏱️  Waiting for React to render...")
        
        # StealthyFetcher returns Response object, need to get Playwright page
        # Wait additional time for JavaScript
        import time
        time.sleep(10)  # Wait 10 seconds for JavaScript to execute
        
        # Get updated HTML after waiting
        logger.info(f"  📄 Getting final HTML...")
        
        # Save HTML
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        html_path = output_dir / f"stealth_{province_name.replace(' ', '_')}.html"
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(page.html_content)
        
        logger.info(f"  📄 HTML saved: {html_path}")
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(page.html_content, 'html.parser')
        
        # Check for selects
        selects = soup.find_all('select')
        logger.info(f"  📋 Found {len(selects)} select elements")
        
        # Check for labels
        labels = soup.find_all('label')
        logger.info(f"  🏷️  Found {len(labels)} labels")
        
        for label in labels[:10]:
            logger.info(f"    - {label.get_text(strip=True)}")
        
        # Check for skeleton/loading
        skeletons = soup.find_all(class_=lambda x: x and 'skeleton' in x.lower())
        logger.info(f"  ⏳ Loading indicators: {len(skeletons)}")
        
        return {
            'province': province_name,
            'status': page.status,
            'selects_found': len(selects),
            'labels_found': len(labels),
            'skeletons_found': len(skeletons),
            'html_path': str(html_path)
        }
        
    except Exception as e:
        logger.error(f"  ❌ Stealth fetch failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main function"""
    print("="*80)
    print("BPS PAD Scraper - Stealth Mode")
    print("Using Scrapling StealthyFetcher to bypass Cloudflare")
    print("="*80)
    
    # Test with first province
    prov_code, prov_info = list(SULAWESI_PROVINCES.items())[0]
    
    print(f"\n{'='*80}")
    print(f"PROVINCE: {prov_info['name']} ({prov_code})")
    print(f"{'='*80}")
    
    result = test_stealth_fetch(
        prov_info['query_builder'],
        prov_info['name']
    )
    
    if result:
        print(f"\n✅ Fetch complete!")
        print(f"📊 Selects found: {result['selects_found']}")
        print(f"🏷️  Labels found: {result['labels_found']}")
        print(f"⏳ Loading indicators: {result['skeletons_found']}")
        print(f"📁 HTML: {result['html_path']}")
        
        if result['selects_found'] > 0:
            print(f"\n🎉 SUCCESS! Form loaded with dropdowns.")
        else:
            print(f"\n⚠️  Form still not loaded. Cloudflare might still be blocking.")
    else:
        print(f"\n❌ Fetch failed.")
    
    print(f"\n{'='*80}")


if __name__ == "__main__":
    main()
