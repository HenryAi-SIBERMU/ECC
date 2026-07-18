import sys

file_path = "pages/2_Kualitas_Lingkungan.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re
match = re.search(r'fig_map1 = px.choropleth_mapbox.*?\)', content, re.DOTALL)
if match:
    print(match.group(0))
else:
    print("Not found")