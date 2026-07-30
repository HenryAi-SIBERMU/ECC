import re

file_path = r'c:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\tools\streamlittopdf\extract_chapter_3.py'
new_md_path = r'c:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\new_md_v2.txt'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

with open(new_md_path, 'r', encoding='utf-8') as f:
    new_md = f.read()

pattern = re.compile(r'    md = f\"\"\"# Beban Kesehatan Masyarakat Terdampak.*?\"\"\"', re.DOTALL)
new_content = pattern.sub(new_md, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated extract_chapter_3.py")
