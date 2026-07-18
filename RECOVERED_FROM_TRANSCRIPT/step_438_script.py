import sys

file_path = "pages/2_Kualitas_Lingkungan.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_map1 = '''        color_continuous_scale=[
            [0.0, '#8B4513'], # Terburuk (Coklat Tua)
            [0.5, '#D2691E'], # Sedang (Coklat)
            [1.0, '#F4A460']  # Terbaik dari yang terburuk (Coklat Muda/Kuning)
        ],
        zoom=3.8, center={"lat": -1.8, "lon": 120.5}, opacity=0.75,'''

new_map1 = '''        color_continuous_scale=[
            [0.0, '#8B4513'], # 0 - Sangat Kurang
            [0.5, '#D2691E'], # 50 - Kurang (Batas Bawah Gradasi Map)
            [0.65, '#F4A460'],# 65 - Kurang (Batas Atas Gradasi Map)
            [0.7, '#87CEEB'], # 70 - Sedang
            [1.0, '#1E90FF']  # 100 - Sangat Baik
        ],
        range_color=[0, 100],
        zoom=3.8, center={"lat": -1.8, "lon": 120.5}, opacity=0.75,'''

if old_map1 in content:
    content = content.replace(old_map1, new_map1)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Map 1 updated successfully.")
else:
    print("Map 1 text not found.")