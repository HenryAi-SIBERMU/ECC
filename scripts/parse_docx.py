import xml.etree.ElementTree as ET
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
tree = ET.parse(r'c:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\refrensi\Ref\outline_extracted\word\document.xml')
root = tree.getroot()
for p in root.findall('.//w:p', ns):
    texts = [t.text for t in p.findall('.//w:t', ns) if t.text]
    if texts:
        print("".join(texts))
