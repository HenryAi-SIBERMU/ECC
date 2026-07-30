import os
import glob
import json

src_dir = r"C:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\tools\parsing_multimodal\output\faskes\nasional\sulawesi"
files = glob.glob(os.path.join(src_dir, 'sulawesi_*.md'))

schema_info = []

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
    title = "Unknown"
    header = []
    
    in_table = False
    for line in lines:
        if line.startswith('#'):
            title = line.strip().replace('#', '').strip()
        elif line.strip().startswith('|'):
            row = [x.strip() for x in line.split('|')[1:-1]]
            chars = set(line.strip().replace('|', '').replace('-', '').replace(':', '').replace(' ', ''))
            
            if len(chars) == 0:
                in_table = True
            elif not in_table:
                header = row

    basename = os.path.basename(f)
    parts = basename.split('_')
    # Name format: sulawesi_2015_Puskesmas_page_282.md
    if len(parts) >= 3:
        year = parts[1]
        faskes_type = parts[2]
        if parts[2] == "Rumah" and parts[3] == "Sakit":
            faskes_type = "Rumah Sakit"
    else:
        year = "Unknown"
        faskes_type = "Unknown"
        
    schema_info.append({
        "file": basename,
        "year": year,
        "type": faskes_type,
        "title": title,
        "columns": header
    })

out_path = os.path.join(src_dir, 'schema_analysis.json')
with open(out_path, 'w', encoding='utf-8') as out:
    json.dump(schema_info, out, indent=2)

print(f"Analyzed {len(files)} files. Output saved to {out_path}")
