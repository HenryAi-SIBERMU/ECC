import sys

file_path = "pages/2_Kualitas_Lingkungan.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. MAP 1
old_map1 = '''        color_continuous_scale=[[0.0, '#8B4513'], [0.3, '#D2691E'], [0.5, '#F4A460'], [0.7, '#87CEEB'], [1.0, '#1E90FF']],
        zoom=3.8, center={"lat": -1.8, "lon": 120.5}, opacity=0.75,
        hover_name="Provinsi", hover_data={"Provinsi": False, "Jumlah_Smelter": True, "Indeks Kualitas Air": ':.1f'},
        mapbox_style="carto-darkmatter", title="IKA BPS (Data Resmi/Paradoks)"
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
content = content.replace(old_map1, new_map1)

# 2. MAP 2
old_map2 = '''        color_continuous_scale=[[0.0, '#1E90FF'], [0.3, '#87CEEB'], [0.5, '#F4A460'], [0.7, '#D2691E'], [1.0, '#8B4513']],
        zoom=3.8, center={"lat": -1.8, "lon": 120.5}, opacity=0.75,'''

new_map2 = '''        color_continuous_scale=[
            [0.0, '#1E90FF'],   # 0 = Bersih (Biru)
            [0.01, '#F4A460'],  # >0 = Langsung Coklat Muda (Tercemar Ringan)
            [0.2, '#D2691E'],   # ~5 Juta Ton = Coklat (Tercemar Sedang)
            [1.0, '#8B4513']    # ~25 Juta Ton = Coklat Tua (Tercemar Berat)
        ],
        range_color=[0, 25000000],
        zoom=3.8, center={"lat": -1.8, "lon": 120.5}, opacity=0.75,'''
content = content.replace(old_map2, new_map2, 1)

# 3. MAP 3 (Second occurrence of old_map2)
new_map3 = '''        color_continuous_scale=[
            [0.0, '#1E90FF'],   # 0 Kasus = Biru
            [0.25, '#F4A460'],  # 1 Kasus = Coklat Muda
            [0.75, '#D2691E'],  # 3 Kasus = Coklat
            [1.0, '#8B4513']    # 4 Kasus = Coklat Tua
        ],
        range_color=[0, 4],
        zoom=3.8, center={"lat": -1.8, "lon": 120.5}, opacity=0.75,'''
content = content.replace(old_map2, new_map3, 1)

# 4. TEXT BLOCK
old_text = '''<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #D32F2F; margin-bottom: 25px;">
    <b>Pembedahan Spasial:</b> Peta geospasial di atas menyingkap realitas berdarah dari hilirisasi. Lingkaran raksasa yang berada di Sulawesi Tengah dan Sulawesi Tenggara merepresentasikan konsentrasi masif fasilitas smelter. Sangat memprihatinkan bahwa pada episentrum industri inilah, warna lingkaran berubah drastis menjadi merah pekat—menandakan skor Indeks Kualitas Air (IKA) yang terjun bebas. Ini bukan lagi sekadar penurunan indikator, melainkan penciptaan <i>zona tumbal ekologis</i> akibat pencemaran aliran sungai dan pembuangan tailing (yang mengandung logam berat mematikan seperti Kromium Heksavalen).
</div>'''

new_text = '''<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #D32F2F; margin-bottom: 25px; line-height: 1.6;">
    <b style="color:#FF5252; font-size:1.1em;">Pembedahan Spasial (Validasi Kehancuran Ekologis):</b><br>
    Ketiga peta di atas justru saling mengkonfirmasi <b>krisis ekologis</b> yang tak terbantahkan. Pada Peta BPS (kiri), data resmi negara sendiri telah mengakui bahwa episentrum tambang nikel (Sulteng, Sultra, Sulsel) berada dalam kondisi kritis dengan skor IKA hanya 54-62 (Kategori: Kurang/Cemar). Namun, di atas ekosistem yang sudah sekarat inilah, industri dibiarkan terus membuang limbah secara ugal-ugalan (Peta Tengah & Kanan) yang dibuktikan oleh temuan empiris lembaga independen (WALHI, JATAM, AEER):<br><br>
    <ul style="margin-top: 0; margin-bottom: 10px;">
        <li><b>Beban Limbah Fantastis (Peta Tengah):</b> Di atas wilayah yang kualitas airnya sudah "Kurang" versi BPS ini, nyatanya terus ditimbun limbah mematikan dalam skala apokaliptik. Di Sulteng (IMIP & sekitarnya), diproduksi <b>12 Juta Ton</b> slag & tailing HPAL, <b>7 Juta Ton</b> dari PT HNC, dan <b>5,5 Juta Ton</b> dari PT QMB per tahun. Di Sultra (VDNI & Konawe), timbulan slag feronikel mencapai <b>6,5 Juta Ton</b> per tahun.</li>
        <li><b>Kematian Sungai & Pencemaran Cr6+ (Peta Kanan):</b> Dampaknya langsung membunuh urat nadi ekologis. Di Sulteng, setidaknya <b>4 sungai dan pesisir (Bahodopi, Laroenai, Morowali, Fatufia)</b> tercemar berat logam beracun (Kromium Heksavalen/Cr6+).</li>
        <li><b>Bencana Ekologis & Migrasi Satwa Buas:</b> Di Sultra, pelepasan <b>800.000 Ton</b> air limbah tambang (oleh PT SCM) ke Sungai Lalindu, Lasolo, dan Konaweha menyebabkan sungai berubah keruh pekat akibat TSS (Total Suspended Solid). Hal ini memicu banjir lumpur masif dan memaksa satwa liar (buaya) bermigrasi hingga ke muara dan pemukiman karena habitat aslinya hancur.</li>
    </ul>
    Tidak ada paradoks di sini; data BPS dan realita lapangan sama-sama berteriak bahwa wilayah ini telah diubah menjadi <i>Zona Tumbal Ekologis</i> demi ambisi hilirisasi industri nikel.
</div>'''
content = content.replace(old_text, new_text)

# 5. IKU COLORBAR FIX
old_iku = '''          marker=dict(
              color=[85],
              colorscale=[[0, '#FF1744'], [0.33, '#FF1744'], [0.33, '#FFD600'], [0.67, '#FFD600'], [0.67, '#00E676'], [1, '#00E676']],
              cmin=80, cmax=95,
              colorbar=dict(
                  title=dict(text="IKU", font=dict(color='#ECEFF1', size=12)),
                  tickvals=[80, 85, 90, 95],
                  ticktext=['80<br>merah = buruk', '85', '90', '95'],
                  len=0.5,
                  y=0.5,
                  x=1.02,
                  tickfont=dict(color='#ECEFF1'),
                  bgcolor='rgba(0,0,0,0)',
                  borderwidth=0,
              ),'''

new_iku = '''          marker=dict(
              color=[85],
              colorscale=[
                  [0.0, '#FF1744'],
                  [0.5, '#FFD600'],
                  [1.0, '#00E676']
              ],
              cmin=80, cmax=95,
              colorbar=dict(
                  title=dict(text="IKU<br>merah = buruk", font=dict(color='#ECEFF1', size=12), side="right"),
                  tickvals=[80, 85, 90, 95],
                  ticktext=['80', '85', '90', '95'],
                  len=0.5,
                  y=0.5,
                  x=1.02,
                  tickfont=dict(color='#ECEFF1'),
                  bgcolor='rgba(0,0,0,0)',
                  borderwidth=0,
              ),'''
content = content.replace(old_iku, new_iku)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("All fixes applied successfully.")
