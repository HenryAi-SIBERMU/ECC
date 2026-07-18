import os

def filter_csv(filepath, valid_headers_start):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    start_idx = 0
    for i, line in enumerate(lines):
        if valid_headers_start in line:
            start_idx = i
            break
            
    if start_idx > 0:
        print(f"Filtering {filepath}, starting from line {start_idx}")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines[start_idx:])

filter_csv('data/raw/raw_kemenkes_diare_2023.csv', 'Jumlah Target Penemuan')
filter_csv('data/raw/raw_kemenkes_kusta_2023.csv', 'Kasus Baru')

