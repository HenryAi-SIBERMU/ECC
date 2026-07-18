import sys

file_path = "pages/2_Kualitas_Lingkungan.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. FIX SPATIAL TEXT (Use find and replace precisely based on what's there now)
old_text = '''<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #D32F2F; margin-bottom: 25px;">
    <b>Pembedahan Spasial:</b> Peta geospasial di atas menyingkap realitas berdarah dari hilirisasi. Lingkaran raksasa yang berada di Sulawesi Tengah dan Sulawesi Tenggara merepresentasikan konsentrasi masif fasilitas smelter. Sangat memprihatinkan bahwa pada episentrum industri inilah, warna lingkaran berubah drastis menjadi merah pekat—menandakan skor Indeks Kualitas Air (IKA) yang terjun bebas. Ini bukan lagi sekadar penurunan indikator, melainkan penciptaan <i>zona tumbal ekologis</i> akibat pencemaran aliran sungai dan pembuangan tailing.
</div>'''

# Let's replace the whole block by finding the start and end since there's a weird unicode dash there
start = content.find('<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #D32F2F; margin-bottom: 25px;">')
end = content.find('</div>', start) + 6

if start != -1 and end != -1:
    actual_old_text = content[start:end]
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
    content = content.replace(actual_old_text, new_text)
    print("Fixed spatial text.")

# 2. IKU LABEL FIX (ONLY change the label, keep the blocks exactly the same)
start_iku = content.find('colorbar=dict(')
iku_loc = content.find('title=dict(text="IKU", font=dict(color=\'#ECEFF1\', size=12))')
if iku_loc != -1:
    new_iku_title = 'title=dict(text="IKU<br>merah = buruk", font=dict(color=\'#ECEFF1\', size=12), side="right")'
    content = content.replace('title=dict(text="IKU", font=dict(color=\'#ECEFF1\', size=12))', new_iku_title)
    content = content.replace("ticktext=['80<br>merah = buruk', '85', '90', '95']", "ticktext=['80', '85', '90', '95']")
    print("Fixed IKU label format.")

# 3. FIX MAP 1 (BPS) COLOR SCALE TO EXACTLY WHAT WAS IN IMAGE 1 (Blue gradient for IKA)
map1_start = content.find('fig_map1 = px.choropleth_mapbox(')
map1_end = content.find('st.plotly_chart(fig_map1, use_container_width=True)', map1_start)
if map1_start != -1 and map1_end != -1:
    map1_code = content[map1_start:map1_end]
    
    # In Image 1, it's just the default Plotly behavior or a very specific color scale from 54-62.
    # We will ensure the color scale uses Blues or similar.
    # The original was likely not hardcoded or used a specific continuous scale.
    # Looking at the original commit we reverted to (b123167), it probably had:
    # color_continuous_scale="Oranges" or something similar if it was red/orange. But Image 1 shows it as BLUE!
    # Let's replace the whole choropleth block to make it blue and match the labels.
    
    new_map1_code = '''fig_map1 = px.choropleth_mapbox(
        df_panel_map_2_1,
        geojson=sulawesi_geojson,
        locations='Provinsi',
        featureidkey='properties.Provinsi',
        color="Indeks Kualitas Air",
        color_continuous_scale=[[0.0, '#E65100'], [0.3, '#F57C00'], [0.5, '#FFB74D'], [0.7, '#81D4FA'], [1.0, '#0277BD']], # Custom Oranges to Blues
        zoom=3.8, center={"lat": -1.8, "lon": 120.5}, opacity=0.75,
        hover_name="Provinsi", hover_data={"Provinsi": False, "Jumlah_Smelter": True, "Indeks Kualitas Air": ':.1f'},
        mapbox_style="carto-darkmatter", title="IKA BPS (Data Resmi)"
    )
    fig_map1.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ECEFF1', size=11),
        coloraxis_colorbar=dict(title="Skor IKA<br><span style='font-size:10px;color:#0277BD;'>(Biru = Baik)</span>")
    )
    '''
    content = content.replace(map1_code, new_map1_code)
    print("Fixed Map 1 to be Blue.")

# 4. FIX MAP 2 (LIMBAH) TO MATCH IMAGE 1
map2_start = content.find('fig_map2 = px.choropleth_mapbox(')
map2_end = content.find('st.plotly_chart(fig_map2, use_container_width=True)', map2_start)
if map2_start != -1 and map2_end != -1:
    map2_code = content[map2_start:map2_end]
    new_map2_code = '''fig_map2 = px.choropleth_mapbox(
        df_limbah_prov,
        geojson=sulawesi_geojson,
        locations='Provinsi',
        featureidkey='properties.Provinsi',
        color="Estimasi_Clean",
        color_continuous_scale=[[0.0, '#0277BD'], [0.3, '#81D4FA'], [0.5, '#FFB74D'], [0.7, '#F57C00'], [1.0, '#E65100']],
        zoom=3.8, center={"lat": -1.8, "lon": 120.5}, opacity=0.75,
        hover_name="Provinsi", hover_data={"Provinsi": False, "Estimasi_Clean": ':.0f'},
        mapbox_style="carto-darkmatter", title="Timbulan Limbah B3 (Realita)"
    )
    fig_map2.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ECEFF1', size=11),
        coloraxis_colorbar=dict(title="Limbah (Ton)<br><span style='font-size:10px;color:#E65100;'>(Coklat = Buruk)</span>")
    )
    '''
    content = content.replace(map2_code, new_map2_code)
    print("Fixed Map 2 to be Brown.")

# 5. FIX MAP 3 (SUNGAI) TO MATCH IMAGE 1
map3_start = content.find('fig_map3 = px.choropleth_mapbox(')
map3_end = content.find('st.plotly_chart(fig_map3, use_container_width=True)', map3_start)
if map3_start != -1 and map3_end != -1:
    map3_code = content[map3_start:map3_end]
    new_map3_code = '''fig_map3 = px.choropleth_mapbox(
        df_sungai,
        geojson=sulawesi_geojson,
        locations='Provinsi',
        featureidkey='properties.Provinsi',
        color="Jumlah_Sungai_Tercemar",
        color_continuous_scale=[[0.0, '#0277BD'], [0.3, '#81D4FA'], [0.5, '#FFB74D'], [0.7, '#F57C00'], [1.0, '#E65100']],
        zoom=3.8, center={"lat": -1.8, "lon": 120.5}, opacity=0.75,
        hover_name="Provinsi", hover_data={"Provinsi": False, "Jumlah_Sungai_Tercemar": True, "Daftar_Sungai": True},
        mapbox_style="carto-darkmatter", title="Kasus Pencemaran Sungai (Laporan NGO)"
    )
    fig_map3.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ECEFF1', size=11),
        coloraxis_colorbar=dict(title="Jml Kasus<br><span style='font-size:10px;color:#E65100;'>(Coklat = Buruk)</span>")
    )
    '''
    content = content.replace(map3_code, new_map3_code)
    print("Fixed Map 3 to be Brown.")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
