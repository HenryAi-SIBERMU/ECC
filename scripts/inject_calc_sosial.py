import sys

with open('pages/6_Audit_D3TLH.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_sosial_calc = open('scripts/rebuild_sosial.py', 'r', encoding='utf-8').read().split('new_sosial_calc = """')[1].split('"""')[0]

calc_start = -1
calc_end = -1
for i, line in enumerate(lines):
    if 'skor_sosial_1 = 0' in line and 'konflik_darat = 0' in lines[i+1]:
        calc_start = i
        break

for i in range(calc_start, len(lines)):
    if 'luas_izin_sentra = 0' in lines[i]:
        calc_end = i
        break

if calc_start != -1 and calc_end != -1:
    del lines[calc_start:calc_end]
    lines.insert(calc_start, new_sosial_calc + '\n\n')
    with open('pages/6_Audit_D3TLH.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print('Success calc replacement')
else:
    print('Failed calc', calc_start, calc_end)
