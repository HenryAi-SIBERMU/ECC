import re

with open('pages/3_Beban_Kesehatan.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_section_3_4 = """
# ══════════════════════════════════════════════════════════
# SUB-BAB 3.4: PETA GEOSPASIAL BEBAN KESEHATAN
# ══════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<h2 style="color: #ECEFF1; font-size: 24px;">3.4 Pemetaan Geospasial: Episentrum Ledakan Penyakit</h2>', unsafe_allow_html=True)
st.markdown('<span style="background:#00695C;color:#B2DFDB;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Choropleth & Bubble Map (GeoJSON)</span>', unsafe_allow_html=True)

st.markdown(\"\"\"
Peta interaktif di bawah ini memproyeksikan secara spasial distribusi absolut beban kesehatan (ISPA dan Diare) pada tahun 2024. Semakin gelap gradasi merah pada suatu wilayah, semakin parah tingkat kesakitan (morbiditas) yang mendera warganya akibat infeksi saluran pernapasan. 
\"\"\")

import folium
from streamlit_folium import st_folium
import json

# Data Prep Map
df_map = df_kes[df_kes['tahun'] == 2024].groupby(['provinsi', 'indikator'])['nilai'].sum().unstack().reset_index()
df_map.fillna(0, inplace=True)

# GeoJSON Prep
geojson_path = "data/raw/gadm41_IDN_1.json"
try:
    with open(geojson_path, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)
except:
    geojson_data = None

if geojson_data:
    # Buat dictionary koordinat pusat provinsi untuk marker
    provinsi_coords = {
        'Sulawesi Selatan': [-4.1449, 119.9289],
        'Sulawesi Tengah': [-1.4300, 121.4456],
        'Sulawesi Tenggara': [-4.1449, 122.1746],
        'Sulawesi Utara': [0.6247, 123.9750],
        'Gorontalo': [0.6999, 122.4467],
        'Sulawesi Barat': [-2.8441, 119.2321]
    }
    
    m = folium.Map(location=[-1.8, 121.0], zoom_start=6, tiles='CartoDB dark_matter')
    
    # Filter fitur GeoJSON hanya untuk Sulawesi agar lebih ringan
    sulawesi_provinces = provinsi_coords.keys()
    filtered_features = [f for f in geojson_data['features'] if f['properties']['NAME_1'] in sulawesi_provinces]
    geojson_data['features'] = filtered_features

    # Choropleth
    folium.Choropleth(
        geo_data=geojson_data,
        name='Beban ISPA 2024',
        data=df_map,
        columns=['provinsi', 'Kasus ISPA/Pneumonia'],
        key_on='feature.properties.NAME_1',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Total Kasus ISPA/Pneumonia (2024)'
    ).add_to(m)
    
    # Bubble Map untuk Diare
    for _, row in df_map.iterrows():
        prov = row['provinsi']
        ispa = row.get('Kasus ISPA/Pneumonia', 0)
        diare = row.get('Kasus Diare Dilayani', 0)
        
        if prov in provinsi_coords:
            lat, lon = provinsi_coords[prov]
            
            # Radius scale based on Diare
            radius = 5 + (diare / 50000) * 15 if diare > 0 else 0
            
            tooltip_html = f\"\"\"
            <div style='font-family: sans-serif; padding: 5px; color: black;'>
                <b>{prov}</b><br>
                <hr style='margin: 3px 0;'>
                ISPA/Pneumonia: <b>{ispa:,.0f}</b> kasus<br>
                Diare: <b>{diare:,.0f}</b> kasus
            </div>
            \"\"\"
            
            if radius > 0:
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=radius,
                    color='#00E5FF',
                    fill=True,
                    fill_color='#00E5FF',
                    fill_opacity=0.5,
                    tooltip=tooltip_html,
                    weight=1
                ).add_to(m)

    st_folium(m, width=800, height=500, returned_objects=[])

    st.caption("🗺️ **Peta Geospasial Interaktif:** Warna merah (*Choropleth*) menunjukkan intensitas kasus ISPA, sementara lingkaran biru (*Bubble*) menandakan volume kasus Diare. Sumber data: Dinas Kesehatan 2024.")

else:
    st.error("Gagal memuat file GeoJSON untuk pemetaan.")
"""

new_content = content + "\\n" + new_section_3_4

with open('pages/3_Beban_Kesehatan.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
    
print("Injeksi Map sukses.")
