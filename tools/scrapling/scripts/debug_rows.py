#!/usr/bin/env python3
"""Debug specific page parsing"""

import requests
from bs4 import BeautifulSoup

url = "https://tanahkita.id/data/konflik?page=2"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'lxml')

table = soup.find('table')
tbody = table.find('tbody')
rows = tbody.find_all('tr')

print(f"Total rows found: {len(rows)}\n")

for i, row in enumerate(rows[:5], 1):
    cols = row.find_all('td', recursive=False)
    
    print(f"="*80)
    print(f"Row {i}:")
    print(f"  Columns count: {len(cols)}")
    
    if len(cols) >= 8:
        print(f"  Col 0 (No): '{cols[0].get_text(strip=True)}' | isdigit: {cols[0].get_text(strip=True).isdigit()}")
        print(f"  Col 1 (Tahun): '{cols[1].get_text(strip=True)}' | isdigit: {cols[1].get_text(strip=True).isdigit()}")
        print(f"  Col 2 (Judul): '{cols[2].get_text(strip=True)[:50]}...'")
        print(f"  Col 3 (Deskripsi): '{cols[3].get_text(strip=True)[:50]}...'")
        print(f"  Col 5 (Lokasi): '{cols[5].get_text(strip=True)}'")
        print(f"  Col 6 (Status): '{cols[6].get_text(strip=True)}'")
        
        # Check for link
        link = cols[7].find('a', href=True)
        print(f"  Col 7 (Detail): {link.get('href') if link else 'NO LINK'}")
    else:
        print(f"  SKIPPED - not enough columns")
