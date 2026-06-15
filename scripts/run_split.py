import re

with open('pages/3_Beban_Kesehatan.py', 'r', encoding='utf-8') as f:
    content = f.read()

parts = content.split('st.markdown("""\\nPeta interaktif di bawah ini')

if len(parts) > 1:
    with open('inject_map_before_after.py', 'r', encoding='utf-8') as f:
        inject_code = f.read()
    
    # Extract just the new_map_code string from inject_map_before_after.py
    match = re.search(r'new_map_code = \"\"\"(.*?)\"\"\"\n\nnew_content =', inject_code, re.DOTALL)
    if match:
        new_map_code = match.group(1)
        new_content = parts[0] + new_map_code
        with open('pages/3_Beban_Kesehatan.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print('Injeksi Dual Map sukses.')
    else:
        print('Gagal mengekstrak new_map_code')
else:
    print('Gagal split.')
