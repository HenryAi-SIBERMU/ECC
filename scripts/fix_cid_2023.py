import re
import os

def decode_cid(match):
    val = int(match.group(1))
    
    # Digits: 882=0, 883=1, ..., 891=9
    if 882 <= val <= 891:
        return chr(val - 834)
    # Lowercase letters: 'a' is 97. (cid:131) is 'a'. 131 - 34 = 97
    elif 131 <= val <= 156:
        return chr(val - 34)
    # Uppercase letters: 'A' is 65. (cid:4) is 'A'? Wait. 
    # S is (cid:22) -> 22+61 = 83. A is 65. 65 - 61 = 4. 
    elif 4 <= val <= 29:
        return chr(val + 61)
    # Space: (cid:3)
    elif val == 3:
        return ' '
    # Dot: (cid:484) -> '.'
    elif val == 484:
        return '.'
    # Comma: (cid:481) -> change to dot so it doesn't break CSV format!
    elif val == 481:
        return '.'
    # Hyphen: (cid:461) maybe? Let's just return ? for unknown
    else:
        return '?'

def fix_file(filepath):
    print(f"Fixing {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    fixed_content = re.sub(r'\(cid:(\d+)\)', decode_cid, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

files = [
    'data/raw/raw_kemenkes_ispa_2023.csv',
    'data/raw/raw_kemenkes_diare_2023.csv',
    'data/raw/raw_kemenkes_kusta_2023.csv',
    'data/raw/raw_kemenkes_malaria_2023.csv'
]

for file in files:
    if os.path.exists(file):
        fix_file(file)
    else:
        print(f"Not found: {file}")
