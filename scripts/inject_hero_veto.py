import sys

with open('pages/6_Audit_D3TLH.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_veto_hero = open('scripts/rebuild_veto.py', 'r', encoding='utf-8').read().split('new_veto_hero = """')[1].split('"""')[0]

hero_start_idx = -1
for i, line in enumerate(lines):
    if '# E. MITOS TATA KELOLA VS OBRAL IZIN' in line:
        hero_start_idx = i - 1
        break

if hero_start_idx != -1:
    del lines[hero_start_idx:]
    lines.insert(hero_start_idx, new_veto_hero + '\n')
    with open('pages/6_Audit_D3TLH.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print('Success hero replacement')
else:
    print('Failed hero start')
