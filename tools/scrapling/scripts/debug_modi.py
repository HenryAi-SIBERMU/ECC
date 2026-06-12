#!/usr/bin/env python3
"""
MODI Portal Debugger
Test different URL patterns and selectors
"""

import sys
from pathlib import Path
from scrapling.fetchers import StealthyFetcher
from bs4 import BeautifulSoup

# URLs to test
URLS_TO_TEST = [
    "https://modi.esdm.go.id",
    "https://modi.esdm.go.id/portal",
    "https://modi.esdm.go.id/portal/",
    "https://modi.esdm.go.id/portal/index",
]

def test_url(url: str):
    """Test a single URL"""
    print(f"\n{'='*80}")
    print(f"Testing: {url}")
    print(f"{'='*80}")
    
    try:
        page = StealthyFetcher.fetch(
            url,
            headless=False,
            network_idle=True,
            timeout=45000
        )
        
        print(f"✅ Status: {page.status}")
        print(f"✅ URL after redirect: {page.url}")
        print(f"✅ Title: {page.title}")
        
        # Save HTML for inspection
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        filename = url.replace("https://", "").replace("/", "_") + ".html"
        html_path = output_dir / filename
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(page.html_content)
        
        print(f"📄 HTML saved: {html_path}")
        
        # Parse and check for table
        soup = BeautifulSoup(page.html_content, 'lxml')
        
        tables = soup.find_all('table')
        print(f"📊 Tables found: {len(tables)}")
        
        if tables:
            print(f"   Table 1 has {len(tables[0].find_all('tr'))} rows")
            
            # Check headers
            headers = tables[0].find_all('th')
            if headers:
                print(f"   Headers: {[h.get_text(strip=True) for h in headers]}")
        
        # Check pagination
        pagination = soup.find(string=lambda x: x and 'dari' in x.lower() and 'data' in x.lower())
        if pagination:
            print(f"📄 Pagination text: {pagination.strip()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("MODI Portal URL Debugger")
    print("="*80)
    
    for url in URLS_TO_TEST:
        success = test_url(url)
        if success:
            print(f"\n✅ {url} works!")
        else:
            print(f"\n❌ {url} failed!")
        
        input("\nPress Enter to test next URL...")
    
    print("\n" + "="*80)
    print("Testing complete! Check output/ folder for HTML files.")
    print("="*80)


if __name__ == "__main__":
    main()
