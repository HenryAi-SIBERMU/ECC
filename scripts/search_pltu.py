import codecs

with codecs.open('pages/2_Kualitas_Lingkungan.py', 'r', 'utf-8') as f:
    content = f.read()

# Let's search for "df_pltu" and its related dataframe preparation to see what the other agent did in the reverted file.
import re

print("Searching for 'Grafik' and 'PLTU'")
for match in re.finditer(r'(.{0,50}PLTU.{0,50})', content, re.IGNORECASE):
    print(f"Match at {match.start()}: {match.group(1)}")
