import codecs
import re

with codecs.open('pages/2_Kualitas_Lingkungan.py', 'r', 'utf-8') as f:
    content = f.read()

# 1. We must restore fig_map2 and fig_map3
fig2_str = '''fig_map2 = px.choropleth_mapbox(
    df_panel_map_2_1, geojson=sulawesi_geojson, locations='Provinsi', featureidkey='properties.Provinsi',
    color="Limbah B3 (Juta Ton)", color_continuous_scale="Reds",
    zoom=4.2, center={"lat": -1.8, "lon": 120.5}, opacity=0.75, hover_name="Provinsi",
    hover_data={"Provinsi": False, "Limbah B3 (Juta Ton)": ':.1f'},
    mapbox_style="carto-darkmatter", title="2. Timbulan Limbah B3"
)'''

fig3_str = '''fig_map3 = px.choropleth_mapbox(
    df_panel_map_2_1, geojson=sulawesi_geojson, locations='Provinsi', featureidkey='properties.Provinsi',
    color="Kromium (mg/L)", color_continuous_scale="Reds",
    zoom=4.2, center={"lat": -1.8, "lon": 120.5}, opacity=0.75, hover_name="Provinsi",
    hover_data={"Provinsi": False, "Kromium (mg/L)": ':.3f'},
    mapbox_style="carto-darkmatter", title="3. Racun Kromium Cr6+"
)'''

if 'fig_map2 = px.choropleth_mapbox(' in content:
    # Just to be safe, find the bad block
    bad_block = '''fig_map2 = px.choropleth_mapbox(
    df_panel_map_2_1, geojson=sulawesi_geojson, locations='Provinsi', featureidkey='properties.Provinsi',
)'''
    content = content.replace(bad_block, fig2_str + '\n# Peta 3: Kromium\n' + fig3_str)

# Let's completely recreate the block between 'Kenyataan ini menelanjangi' and 'fig_map1 ='
pattern = re.compile(r'Kenyataan ini menelanjangi.*?fig_map1 = px\.choropleth_mapbox\(', re.DOTALL)
replacement = '''Kenyataan ini menelanjangi narasi manis di balik angka investasi, bahwa metrik IKA bukan lagi sekadar indikasi polusi administratif, melainkan bukti forensik terciptanya *zona tumbal ekologis* (sacrifice zones). Nelayan dan masyarakat pesisir dipaksa menelan dampak pencemaran air secara langsung, sementara keuntungan ekstraktif lari terbang ke pemodal raksasa asing maupun domestik. Sub-bab ini menguji hipotesis secara empiris: **Apakah kepadatan smelter secara konsisten menurunkan Indeks Kualitas Air (IKA)?**
""")

# Choropleth Map Plotly
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
fig_map1 = px.choropleth_mapbox('''

content = pattern.sub(replacement, content)

with codecs.open('pages/2_Kualitas_Lingkungan.py', 'w', 'utf-8') as f:
    f.write(content)
print('Fixed!')
