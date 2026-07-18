import codecs

with codecs.open('pages/2_Kualitas_Lingkungan.py', 'r', 'utf-8') as f:
    content = f.read()

import re
print("Searching for 'Limbah B3'...")
for match in re.finditer(r'(.{0,50}Limbah B3.{0,50})', content, re.IGNORECASE):
    print(f"Match at {match.start()}: {match.group(1)}")
