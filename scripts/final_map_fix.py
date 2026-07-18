import codecs

def fix_map():
    with codecs.open('pages/1_Ekspansi_Industri.py', 'r', 'utf-8') as f:
        content = f.read()

    start_marker = "# === Peta Jalur Distribusi Logistik"
    start_idx = content.find(start_marker)
    
    if start_idx == -1:
        print("Marker Peta tidak ditemukan!")
        return
        
    new_map_code = '''# === Peta Jalur Distribusi Logistik (Plotly) ===
import plotly.graph_objects as go
import math

MAP_ROUTES = [
    # label, src_lon, src_lat, tgt_lon, tgt_lat, hex_color, curve_offset
    ("IMIP",         122.15, -2.82, 113.8, 22.8,  "rgb(230, 25, 25)",  0.15),
    ("GNI",          121.32, -1.91, 113.8, 22.8,  "rgb(255, 140, 0)",  0.02),
    ("VDNI",         122.42, -3.83, 113.8, 22.8,  "rgb(0, 112, 220)",  -0.10),
    ("OSS",          122.48, -3.80, 113.8, 22.8,  "rgb(0, 190, 220)",  -0.15),
    ("ANTAM",        121.60, -4.18, 135.0, 35.0,  "rgb(0, 180, 80)",   0.12),
    ("PT Vale",      121.34, -2.56, 135.0, 35.0,  "rgb(180, 0, 200)",  -0.05),
]

fig = go.Figure()

def get_curve(slon, slat, tlon, tlat, offset):
    mid_lon = (slon + tlon) / 2
    mid_lat = (slat + tlat) / 2
    angle = math.atan2(tlat - slat, tlon - slon)
    perp_angle = angle + math.pi/2
    dist = math.sqrt((tlat - slat)**2 + (tlon - slon)**2)
    c_lon = mid_lon + math.cos(perp_angle) * dist * offset
    c_lat = mid_lat + math.sin(perp_angle) * dist * offset
    lons, lats = [], []
    for i in range(40):
        t = i / 39.0
        lon = (1-t)**2 * slon + 2*(1-t)*t * c_lon + t**2 * tlon
        lat = (1-t)**2 * slat + 2*(1-t)*t * c_lat + t**2 * tlat
        lons.append(lon)
        lats.append(lat)
    return lons, lats

# Trace Garis Melengkung (Bezier) dan Label di atas garis
for label, slon, slat, tlon, tlat, color, offset in MAP_ROUTES:
    curve_lons, curve_lats = get_curve(slon, slat, tlon, tlat, offset)
    
    # 1. Gambar Garis
    fig.add_trace(go.Scattergeo(
        lon = curve_lons,
        lat = curve_lats,
        mode = 'lines',
        line = dict(width = 3.5, color = color),
        name = label,
        hoverinfo = 'skip',
        showlegend = True
    ))
    
    # 2. Letakkan teks tepat di atas garis (15% - 25% jalan dari Sulawesi)
    t_idx = 6 # Titik ke-6 dari 40 (sekitar 15%)
    if label == "PT Vale":
        t_idx = 10
    elif label == "ANTAM":
        t_idx = 14
    elif label == "VDNI":
        t_idx = 8
    elif label == "OSS":
        t_idx = 12
        
    pos = "middle left" if offset < 0 else "middle right"
    
    fig.add_trace(go.Scattergeo(
        lon = [curve_lons[t_idx]],
        lat = [curve_lats[t_idx]],
        mode = 'text',
        text = [f"<b>{label}</b>"],
        textposition = pos,
        textfont = dict(size=14, color=color, family="Inter"),
        showlegend = False,
        hoverinfo='skip'
    ))

# Trace Titik Smelter Asli (Tanpa Teks)
src_lons = [r[1] for r in MAP_ROUTES]
src_lats = [r[2] for r in MAP_ROUTES]
src_colors = [r[5] for r in MAP_ROUTES]

fig.add_trace(go.Scattergeo(
    lon = src_lons,
    lat = src_lats,
    mode = 'markers',
    marker = dict(size = 9, color = src_colors, symbol='circle'),
    name = "Smelter Sulawesi",
    hoverinfo = 'skip',
    showlegend = False
))

# Trace Destinasi Utama
fig.add_trace(go.Scattergeo(
    lon = [113.8, 135.0],
    lat = [22.8, 35.0],
    mode = 'markers+text',
    marker = dict(size = 14, color = 'rgba(50,50,50,0.8)', symbol='circle'),
    text = ["China (Pasar Utama)", "Jepang/Korea"],
    textposition=["middle left", "top right"],
    textfont=dict(size=15, color="#111", family="Inter", weight="bold"),
    name = "Destinasi",
    hoverinfo='text',
    showlegend=False
))

fig.update_layout(
    geo = dict(
        projection_type = "natural earth",
        showland = True,
        landcolor = "#f4f4f4",
        countrycolor = "#d1d1d1",
        showocean = True,
        oceancolor = "#e8f4f8",
        showcountries=True,
        center = dict(lon=118, lat=15),
        lataxis = dict(range=[-12, 45]),
        lonaxis = dict(range=[50, 180]) 
    ),
    margin = dict(l=0, r=0, t=10, b=0),
    legend = dict(
        orientation="h", 
        yanchor="bottom", 
        y=-0.1, 
        xanchor="center", 
        x=0.5, 
        font=dict(size=14, family="Inter")
    ),
    autosize=True,
    height=600
)

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# Analisis Kritis (Sesuai Pedoman UI/UX Celios)
st.markdown("""
<div style="background-color: rgba(255,255,255,0.02); border: 1px solid #3A3F4B; border-left: 4px solid #D32F2F; padding: 15px; border-radius: 5px; margin-top: 15px; margin-bottom: 15px;">
    <h4 style="margin-top: 0; color: #D32F2F; font-size: 1.1rem; font-weight: 600;">Ketergantungan Struktural Rantai Pasok</h4>
    <p style="font-size: 0.95rem; line-height: 1.6; color: #ECEFF1; margin-bottom: 10px;">
        Peta rute logistik maritim di atas mengilustrasikan realitas geopolitik dari ambisi hilirisasi nikel di Sulawesi. Alih-alih membangun kemandirian industri manufaktur nasional, data pergerakan kapal dan desain pelabuhan menunjukkan <b>ketergantungan absolut pada rantai pasok asing</b>.
    </p>
    <ul style="font-size: 0.95rem; line-height: 1.6; color: #ECEFF1; margin-bottom: 0; padding-left: 20px;">
        <li style="margin-bottom: 8px;"><b>Dominasi Ekspor ke China:</b> Tiga raksasa kawasan industri baru (IMIP, GNI, VDNI/OSS) yang menikmati fasilitas kemudahan Proyek Strategis Nasional (PSN) mengirimkan hampir seluruh <i>output</i> barang setengah jadi (NPI, Feronikel, Matte) langsung ke sentra industri di China Timur dan Selatan.</li>
        <li style="margin-bottom: 8px;"><b>Absennya Interkoneksi Domestik:</b> Sangat minim jalur distribusi logistik yang menghubungkan kawasan smelter raksasa ini dengan pusat industri manufaktur di dalam negeri (seperti di Pulau Jawa). Hal ini mengonfirmasi temuan bahwa Sulawesi saat ini lebih difungsikan murni sebagai <i>extractive feeder</i> (daerah penyuplai ekstraktif) bagi mesin industrialisasi negara lain, bukan sebagai fondasi terintegrasi untuk ekosistem mobil listrik domestik.</li>
        <li><b>Pergeseran Geopolitik:</b> Sementara pemain lama seperti PT Vale dan ANTAM memiliki rute pasokan yang mapan ke pasar otomotif tradisional di Jepang dan Korea Selatan, dominasi logistik dan tonase kini telah bergeser drastis seiring dengan ledakan pembangunan smelter baru yang terintegrasi langsung dengan pasar China.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Transparansi Data Mentah
with st.expander("Lihat Data Mentah: Jalur Distribusi Logistik Nikel Sulawesi", expanded=False):
    df_logistik_map = pd.DataFrame(MAP_ROUTES, columns=["Nama Smelter", "Lon Origin", "Lat Origin", "Lon Dest", "Lat Dest", "Color", "Curve Offset"])
    st.dataframe(df_logistik_map[["Nama Smelter", "Lon Origin", "Lat Origin", "Lon Dest", "Lat Dest"]], use_container_width=True, hide_index=True)
    st.caption("📁 **Sumber File:** data/processed/sulawesi_logistik_simpul_nikel.csv - Pemetaan koordinat smelter dan pelabuhan tujuan akhir (agregasi spasial).")
'''
    content = content[:start_idx] + new_map_code
    
    with codecs.open('pages/1_Ekspansi_Industri.py', 'w', 'utf-8') as f:
        f.write(content)

fix_map()
print("OK")
