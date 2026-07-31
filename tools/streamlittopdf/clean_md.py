import re
import os

filepath = r"c:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\tools\streamlittopdf\chapter_3.md"
out_filepath = r"c:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\tools\streamlittopdf\chapter_3_clean.md"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove <style> tags and their content
content = re.sub(r'<style.*?>.*?</style>', '', content, flags=re.DOTALL)

# 2. Convert Metric Cards to a Markdown Table
# First, let's find all metric cards
cards = re.findall(r'<div class="metric-card">(.*?)</div>\s*(?=</div>|<div|<!--|$)', content, flags=re.DOTALL)

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
    
    # We need to replace the HTML block containing these cards with the new table.
    # We can match the encompassing div if possible, or just replace the first card and remove others.
    # Actually, a simpler way is to find the bounds of the cards.
    first_card_start = content.find('<div class="metric-card">')
    last_card_end = content.rfind('</div>', 0, content.rfind('<div class="metric-card">') + len(card) + 100) # approximate
    # Let's just use regex to replace the whole chunk of cards
    # Assuming they are together in a layout.
    content = re.sub(r'(<div class="metric-card">.*?</div>\s*)+', table + '\n', content, count=1, flags=re.DOTALL)

# 3. Remove all other raw HTML tags but keep the text
# However, we must not remove markdown tags like ![Chart](...) or tables. 
# HTML tags like <div ...>, </div>, <span ...>, </span>
content = re.sub(r'</?(div|span|h\d|p|br|hr|b|i|strong|em|ul|ol|li|a)[^>]*>', '', content)

# Remove any leftover empty HTML tags just in case
content = re.sub(r'<[a-zA-Z]+[^>]*>\s*</[a-zA-Z]+>', '', content)

# 4. Clean up multiple newlines and spaces
content = re.sub(r'\n{3,}', '\n\n', content)

with open(out_filepath, 'w', encoding='utf-8') as f:
    f.write(content.strip())
print("Done")
