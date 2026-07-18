#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

r = requests.get('https://tanahkita.id/data/konflik/detil/RzJuX0hXU2VlaDg')
soup = BeautifulSoup(r.text, 'html.parser')

# Find KETERLIBATAN heading
h4 = soup.find('h4', string=lambda s: s and 'KETERLIBATAN' in s)
print('Found H4:', h4)

if h4:
    print('\nNext siblings:')
    for i, sib in enumerate(h4.find_next_siblings()):
        if sib.name:
            print(f'{i}. <{sib.name}>: {sib.get_text(strip=True)[:150]}')
            if 'KONTEN' in sib.get_text(strip=True):
                break
