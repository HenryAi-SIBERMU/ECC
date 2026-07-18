import re

with open('pages/12_Infografis_Summary.py', 'r', encoding='utf-8') as f:
    content = f.read()

# find row_02_html block
match = re.search(r'(row_02_html = f\"\"\"[\s\S]*?\"\"\")', content)
if match:
    row_02_code = match.group(1)
    
    # remove it from current location
    content = content.replace(row_02_code + '\n', '')
    
    # insert before poster_html
    insert_marker = 'poster_html = f"""<!DOCTYPE html>'
    if insert_marker in content:
        content = content.replace(insert_marker, row_02_code + '\n\n' + insert_marker)
        with open('pages/12_Infografis_Summary.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print('Successfully moved row_02_html up!')
    else:
        print('Could not find insert_marker')
else:
    print('Could not find row_02_html block')
