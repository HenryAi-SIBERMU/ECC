import codecs

filepath = 'pages/2_Kualitas_Lingkungan.py'
with codecs.open(filepath, 'r', 'utf-8') as f:
    content = f.read()

# 1. Remove cache for load_all_data
content = content.replace(
    "@st.cache_data\ndef load_all_data():",
    "# Cache disabled to reload CSV changes\ndef load_all_data():"
)

# 2. Update Choropleth mapping for Limbah B3
old_map = """df_panel_map_2_1['Limbah B3 (Juta Ton)'] = df_panel_map_2_1['Provinsi'].map({
    'Sulawesi Tengah': 12.0,
    'Sulawesi Tenggara': 6.5,
    'Sulawesi Selatan': 0.5,
    'Sulawesi Utara': 0.2,
    'Gorontalo': 0.1,
    'Sulawesi Barat': 0.1
}).fillna(0)"""

new_map = """# Dynamic Calculation from df_b3
df_b3['Estimasi Timbulan (Ton/Tahun)'] = pd.to_numeric(df_b3['Estimasi Timbulan (Ton/Tahun)'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
limbah_per_prov = df_b3.groupby('Provinsi')['Estimasi Timbulan (Ton/Tahun)'].sum() / 1e6
df_panel_map_2_1['Limbah B3 (Juta Ton)'] = df_panel_map_2_1['Provinsi'].map(limbah_per_prov).fillna(0)"""

content = content.replace(old_map, new_map)

with codecs.open(filepath, 'w', 'utf-8') as f:
    f.write(content)

print("Updated 2_Kualitas_Lingkungan.py successfully.")
