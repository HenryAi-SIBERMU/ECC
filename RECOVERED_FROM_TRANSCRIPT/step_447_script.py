import sys

file_path = "pages/2_Kualitas_Lingkungan.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_map1 = '''        color_continuous_scale=[
            [0.0, '#8B4513'], # Terburuk (Coklat Tua)
            [0.5, '#D2691E'], # Sedang (Coklat)
            [1.0, '#F4A460']  # Terbaik dari yang terburuk (Coklat Muda/Kuning)
        ],
        zoom=3.8, center={"lat": -1.8, "lon": 120.5}, opacity=0.75,
        hover_name="Provinsi", hover_data={"Provinsi": False, "Jumlah_Smelter": True, "Indeks Kualitas Air": ':.1f'},
        mapbox_style="carto-darkmatter", title="IKA BPS (Data Resmi)"
    )
    fig_map1.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ECEFF1', size=11),
        coloraxis_colorbar=dict(title="Skor IKA<br><span style='font-size:10px;color:#D2691E;'>(Coklat = Buruk)</span>")
    )'''

new_map1 = '''        color_continuous_scale=[
            [0.0, '#8B4513'], # 0 - Sangat Kurang
            [0.5, '#D2691E'], # 50 - Kurang
            [0.7, '#F4A460'], # 70 - Sedang
            [0.9, '#87CEEB'], # 90 - Baik
            [1.0, '#1E90FF']  # 100 - Sangat Baik
        ],
        range_color=[0, 100],
        zoom=3.8, center={"lat": -1.8, "lon": 120.5}, opacity=0.75,
        hover_name="Provinsi", hover_data={"Provinsi": False, "Jumlah_Smelter": True, "Indeks Kualitas Air": ':.1f'},
        mapbox_style="carto-darkmatter", title="IKA BPS (Data Resmi)"
    )
    fig_map1.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ECEFF1', size=11),
        coloraxis_colorbar=dict(title="Skor IKA<br><span style='font-size:10px;color:#ECEFF1;'>(Standar KLHK 0-100)</span><br><span style='font-size:9px;color:#1E90FF;'>Biru = Baik</span><br><span style='font-size:9px;color:#D2691E;'>Coklat = Kurang</span>")
    )'''

if old_map1 in content:
    content = content.replace(old_map1, new_map1)
else:
    print("Map 1 text not found.")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated Map 1 to 0-100 scale successfully.")