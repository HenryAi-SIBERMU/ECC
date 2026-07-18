with open('pages/0_Overview_Temuan.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

def find_header(text):
    for i, line in enumerate(lines):
        if text in line:
            return i
    return -1

idx_1_1 = find_header('1.1 Tren Izin')
idx_1_2 = find_header('1.2 PLTU Captive')
idx_1_3 = find_header('1.3 Treemap Breakdown')
idx_1_4 = find_header('1.4 Pelabuhan Ekspor')
idx_end = find_header('PAGE 2') - 2

print(f"Indices: 1.1={idx_1_1}, 1.2={idx_1_2}, 1.3={idx_1_3}, 1.4={idx_1_4}, end={idx_end}")

if idx_1_1 != -1 and idx_1_2 != -1 and idx_1_3 != -1 and idx_1_4 != -1 and idx_end != -1:
    block_1 = lines[idx_1_1:idx_1_2]
    block_2 = lines[idx_1_2:idx_1_3]
    block_3 = lines[idx_1_3:idx_1_4]
    block_4 = lines[idx_1_4:idx_end]

    def replace_in_block(block, old, new):
        return [l.replace(old, new) for l in block]

    block_1 = replace_in_block(block_1, '1.1 Tren Pertumbuhan', '1.3 Tren Pertumbuhan')
    block_1 = replace_in_block(block_1, '1.1 Tren Izin', '1.3 Tren Izin')

    block_3 = replace_in_block(block_3, '1.3 Realisasi Investasi', '1.4 Realisasi Investasi')
    block_3 = replace_in_block(block_3, '1.3 Treemap Breakdown', '1.4 Treemap Breakdown')

    block_4 = replace_in_block(block_4, '1.4 Pelabuhan Ekspor', '1.5 Pelabuhan Ekspor')

    new_lines = lines[:idx_1_1] + block_2 + block_1 + block_3 + block_4 + lines[idx_end:]

    with open('pages/0_Overview_Temuan.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print('Success')
else:
    print('Failed to find indices')
