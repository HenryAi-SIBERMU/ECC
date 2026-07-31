import re
import os

filepath = r"c:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\tools\streamlittopdf\chapter_3.md"
out_filepath = r"c:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\tools\streamlittopdf\chapter_3_clean.md"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove CSS part
start_marker = "CELIOS — Center of Economic and Law Studies"
idx = content.find(start_marker)
if idx != -1:
    content = content[idx + len(start_marker):].strip()

# Add proper header
lines = content.split('\n')
if len(lines) > 2:
    title = lines[0].strip()
    subtitle = lines[2].strip() if len(lines) > 2 else ""
    
    # recreate top part
    rest = '\n'.join(lines[3:]).strip()
    content = f"# {title}\n\n*{subtitle}*\n\n{rest}"

# 2. Convert Metric Cards to a Markdown Table
# First, let's find all metric cards
cards = re.findall(r'<div class="metric-card">(.*?)</div>\s*(?=</div>|<div|<!--|$|<)', content, flags=re.DOTALL)

def extract_tag_content(tag_class, text):
    match = re.search(f'<div class="{tag_class}">(.*?)</div>', text, flags=re.DOTALL)
    if not match:
        return ""
    val = match.group(1).strip()
    val = re.sub(r'<br\s*/?>', ' ', val)
    val = re.sub(r'<[^>]+>', '', val).strip()
    val = val.replace('\n', ' ')
    # remove extra spaces
    val = re.sub(r'\s+', ' ', val)
    return val

if cards:
    table = "### Metrik Agregat\n\n| Indikator | Nilai | Deskripsi | Sumber |\n| :--- | :--- | :--- | :--- |\n"
    for card in cards:
        val = extract_tag_content("metric-value", card)
        label = extract_tag_content("metric-label", card)
        desc = extract_tag_content("metric-desc", card)
        source = extract_tag_content("metric-source", card)
        table += f"| **{label}** | **{val}** | {desc} | {source} |\n"
    
    # replace the entire block of cards
    content = re.sub(r'(<div class="metric-card">.*?</div>\s*)+', table + '\n\n', content, count=1, flags=re.DOTALL)

# 3. Clean up other HTML tags but don't break markdown
content = re.sub(r'</?(div|span|h\d|p|br|hr|b|i|strong|em|ul|ol|li|a)[^>]*>', '', content)
content = re.sub(r'<[a-zA-Z]+[^>]*>\s*</[a-zA-Z]+>', '', content)

# 4. Some fixes for tables that might be broken by indentation
# In chapter_3.md, some markdown like `| Indikator | Nilai | ...` is indented. Let's un-indent table lines.
content = re.sub(r'^[ \t]+(\|.*\|)$', r'\1', content, flags=re.MULTILINE)

# 5. Clean multiple newlines
content = re.sub(r'\n{3,}', '\n\n', content)
content = content.replace("    **Alur Kausalitas", "> **Alur Kausalitas")

with open(out_filepath, 'w', encoding='utf-8') as f:
    f.write(content.strip())
print("Done")
