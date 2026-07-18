#!/usr/bin/env python3
"""Debug pagination links"""

import requests
from bs4 import BeautifulSoup

url = "https://tanahkita.id/data/konflik"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'lxml')

# Find pagination
pagination = soup.find('ul', class_=lambda x: x and 'pagination' in str(x))

if pagination:
    print("Pagination found!")
    print("\nPagination HTML:")
    print(pagination.prettify()[:500])
    
    print("\n\nPagination links:")
    for li in pagination.find_all('li')[:10]:  # First 10 items
        link = li.find('a')
        if link and link.get('href'):
            href = link.get('href')
            text = link.get_text(strip=True)
            print(f"  Text: '{text}' | href: '{href}'")
else:
    print("No pagination found!")
    
    # Try alternative selectors
    print("\nSearching for any pagination elements...")
    pag_divs = soup.find_all(class_=lambda x: x and 'pag' in str(x).lower())
    if pag_divs:
        print(f"Found {len(pag_divs)} elements with 'pag' in class")
        for div in pag_divs[:3]:
            print(div.prettify()[:300])
