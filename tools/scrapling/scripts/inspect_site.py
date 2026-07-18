#!/usr/bin/env python3
"""
Quick site inspector untuk tanahkita.id
Mencari URL dan struktur table yang benar
"""

import requests
from bs4 import BeautifulSoup
import re

def inspect_homepage():
    """Inspect homepage untuk cari link ke data konflik"""
    print("🔍 Inspecting tanahkita.id homepage...\n")
    
    response = requests.get("https://tanahkita.id")
    soup = BeautifulSoup(response.content, 'lxml')
    
    # Cari link yang mengandung "konflik" atau "data"
    print("📋 Links yang relevan:")
    links = soup.find_all('a', href=True)
    
    konflik_links = []
    for link in links:
        href = link.get('href', '')
        text = link.get_text(strip=True)
        
        if any(keyword in href.lower() for keyword in ['konflik', 'data', 'peta']):
            full_url = href if href.startswith('http') else f"https://tanahkita.id{href}"
            konflik_links.append((text, full_url))
            print(f"  - {text}: {full_url}")
    
    print()
    return konflik_links

def test_url(url):
    """Test apakah URL bisa diakses dan punya table"""
    print(f"\n🧪 Testing: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Cari table
            tables = soup.find_all('table')
            print(f"   Tables found: {len(tables)}")
            
            # Cari pagination text
            pagination = soup.find(string=re.compile(r'of \d+ entries'))
            if pagination:
                print(f"   ✅ Pagination: {pagination.strip()}")
            
            # Cari rows
            if tables:
                rows = tables[0].find_all('tr')
                print(f"   Rows in first table: {len(rows)}")
            
            return response.status_code == 200 and len(tables) > 0
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

if __name__ == "__main__":
    # Inspect homepage
    links = inspect_homepage()
    
    # Test common URL patterns
    print("\n" + "="*60)
    print("🧪 Testing common URL patterns...")
    print("="*60)
    
    test_urls = [
        "https://tanahkita.id/data-konflik",
        "https://tanahkita.id/konflik",
        "https://tanahkita.id/peta",
        "https://tanahkita.id/data",
    ]
    
    working_urls = []
    for url in test_urls:
        if test_url(url):
            working_urls.append(url)
    
    # Summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    
    if working_urls:
        print("✅ Working URLs dengan table:")
        for url in working_urls:
            print(f"   - {url}")
    else:
        print("❌ No working URLs found with tables")
        print("\n💡 Suggestion: Inspect the website manually in browser")
        print("   Look for navigation menu or data section")
