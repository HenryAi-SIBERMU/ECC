import re

with open('pages/3_Beban_Kesehatan.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Truncate at line 684 (index 683)
truncated_lines = lines[:683]

with open('inject_map_before_after.py', 'r', encoding='utf-8') as f:
    inject_code = f.read()

match = re.search(r'new_map_code = \"\"\"(.*?)\"\"\"\n\nnew_content =', inject_code, re.DOTALL)
if match:
    new_map_code = match.group(1)
    with open('pages/3_Beban_Kesehatan.py', 'w', encoding='utf-8') as f:
        f.writelines(truncated_lines)
        f.write(new_map_code)
    print('Injeksi Dual Map sukses by lines.')
else:
    print('Gagal extract new_map_code.')
