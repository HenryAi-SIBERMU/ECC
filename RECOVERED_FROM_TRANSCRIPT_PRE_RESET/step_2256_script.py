import sys

file_path = "pages/2_Kualitas_Lingkungan.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the Map 1 configuration
old_map1 = '''        color_continuous_scale=[[0.0, '#8B4513'], [0.3, '#D2691E'], [0.5, '#F4A460'], [0.7, '#87CEEB'], [1.0, '#1E90FF']],
        zoom=3.8, center={"lat": -1.8, "lon": 120.5}, opacity=0.75,'''

new_map1 = '''        color_continuous_scale=[
            [0.0, '#8B4513'], # 0 - Sangat Kurang
            [0.5, '#D2691E'], # 50 - Kurang
            [0.7, '#F4A460'], # 70 - Sedang
            [0.9, '#87CEEB'], # 90 - Baik
            [1.0, '#1E90FF']  # 100 - Sangat Baik
        ],
        range_color=[0, 100],
        zoom=3.8, center={"lat": -1.8, "lon": 120.5}, opacity=0.75,'''

if old_map1 in content:
    content = content.replace(old_map1, new_map1)
else:
    print("Map 1 text not found.")

# Replace the Map 2 configuration to match the 5-stop reverse scale properly
old_map2 = '''        color_continuous_scale=[[0.0, '#1E90FF'], [0.3, '#87CEEB'], [0.5, '#F4A460'], [0.7, '#D2691E'], [1.0, '#8B4513']],
        zoom=3.8, center={"lat": -1.8, "lon": 120.5}, opacity=0.75,'''

new_map2 = '''        color_continuous_scale=[
            [0.0, '#1E90FF'], 
            [0.1, '#87CEEB'], 
            [0.3, '#F4A460'], 
            [0.5, '#D2691E'], 
            [1.0, '#8B4513']
        ],
        zoom=3.8, center={"lat": -1.8, "lon": 120.5}, opacity=0.75,'''

if old_map2 in content:
    content = content.replace(old_map2, new_map2)
else:
    print("Map 2 text not found.")

# Replace Map 3 configuration
if old_map2 in content: # Using old_map2 since the string is identical for map3
    content = content.replace(old_map2, new_map2)

# Replace the Spatial Analysis Text
old_text = '''Pada Peta BPS (kiri), episentrum tambang nikel seperti Sulawesi Tengah dan Tenggara justru dilukiskan dengan warna <b>Biru (Aman/Baik)</b>. Namun, ilusi ini runtuh seketika saat dihadapkan pada realita lapangan (Peta Tengah & Kanan) yang dibuktikan oleh temuan empiris lembaga independen (WALHI, JATAM, AEER):'''

new_text = '''Pada Peta BPS (kiri), jika kita menstandarkan pewarnaan pada ambang batas resmi IKA KLHK (0-100), episentrum tambang nikel seperti Sulteng dan Sultra nyatanya hanya mencetak skor 54-62 (Kategori: Kurang/Tercemar Ringan). Secara visual, warnanya langsung pudar menjadi <b>Coklat Muda/Kusam</b> (bukan biru bersih). Kehancuran ini mencapai puncaknya (Coklat Pekat) saat dihadapkan pada realita lapangan (Peta Tengah & Kanan) yang dibuktikan oleh temuan empiris lembaga independen (WALHI, JATAM, AEER):'''

if old_text in content:
    content = content.replace(old_text, new_text)
else:
    print("Text text not found.")
    
# Remove the part about "diklaim biru oleh BPS" in bullet 1
old_bullet = '''Wilayah yang diklaim "biru" oleh BPS ini justru menimbun limbah mematikan.'''
new_bullet = '''Wilayah yang kualitas airnya "kurang" versi BPS ini nyatanya menimbun limbah mematikan dalam skala apokaliptik.'''
if old_bullet in content:
    content = content.replace(old_bullet, new_bullet)


with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("All replacements done!")