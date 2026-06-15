import re

with open('pages/3_Beban_Kesehatan.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Kita akan memotong konten mulai dari st.markdown(""" Peta interaktif
split_marker = 'st.markdown("""\nPeta interaktif di bawah ini memproyeksikan secara spasial'
parts = content.split('st.markdown("""\\nPeta interaktif di bawah ini memproyeksikan secara spasial')

if len(parts) == 1:
    # Coba marker lain yang mungkin berbeda line break
    parts = content.split('st.markdown("""\\nPeta interaktif di bawah')
    if len(parts) == 1:
        print("Gagal menemukan split marker.")
        import sys
        sys.exit()

new_map_code = """st.markdown(\"\"\"
Peta interaktif di bawah ini memproyeksikan secara spasial perbandingan absolut beban kesehatan (ISPA dan Diare) antara **Awal Ekstraksi (2014)** dan **Kondisi Terkini (2024)**. Sesuai *framework Before-After Analysis*, Anda bisa melihat bagaimana ledakan penyakit menyebar seiring dengan masifnya perluasan kawasan industri. 
\"\"\")

import folium
from streamlit_folium import st_folium
import json

# Data Prep Map (2014 & 2024)
df_map_2014 = df_kes[df_kes['tahun'] == 2014].groupby(['provinsi', 'indikator'])['nilai'].sum().unstack().reset_index()
df_map_2014.fillna(0, inplace=True)
df_map_2024 = df_kes[df_kes['tahun'] == 2024].groupby(['provinsi', 'indikator'])['nilai'].sum().unstack().reset_index()
df_map_2024.fillna(0, inplace=True)

# GeoJSON Prep
geojson_path = "data/raw/indonesia-province.json"
try:
    with open(geojson_path, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)
except:
    geojson_data = None

if geojson_data:
    # Sesuaikan format nama provinsi dengan GeoJSON (UPPERCASE)
    df_map_2014['prov_geojson'] = df_map_2014['provinsi'].str.upper()
    df_map_2024['prov_geojson'] = df_map_2024['provinsi'].str.upper()
    
    # Buat dictionary koordinat pusat provinsi untuk marker
    provinsi_coords = {
        'Sulawesi Selatan': [-4.1449, 119.9289],
        'Sulawesi Tengah': [-1.4300, 121.4456],
        'Sulawesi Tenggara': [-4.1449, 122.1746],
        'Sulawesi Utara': [0.6247, 123.9750],
        'Gorontalo': [0.6999, 122.4467],
        'Sulawesi Barat': [-2.8441, 119.2321]
    }
    
    # Filter fitur GeoJSON hanya untuk Sulawesi agar lebih ringan
    sulawesi_provinces = [p.upper() for p in provinsi_coords.keys()]
    filtered_features = [f for f in geojson_data['features'] if f['properties']['Propinsi'] in sulawesi_provinces]
    geojson_data['features'] = filtered_features

    # Buat 2 kolom untuk Before-After
    col_map1, col_map2 = st.columns(2)
    
    # Parameter map standard
    map_center = [-1.8, 121.0]
    map_zoom = 5
    
    def create_map(df_map, year, title):
        m = folium.Map(location=map_center, zoom_start=map_zoom, tiles='CartoDB dark_matter')
        
        # Max scale for ISPA across both years so colors are comparable
        # Max ISPA 2024 is around 180k (Sulteng)
        
        # Choropleth
        folium.Choropleth(
            geo_data=geojson_data,
            name=f'Beban ISPA {year}',
            data=df_map,
            columns=['prov_geojson', 'Kasus ISPA/Pneumonia'],
            key_on='feature.properties.Propinsi',
            fill_color='YlOrRd',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=f'ISPA {year}',
            bins=[0, 10000, 50000, 100000, 200000, 300000] # Fixed bins for comparison
        ).add_to(m)
        
        # Bubble Map untuk Diare
        for _, row in df_map.iterrows():
            prov = row['provinsi']
            ispa = row.get('Kasus ISPA/Pneumonia', 0)
            diare = row.get('Kasus Diare Dilayani', 0)
            
            if prov in provinsi_coords:
                lat, lon = provinsi_coords[prov]
                
                # Radius scale based on Diare (max scale set to handle 100k)
                radius = 5 + (diare / 50000) * 15 if diare > 0 else 0
                
                tooltip_html = f\"\"\"
                <div style='font-family: sans-serif; padding: 5px; color: black;'>
                    <b>{prov} ({year})</b><br>
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
        return m

    with col_map1:
        st.markdown(f"<h4 style='text-align: center; color: #FFF59D;'>Tahun 2014 (Kondisi Awal)</h4>", unsafe_allow_html=True)
        m_2014 = create_map(df_map_2014, 2014, "Awal")
        st_folium(m_2014, width=380, height=450, returned_objects=[], key="map_2014")

    with col_map2:
        st.markdown(f"<h4 style='text-align: center; color: #FFCDD2;'>Tahun 2024 (Kondisi Terkini)</h4>", unsafe_allow_html=True)
        m_2024 = create_map(df_map_2024, 2024, "Terkini")
        st_folium(m_2024, width=380, height=450, returned_objects=[], key="map_2024")

    st.caption("🗺️ **Before-After Geospasial:** Warna merah (*Choropleth*) menunjukkan keparahan absolut ISPA, sedangkan lingkaran biru (*Bubble*) merepresentasikan skala Diare. Skala legenda disamakan agar komparasi antar-tahun lebih adil. Sumber: Dinas Kesehatan 2014 & 2024.")

else:
    st.error("Gagal memuat file GeoJSON untuk pemetaan.")
"""

new_content = parts[0] + new_map_code

with open('pages/3_Beban_Kesehatan.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Injeksi Dual Map sukses.")
