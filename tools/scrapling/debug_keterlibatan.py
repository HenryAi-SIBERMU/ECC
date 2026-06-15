#!/usr/bin/env python3
"""Debug keterlibatan extraction"""

import requests
from bs4 import BeautifulSoup

url = "https://tanahkita.id/data/konflik/detil/RzJuX0hXU2VlaDg"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

print("=== Looking for KETERLIBATAN section ===\n")

# Find all text containing "KETERLIBATAN"
for elem in soup.find_all(string=lambda text: text and 'KETERLIBATAN' in text.upper()):
    print(f"Found in: {elem.parent.name}")
    print(f"Text: {elem[:100]}")
    print()

# Find the section
print("\n=== Finding KETERLIBATAN structure ===\n")
for section in soup.find_all(['div', 'section', 'table']):
    text = section.get_text(strip=True)
    if 'KETERLIBATAN' in text.upper():
        print(f"Section type: {section.name}")
        print(f"Section class: {section.get('class')}")
        print(f"Full HTML:\n{section.prettify()[:1000]}")
        break

print("\n=== Looking for SUMBER ===\n")
for elem in soup.find_all(string=lambda text: text and 'Sumber' in text):
    print(f"Found: {elem.parent.name}")
    parent = elem.parent
    print(f"Next sibling: {parent.find_next_sibling()}")
    print()
