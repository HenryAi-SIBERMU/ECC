import re

with open('pages/0_Overview_Temuan.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

def get_block(start_idx, end_idx):
    return lines[start_idx:end_idx]

# Find indices based on headers
def find_header(pattern):
    for i, line in enumerate(lines):
        if re.search(pattern, line):
            return i
    return -1

idx_1_1 = find_header(r'# \xef\xbf\xbd 1\.1 Tren Izin')
idx_1_2 = find_header(r'# \xef\xbf\xbd 1\.2 PLTU Captive')
idx_1_3 = find_header(r'# \xef\xbf\xbd 1\.3 Treemap Breakdown')
idx_1_4 = find_header(r'# \xef\xbf\xbd 1\.4 Pelabuhan Ekspor')
idx_end = find_header(r'# \xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\n# PAGE 2')

if idx_end == -1:
    idx_end = find_header(r'# PAGE 2') - 1

print(f"Indices: 1.1={idx_1_1}, 1.2={idx_1_2}, 1.3={idx_1_3}, 1.4={idx_1_4}, end={idx_end}")

block_1 = lines[idx_1_1:idx_1_2]
block_2 = lines[idx_1_2:idx_1_3]
block_3 = lines[idx_1_3:idx_1_4]
block_4 = lines[idx_1_4:idx_end]

# Rename headers in blocks
def replace_in_block(block, old, new):
    return [l.replace(old, new) for l in block]

block_1 = replace_in_block(block_1, '1.1 Tren Pertumbuhan', '1.3 Tren Pertumbuhan')
block_1 = replace_in_block(block_1, '1.1 Tren Izin', '1.3 Tren Izin')

block_3 = replace_in_block(block_3, '1.3 Realisasi Investasi', '1.4 Realisasi Investasi')
block_3 = replace_in_block(block_3, '1.3 Treemap Breakdown', '1.4 Treemap Breakdown')

block_4 = replace_in_block(block_4, '1.4 Pelabuhan Ekspor', '1.5 Pelabuhan Ekspor')

# New order: block 2, block 1, block 3, block 4
new_lines = lines[:idx_1_1] + block_2 + block_1 + block_3 + block_4 + lines[idx_end:]

with open('pages/0_Overview_Temuan.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Success')
