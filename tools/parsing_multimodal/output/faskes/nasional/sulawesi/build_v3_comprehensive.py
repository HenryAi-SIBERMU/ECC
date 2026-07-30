import os
import glob
import pandas as pd

src_dir = r"C:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\tools\parsing_multimodal\output\faskes\nasional\sulawesi"
out_path = r"C:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\data\processed\sulawesi_faskes_agregat_v3.csv"

sulawesi_provinces = [
    "Sulawesi Utara",
    "Sulawesi Tengah",
    "Sulawesi Selatan",
    "Sulawesi Tenggara",
    "Gorontalo",
    "Sulawesi Barat"
]

def parse_md_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    title = "Unknown"
    for line in lines:
        if line.startswith('#'):
            title = line.strip().replace('#', '').strip()
            break
            
    header = []
    data_rows = []
    
    in_table = False
    for line in lines:
        if line.strip().startswith('|'):
            row = [x.strip() for x in line.split('|')[1:-1]]
            chars = set(line.strip().replace('|', '').replace('-', '').replace(':', '').replace(' ', ''))
            
            if len(chars) == 0:
                in_table = True
            elif not in_table:
                header = row
            else:
                data_rows.append(row)
                
    return title, header, data_rows

def main():
    all_data = []
    
    files = glob.glob(os.path.join(src_dir, 'sulawesi_*.md'))
    for f in files:
        basename = os.path.basename(f)
        parts = basename.split('_')
        year = parts[1] if len(parts) > 1 else "Unknown"
        
        faskes_type = "Unknown"
        if "Puskesmas" in basename:
            faskes_type = "Puskesmas"
        elif "Rumah_Sakit" in basename:
            faskes_type = "Rumah Sakit"
            
        title, header, data_rows = parse_md_file(f)
        
        for row in data_rows:
            # Find the province column in the current row
            prov_col_idx = -1
            found_prov = None
            for idx, cell in enumerate(row):
                for p in sulawesi_provinces:
                    if p.lower() in cell.lower():
                        prov_col_idx = idx
                        found_prov = p
                        break
                if prov_col_idx != -1:
                    break
            
            # If no province found in row, skip (e.g. might be a sub-header or malformed row)
            if found_prov is None:
                continue
                
            # Iterate over columns to extract values
            for idx, cell in enumerate(row):
                if idx == prov_col_idx:
                    continue
                
                var_name = header[idx] if idx < len(header) else f"Column_{idx}"
                
                # Skip the "No" counter column
                if var_name.lower() == 'no' or var_name.lower() == 'provinsi' or var_name.lower() == 'fasilitas kesehatan':
                    continue
                    
                val = cell.strip()
                
                # Append record
                all_data.append({
                    "tahun": year,
                    "provinsi": found_prov,
                    "jenis_faskes": faskes_type,
                    "judul_tabel": title,
                    "variabel": var_name,
                    "nilai": val,
                    "sumber_file": f"nasional/sulawesi/{basename}"
                })
                
    df = pd.DataFrame(all_data)
    df.to_csv(out_path, index=False)
    print(f"Generated comprehensive v3 dataset with {len(df)} records at {out_path}")

if __name__ == "__main__":
    main()
