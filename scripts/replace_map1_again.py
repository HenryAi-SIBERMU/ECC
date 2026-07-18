import sys

file_path = "pages/2_Kualitas_Lingkungan.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_text = '''        color_continuous_scale=[
            [0.0, '#8B4513'], # Terburuk (Coklat Tua)
            [0.5, '#D2691E'], # Sedang (Coklat)
            [1.0, '#F4A460']  # Terbaik dari yang terburuk (Coklat Muda/Kuning)
        ],'''

new_text = '''        color_continuous_scale=[
            [0.0, '#8B4513'], # 0 - Sangat Kurang
            [0.5, '#D2691E'], # 50 - Kurang
            [0.7, '#F4A460'], # 70 - Sedang
            [0.9, '#87CEEB'], # 90 - Baik
            [1.0, '#1E90FF']  # 100 - Sangat Baik
        ],'''

if old_text in content:
    content = content.replace(old_text, new_text)
else:
    print("Color scale not found.")

old_colorbar = '''coloraxis_colorbar=dict(title="Skor IKA<br><span style='font-size:10px;color:#D2691E;'>(Coklat = Buruk)</span>")'''
new_colorbar = '''coloraxis_colorbar=dict(title="Skor IKA<br><span style='font-size:10px;color:#ECEFF1;'>(Standar KLHK 0-100)</span><br><span style='font-size:9px;color:#1E90FF;'>Biru = Baik</span><br><span style='font-size:9px;color:#D2691E;'>Coklat = Kurang</span>")'''

if old_colorbar in content:
    content = content.replace(old_colorbar, new_colorbar)
else:
    print("Colorbar text not found.")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated!")
