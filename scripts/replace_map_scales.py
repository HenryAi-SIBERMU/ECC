import sys

file_path = "pages/2_Kualitas_Lingkungan.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace Map 2
old_map2 = '''        color_continuous_scale=[
            [0.0, '#1E90FF'], 
            [0.1, '#87CEEB'], 
            [0.3, '#F4A460'], 
            [0.5, '#D2691E'], 
            [1.0, '#8B4513']
        ],
        zoom=3.8, center={"lat": -1.8, "lon": 120.5}, opacity=0.75,'''

new_map2 = '''        color_continuous_scale=[
            [0.0, '#1E90FF'],   # 0 = Bersih (Biru)
            [0.01, '#F4A460'],  # >0 = Langsung Coklat Muda (Tercemar Ringan)
            [0.2, '#D2691E'],   # ~5 Juta Ton = Coklat (Tercemar Sedang)
            [1.0, '#8B4513']    # ~25 Juta Ton = Coklat Tua (Tercemar Berat)
        ],
        range_color=[0, 25000000],
        zoom=3.8, center={"lat": -1.8, "lon": 120.5}, opacity=0.75,'''

if old_map2 in content:
    content = content.replace(old_map2, new_map2, 1) # Only replace first occurrence (Map 2)
else:
    print("Map 2 text not found.")

# Replace Map 3 (since old_map2 was duplicated for map3, the remaining one is map 3)
new_map3 = '''        color_continuous_scale=[
            [0.0, '#1E90FF'],   # 0 Kasus = Biru
            [0.25, '#F4A460'],  # 1 Kasus = Coklat Muda
            [0.75, '#D2691E'],  # 3 Kasus = Coklat
            [1.0, '#8B4513']    # 4 Kasus = Coklat Tua
        ],
        range_color=[0, 4],
        zoom=3.8, center={"lat": -1.8, "lon": 120.5}, opacity=0.75,'''

if old_map2 in content: # The second occurrence
    content = content.replace(old_map2, new_map3, 1)
else:
    print("Map 3 text not found.")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated Map 2 and Map 3 scales.")
