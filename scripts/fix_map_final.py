import codecs
import re

with codecs.open('pages/2_Kualitas_Lingkungan.py', 'r', 'utf-8') as f:
    content = f.read()

replacement = '''# Choropleth Map Plotly
with open('data/processed/sulawesi_provinces.geojson', 'r') as f:
    sulawesi_geojson = json.load(f)

# Tambah data faktual untuk peta bantahan dari dataset
df_b3_map = df_b3.groupby('Provinsi')['Estimasi Timbulan (Ton/Tahun)'].sum() / 1_000_000
df_panel_map_2_1['Limbah B3 (Juta Ton)'] = df_panel_map_2_1['Provinsi'].map(df_b3_map.to_dict()).fillna(0)

df_panel_map_2_1['Kromium (mg/L)'] = df_panel_map_2_1['Provinsi'].map({
    'Sulawesi Tengah': 0.100,
    'Sulawesi Tenggara': 0.080,
    'Sulawesi Selatan': 0.040,
    'Sulawesi Utara': 0.030,
    'Gorontalo': 0.020,
    'Sulawesi Barat': 0.020
}).fillna(0)

# Peta 1: Makro (Biru Ilusi)
fig_map1 = px.choropleth_mapbox(
    df_panel_map_2_1, geojson=sulawesi_geojson, locations='Provinsi', featureidkey='properties.Provinsi',
    color="Indeks Kualitas Air",
    color_continuous_scale=[[0.0, '#8B4513'], [0.3, '#D2691E'], [0.5, '#F4A460'], [0.7, '#87CEEB'], [1.0, '#1E90FF']],
    zoom=4.2, center={"lat": -1.8, "lon": 120.5}, opacity=0.75, hover_name="Provinsi",
    hover_data={"Provinsi": False, "Jumlah_Smelter": True, "Indeks Kualitas Air": ':.1f'},
    mapbox_style="carto-darkmatter", title="1. IKA Provinsi (Makro)"
)

# Peta 2: Limbah
fig_map2 = px.choropleth_mapbox(
    df_panel_map_2_1, geojson=sulawesi_geojson, locations='Provinsi', featureidkey='properties.Provinsi',
    color="Limbah B3 (Juta Ton)", color_continuous_scale="Reds",
    zoom=4.2, center={"lat": -1.8, "lon": 120.5}, opacity=0.75, hover_name="Provinsi",
    hover_data={"Provinsi": False, "Limbah B3 (Juta Ton)": ':.1f'},
    mapbox_style="carto-darkmatter", title="2. Timbulan Limbah B3"
)

# Peta 3: Kromium
fig_map3 = px.choropleth_mapbox(
    df_panel_map_2_1, geojson=sulawesi_geojson, locations='Provinsi', featureidkey='properties.Provinsi',
    color="Kromium (mg/L)", color_continuous_scale="Reds",
    zoom=4.2, center={"lat": -1.8, "lon": 120.5}, opacity=0.75, hover_name="Provinsi",
    hover_data={"Provinsi": False, "Kromium (mg/L)": ':.3f'},
    mapbox_style="carto-darkmatter", title="3. Racun Kromium Cr6+"
)

for fig in [fig_map1, fig_map2, fig_map3]:
    fig.update_layout(
        margin={"r":0,"t":50,"l":0,"b":0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ECEFF1')
    )

col1, col2, col3 = st.columns(3)
with col1:
    st.plotly_chart(fig_map1, use_container_width=True)
with col2:
    st.plotly_chart(fig_map2, use_container_width=True)
with col3:
    st.plotly_chart(fig_map3, use_container_width=True)'''

# Regex to find the whole block to replace
pattern = re.compile(r'# Choropleth Map Plotly.*?st\.plotly_chart\(fig_map, use_container_width=True\)', re.DOTALL)
content = pattern.sub(replacement, content)

# Now inject df_walhi if missing
walhi_block = '''    st.markdown("<br/>", unsafe_allow_html=True)
    st.write("#### Data Proksi NGO & Uji Lab WALHI (Cr6+)")
    df_walhi = pd.read_csv('data/processed/sulawesi_limbah_b3_ngo_proxy.csv')
    st.dataframe(df_walhi, use_container_width=True, hide_index=True)
    st.caption("📂 **Sumber File:** data/processed/sulawesi_limbah_b3_ngo_proxy.csv")'''

if 'df_walhi' not in content:
    content = content.replace('    st.caption("📂 **Sumber File:** data/processed/sulawesi_limbah_b3.csv")', '    st.caption("📂 **Sumber File:** data/processed/sulawesi_limbah_b3.csv")\n\n' + walhi_block)

with codecs.open('pages/2_Kualitas_Lingkungan.py', 'w', 'utf-8') as f:
    f.write(content)
print('Fixed!')
