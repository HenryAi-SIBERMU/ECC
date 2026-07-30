import os
import glob

# Define the source and destination directories
src_dir = r"C:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\tools\parsing_multimodal\output\faskes\nasional\golden_tables"
dest_dir = r"C:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\tools\parsing_multimodal\output\faskes\nasional"

# 6 Sulawesi provinces
sulawesi_provinces = [
    "Sulawesi Utara",
    "Sulawesi Tengah",
    "Sulawesi Selatan",
    "Sulawesi Tenggara",
    "Gorontalo",
    "Sulawesi Barat"
]

def filter_markdown_table(filepath, dest_dir):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    out_lines = []
    
    table_started = False
    header_found = False
    
    for line in lines:
        if line.strip().startswith('|'):
            table_started = True
            
            # Check if it is a separator line containing only |, -, :, and spaces
            chars_in_line = set(line.strip().replace('|', '').replace('-', '').replace(':', '').replace(' ', ''))
            
            if len(chars_in_line) == 0:
                # It's a separator line
                out_lines.append(line)
                header_found = True
            elif not header_found:
                # It's a table header line
                out_lines.append(line)
            else:
                # It's a data row
                # Check if it contains any of the Sulawesi provinces
                if any(prov.lower() in line.lower() for prov in sulawesi_provinces):
                    out_lines.append(line)
        else:
            # Non-table lines (e.g., titles, headers, empty lines)
            out_lines.append(line)
            # Reset if we left the table
            if table_started and line.strip() == '':
                table_started = False
                header_found = False
            
    basename = os.path.basename(filepath)
    new_filename = f"sulawesi_{basename}"
    dest_path = os.path.join(dest_dir, new_filename)
    
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.writelines(out_lines)

def main():
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    md_files = glob.glob(os.path.join(src_dir, "*.md"))
    print(f"Found {len(md_files)} markdown files in {src_dir}")
    
    count = 0
    for md_file in md_files:
        filter_markdown_table(md_file, dest_dir)
        count += 1
        
    print(f"Successfully processed and generated {count} markdown files for Sulawesi in {dest_dir}")

if __name__ == "__main__":
    main()
