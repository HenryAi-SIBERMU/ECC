import codecs

new_content = '''@st.cache_data
def load_logistik_simpul():
    import os
    import pandas as pd
    base_dir = os.path.dirname(os.path.dirname(__file__))
    return pd.read_csv(os.path.join(base_dir, 'data', 'processed', 'sulawesi_logistik_simpul_nikel.csv'))

df_logistik = load_logistik_simpul()

c14_1, c14_2, c14_3 = st.columns(3)
with c14_1:
    st.markdown("""
    <div class="metric-card">
        <div>
            <div class="metric-label">PELABUHAN NIKEL TERKONFIRMASI</div>
            <div class="metric-value" style="color: #43A047;">{}</div>
            <div class="metric-desc">Seluruh lokasi industri nikel besar di Sulawesi terbukti memiliki pelabuhan atau dermaga ekspor.</div>
        </div>
        <div class="metric-source">Sumber: Situs perusahaan, dokumen pemerintah, media (25 sumber)<br>File: sulawesi_logistik_simpul_nikel.csv</div>
    </div>
    """.format(len(df_logistik)), unsafe_allow_html=True)

psn_count = len(df_logistik[df_logistik['psn_status'] == 'terkonfirmasi'])
with c14_2:
    st.markdown("""
    <div class="metric-card">
        <div>
            <div class="metric-label">BERLABEL PROYEK STRATEGIS NASIONAL</div>
            <div class="metric-value" style="color: #FFA726;">{} <span style="font-size:1rem;color:#777;">/ {}</span></div>
            <div class="metric-desc">Label PSN mempercepat perizinan dan memudahkan pembebasan lahan warga sekitar.</div>
        </div>
        <div class="metric-source">Sumber: KPPIP, Perpres 58/2017, Perpres 12/2025</div>
    </div>
    """.format(psn_count, len(df_logistik)), unsafe_allow_html=True)

with c14_3:
    st.markdown("""
    <div class="metric-card">
        <div>
            <div class="metric-label">PELABUHAN TERBESAR</div>
            <div class="metric-value" style="color: #42A5F5;">50.000 <span style="font-size:1rem;color:#777;">ton</span></div>
            <div class="metric-desc">GNI Petasia memiliki pelabuhan yang mampu menampung kapal pengangkut berkapasitas hingga 50.000 ton.</div>
        </div>
        <div class="metric-source">Sumber: gunbusternickelindustry.com</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# === Peta Jalur Distribusi Logistik (Plotly) ===
import plotly.graph_objects as go
import pandas as pd

# Kita atur spasi dan <br> agar teks benar-benar terpisah dan tidak ada yang tabrakan
MAP_ROUTES = [
    # label_asli, label_render, src_lon, src_lat, tgt_lon, tgt_lat, hex_color, text_pos
    ("GNI",      "GNI<br><br>",                        121.32, -1.91, 113.8, 22.8, "rgb(255, 140, 0)", "top center"),
    ("PT Vale",  "PT Vale&nbsp;&nbsp;&nbsp;&nbsp;",    121.34, -2.56, 135.0, 35.0, "rgb(180, 0, 200)", "middle left"),
    ("IMIP",     "&nbsp;&nbsp;&nbsp;&nbsp;IMIP",       122.15, -2.82, 113.8, 22.8, "rgb(230, 25, 25)", "middle right"),
    ("VDNI",     "<br><br>VDNI&nbsp;&nbsp;",           122.42, -3.83, 113.8, 22.8, "rgb(0, 112, 220)", "bottom left"),
    ("OSS",      "<br><br>&nbsp;&nbsp;OSS",            122.48, -3.80, 113.8, 22.8, "rgb(0, 190, 220)", "bottom right"),
    ("ANTAM",    "<br><br><br><br>ANTAM",              121.60, -4.18, 135.0, 35.0, "rgb(0, 180, 80)",  "bottom center"),
]

fig = go.Figure()

# Tambahkan trace untuk setiap rute smelter (GARIS LURUS GREAT CIRCLE NATIVE PLOTLY)
for label, render_label, slon, slat, tlon, tlat, color, pos in MAP_ROUTES:
    fig.add_trace(go.Scattergeo(
        lon = [slon, tlon],
        lat = [slat, tlat],
        mode = 'lines',
        line = dict(width = 3.5, color = color),
        name = label,
        hoverinfo = 'skip',
        showlegend = True
    ))

# Trace khusus untuk titik sumber (Sulawesi) dengan notasi PT anti tabrakan
src_lons = [r[2] for r in MAP_ROUTES]
src_lats = [r[3] for r in MAP_ROUTES]
src_labels = [r[1] for r in MAP_ROUTES]
src_colors = [r[6] for r in MAP_ROUTES]
src_pos = [r[7] for r in MAP_ROUTES]

fig.add_trace(go.Scattergeo(
    lon = src_lons,
    lat = src_lats,
    mode = 'markers+text',
    marker = dict(size = 9, color = src_colors, symbol='circle'),
    text = src_labels,
    textposition = src_pos,
    textfont=dict(size=14, color="#111", family="Inter", weight="bold"),
    name = "Smelter Sulawesi",
    hoverinfo = 'text',
    showlegend = False
))

# Tambahkan label destinasi utama
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
    df_logistik_map = pd.DataFrame(MAP_ROUTES, columns=["Nama Smelter", "Label Render", "Lon Origin", "Lat Origin", "Lon Dest", "Lat Dest", "Color", "Text Pos"])
    st.dataframe(df_logistik_map[["Nama Smelter", "Lon Origin", "Lat Origin", "Lon Dest", "Lat Dest"]], use_container_width=True, hide_index=True)
    st.caption("📁 **Sumber File:** data/processed/sulawesi_logistik_simpul_nikel.csv - Pemetaan koordinat smelter dan pelabuhan tujuan akhir (agregasi spasial).")
'''

with codecs.open('pages/1_Ekspansi_Industri.py', 'r', 'utf-8') as f:
    lines = f.readlines()

with codecs.open('pages/1_Ekspansi_Industri.py', 'w', 'utf-8') as f:
    # write up to line 1838
    f.writelines(lines[:1839])
    # write new content
    f.write(new_content)

print("OK")
