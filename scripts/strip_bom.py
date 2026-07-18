filename = 'pages/1_Ekspansi_Industri.py'
with open(filename, 'rb') as f:
    content = f.read()

content = content.replace(b'\xef\xbb\xbf', b'') # remove utf-8 BOM
content = content.replace(b'\xfe\xff', b'')     # remove utf-16 BE BOM
content = content.replace(b'\xff\xfe', b'')     # remove utf-16 LE BOM

# just in case it got parsed as a character instead of byte bom
text = content.decode('utf-8')
text = text.replace('\ufeff', '')

with open(filename, 'w', encoding='utf-8', newline='') as f:
    f.write(text)
