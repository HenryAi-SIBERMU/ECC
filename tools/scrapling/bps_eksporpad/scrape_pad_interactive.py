#!/usr/bin/env python3
"""
BPS PAD Data Scraper with Full Browser Interaction
CELIOS ECC Intelligence System

Uses Playwright directly for complete form interaction
"""

import sys
from pathlib import Path
from datetime import datetime
import pandas as pd
import time
import logging
import json
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

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


def scrape_pad_data(url: str, province_name: str, headless: bool = True) -> pd.DataFrame:
    """
    Scrape PAD data menggunakan Playwright dengan interaksi form
    
    Args:
        url: Query builder URL
        province_name: Nama provinsi
        headless: Run browser headless atau visible
        
    Returns:
        DataFrame dengan data PAD
    """
    logger.info(f"🌐 Opening browser for: {province_name}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = context.new_page()
        
        # Monitor network requests
        api_calls = []
        console_logs = []
        
        def log_request(request):
            if 'api' in request.url or 'query' in request.url.lower():
                api_calls.append(request.url)
                logger.info(f"  🌐 API Call: {request.url}")
        
        def log_console(msg):
            console_logs.append(f"{msg.type}: {msg.text}")
            if msg.type in ['error', 'warning']:
                logger.warning(f"  ⚠️  Console {msg.type}: {msg.text}")
        
        page.on('request', log_request)
        page.on('console', log_console)
        
        try:
            # Navigate to query builder
            logger.info(f"  📄 Loading: {url}")
            page.goto(url, wait_until='networkidle', timeout=30000)
            
            # Wait for page to be fully loaded
            page.wait_for_load_state('domcontentloaded')
            
            # Close popup if exists
            try:
                close_btn = page.query_selector('button:has-text("Tutup")')
                if close_btn:
                    logger.info(f"  🔘 Closing popup...")
                    close_btn.click()
                    time.sleep(1)
            except:
                pass
            
            logger.info(f"  ⏱️  Waiting for form to load...")
            time.sleep(5)  # Wait longer for React/AJAX to populate selects
            
            # Wait for skeleton to disappear (sign that data loaded)
            try:
                page.wait_for_selector('.skeleton-box', state='hidden', timeout=10000)
                logger.info(f"  ✅ Form loaded (skeleton removed)")
            except:
                logger.warning(f"  ⚠️  Skeleton still visible, continuing anyway...")
            
            # Log current page state
            logger.info(f"  ✅ Page loaded successfully")
            
            # Dump HTML for inspection
            html_path = Path("output") / f"page_{province_name.replace(' ', '_')}.html"
            html_path.parent.mkdir(exist_ok=True)
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(page.content())
            logger.info(f"  📄 HTML saved: {html_path}")
            
            # Find all select elements
            selects = page.query_selector_all('select')
            logger.info(f"  📋 Found {len(selects)} native select dropdowns")
            
            # Also try to find custom dropdowns (div-based)
            custom_dropdowns = page.query_selector_all('[role="combobox"], [role="listbox"]')
            logger.info(f"  📋 Found {len(custom_dropdowns)} custom dropdowns")
            
            # Check for loading state
            loading_indicators = page.query_selector_all('.skeleton-box, .loading, [class*="skeleton"]')
            logger.info(f"  ⏳ Still loading: {len(loading_indicators)} skeleton elements")
            
            # Log all labels to see what's on the form
            labels = page.query_selector_all('label')
            logger.info(f"  🏷️  Found {len(labels)} labels:")
            for label in labels[:10]:  # First 10 labels
                text = label.inner_text()
                label_id = label.get_attribute('id') or label.get_attribute('for')
                logger.info(f"    - {text} (id/for: {label_id})")
            
            # Try to find subject/category dropdown
            subject_found = False
            for i, select in enumerate(selects):
                select_id = select.get_attribute('id') or f'select_{i}'
                select_name = select.get_attribute('name') or 'unknown'
                
                # Get options count
                options = select.query_selector_all('option')
                logger.info(f"    Select {i}: id='{select_id}', name='{select_name}', options={len(options)}")
                
                # Check if this is subject/category dropdown
                if any(keyword in select_name.lower() for keyword in ['subject', 'category', 'topik']):
                    subject_found = True
                    logger.info(f"  ✅ Found subject dropdown: {select_name}")
                    
                    # Look for PAD-related option
                    for opt in options:
                        text = opt.inner_text().lower()
                        value = opt.get_attribute('value')
                        
                        if any(kw in text for kw in ['keuangan', 'pendapatan', 'pad', 'apbd']):
                            logger.info(f"    ✅ Found PAD option: {opt.inner_text()} (value={value})")
                            
                            # Select the option
                            select.select_option(value=value)
                            logger.info(f"    ✅ Selected PAD category")
                            
                            # Wait for page to update
                            time.sleep(2)
                            
                            # Look for table dropdown
                            table_selects = page.query_selector_all('select')
                            logger.info(f"    📋 After selection: {len(table_selects)} dropdowns")
                            
                            # Find table/indicator dropdown
                            for table_select in table_selects:
                                table_name = table_select.get_attribute('name') or ''
                                if any(kw in table_name.lower() for kw in ['table', 'indicator', 'tabel']):
                                    logger.info(f"    📊 Found table dropdown: {table_name}")
                                    
                                    # Get table options
                                    table_opts = table_select.query_selector_all('option')
                                    for topt in table_opts:
                                        ttext = topt.inner_text().lower()
                                        tvalue = topt.get_attribute('value')
                                        
                                        if 'realisasi' in ttext and 'pendapatan' in ttext:
                                            logger.info(f"      ✅ Found PAD table: {topt.inner_text()}")
                                            table_select.select_option(value=tvalue)
                                            time.sleep(2)
                                            
                                            # Click submit button
                                            submit_btn = page.query_selector('button[type="submit"], input[type="submit"]')
                                            if submit_btn:
                                                logger.info(f"    🖱️  Clicking submit...")
                                                submit_btn.click()
                                                
                                                # Wait for table to appear
                                                page.wait_for_selector('table', timeout=10000)
                                                time.sleep(2)
                                                
                                                # Extract table
                                                html = page.content()
                                                tables = pd.read_html(html)
                                                
                                                if tables:
                                                    logger.info(f"  ✅ Extracted {len(tables)} tables")
                                                    largest = max(tables, key=len)
                                                    largest['province'] = province_name
                                                    largest['scraped_at'] = datetime.now().isoformat()
                                                    
                                                    browser.close()
                                                    return largest
            
            # If we get here, couldn't find the data
            if not subject_found:
                logger.warning(f"  ⚠️  No subject dropdown found")
            
            # Save screenshot for debugging
            screenshot_path = Path("output") / f"debug_{province_name.replace(' ', '_')}.png"
            screenshot_path.parent.mkdir(exist_ok=True)
            page.screenshot(path=str(screenshot_path))
            logger.info(f"  📸 Screenshot saved: {screenshot_path}")
            
            browser.close()
            return pd.DataFrame()
            
        except PlaywrightTimeout as e:
            logger.error(f"  ❌ Timeout: {e}")
            browser.close()
            return pd.DataFrame()
            
        except Exception as e:
            logger.error(f"  ❌ Error: {e}")
            browser.close()
            return pd.DataFrame()


def main():
    """Main function"""
    print("="*80)
    print("BPS PAD Scraper - Interactive Browser Mode")
    print("Using Playwright Direct API")
    print("="*80)
    
    # Test with first province (visible browser for debugging)
    prov_code, prov_info = list(SULAWESI_PROVINCES.items())[0]
    
    print(f"\n{'='*80}")
    print(f"PROVINCE: {prov_info['name']} ({prov_code})")
    print(f"{'='*80}")
    
    data = scrape_pad_data(
        prov_info['query_builder'],
        prov_info['name'],
        headless=False  # Show browser for debugging
    )
    
    if not data.empty:
        # Save immediately
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / f"pad_{prov_code}_{prov_info['name'].replace(' ', '_').lower()}.csv"
        data.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        print(f"\n✅ Success!")
        print(f"📁 Output: {output_file}")
        print(f"📊 Rows: {len(data)}")
        print(f"📋 Columns: {list(data.columns)}")
    else:
        print(f"\n⚠️  No data scraped. Check debug screenshot in output/")
    
    print(f"\n{'='*80}")


if __name__ == "__main__":
    main()
