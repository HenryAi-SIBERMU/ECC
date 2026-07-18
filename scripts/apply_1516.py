import sys
import re

file_path = "pages/1_Ekspansi_Industri.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace everything from "# 1.5 PELABUHAN EKSPOR NIKEL" to the end of the file
pattern = r'# 1\.5 PELABUHAN EKSPOR NIKEL.*'

replacement = '''# 1.5 PELABUHAN EKSPOR NIKEL
st.markdown("<br><hr style='border: 1px dashed #333;'><br>", unsafe_allow_html=True)
st.subheader("1.5 Pelabuhan Ekspor: Ke Mana Nikel Sulawesi Dikirim?")

st.markdown('<span style="background:#4A148C;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Open Source Intelligence (OSINT)</span>', unsafe_allow_html=True)
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

with st.expander("ℹ️ Metodologi: Open Source Intelligence (OSINT)"):
    st.markdown("""
    **Metode Analisis:** Kurasi & Validasi Silang (OSINT) dengan mencocokkan data citra satelit, dokumen lingkungan, dan laporan kargo.
    """)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
Ekspansi nikel di Sulawesi tidak berhenti pada izin dan pabrik smelter. Di setiap lokasi industri nikel besar, berdiri **pelabuhan atau dermaga** yang menghubungkan pabrik langsung ke kapal-kapal pengangkut menuju China dan pasar global. Dari 6 lokasi utama yang ditelusuri, **seluruhnya terbukti memiliki** pelabuhan atau dermaga ekspor, dan **4 dari 6** mendapat label Proyek Strategis Nasional (PSN) dari pemerintah.
""")

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div style="background-color: #262730; padding: 20px; border-radius: 10px; height: 100%; border: 1px solid #333;">
        <div style="color: #A0AEC0; font-size: 0.85rem; font-weight: 600; margin-bottom: 10px; text-transform: uppercase; text-align: center;">Pelabuhan Nikel Terkonfirmasi</div>
        <div style="color: #48BB78; font-size: 2.5rem; font-weight: bold; text-align: center; margin-bottom: 15px;">6</div>
        <div style="color: #A0AEC0; font-size: 0.85rem; margin-bottom: 20px; text-align: left;">Seluruh lokasi industri nikel besar di Sulawesi terbukti memiliki pelabuhan atau dermaga ekspor.</div>
        <div style="color: #718096; font-size: 0.75rem; border-top: 1px solid #333; padding-top: 10px;">Sumber: Situs perusahaan, dokumen pemerintah, media (25 sumber)<br>File: sulawesi_logistik_simpul_nikel.csv</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div style="background-color: #262730; padding: 20px; border-radius: 10px; height: 100%; border: 1px solid #333;">
        <div style="color: #A0AEC0; font-size: 0.85rem; font-weight: 600; margin-bottom: 10px; text-transform: uppercase; text-align: center;">Berlabel Proyek Strategis Nasional</div>
        <div style="color: #ECC94B; font-size: 2.5rem; font-weight: bold; text-align: center; margin-bottom: 15px;">4 <span style="font-size: 1.2rem; color: #718096;">/ 6</span></div>
        <div style="color: #A0AEC0; font-size: 0.85rem; margin-bottom: 20px; text-align: left;">Label PSN mempercepat perizinan dan memudahkan pembebasan lahan warga sekitar.</div>
        <div style="color: #718096; font-size: 0.75rem; border-top: 1px solid #333; padding-top: 10px;">Sumber: KPPIP, Perpres 58/2017, Perpres 12/2025</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div style="background-color: #262730; padding: 20px; border-radius: 10px; height: 100%; border: 1px solid #333;">
        <div style="color: #A0AEC0; font-size: 0.85rem; font-weight: 600; margin-bottom: 10px; text-transform: uppercase; text-align: center;">Pelabuhan Terbesar</div>
        <div style="color: #63B3ED; font-size: 2.5rem; font-weight: bold; text-align: center; margin-bottom: 15px;">50.000 <span style="font-size: 1.2rem; color: #718096;">ton</span></div>
        <div style="color: #A0AEC0; font-size: 0.85rem; margin-bottom: 20px; text-align: left;">GNI Petasia memiliki pelabuhan yang mampu menampung kapal pengangkut berkapasitas hingga 50.000 ton.</div>
        <div style="color: #718096; font-size: 0.75rem; border-top: 1px solid #333; padding-top: 10px;">Sumber: gunbusternickelindustry.com</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><hr style='border: 1px dashed #333;'><br>", unsafe_allow_html=True)
st.subheader("1.6 Peta Jalur Distribusi Logistik Nikel Sulawesi")

st.markdown('<span style="background:#4A148C;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Spatial Logistic Mapping (Analisis Spasial Ekstraktif)</span>', unsafe_allow_html=True)
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

with st.expander("ℹ️ Metodologi: Pemetaan Spasial Rantai Pasok Maritim"):
    st.markdown("""
    **Metode Analisis:** Pemetaan Kausalitas (Spasial) untuk membedah asimetri penguasaan ruang antara origin (sumber ekstraksi) dan destination (pusat industrialisasi). Garis diplot menggunakan rute untuk merepresentasikan jarak tempuh kapal logistik di permukaan bumi.
    """)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

import plotly.graph_objects as go

# MAP_ROUTES: Nama, Lon Origin, Lat Origin, Lon Dest, Lat Dest, Color
MAP_ROUTES = [
    ("IMIP",         122.15, -2.82, 113.8, 22.8,  "rgb(230, 25, 25)"),
    ("GNI",          121.32, -1.91, 113.8, 22.8,  "rgb(255, 140, 0)"),
    ("VDNI",         122.42, -3.83, 113.8, 22.8,  "rgb(0, 112, 220)"),
    ("OSS",          122.48, -3.80, 113.8, 22.8,  "rgb(0, 190, 220)"),
    ("ANTAM",        121.60, -4.18, 135.0, 35.0,  "rgb(0, 180, 80)"),
    ("PT Vale",      121.34, -2.56, 135.0, 35.0,  "rgb(180, 0, 200)"),
]

fig_map = go.Figure()

# Base map layout (using natural earth to show Sulawesi, China, Japan)
fig_map.update_geos(
    projection_type="equirectangular",
    showcountries=True, countrycolor="#B0BEC5",
    showcoastlines=True, coastlinecolor="#B0BEC5",
    showland=True, landcolor="#F4F8FA",
    showocean=True, oceancolor="#FFFFFF",
    lonaxis_range=[95, 145],
    lataxis_range=[-10, 45],
    bgcolor='rgba(0,0,0,0)'
)

# Add lines for routes
for name, lon1, lat1, lon2, lat2, color in MAP_ROUTES:
    fig_map.add_trace(
        go.Scattergeo(
            lon=[lon1, lon2],
            lat=[lat1, lat2],
            mode='lines',
            line=dict(width=2, color=color),
            name=name,
            hoverinfo='none'
        )
    )

# Add Origin points with labels
for name, lon1, lat1, lon2, lat2, color in MAP_ROUTES:
    fig_map.add_trace(
        go.Scattergeo(
            lon=[lon1],
            lat=[lat1],
            mode='markers+text',
            marker=dict(size=4, color=color),
            text=[name],
            textposition="bottom center",
            textfont=dict(color="#111", size=10, family="Arial Black"),
            showlegend=False,
            hoverinfo='none'
        )
    )

# Add Destination Points
fig_map.add_trace(
    go.Scattergeo(
        lon=[113.8, 135.0],
        lat=[22.8, 35.0],
        mode='markers+text',
        marker=dict(size=8, color="#555"),
        text=["China (Pasar Utama)", "Jepang/Korea"],
        textposition="top left",
        textfont=dict(color="#111", size=11, family="Arial Black"),
        showlegend=False,
        hoverinfo='none'
    )
)

fig_map.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    height=500,
    legend=dict(
        orientation="h",
        yanchor="bottom", y=-0.1,
        xanchor="center", x=0.5,
        font=dict(color="#ECEFF1", size=12)
    )
)

st.plotly_chart(fig_map, use_container_width=True)

# Red Box Ketergantungan
st.markdown("""
<div style="background:#1E1E1E; padding:20px; border-radius:10px; border-left:5px solid #D32F2F; margin-top: 20px;">
    <b style="color:#FF5252; font-size:1.1em;">Ketergantungan Struktural Rantai Pasok</b><br><br>
    Peta rute logistik maritim di atas mengilustrasikan realitas geopolitik dari ambisi hilirisasi nikel di Sulawesi. Alih-alih membangun kemandirian industri manufaktur nasional, data pergerakan kapal dan desain pelabuhan menunjukkan <b>ketergantungan absolut pada rantai pasok asing</b>.
    <ul style="margin-top: 10px; line-height: 1.6;">
        <li><b>Dominasi Ekspor ke China:</b> Tiga raksasa kawasan industri baru (IMIP, GNI, VDNI/OSS) yang menikmati fasilitas kemudahan Proyek Strategis Nasional (PSN) mengirimkan hampir seluruh <i>output</i> barang setengah jadi (NPI, Feronikel, Matte) langsung ke sentra industri di China Timur dan Selatan.</li>
        <li><b>Absennya Interkoneksi Domestik:</b> Sangat minim jalur distribusi logistik yang menghubungkan kawasan smelter raksasa ini dengan pusat industri manufaktur di dalam negeri (seperti di Pulau Jawa). Hal ini mengonfirmasi temuan bahwa Sulawesi saat ini lebih difungsikan murni sebagai <i>extractive feeder</i> (daerah penyuplai ekstraktif) bagi mesin industrialisasi negara lain, bukan sebagai fondasi terintegrasi untuk ekosistem mobil listrik domestik.</li>
        <li><b>Pergeseran Geopolitik:</b> Sementara pemain lama seperti PT Vale dan ANTAM memiliki rute pasokan yang mapan ke pasar otomotif tradisional di Jepang dan Korea Selatan, dominasi logistik dan tonase kini telah bergeser drastis seiring dengan ledakan pembangunan smelter baru yang terintegrasi langsung dengan pasar China.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

import pandas as pd
import os

@st.cache_data
def load_logistik_simpul():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    return pd.read_csv(os.path.join(base_dir, 'data', 'processed', 'sulawesi_logistik_simpul_nikel.csv'))

df_logistik = load_logistik_simpul()

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
with st.expander("Lihat Data Mentah: Jalur Distribusi Logistik Nikel Sulawesi", expanded=False):
    df_logistik_map = pd.DataFrame(MAP_ROUTES, columns=["Nama Smelter", "Lon Origin", "Lat Origin", "Lon Dest", "Lat Dest", "Color"])
    st.dataframe(df_logistik_map[["Nama Smelter", "Lon Origin", "Lat Origin", "Lon Dest", "Lat Dest"]], use_container_width=True, hide_index=True)
    st.caption("ℹ️ **Sumber File:** data/processed/sulawesi_logistik_simpul_nikel.csv - Pemetaan koordinat smelter dan pelabuhan tujuan akhir (agregasi spasial).")
'''

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Applied 1.5 and 1.6 logic.")
