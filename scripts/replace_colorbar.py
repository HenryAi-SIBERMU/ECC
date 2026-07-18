import sys
import re

file_path = "pages/2_Kualitas_Lingkungan.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

pattern = r'coloraxis_colorbar=dict\(title="Skor IKA<br><span style=\'font-size:10px;color:#D2691E;\'><.*?</span>"\)'

replacement = r'''coloraxis_colorbar=dict(title="Skor IKA<br><span style='font-size:10px;color:#ECEFF1;'>(Standar KLHK 0-100)</span><br><span style='font-size:9px;color:#1E90FF;'>Biru = Baik</span><br><span style='font-size:9px;color:#D2691E;'>Coklat = Kurang</span>")'''

new_content = re.sub(pattern, replacement, content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)
print("Colorbar updated.")
