import re

with open('tools/streamlittopdf/chapter_3.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove all <style>...</style> blocks
text = re.sub(r'<style>.*?</style>', '', text, flags=re.DOTALL)

# 2. Remove the top sidebar dummy text
text = re.sub(r'<div style="text-align:center; padding: 6px 0 2px 0;">.*?</div>', '', text, flags=re.DOTALL)
text = re.sub(r'<div class="sidebar-label">.*?</div>', '', text, flags=re.DOTALL)
text = re.sub(r'> CELIOS · ECC Intelligence System .*?\n', '', text, flags=re.DOTALL)

# 3. Titles
text = re.sub(r'<div class="org-badge">.*?</div>\n*', '', text, flags=re.DOTALL)
text = re.sub(r'<div class="main-title">(.*?)</div>', r'# \1\n', text, flags=re.DOTALL)
text = re.sub(r'<div class="sub-title">(.*?)</div>', r'*\1*\n', text, flags=re.DOTALL)

# 4. Paragraph blocks (with h2 and p)
def p_replacer(match):
    content = match.group(1)
    content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1\n', content, flags=re.DOTALL)
    content = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n', content, flags=re.DOTALL)
    content = re.sub(r'<i>(.*?)</i>', r'*\1*', content, flags=re.DOTALL)
    content = re.sub(r'<b>(.*?)</b>', r'**\1**', content, flags=re.DOTALL)
    content = re.sub(r'<[^>]+>', '', content)
    return content.strip() + '\n\n'

text = re.sub(r'<div style="background-color: transparent; padding: 10px 0px; margin-bottom: 25px;">(.*?)</div>', p_replacer, text, flags=re.DOTALL)

# 5. Metric Cards -> Table
# Extracting cards first
cards = re.findall(r'<div class="metric-card">.*?<div class="metric-label">(.*?)</div>.*?<div class="metric-value"[^>]*>(.*?)</div>.*?<div class="metric-desc">(.*?)</div>.*?<div class="metric-source">(.*?)</div>.*?</div>', text, flags=re.DOTALL)

if cards:
    table = '### Metrik Agregat\n\n| Indikator | Nilai | Deskripsi | Sumber |\n| :--- | :--- | :--- | :--- |\n'
    for label, value, desc, source in cards:
        label = label.strip()
        value = re.sub(r'<[^>]+>', ' ', value).strip()
        value = re.sub(r'\s+', ' ', value)
        desc = re.sub(r'<i>(.*?)</i>', r'*\1*', desc)
        desc = re.sub(r'<b>(.*?)</b>', r'**\1**', desc)
        desc = desc.replace('\n', ' ').strip()
        source = source.replace('<b>', '**').replace('</b>', '**').replace('<i>', '*').replace('</i>', '*')
        source = source.replace('<br/>', '<br>').replace('<br>', '<br>').strip()
        source = re.sub(r'\s+', ' ', source).replace('<br>', '<br/>')
        table += f'| **{label}** | **{value}** | {desc} | {source} |\n'
    
    # We can identify the whole block of metric cards. They are grouped together.
    # Let's find the start index of the first card and the end index of the last.
    first_card = text.find('<div class="metric-card">')
    # find the end of the last card (there are exactly 5 cards). Let's just remove them individually with a better regex
    # metric-card usually ends with </div>\n</div> or similar. Let's just use regex to remove anything from <div class="metric-card"> up to the next <div class="metric-card"> or <br> or <hr> or ---
    
    # To be safe, we'll replace the block from first <div class="metric-card"> up to the <br><br>\n\n---
    end_block = text.find('<br><br>', first_card)
    if end_block == -1: end_block = text.find('---', first_card)
    if first_card != -1 and end_block != -1:
        text = text[:first_card] + table + '\n\n' + text[end_block:]

# 6. Other Headers
text = re.sub(r'<h2[^>]*>(.*?)</h2>', r'### \1', text, flags=re.DOTALL)
text = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1', text, flags=re.DOTALL)

# 7. Sub-headers with span
text = re.sub(r'<span style="background:#4A148C[^>]*>(.*?)</span>', r'> **\1**', text, flags=re.DOTALL)

# 8. Result: TIDAK SIGNIFIKAN
def result_replacer(match):
    content = match.group(1).strip()
    content = content.replace('<br>', '\n')
    return '**Result: TIDAK SIGNIFIKAN**\n\n' + content

text = re.sub(r'<div style="border: 2px solid #F44336[^>]*>.*?<h4[^>]*>.*?</h4>.*?<p[^>]*>(.*?)</p>.*?</div>', result_replacer, text, flags=re.DOTALL)

# 9. Interpretasi Ekologis
def interpret_replacer(match):
    content = match.group(1)
    content = re.sub(r'<b>(.*?)</b>', r'**\1**', content)
    content = content.replace('<br><br>', '\n> \n> ')
    content = content.replace('<br>', '\n> ')
    return '> ' + content.strip()

text = re.sub(r'<div style="background:#1E1E1E[^>]*>(.*?)</div>', interpret_replacer, text, flags=re.DOTALL)

# 10. Pembedahan Realitas Ekologis
def realitas_replacer(match):
    content = match.group(1)
    content = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', content, flags=re.DOTALL)
    content = re.sub(r'<div[^>]*>', '', content, flags=re.DOTALL)
    content = content.replace('</div>', '')
    content = re.sub(r'<i>(.*?)</i>', r'*\1*', content, flags=re.DOTALL)
    content = content.replace('<br><br>', '\n> \n> ')
    content = content.replace('<br>', '\n> ')
    lines = content.split('\n')
    return '> ' + '\n> '.join([l.strip() for l in lines if l.strip()])

text = re.sub(r'<div style="background-color: rgba\(255, 152, 0, 0.15\)[^>]*>(.*?)</div>', realitas_replacer, text, flags=re.DOTALL)

# 11. Empty divs and brs and specific divs
text = re.sub(r'<div style=\'height: \d+px;\'></div>', '', text)
text = re.sub(r'<div style="color:#B0BEC5[^>]*>(.*?)</div>', r'\1', text, flags=re.DOTALL)
text = re.sub(r'<div style=\'height:\d+px;\'></div>', '', text)

# 12. Paragraphs inside tags
text = re.sub(r'<p style="color:#B0BEC5[^>]*>(.*?)</p>', r'\1\n', text, flags=re.DOTALL)
text = re.sub(r'<p style="color:#E0E0E0[^>]*>(.*?)</p>', r'\1\n', text, flags=re.DOTALL)
text = re.sub(r'<p style="margin: 0; font-family: monospace;\">(.*?)</p>', r'\1\n', text, flags=re.DOTALL)

# Clean up remaining <b> and <i> tags everywhere
text = re.sub(r'<b>(.*?)</b>', r'**\1**', text, flags=re.DOTALL)
text = re.sub(r'<i>(.*?)</i>', r'*\1*', text, flags=re.DOTALL)
text = re.sub(r'<br/?>', '', text)

# Clean up multiple newlines
text = re.sub(r'\n{3,}', '\n\n', text)
text = re.sub(r'---(\n---)+', '---\n', text)

with open('tools/streamlittopdf/chapter_3_clean.md', 'w', encoding='utf-8') as f:
    f.write(text)
