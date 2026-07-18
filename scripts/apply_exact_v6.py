import sys

file_path = "pages/2_Kualitas_Lingkungan.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 2. IKU LABEL FIX (ONLY change the label, keep the blocks exactly the same)
start_iku = content.find('colorbar=dict(')
iku_loc = content.find('title=dict(text="IKU", font=dict(color=\'#ECEFF1\', size=12))')
if iku_loc != -1:
    new_iku_title = 'title=dict(text="IKU<br>merah = buruk", font=dict(color=\'#ECEFF1\', size=12), side="right")'
    content = content.replace('title=dict(text="IKU", font=dict(color=\'#ECEFF1\', size=12))', new_iku_title)
    content = content.replace("ticktext=['80<br>merah = buruk', '85', '90', '95']", "ticktext=['80', '85', '90', '95']")
    print("Fixed IKU label format.")
else:
    print("Could not find exact IKU label to replace.")

# 3. FIX MAP 1 (BPS) COLOR SCALE TO EXACTLY WHAT WAS IN IMAGE 1 (Blue gradient for IKA)
map1_start = content.find('fig_map1 = px.choropleth_mapbox(')
map1_end = content.find('st.plotly_chart(fig_map1, use_container_width=True)', map1_start)
if map1_start != -1 and map1_end != -1:
    map1_code = content[map1_start:map1_end]
    
    new_map1_code = '''fig_map1 = px.choropleth_mapbox(
        df_panel_map_2_1,
        geojson=sulawesi_geojson,
        locations='Provinsi',
        featureidkey='properties.Provinsi',
        color="Indeks Kualitas Air",
        color_continuous_scale=[[0.0, '#E65100'], [0.3, '#F57C00'], [0.5, '#FFB74D'], [0.7, '#81D4FA'], [1.0, '#0277BD']],
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
