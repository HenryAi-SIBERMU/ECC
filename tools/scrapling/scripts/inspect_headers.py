#!/usr/bin/env python3
"""Inspect table headers dan row structure secara detail"""

import requests
from bs4 import BeautifulSoup

url = "https://tanahkita.id/data/konflik"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'lxml')

table = soup.find('table')
if not table:
    print("No table found!")
    exit()

# Check headers
print("="*80)
print("TABLE HEADERS")
print("="*80)

thead = table.find('thead')
if thead:
    headers_row = thead.find('tr')
    if headers_row:
        headers = headers_row.find_all(['th', 'td'])
        for i, header in enumerate(headers):
            print(f"Header {i}: {header.get_text(strip=True)}")
else:
    print("No thead found, checking first row...")
    first_row = table.find('tr')
    if first_row:
        headers = first_row.find_all(['th', 'td'])
        for i, header in enumerate(headers):
            print(f"Header {i}: {header.get_text(strip=True)}")

# Check data rows
print("\n" + "="*80)
print("SAMPLE DATA ROWS (first 3)")
print("="*80)

tbody = table.find('tbody')
if tbody:
    rows = tbody.find_all('tr')[:3]
else:
    rows = table.find_all('tr')[1:4]  # Skip header

for row_idx, row in enumerate(rows):
    print(f"\n--- ROW {row_idx + 1} ---")
    cols = row.find_all('td')
    print(f"Total columns: {len(cols)}")
    
    for i, col in enumerate(cols):
        text = col.get_text(strip=True)[:80]
        print(f"  Col {i}: {text}")

# Check pagination untuk total entries
print("\n" + "="*80)
print("PAGINATION INFO")
print("="*80)

import re
pagination = soup.find(string=re.compile(r'of \d+ entries'))
if pagination:
    print(f"Found: {pagination.strip()}")
