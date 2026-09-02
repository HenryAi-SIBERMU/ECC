import re

file_path = "bab1 bismillah.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update DOCX
docx_pattern = re.compile(r'(master_rows\s*=\s*\[\s*)(.*?)(\s*\])', re.DOTALL)

def docx_replacer(match):
    rows_str = match.group(2)
    new_rows = []
    lines = rows_str.strip().split('\n')
    
    mapping = [
        "sulawesi_izin_baru_per_tahun.csv",
        "sulawesi_kawasan_nikel_luas.csv",
        "sulawesi_pltu_captive.csv",
        "sulawesi_esdm_nikel.csv",
        "sulawesi_investasi_pmdn_2016_2024.csv",
        "sulawesi_pdrb_sektoral_2016_2024.csv",
        "sulawesi_pdrb_sektoral_kabupaten_2016_2024.csv",
        "sulawesi_pad_breakdown_2016_2024.csv",
        "sulawesi_gfw_master_1_dekade_2014_2023_v3.csv",
        "sulawesi_logistik_simpul_nikel.csv"
    ]
    
    for i, line in enumerate(lines):
        if "]" in line and len(line.split(',')) > 3 and i < 10:
            if "sulawesi" not in line:
                line = line.replace('],', f', "{mapping[i]}"],').replace(']', f', "{mapping[i]}"]')
        new_rows.append(line)
        
    return match.group(1) + '\n'.join(new_rows) + match.group(3)

content = docx_pattern.sub(docx_replacer, content)

# 2. Update MD
md_pattern = re.compile(r'(\| No \| Nama Indikator.*?)(?=^\s*""|\Z)', re.MULTILINE | re.DOTALL)

def md_replacer(match):
    text = match.group(1)
    lines = text.strip().split('\n')
    new_lines = []
    
    mapping = [
        "sulawesi_izin_baru_per_tahun.csv",
        "sulawesi_kawasan_nikel_luas.csv",
        "sulawesi_pltu_captive.csv",
        "sulawesi_esdm_nikel.csv",
        "sulawesi_investasi_pmdn_2016_2024.csv",
        "sulawesi_pdrb_sektoral_2016_2024.csv",
        "sulawesi_pdrb_sektoral_kabupaten_2016_2024.csv",
        "sulawesi_pad_breakdown_2016_2024.csv",
        "sulawesi_gfw_master_1_dekade_2014_2023_v3.csv",
        "sulawesi_logistik_simpul_nikel.csv"
    ]
    
    data_idx = 0
    for line in lines:
        if '"| No | Nama Indikator' in line:
            line = line.replace(' Resmi |",', ' Resmi | Data File Asli |",')
            new_lines.append(line)
        elif line.startswith('        "| :---:'):
            new_lines.append('        "| :---: | :--- | :--- | :---: | :---: | :--- | :--- |",')
        elif line.startswith('        "|') and data_idx < 10:
            if "sulawesi" not in line:
                line = line.replace(' |",', f' | `{mapping[data_idx]}` |",').replace(' |"', f' | `{mapping[data_idx]}` |"')
            new_lines.append(line)
            data_idx += 1
        else:
            new_lines.append(line)
            
    return '\n'.join(new_lines) + '\n'

content = md_pattern.sub(md_replacer, content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated successfully")
