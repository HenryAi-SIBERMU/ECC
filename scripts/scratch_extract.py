import re
with open('pages/3_Beban_Kesehatan.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Extract f-string markdown
matches = re.findall(r'st\.markdown\(\s*f?\"\"\"(.*?)\"\"\"', content, re.DOTALL)
with open('extracted_3.md', 'w', encoding='utf-8') as f:
    for i, m in enumerate(matches):
        f.write(f'--- BLOCK {i} ---\n')
        f.write(m.strip() + '\n\n')
