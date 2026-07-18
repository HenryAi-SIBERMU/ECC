import sys
filename = 'pages/1_Ekspansi_Industri.py'
with open(filename, 'r', encoding='utf-8') as f:
    lines = f.readlines()

out_lines = []
for i, line in enumerate(lines):
    if line.strip() == '# === Peta Jalur Distribusi Logistik (PyDeck) ===':
        break
    out_lines.append(line)

with open(filename, 'w', encoding='utf-8') as f:
    f.writelines(out_lines)
