import sys
import re

file_path = "pages/2_Kualitas_Lingkungan.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Pattern to replace everything between color="Indeks Kualitas Air", and zoom=3.8,
pattern = r'(color="Indeks Kualitas Air",\s*)color_continuous_scale=\[.*?\],\s*(zoom=3.8,)'

replacement = r'''\g<1>color_continuous_scale=[
            [0.0, '#8B4513'], # 0 - Sangat Kurang
            [0.5, '#D2691E'], # 50 - Kurang
            [0.7, '#F4A460'], # 70 - Sedang
            [0.9, '#87CEEB'], # 90 - Baik
            [1.0, '#1E90FF']  # 100 - Sangat Baik
        ],
        range_color=[0, 100],
        \g<2>'''

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)
print("Updated successfully via regex.")
