#!/usr/bin/env python3
"""
BPS PAD Data Scraper with Browser Automation
CELIOS ECC Intelligence System

Uses Scrapling's PlaywrightFetcher to handle JavaScript-rendered content
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
import time
import logging
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scrapling.fetchers import DynamicFetcher

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


def scrape_with_browser(url: str, province_name: str) -> dict:
    """
    Scrape using browser automation to handle JavaScript
    
    Args:
        url: Query builder URL
        province_name: Province name
        
    Returns:
        Dict with scraped information
    """
    logger.info(f"🌐 Opening browser for: {province_name}")
    
    try:
        # Use DynamicFetcher for JavaScript rendering
        page = DynamicFetcher.fetch(
            url,
            headless=True,  # Run without GUI
            wait_selector='body',  # Wait for body to load
            network_idle=True  # Wait for network to be idle
        )
        
        logger.info(f"  ✅ Page loaded: {province_name}")
        
        # Get page content after JavaScript execution
        html = page.html_content
        soup = BeautifulSoup(html, 'html.parser')
        
        # Look for PAD-related elements
        page_text = soup.get_text().lower()
        
        pad_keywords = [
            'pendapatan asli daerah',
            'realisasi pendapatan',
            'belanja pemerintah',
            'keuangan daerah'
        ]
        
        found = [kw for kw in pad_keywords if kw in page_text]
        
        # Look for dropdowns/selects
        selects = soup.find_all('select')
        select_info = []
        
        for select in selects:
            select_id = select.get('id', 'N/A')
            options = [opt.get_text(strip=True) for opt in select.find_all('option')]
            
            # Check if this select has PAD-related options
            pad_options = [opt for opt in options if any(kw in opt.lower() for kw in pad_keywords)]
            
            if pad_options:
                select_info.append({
                    'id': select_id,
                    'pad_options': pad_options
                })
        
        # Look for tables already rendered
        tables = soup.find_all('table')
        table_count = len(tables)
        
        result = {
            'province': province_name,
            'url': url,
            'keywords_found': found,
            'selects_with_pad': select_info,
            'tables_found': table_count,
            'scraped_at': datetime.now().isoformat()
        }
        
        logger.info(f"  📊 Found: {len(found)} keywords, {len(select_info)} PAD selects, {table_count} tables")
        
        # Try to extract table data if any
        if tables:
            logger.info(f"  🔍 Attempting to parse tables...")
            table_data = []
            
            for i, table in enumerate(tables):
                try:
                    df = pd.read_html(str(table))[0]
                    if len(df) > 0:
                        df['table_index'] = i
                        df['province'] = province_name
                        table_data.append(df)
                        logger.info(f"    ✅ Table {i}: {len(df)} rows")
                except:
                    continue
            
            if table_data:
                result['tables_data'] = table_data
        
        return result
        
    except Exception as e:
        logger.error(f"  ❌ Browser scrape failed for {province_name}: {e}")
        return None


def try_interactive_scrape(url: str, province_name: str) -> pd.DataFrame:
    """
    Try to interact with the page (click buttons, select dropdowns)
    
    Args:
        url: Query builder URL
        province_name: Province name
        
    Returns:
        DataFrame with data
    """
    logger.info(f"🎯 Interactive scrape: {province_name}")
    
    try:
        # Fetch with DynamicFetcher
        page = DynamicFetcher.fetch(
            url,
            headless=False,  # Show browser for debugging
            network_idle=True
        )
        
        # Get the Playwright page object for interaction
        pw_page = page.page  # Access underlying Playwright page
        
        # Wait for selects to load
        pw_page.wait_for_selector('select', timeout=5000)
        
        # Look for subject/category dropdown
        subject_select = pw_page.query_selector('select[name*="subject"], select[id*="subject"]')
        
        if subject_select:
            logger.info("  📋 Found subject selector")
            
            # Get all options
            options = pw_page.query_selector_all('select option')
            pad_option = None
            
            for opt in options:
                text = opt.inner_text().lower()
                if 'keuangan' in text or 'pendapatan' in text:
                    pad_option = opt
                    logger.info(f"  ✅ Found PAD option: {opt.inner_text()}")
                    break
            
            if pad_option:
                # Select the PAD option
                value = pad_option.get_attribute('value')
                subject_select.select_option(value)
                logger.info(f"  ✅ Selected: {value}")
                
                # Wait for table list to update
                time.sleep(2)
                
                # Look for table dropdown
                table_select = pw_page.query_selector('select[name*="table"], select[id*="indicator"]')
                
                if table_select:
                    # Get PAD table options
                    table_options = pw_page.query_selector_all('select option')
                    
                    for opt in table_options:
                        text = opt.inner_text().lower()
                        if 'realisasi' in text and 'pendapatan' in text:
                            table_value = opt.get_attribute('value')
                            table_select.select_option(table_value)
                            logger.info(f"  ✅ Selected table: {opt.inner_text()}")
                            break
                    
                    # Wait for form update
                    time.sleep(2)
                    
                    # Click submit button
                    submit_btn = pw_page.query_selector('button[type="submit"], input[type="submit"], button:has-text("Submit")')
                    
                    if submit_btn:
                        submit_btn.click()
                        logger.info("  🖱️  Clicked submit")
                        
                        # Wait for table to appear
                        pw_page.wait_for_selector('table', timeout=10000)
                        
                        # Get the rendered HTML
                        html = pw_page.content()
                        
                        # Parse tables
                        tables = pd.read_html(html)
                        
                        if tables:
                            logger.info(f"  ✅ Extracted {len(tables)} tables")
                            largest = max(tables, key=len)
                            largest['province'] = province_name
                            largest['scraped_at'] = datetime.now().isoformat()
                            return largest
        
        logger.warning(f"  ⚠️  Could not find PAD data for {province_name}")
        return pd.DataFrame()
        
    except Exception as e:
        logger.error(f"  ❌ Interactive scrape failed: {e}")
        return pd.DataFrame()
    finally:
        try:
            pw_page.close()
        except:
            pass


def main():
    """Main function"""
    print("="*80)
    print("BPS PAD Scraper - Browser Automation Mode")
    print("Using Scrapling DynamicFetcher")
    print("="*80)
    
    # First pass: Discover structure
    discoveries = []
    
    for prov_code, prov_info in list(SULAWESI_PROVINCES.items())[:1]:  # Start with 1 province
        print(f"\n{'='*80}")
        print(f"PROVINCE: {prov_info['name']}")
        print(f"{'='*80}")
        
        discovery = scrape_with_browser(
            prov_info['query_builder'],
            prov_info['name']
        )
        
        if discovery:
            discoveries.append(discovery)
            
            # If we found PAD selects, try interactive scrape
            if discovery.get('selects_with_pad'):
                print("\n  🎯 Found PAD selects! Trying interactive scrape...")
                data = try_interactive_scrape(
                    prov_info['query_builder'],
                    prov_info['name']
                )
                
                if not data.empty:
                    # Save immediately
                    output_dir = Path("output")
                    output_dir.mkdir(exist_ok=True)
                    
                    output_file = output_dir / f"pad_{prov_code}_{prov_info['name'].replace(' ', '_').lower()}.csv"
                    data.to_csv(output_file, index=False, encoding='utf-8-sig')
                    
                    print(f"\n  ✅ Saved: {output_file}")
                    print(f"  📊 Rows: {len(data)}")
        
        # Rate limiting
        time.sleep(3)
    
    # Save discoveries
    if discoveries:
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        with open(output_dir / "browser_discoveries.json", "w", encoding="utf-8") as f:
            json.dump(discoveries, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n{'='*80}")
        print("✅ Discovery complete!")
        print(f"📁 Check output/browser_discoveries.json for structure")
        print(f"{'='*80}")


if __name__ == "__main__":
    main()
