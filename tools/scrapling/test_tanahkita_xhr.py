#!/usr/bin/env python3
"""Test TanahKita detail page structure"""

import requests
from bs4 import BeautifulSoup
import json

# Test URL (case #1)
url = "https://tanahkita.id/data/konflik/detil/S2QwbDdDLWttVEk"

print(f"Fetching: {url}\n")

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all tables
tables = soup.find_all('table')
print(f"=== Found {len(tables)} tables ===\n")

for i, table in enumerate(tables):
    print(f"\n--- Table {i+1} ---")
    rows = table.find_all('tr')
    for row in rows[:10]:  # First 10 rows
        cells = row.find_all(['td', 'th'])
        if cells:
            print(" | ".join([cell.get_text(strip=True) for cell in cells]))

# Check for any API/XHR endpoints in script tags
print("\n\n=== Checking for API endpoints in scripts ===")
scripts = soup.find_all('script')
for script in scripts:
    if script.string:
        if 'api' in script.string.lower() or 'xhr' in script.string.lower() or 'fetch' in script.string.lower():
            print("Found potential API call:")
            print(script.string[:300])
            print("...")

# Look for data attributes or JSON
print("\n\n=== Checking for data attributes ===")
elements_with_data = soup.find_all(attrs={'data-detail': True}) + soup.find_all(attrs={'data-konflik': True})
for elem in elements_with_data[:5]:
    print(f"Tag: {elem.name}, Data: {elem.attrs}")
