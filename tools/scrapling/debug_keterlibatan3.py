#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

r = requests.get('https://tanahkita.id/data/konflik/detil/RzJuX0hXU2VlaDg')
soup = BeautifulSoup(r.text, 'html.parser')

h4 = soup.find('h4', string=lambda s: s and 'KETERLIBATAN' in s)
if h4:
    next_div = h4.find_next_sibling('div')
    print('Next DIV HTML:')
    print(next_div.prettify()[:2000])
    
    # Look for columns
    cols = next_div.find_all('div', class_=lambda x: x and 'col' in str(x))
    print(f'\n\nFound {len(cols)} columns')
    for i, col in enumerate(cols):
        print(f'\n--- Column {i+1} ---')
        print(col.get_text(separator=' ', strip=True)[:200])
