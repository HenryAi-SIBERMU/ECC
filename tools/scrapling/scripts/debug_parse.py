#!/usr/bin/env python3
"""Debug script untuk inspect HTML structure - UPDATED"""

import requests
from bs4 import BeautifulSoup

url = "https://tanahkita.id/data/konflik"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'lxml')

table = soup.find('table')
if not table:
    print("No table found!")
    exit()

# Get first row untuk inspect structure
tbody = table.find('tbody')
if tbody:
    rows = tbody.find_all('tr')
    
    if rows:
        print("="*80)
        print("FIRST ROW - DETAILED STRUCTURE")
        print("="*80)
        
        first_row = rows[0]
        cols = first_row.find_all('td')
        
        print(f"\nTotal columns: {len(cols)}\n")
        
        for i, col in enumerate(cols):
            print(f"{'='*60}")
            print(f"Column {i}:")
            print(f"{'='*60}")
            print(f"Raw HTML:\n{col.prettify()[:300]}...")
            print(f"\nText: {col.get_text(strip=True)[:100]}")
            
            # Check for links
            links = col.find_all('a', href=True)
            if links:
                print(f"\n✅ Links found: {len(links)}")
                for link in links:
                    print(f"    - href: {link.get('href')}")
                    print(f"      text: {link.get_text(strip=True)[:50]}")
            
            # Check for badges
            badges = col.find_all(class_=lambda x: x and ('badge' in str(x)))
            if badges:
                print(f"\n✅ Badges found:")
                for b in badges:
                    print(f"    - class: {b.get('class')}")
                    print(f"      text: {b.get_text(strip=True)}")
                    print(f"      style: {b.get('style')}")
            
            # Check for buttons
            buttons = col.find_all('button')
            if buttons:
                print(f"\n✅ Buttons found: {len(buttons)}")
            
            print()
        
        print("\n" + "="*80)
        print("ROW 6 (for comparison - has 'Hutan Lindung' status)")
        print("="*80)
        
        if len(rows) >= 6:
            row6 = rows[5]  # Row 6 (0-indexed as 5)
            cols6 = row6.find_all('td')
            print(f"\nTotal columns in row 6: {len(cols6)}")
            
            if len(cols6) >= 6:
                print(f"\nColumn 5 (Status) in row 6:")
                print(cols6[5].prettify())
                
            if len(cols6) >= 7:
                print(f"\nColumn 6 (Detail) in row 6:")
                print(cols6[6].prettify())
