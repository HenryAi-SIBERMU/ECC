import streamlit as st
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar

st.set_page_config(page_title="CELIOS ECC", layout="wide")
render_sidebar()

import pandas as pd

# ── Styles (Sesuai Pedoman UI/UX CELIOS) ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* { font-family: 'Inter', sans-serif; }

.main-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #43A047, #66BB6A, #81C784);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
    line-height: 1.2;
}

.sub-title {
    font-size: 1.1rem;
    color: #9E9E9E;
    font-weight: 300;
    margin-top: 0;
    margin-bottom: 2rem;
}

.org-badge {
    display: inline-block;
    background: linear-gradient(135deg, #1B5E20, #2E7D32);
    color: white;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.metric-card {
    background: linear-gradient(135deg, #1A1F2B, #232B3B);
    border: 1px solid #333;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
}
.metric-value {
    font-size: 2rem;
    font-weight: 700;
}
.metric-label {
    font-size: 0.9rem;
    color: #AAA;
    margin-bottom: 5px;
    font-weight: 600;
}
.metric-desc {
    font-size: 0.8rem;
    color: #9E9E9E;
    margin-top: 10px;
    line-height: 1.4;
    text-align: left;
}
.metric-source {
    font-size: 0.75rem;
    color: #777;
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px dotted #444;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DATA PREPARATION (PURE DATA-DRIVEN)
# ---------------------------------------------------------
def load_konflik_data_full():
    df_konflik = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'processed', 'sulawesi_konflik_agraria_tanahkita.csv'))
    
    # FILTER REGIONAL SULAWESI + MALUKU UTARA (Sentra Nikel)
    keywords = r'\b(sulawesi|sulsel|sulteng|sultra|sulut|sulbar|gorontalo|morowali|konawe|kolaka|bombana|poso|donggala|makassar|manado|minahasa|sangihe|mamuju|majene|polewali|halmahera|maluku utara|weda|obi|soroako|luwu|bantaeng|buton|muna|wakatobi|banggai|buol|toli-toli|parigi|luwuk|kendari|baubau|palu|bitung|tomohon|kotamobagu|gowa|takalar|jeneponto|bulukumba|sinjai|bone|maros|pangkep|barru|pinrang|enrekang|toraja|palopo)\b'
    mask = df_konflik['judul'].str.contains(keywords, case=False, na=False, regex=True) | \
           df_konflik['deskripsi'].str.contains(keywords, case=False, na=False, regex=True) | \
           df_konflik['narasi'].str.contains(keywords, case=False, na=False, regex=True) | \
           df_konflik['lokasi'].str.contains(keywords, case=False, na=False, regex=True)
    return df_konflik[mask].copy()

df_konflik = load_konflik_data_full()

# Kalkulasi Metrik Agregat untuk Bento Cards
total_konflik = len(df_konflik)
konflik_kebun = len(df_konflik[df_konflik['status'].str.contains('Perkebunan', case=False, na=False)])
konflik_tambang = len(df_konflik[df_konflik['status'].str.contains('Pertambangan', case=False, na=False)])

# Grouping Sektor Lain
mask_kehutanan = df_konflik['status'].str.contains('Hutan', case=False, na=False)
konflik_hutan = len(df_konflik[mask_kehutanan])

mask_infrastruktur = df_konflik['status'].str.contains('Infrastruktur|Bendungan|Transmigrasi|Energi|Fasilitas|Jalan', case=False, na=False)
konflik_infrastruktur = len(df_konflik[mask_infrastruktur])

mask_pariwisata = df_konflik['status'].str.contains('Pariwisata|Konservasi Laut', case=False, na=False)
konflik_pariwisata = len(df_konflik[mask_pariwisata])

rasio_ekstraktif = ((konflik_tambang + konflik_kebun + konflik_hutan) / total_konflik) * 100 if total_konflik > 0 else 0

# Kalkulasi Metrik Tambahan
df_konflik['dampak_masyarakat_jiwa'] = pd.to_numeric(df_konflik['dampak_masyarakat_jiwa'], errors='coerce').fillna(0)
total_jiwa = int(df_konflik['dampak_masyarakat_jiwa'].sum())
status_belum_selesai = len(df_konflik[df_konflik['status_konflik'].str.contains('Belum Ditangani', na=False)])
libat_pemerintah = df_konflik['keterlibatan_pemerintah'].notna().sum()
libat_perusahaan = df_konflik['keterlibatan_perusahaan'].notna().sum()
libat_masyarakat = df_konflik['keterlibatan_masyarakat'].notna().sum()

# ── Header Halaman ──
st.markdown('<div class="org-badge">CELIOS — Center of Economic and Law Studies</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Ruang Hidup yang Terampas</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Analisis dinamika konflik sosial dan alokasi ruang agraria dalam konteks pembangunan kawasan.</div>', unsafe_allow_html=True)

# ── Dropdown Metodologi ──
with st.expander("🔍 Metodologi", expanded=False):
    st.markdown("""
    **Alur Kausalitas (Ekonomi Politik Ekologi):** `Ekspansi Industri & Proyek Strategis` → `Perampasan Ruang Hidup & Lahan` → `Eskalasi Konflik Sosial/Agraria`
    
    Tesis dari analisis ini membantah narasi kesejahteraan dengan memperlihatkan bahwa agresivitas izin konsesi, proyek strategis nasional, hingga perluasan taman nasional dan pariwisata berbanding lurus dengan meningkatnya resistensi dan terdepaknya masyarakat lokal dari ruang kelolanya.
    
    **Variabel Dampak (Y):**
    *   **Jumlah Konflik:** Riwayat insiden konflik agraria historis berdasarkan database independen masyarakat sipil.
    *   **Sektor Pemicu:** Tipologi konflik yang dipecah berdasarkan klasifikasi sektor penyebab dominan.
    
    **Metode Pengolahan Data:**
    Analisis menggunakan pendekatan *Trend Analysis* dan tabulasi silang (*Crosstabulation*). Menyandingkan matriks kejadian konflik secara sektoral untuk memetakan konsentrasi sengketa.
    """)

# ── Hero Statement (Narasi Kritis Utama) ──
st.markdown(f"""
<div style="background-color: transparent; padding: 10px 0px; margin-bottom: 25px;">
    <h2 style="color: #FFFFFF; font-size: 1.8rem; margin-bottom: 15px; font-weight: 700;">Dinamika Hilirisasi dan Konflik Agraria</h2>
    <p style="color: #CCCCCC; font-size: 1.05rem; line-height: 1.7; margin-bottom: 15px; text-align: justify;">
        Ekspansi industri ekstraktif dan proyek strategis berimplikasi pada dinamika sosial dan penggunaan lahan masyarakat. Data empiris mencatat akumulasi <b>{total_konflik} kasus konflik agraria</b>. Konflik ini berkaitan erat dengan perubahan tata guna lahan dan alokasi ruang di berbagai daerah. 
    </p>
    <p style="color: #CCCCCC; font-size: 1.05rem; line-height: 1.7; text-align: justify;">
        Aktor dan sektor pemicu konflik mencakup sektor <b>Kehutanan</b> (Hutan Lindung, Produksi, Konservasi), <b>Infrastruktur & PSN</b> (Bendungan, Transmigrasi, Kawasan Industri), hingga proyek <b>Pariwisata & Pesisir</b>. Tiga sektor utama (Perkebunan, Kehutanan, dan Pertambangan) menyumbang porsi <b>{rasio_ekstraktif:.1f}%</b> dari keseluruhan catatan konflik.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Kartu Metrik Agregat (Bento Cards) - Baris 1 (4 Kolom) ──
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Total Kasus Konflik</div>
            <div class="metric-value" style="color: #B71C1C;">{total_konflik} <span style="font-size:16px; color:#B0BEC5;">kasus</span></div>
            <div class="metric-desc">Catatan insiden sengketa agraria dan tata guna lahan.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Korban Terdampak (Jiwa)</div>
            <div class="metric-value" style="color: #C62828;">{total_jiwa:,} <span style="font-size:16px; color:#B0BEC5;">jiwa</span></div>
            <div class="metric-desc">Estimasi jumlah warga yang terdampak oleh konflik sengketa lahan.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Status: Belum Ditangani</div>
            <div class="metric-value" style="color: #D32F2F;">{status_belum_selesai} <span style="font-size:16px; color:#B0BEC5;">kasus</span></div>
            <div class="metric-desc">Kasus sengketa yang masih dalam proses penanganan.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Komunitas Terdampak</div>
            <div class="metric-value" style="color: #E53935;">{libat_masyarakat} <span style="font-size:16px; color:#B0BEC5;">komunitas</span></div>
            <div class="metric-desc">Kelompok tani dan komunitas lokal yang terlibat dalam sengketa.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# ── Kartu Metrik Agregat (Bento Cards) - Baris 2 (3 Kolom Sektor Utama) ──
col5, col6, col7 = st.columns(3)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Sektor Perkebunan</div>
            <div class="metric-value" style="color: #D32F2F;">{konflik_kebun} <span style="font-size:16px; color:#B0BEC5;">kasus</span></div>
            <div class="metric-desc">Sengketa tumpang tindih Hak Guna Usaha (HGU) perkebunan dengan lahan masyarakat.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Sektor Kehutanan</div>
            <div class="metric-value" style="color: #F4511E;">{konflik_hutan} <span style="font-size:16px; color:#B0BEC5;">kasus</span></div>
            <div class="metric-desc">Sengketa batas kawasan hutan produksi dan konservasi dengan wilayah kelola lokal.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col7:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Sektor Pertambangan</div>
            <div class="metric-value" style="color: #FF6F00;">{konflik_tambang} <span style="font-size:16px; color:#B0BEC5;">kasus</span></div>
            <div class="metric-desc">Sengketa alokasi lahan untuk operasi pertambangan dan fasilitas hilirisasi.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# ── Kartu Metrik Agregat (Bento Cards) - Baris 3 (4 Kolom Sektor Lain & Aktor) ──
col8, col9, col10, col11 = st.columns(4)

with col8:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Infrastruktur & PSN</div>
            <div class="metric-value" style="color: #FF8A65;">{konflik_infrastruktur} <span style="font-size:16px; color:#B0BEC5;">kasus</span></div>
            <div class="metric-desc">Sengketa pengadaan tanah untuk Proyek Strategis Nasional.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col9:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Pariwisata & Pesisir</div>
            <div class="metric-value" style="color: #FFAB91;">{konflik_pariwisata} <span style="font-size:16px; color:#B0BEC5;">kasus</span></div>
            <div class="metric-desc">Sengketa pemanfaatan wilayah pesisir dan kawasan pariwisata.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col10:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Keterlibatan Pemerintah</div>
            <div class="metric-value" style="color: #E53935;">{libat_pemerintah} <span style="font-size:16px; color:#B0BEC5;">kasus</span></div>
            <div class="metric-desc">Keterlibatan instansi pemerintah dalam fasilitasi atau sengketa lahan.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col11:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Keterlibatan Korporasi</div>
            <div class="metric-value" style="color: #EF5350;">{libat_perusahaan} <span style="font-size:16px; color:#B0BEC5;">kasus</span></div>
            <div class="metric-desc">Entitas BUMN atau swasta yang terlibat dalam sengketa lahan.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='metric-source' style='text-align:right; margin-top:15px;'><b>Sumber Analisis Data:</b> Konsorsium Pembaruan Agraria (KPA) / Tanah Kita</div>", unsafe_allow_html=True)
st.markdown("---")


# ---------------------------------------------------------
# PLACEHOLDER UNTUK SECTION LAINNYA
# ---------------------------------------------------------
import plotly.express as px

st.subheader("4.1 Tren Eskalasi Konflik Agraria Seiring Ekspansi Industri")
st.markdown('<span style="background:#4A148C;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Analisis Tren Time-Series (Sumber: KPA / Tanah Kita)</span>', unsafe_allow_html=True)
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

with st.expander("ℹ️ Metodologi: Analisis Tren Time-Series"):
    st.markdown("""
    **Metode Analisis:** Sub-bab ini menggunakan visualisasi tren runtun waktu (*Time-Series Trend Analysis*) untuk melacak eskalasi kasus perampasan lahan secara historis.

    1. **Model Analisis Tren Historis:**
        * **Time-Series Tracking:** Memetakan fluktuasi dan eskalasi frekuensi letupan konflik agraria dalam rentang waktu memanjang (longitudinal).
        * **Komparasi Periodik:** Membandingkan volume letupan konflik antara fase pra-ekspansi (sebelum hilirisasi masif) dengan fase pasca-ekspansi (era Proyek Strategis Nasional).
        * **Pemetaan Eskalasi:** Mengidentifikasi pola lonjakan kasus perampasan lahan untuk membuktikan secara empiris relasi antara percepatan industrialisasi dengan peningkatan konflik sosial.
    2. **Kalkulasi/Formula Pengolahan:** Agregasi jumlah konflik berdasarkan periode tahun pencatatan dan sektor industri.
        * `Total_Konflik_Tahunan = COUNT(Kasus) GROUP BY Tahun, Sektor`
        * `Lonjakan_Eskalasi = (Kasus_Pasca - Kasus_Pra) / Kasus_Pra * 100%`
    3. **Variabel & Fitur Data:**
        * **Waktu (Independen):** Tahun pencatatan konflik (1990 - 2025).
        * **Frekuensi & Sektor (Dependen):** Jumlah insiden perampasan ruang dan sektor korporasi yang memicu konflik.
    4. **Dataset & File:**
        * Catatan Konflik Agraria: `data/processed/sulawesi_konflik_agraria_tanahkita.csv`
    """)

# Pemrosesan Data untuk Time-Series
def map_sektor(status):
    status = str(status).lower()
    if 'kebun' in status: return 'Perkebunan'
    if 'tambang' in status: return 'Pertambangan'
    if 'hutan' in status: return 'Kehutanan'
    if any(x in status for x in ['infrastruktur', 'bendungan', 'transmigrasi', 'energi', 'fasilitas', 'jalan', 'industri']): return 'Infrastruktur & PSN'
    if any(x in status for x in ['pariwisata', 'laut', 'pesisir']): return 'Pariwisata & Pesisir'
    return 'Lainnya'

df_ts = df_konflik.copy()
df_ts['Sektor_Grup'] = df_ts['status'].apply(map_sektor)

# Filter tahun mulai dari 1990 agar grafik lebih fokus pada era modern/ekspansi
df_ts_modern = df_ts[df_ts['tahun'] >= 1990]

# Pemrosesan Data untuk Narasi Analisis Data-Driven
total_ts = len(df_ts)
pasca_2005 = len(df_ts[df_ts['tahun'] >= 2005])
pra_2005 = len(df_ts[df_ts['tahun'] < 2005])
lonjakan = (pasca_2005 / pra_2005 * 100) if pra_2005 > 0 else 0

st.markdown(f"""
Visualisasi *time-series* di bawah ini memberikan gambaran korelasi antara ekspansi industri dan dinamika konflik agraria di daratan Sulawesi. Secara historis, perbandingan dua periode waktu menunjukkan perbedaan tingkat insidensi konflik. Pada periode pra-2005, sistem pendataan mencatat **{pra_2005} kasus** konflik agraria.

Pada periode pasca-2005 hingga saat ini, data mencatat **{pasca_2005} kasus** konflik lahan, yang mencerminkan peningkatan sebesar **{lonjakan:,.1f}%** dibandingkan periode sebelumnya. Perubahan tren ini beriringan dengan penerbitan Izin Usaha Pertambangan (IUP) serta ekspansi Hak Guna Usaha (HGU) untuk perkebunan.

Penelusuran tren satu dekade terakhir menunjukkan bahwa sengketa agraria mencakup berbagai sektor, termasuk pertambangan nikel, infrastruktur, dan Proyek Strategis Nasional. Akumulasi **{total_ts} insiden historis** ini mengindikasikan perlunya tata kelola alokasi lahan dan perlindungan hak masyarakat lokal yang lebih seimbang di kawasan investasi.
""")
def map_sektor(status):
    status = str(status).lower()
    if 'kebun' in status: return 'Perkebunan'
    if 'tambang' in status: return 'Pertambangan'
    if 'hutan' in status: return 'Kehutanan'
    if any(x in status for x in ['infrastruktur', 'bendungan', 'transmigrasi', 'energi', 'fasilitas', 'jalan', 'industri']): return 'Infrastruktur & PSN'
    if any(x in status for x in ['pariwisata', 'laut', 'pesisir']): return 'Pariwisata & Pesisir'
    return 'Lainnya'

df_ts = df_konflik.copy()
df_ts['Sektor_Grup'] = df_ts['status'].apply(map_sektor)

# Filter tahun mulai dari 1990 agar grafik lebih fokus pada era modern/ekspansi
df_ts_modern = df_ts[df_ts['tahun'] >= 1990]

# Agregasi data
df_agg = df_ts_modern.groupby(['tahun', 'Sektor_Grup']).size().reset_index(name='Jumlah')

# Definisi Warna Sektor (Sesuai Pedoman Celios)
color_map = {
    'Perkebunan': '#FFC107',
    'Kehutanan': '#8BC34A',
    'Pertambangan': '#FF9800',
    'Infrastruktur & PSN': '#03A9F4',
    'Pariwisata & Pesisir': '#E91E63',
    'Lainnya': '#9E9E9E'
}

# Membuat Grafik Stacked Bar
fig_ts = px.bar(
    df_agg, 
    x='tahun', 
    y='Jumlah', 
    color='Sektor_Grup',
    color_discrete_map=color_map,
    title='Tren Konflik Agraria di Sulawesi (1990 - 2025)',
    labels={'tahun': 'Tahun', 'Jumlah': 'Total Letupan Konflik', 'Sektor_Grup': 'Sektor Pemicu'},
    template='plotly_dark'
)

fig_ts.update_layout(
    xaxis=dict(tickmode='linear', dtick=2),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    hovermode='x unified',
    legend=dict(
        title="",
        orientation="h",
        yanchor="bottom",
        y=1.05,
        xanchor="center",
        x=0.5
    ),
    margin=dict(t=80)
)

# Dinamis Hitung Puncak untuk Anotasi
df_total_per_tahun = df_ts_modern.groupby('tahun').size().reset_index(name='Jumlah')
if not df_total_per_tahun.empty:
    max_year_row = df_total_per_tahun.loc[df_total_per_tahun['Jumlah'].idxmax()]
    peak_year = int(max_year_row['tahun'])
    peak_value = int(max_year_row['Jumlah'])

    # Anotasi Puncak Konflik
    fig_ts.add_annotation(
        x=peak_year,
        y=peak_value,
        text=f"Puncak Insidensi:<br><b>{peak_value} Kasus ({peak_year})</b>",
        showarrow=True,
        arrowhead=2,
        arrowsize=1.5,
        arrowwidth=2,
        arrowcolor="#D32F2F",
        ax=-40,
        ay=-50,
        font=dict(size=12, color="#FFCDD2"),
        bgcolor="rgba(211, 47, 47, 0.8)",
        bordercolor="#B71C1C",
        borderwidth=1,
        borderpad=4
    )
    
    # Anotasi Mula Eskalasi Pasca-2005 (Misal 2006)
    if 2006 in df_total_per_tahun['tahun'].values:
        val_2006 = int(df_total_per_tahun[df_total_per_tahun['tahun'] == 2006]['Jumlah'].values[0])
        fig_ts.add_annotation(
            x=2006,
            y=val_2006,
            text=f"Eskalasi Ekstraktif Dimulai<br><b>{val_2006} Kasus (2006)</b>",
            showarrow=True,
            arrowhead=2,
            arrowsize=1.5,
            arrowwidth=2,
            arrowcolor="#F57C00",
            ax=-50,
            ay=-40,
            font=dict(size=11, color="#FFE0B2"),
            bgcolor="rgba(245, 124, 0, 0.8)",
            bordercolor="#E65100",
            borderwidth=1,
            borderpad=4
        )

st.plotly_chart(fig_ts, use_container_width=True, config={'displayModeBar': False})

st.markdown("""
<div style="background-color: rgba(3, 169, 244, 0.05); border-left: 4px solid #03A9F4; padding: 15px; border-radius: 4px; margin-bottom: 20px;">
    <h4 style="color: #03A9F4; margin-top: 0; font-size: 1.05rem;">Interpretasi Ekologis: Puncak Insidensi Konflik 2017</h4>
    <p style="color: #ECEFF1; font-size: 0.95rem; line-height: 1.6; margin-bottom: 0;">
        Grafik memperlihatkan peningkatan insidensi konflik yang memuncak pada <b>tahun 2017</b> dengan <b>75 kasus konflik</b>. Pembedahan data sektoral menunjukkan konsentrasi pada sektor <b>Kehutanan (40 kasus)</b> dan <b>Perkebunan (21 kasus)</b>, diikuti oleh <b>Pertambangan dan Infrastruktur PSN</b>. Periode ini bertepatan dengan percepatan pelepasan kawasan hutan dan Izin Pinjam Pakai Kawasan Hutan (IPPKH) untuk mendukung proyek strategis dan kawasan industri.
    </p>
</div>
""", unsafe_allow_html=True)

with st.expander("Lihat Data Mentah: Historis Konflik Agraria", expanded=False):
    st.dataframe(df_ts_modern, use_container_width=True, hide_index=True)
    st.caption("📁 <b>Sumber File:</b> <code>data/processed/sulawesi_konflik_agraria_tanahkita.csv</code> - Basis data agregasi konflik agraria dari KPA/Tanah Kita.", unsafe_allow_html=True)

st.markdown("""
<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #FF9800; margin-bottom: 25px;">
    <b style="color: #FF9800;">Interpretasi Ekologis dan Sosial:</b> Peningkatan insidensi konflik beririsan dengan dinamika perizinan kawasan. Pengelolaan alokasi ruang dan perlindungan hak masyarakat di wilayah investasi menjadi faktor penting untuk meminimalkan dampak sosial.
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# SUB-BAB 4.2: SEBARAN SEKTORAL DAMPAK
# ══════════════════════════════════════════════════════════
st.subheader("4.2 Sebaran Sektoral: Dampak Masyarakat dan Penggunaan Lahan")
st.markdown('<span style="background:#4A148C;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Analisis Komparatif Dampak Sosial-Ekologis (Sumber: KPA / Tanah Kita)</span>', unsafe_allow_html=True)
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

with st.expander("ℹ️ Metodologi: Analisis Komparatif Dampak Sosial-Ekologis"):
    st.markdown("""
    **Metode Analisis:** Sub-bab ini menggunakan agregasi komparatif (*Comparative Aggregation Analysis*) untuk membedah skala kehancuran sosial (korban terdampak) dan monopoli ruang (hektar) antar sektor.

    1. **Model Analisis Beban Sektoral (Sectoral Burden Analysis):**
        * **Kategorisasi Sektoral (Profiling):** Mengklasifikasikan sumber konflik (sektor Tambang, Perkebunan, Kehutanan, dll.) sebagai basis pengelompokan (*grouping*).
        * **Kuantifikasi Monopoli:** Menghitung total agregat luasan daratan (hektar) yang dirampas dan jumlah masyarakat (jiwa) yang terdampak per sektor industri.
        * **Evaluasi Dominasi:** Membedah asimetri penguasaan ruang untuk mengidentifikasi sektor mana yang bertindak sebagai aktor dominan dalam praktik perampasan tanah (*land grabbing*).
    2. **Kalkulasi/Formula Pengolahan:** Perhitungan sum/agregat dari seluruh korban jiwa (bukan korban meninggal, melainkan terdampak) dan hektar.
        * `Total_Jiwa_Terdampak = SUM(Jiwa) GROUP BY Sektor`
        * `Total_Monopoli_Area = SUM(Hektar) GROUP BY Sektor`
    3. **Variabel & Fitur Data:**
        * **Sektor (Independen):** Kategori proyek (Perkebunan, Kehutanan, Pertambangan, dll).
        * **Korban Jiwa & Luas Area (Dependen):** Jumlah orang terdampak (Jiwa) dan luas sengketa (Ha).
    4. **Dataset & File:**
        * Dampak Konflik: `data/processed/sulawesi_konflik_agraria_tanahkita.csv`
    """)

# Pemrosesan Data untuk Dampak Sektoral
df_dampak = df_ts.copy()
df_dampak['dampak_masyarakat_jiwa'] = pd.to_numeric(df_dampak['dampak_masyarakat_jiwa'], errors='coerce').fillna(0)
df_dampak['luas_ha'] = pd.to_numeric(df_dampak['luas_ha'], errors='coerce').fillna(0)

df_sektor_agg = df_dampak.groupby('Sektor_Grup').agg({
    'dampak_masyarakat_jiwa': 'sum', 
    'luas_ha': 'sum'
}).reset_index()
df_sektor_agg = df_sektor_agg[df_sektor_agg['Sektor_Grup'] != 'Lainnya'] # Hilangkan Lainnya agar fokus

# Variabel dinamis untuk f-strings
jiwa_kehutanan = df_sektor_agg[df_sektor_agg['Sektor_Grup'] == 'Kehutanan']['dampak_masyarakat_jiwa'].sum()
jiwa_tambang = df_sektor_agg[df_sektor_agg['Sektor_Grup'] == 'Pertambangan']['dampak_masyarakat_jiwa'].sum()
ha_kebun = df_sektor_agg[df_sektor_agg['Sektor_Grup'] == 'Perkebunan']['luas_ha'].sum()
ha_kehutanan = df_sektor_agg[df_sektor_agg['Sektor_Grup'] == 'Kehutanan']['luas_ha'].sum()
ha_tambang = df_sektor_agg[df_sektor_agg['Sektor_Grup'] == 'Pertambangan']['luas_ha'].sum()

st.markdown(f"""
Visualisasi komparatif di bawah ini menggambarkan skala dampak sosial dan penggunaan lahan berdasarkan sektor industri. Data menunjukkan bahwa **Sektor Kehutanan** mencatatkan jumlah warga terdampak sebanyak **{jiwa_kehutanan:,.0f} jiwa**, berkaitan dengan tumpang tindih kawasan hutan produksi, konservasi, dan Hutan Tanaman Industri (HTI) dengan wilayah kelola masyarakat lokal.

Menyusul berikutnya adalah **Sektor Pertambangan** dengan total korban terdampak sebanyak **{jiwa_tambang:,.0f} jiwa**, yang beririsan dengan proyek hilirisasi nikel dan tambang terbuka di kawasan pesisir dan pertanian.

Dari dimensi penggunaan lahan (luasan hektar yang terlibat sengketa), **Sektor Perkebunan** mencatatkan luas sengketa terbesar yaitu **{ha_kebun:,.0f} Hektar**, disusul oleh sektor Kehutanan seluas **{ha_kehutanan:,.0f} Ha** dan Pertambangan seluas **{ha_tambang:,.0f} Ha**. Data ini menunjukkan bahwa dinamika penguasaan lahan di tiga sektor tersebut berkorelasi dengan tingginya insidensi sengketa agraria di tingkat lokal.
""")

col_jiwa, col_ha = st.columns(2)

# Menggunakan data dari 1990 agar sumbu X selaras dengan grafik di 4.1
df_sektor_tahun = df_dampak[df_dampak['tahun'] >= 1990].groupby(['tahun', 'Sektor_Grup']).agg({
    'dampak_masyarakat_jiwa': 'sum', 
    'luas_ha': 'sum'
}).reset_index()

with col_jiwa:
    fig_jiwa = px.bar(
        df_sektor_tahun,
        x='tahun',
        y='dampak_masyarakat_jiwa',
        color='Sektor_Grup',
        title='Distribusi Korban Terdampak (Jiwa) per Tahun',
        color_discrete_map=color_map,
        labels={'dampak_masyarakat_jiwa': 'Total Korban (Jiwa)', 'tahun': 'Tahun', 'Sektor_Grup': 'Sektor Pemicu'},
        barmode='stack'
    )
    fig_jiwa.update_layout(
        showlegend=False, 
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickmode='linear', dtick=2),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        margin=dict(t=60, b=40)
    )
    
    top_jiwa = df_sektor_tahun.groupby('tahun')['dampak_masyarakat_jiwa'].sum().sort_values(ascending=False)
    top_jiwa = top_jiwa[top_jiwa > 0].head(2)
    for i, (year, val) in enumerate(top_jiwa.items(), 1):
        fig_jiwa.add_annotation(
            x=year, y=val,
            text=f"<a href='#anomali-jiwa-{year}' target='_self' style='color:white;text-decoration:none;'><b>Anomali Jiwa {i}</b></a>",
            hovertext=f"<b>{year} (Lonjakan Korban)</b><br>Klik untuk melihat detail di bawah",
            showarrow=True, arrowhead=2, arrowcolor="#FF5252", ax=0, ay=-35,
            font=dict(size=11, color="white"), bgcolor="rgba(211,47,47,0.8)", bordercolor="#FF5252"
        )

    st.plotly_chart(fig_jiwa, use_container_width=True, config={'displayModeBar': False})

with col_ha:
    fig_ha = px.bar(
        df_sektor_tahun,
        x='tahun',
        y='luas_ha',
        color='Sektor_Grup',
        title='Distribusi Area Konflik (Hektar) per Tahun',
        color_discrete_map=color_map,
        labels={'luas_ha': 'Luas Daratan (Hektar)', 'tahun': 'Tahun', 'Sektor_Grup': 'Sektor Pemicu'},
        barmode='stack'
    )
    fig_ha.update_layout(
        showlegend=False, 
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickmode='linear', dtick=2),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        margin=dict(t=60, b=40)
    )

    top_ha = df_sektor_tahun.groupby('tahun')['luas_ha'].sum().sort_values(ascending=False)
    top_ha = top_ha[top_ha > 0].head(2)
    for i, (year, val) in enumerate(top_ha.items(), 1):
        fig_ha.add_annotation(
            x=year, y=val,
            text=f"<a href='#anomali-ha-{year}' target='_self' style='color:#111;text-decoration:none;'><b>Anomali Area {i}</b></a>",
            hovertext=f"<b>{year} (Lonjakan Area)</b><br>Klik untuk melihat detail di bawah",
            showarrow=True, arrowhead=2, arrowcolor="#FFC107", ax=0, ay=-35,
            font=dict(size=11, color="#111"), bgcolor="rgba(255,193,7,0.9)", bordercolor="#FFB300"
        )

    st.plotly_chart(fig_ha, use_container_width=True, config={'displayModeBar': False})

st.markdown("""
<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #F44336; margin-bottom: 25px;">
    <b style="color: #F44336;">Interpretasi Ekologis dan Sosial:</b> Dinamika Grafik mencerminkan akumulasi dampak sosial di wilayah industri yang memerlukan perhatian dalam pengelolaan sengketa lahan.
</div>
""", unsafe_allow_html=True)

with st.expander("🔍 Bedah Forensik Anomali (Spike) Konflik Agraria", expanded=True):
    st.markdown("""
Berdasarkan ekstraksi dataset secara mendalam, berikut adalah bedah anatomis dari lonjakan-lonjakan ekstrem (*spikes*) yang terjadi pada grafik **Ledakan Korban Terdampak (Jiwa)** dan **Monopoli Area Konflik (Hektar)** di wilayah ini.
    """)
    
    # Process and display Jiwa Anomalies
    for i, year in enumerate(top_jiwa.index, 1):
        st.markdown(f"---")
        st.markdown(f"<a id='anomali-jiwa-{year}'></a>", unsafe_allow_html=True)
        st.markdown(f"#### ANOMALI JIWA {i}: Lonjakan Korban Jiwa Tahun {year}")
        
        # Get top case
        cases = df_konflik[df_konflik['tahun'] == year].copy()
        cases['jiwa_num'] = pd.to_numeric(cases['dampak_masyarakat_jiwa'].astype(str).str.replace(',', '').str.replace(' Jiwa', ''), errors='coerce').fillna(0)
        top_case = cases.sort_values('jiwa_num', ascending=False).iloc[0] if not cases.empty else None
        
        if top_case is not None:
            judul = top_case['judul']
            korban = top_case['jiwa_num']
            pt = top_case['keterlibatan_perusahaan'] if pd.notna(top_case['keterlibatan_perusahaan']) else 'Tidak/Belum Teridentifikasi'
            narasi = str(top_case['narasi'])[:450] + "..." if pd.notna(top_case['narasi']) and str(top_case['narasi']).strip() != 'nan' else (str(top_case['deskripsi'])[:450] + "...")
            
            sumber_lsm = top_case['sumber'] if 'sumber' in top_case and pd.notna(top_case['sumber']) else 'Kompilasi LSM'
            tk_link = top_case['detail_url'] if 'detail_url' in top_case and pd.notna(top_case['detail_url']) else '#'
            import urllib.parse
            search_query = urllib.parse.quote(f"{judul} {pt}")
            link = f"https://www.google.com/search?q={search_query}"
            
            st.markdown(f"**Kasus Utama Pendongkrak Statistik: {judul}**")
            st.markdown(f"* **Total Korban (Kasus Ini):** {int(korban):,} Jiwa")
            st.markdown(f"* **Perusahaan Terlibat:** {pt}")
            st.markdown(f"* **Narasi Singkat:** {narasi}")
            st.markdown(f"* **Sumber Referensi:** Laporan {sumber_lsm} ([Telusuri Berita Kasus]({link}) | [Link Asli TanahKita]({tk_link}))")

    # Process and display HA Anomalies
    for i, year in enumerate(top_ha.index, 1):
        st.markdown(f"---")
        st.markdown(f"<a id='anomali-ha-{year}'></a>", unsafe_allow_html=True)
        st.markdown(f"#### ANOMALI AREA {i}: Monopoli Area Konflik Tahun {year}")
        
        # Get top case
        cases = df_konflik[df_konflik['tahun'] == year].copy()
        cases['ha_num'] = pd.to_numeric(cases['luas_ha'].astype(str).str.replace(',', '').str.replace(' Ha', ''), errors='coerce').fillna(0)
        top_case = cases.sort_values('ha_num', ascending=False).iloc[0] if not cases.empty else None
        
        if top_case is not None:
            judul = top_case['judul']
            luas = top_case['ha_num']
            pt = top_case['keterlibatan_perusahaan'] if pd.notna(top_case['keterlibatan_perusahaan']) else 'Tidak/Belum Teridentifikasi'
            narasi = str(top_case['narasi'])[:450] + "..." if pd.notna(top_case['narasi']) and str(top_case['narasi']).strip() != 'nan' else (str(top_case['deskripsi'])[:450] + "...")
            
            sumber_lsm = top_case['sumber'] if 'sumber' in top_case and pd.notna(top_case['sumber']) else 'Kompilasi LSM'
            tk_link = top_case['detail_url'] if 'detail_url' in top_case and pd.notna(top_case['detail_url']) else '#'
            import urllib.parse
            search_query = urllib.parse.quote(f"{judul} {pt}")
            link = f"https://www.google.com/search?q={search_query}"

            st.markdown(f"**Kasus Utama Pendongkrak Statistik: {judul}**")
            st.markdown(f"* **Total Daratan Dirampas (Kasus Ini):** {int(luas):,} Hektar")
            st.markdown(f"* **Perusahaan Terlibat:** {pt}")
            st.markdown(f"* **Narasi Singkat:** {narasi}")
            st.markdown(f"* **Sumber Referensi:** Laporan {sumber_lsm} ([Telusuri Berita Kasus]({link}) | [Link Asli TanahKita]({tk_link}))")

st.subheader("4.3 Indikasi Represi dan Kriminalisasi dalam Konflik Agraria")
st.markdown('<span style="background:#4A148C;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Analisis Agregat Kasus Represi & Pelanggaran HAM (Sumber: Database Tanah Kita)</span>', unsafe_allow_html=True)
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

with st.expander("ℹ️ Metodologi: Analisis Agregat Kasus Represi & Pelanggaran HAM"):
    st.markdown("""
    **Metode Analisis:** Sub-bab ini menggunakan agregasi kasus indikasi pelanggaran Hak Asasi Manusia dan Kriminalisasi Pejuang Lingkungan melalui ekstraksi metrik fatalitas.

    1. **Pemodelan Indikator Kekerasan & Represi:**
        * **Violence & Criminalization Tracking:** Mendokumentasikan kasus penangkapan, intimidasi, kekerasan fisik, hingga jatuhnya korban jiwa di pihak warga dan aktivis lingkungan.
        * **Kuantifikasi Fatalitas:** Menghitung akumulasi jumlah korban kriminalisasi dan korban tewas sebagai proksi tingkat represi struktural.
        * **Pemetaan Ruang Sipil:** Mengevaluasi sejauh mana ekspansi investasi industri ekstraktif beroperasi dengan menggunakan instrumen represi aparatur keamanan (penyempitan ruang sipil).
    2. **Kalkulasi/Formula Pengolahan:** Penghitungan jumlah insiden kriminalisasi serta total akumulasi korban represi kekerasan fisik.
        * `Total_Kasus_Kriminalisasi = COUNT(Kasus) WHERE Indikasi_Kriminalisasi = TRUE`
        * `Total_Korban_Tewas = SUM(Jumlah_Tewas) GROUP BY Sektor`
    3. **Variabel & Fitur Data:**
        * **Status Represi (Dependen):** Boolean (Ya/Tidak) terjadinya indikasi kriminalisasi dalam konflik.
        * **Kuantitas Korban (Dependen):** Angka mutlak (integer) korban tertangkap, terluka, dan meninggal.
    4. **Dataset & File:**
        * Represi dan Kriminalisasi: `data/processed/sulawesi_konflik_agraria_tanahkita.csv`
    """)

# Pastikan kolom kriminalisasi berupa numerik yang aman
df_dampak['jumlah_ditangkap'] = pd.to_numeric(df_dampak['jumlah_ditangkap'], errors='coerce').fillna(0)
df_dampak['jumlah_luka'] = pd.to_numeric(df_dampak['jumlah_luka'], errors='coerce').fillna(0)
df_dampak['jumlah_tewas'] = pd.to_numeric(df_dampak['jumlah_tewas'], errors='coerce').fillna(0)

# Kalkulasi metrik agregat
total_kriminalisasi = df_dampak[df_dampak['indikasi_kriminalisasi'] == True].shape[0]
total_ditangkap = int(df_dampak['jumlah_ditangkap'].sum())
total_luka = int(df_dampak['jumlah_luka'].sum())
total_tewas = int(df_dampak['jumlah_tewas'].sum())

# Kalkulasi untuk narasi
df_krim_tahun = df_dampak[(df_dampak['indikasi_kriminalisasi'] == True) & (df_dampak['tahun'] >= 2000)].groupby('tahun').size().reset_index(name='jumlah_kasus')
df_krim_sektor = df_dampak[(df_dampak['indikasi_kriminalisasi'] == True) & (df_dampak['Sektor_Grup'] != 'Lainnya')].groupby('Sektor_Grup').size().reset_index(name='jumlah_kasus').sort_values('jumlah_kasus', ascending=True)

top_sektor = df_krim_sektor.iloc[-1]['Sektor_Grup'] if not df_krim_sektor.empty else "Industri"
top_sektor_count = df_krim_sektor.iloc[-1]['jumlah_kasus'] if not df_krim_sektor.empty else 0
top_tahun = int(df_krim_tahun.loc[df_krim_tahun['jumlah_kasus'].idxmax()]['tahun']) if not df_krim_tahun.empty else 0
top_tahun_count = int(df_krim_tahun['jumlah_kasus'].max()) if not df_krim_tahun.empty else 0

st.markdown(f"""
Data kuantitatif di wilayah Sulawesi mencatat indikasi terjadinya represi dan tindakan kriminalisasi dalam sebagian sengketa agraria. Dari database yang didokumentasikan, terdapat **{total_kriminalisasi} kasus indikasi kriminalisasi** dan **{total_ditangkap} warga/aktivis lingkungan yang tercatat pernah ditangkap** dalam penanganan sengketa lahan.

Berdasarkan distribusi sektoral, **Sektor {top_sektor}** mencatatkan frekuensi indikasi represi tertinggi dengan **{top_sektor_count} kasus**. Tahun dengan jumlah catatan insiden represi tertinggi adalah **{top_tahun}** dengan **{top_tahun_count} kasus**.

Catatan ini menunjukkan pentingnya pendekatan hukum yang adil, penyelesaian konflik secara ramah HAM, serta jaminan perlindungan bagi pejuang lingkungan dan komunitas lokal sesuai dengan peraturan perundang-undangan.
""")

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric(label="Kasus Indikasi Kriminalisasi", value=f"{total_kriminalisasi} Kasus")
with col_m2:
    st.metric(label="Warga/Aktivis Ditangkap", value=f"{total_ditangkap} Orang")
with col_m3:
    st.metric(label="Korban Luka-luka", value=f"{total_luka} Orang")
with col_m4:
    st.metric(label="Korban Tewas", value=f"{total_tewas} Orang")

st.markdown("---")

col_trend, col_sektor = st.columns(2)

# Chart 1: Tren Kriminalisasi per Tahun (hanya menampilkan sejak 2000 untuk kejelasan tren modern)
df_krim_tahun = df_dampak[(df_dampak['indikasi_kriminalisasi'] == True) & (df_dampak['tahun'] >= 2000)].groupby('tahun').size().reset_index(name='jumlah_kasus')

with col_trend:
    fig_krim_tahun = px.line(
        df_krim_tahun, 
        x='tahun', 
        y='jumlah_kasus',
        markers=True,
        title='Tren Kasus Kriminalisasi & Represi (Pasca 2000)',
        labels={'jumlah_kasus': 'Total Kasus', 'tahun': 'Tahun Kejadian'}
    )
    fig_krim_tahun.update_traces(line_color='#E53935', marker=dict(size=8, color='#B71C1C'))
    fig_krim_tahun.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, tickmode='linear', dtick=2), 
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        margin=dict(t=50, b=40)
    )
    st.plotly_chart(fig_krim_tahun, use_container_width=True, config={'displayModeBar': False})
    with st.expander("Lihat Data Mentah: Tren Kriminalisasi", expanded=False):
        st.dataframe(df_krim_tahun, use_container_width=True, hide_index=True)
        st.caption("📁 **Sumber File:** `data/processed/sulawesi_konflik_agraria_tanahkita.csv` - Tren jumlah kasus kriminalisasi per tahun.")

with col_sektor:
    fig_krim_sektor = px.bar(
        df_krim_sektor,
        y='Sektor_Grup',
        x='jumlah_kasus',
        orientation='h',
        color='Sektor_Grup',
        color_discrete_map=color_map,
        title='Sektor Industri Paling Represif',
        labels={'jumlah_kasus': 'Total Kasus', 'Sektor_Grup': 'Sektor Pemicu'}
    )
    fig_krim_sektor.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'), 
        yaxis=dict(showgrid=False),
        margin=dict(t=50, b=40)
    )
    st.plotly_chart(fig_krim_sektor, use_container_width=True, config={'displayModeBar': False})
    with st.expander("Lihat Data Mentah: Sektor Represif", expanded=False):
        st.dataframe(df_krim_sektor, use_container_width=True, hide_index=True)
        st.caption("📁 **Sumber File:** `data/processed/sulawesi_konflik_agraria_tanahkita.csv` - Total kasus kriminalisasi dikelompokkan per sektor.")

st.markdown(f"""
<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #E53935; margin-bottom: 25px; margin-top: 25px;">
    <b>Interpretasi Ekologis & Hak Asasi Manusia:</b> Keberadaan kasus kriminalisasi di sekitar area konsesi (terutama {top_sektor}) mengindikasikan pentingnya jaminan perlindungan ruang sipil dan penghormatan HAM dalam setiap proses pembangunan.
</div>
""", unsafe_allow_html=True)

st.markdown("#### Arsip Kasus Represi dan Kekerasan Fisik Tertinggi")
st.caption("Menampilkan 10 kasus dengan jumlah korban penangkapan atau tewas terbanyak berdasarkan data yang berhasil didokumentasikan.")

df_kekerasan = df_dampak[(df_dampak['jumlah_ditangkap'] > 0) | (df_dampak['jumlah_tewas'] > 0)].sort_values(['jumlah_ditangkap', 'jumlah_tewas'], ascending=[False, False])
df_kekerasan_display = df_kekerasan[['tahun', 'Sektor_Grup', 'keterlibatan_perusahaan', 'jumlah_ditangkap', 'jumlah_tewas', 'deskripsi']].copy()
df_kekerasan_display['keterlibatan_perusahaan'] = df_kekerasan_display['keterlibatan_perusahaan'].fillna('Tidak/Belum Teridentifikasi')
df_kekerasan_display.columns = ['Tahun', 'Sektor', 'Perusahaan Terlibat', 'Ditangkap (Jiwa)', 'Tewas (Jiwa)', 'Narasi Singkat Kejadian']

st.dataframe(df_kekerasan_display.head(10), use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════
# SUB-BAB 4.4: KONFLIK SOSIAL DAN RESISTENSI MASYARAKAT
# ══════════════════════════════════════════════════════════
st.markdown("---")
st.subheader("4.4 Pembuktian Statistik: Ekspansi vs Eskalasi Konflik")
st.markdown('<span style="background:#4A148C;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Before-After Analysis & Crosstabulation</span>', unsafe_allow_html=True)
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

with st.expander("ℹ️ Metodologi: Before-After Analysis & Crosstabulation"):
    st.markdown("""
    **Metode Analisis:** Sub-bab ini menggunakan Uji Chi-Square (*Crosstabulation*) dan kalkulasi risiko peluang (*Odds Ratio*) untuk menguji validitas empiris secara akademis.

    1. **Uji Korelasi Variabel Kategorikal:**
        * **Crosstabulation:** Mentabulasi silang frekuensi kemunculan dua kondisi (Contoh: Keterlibatan Perusahaan vs Adanya Kriminalisasi) untuk mencari relasi ketergantungan.
        * `H0 (Null Hypothesis): Variabel baris (Periode/Aktor) saling bebas (independent) secara absolut terhadap variabel kolom (Represi/Kematian).`
        * `Decision Rule: Chi-Square Asymptotic Significance (P-Value) < 0.05, maka tolak H0 (Terdapat korelasi yang signifikan).`
    2. **Kalkulasi/Formula Pengolahan:** Algoritma Uji Tabulasi Silang Chi-Square.
        * `Chi-Square (χ²) = Σ [(Observed - Expected)² / Expected]`
        * `Odds Ratio (OR) = (Sel A × Sel D) / (Sel B × Sel C)`
    3. **Variabel & Fitur Data:**
        * **Matriks Ekspansi (Independen):** Dikotomi rentang waktu (Pra/Pasca 2014) dan kehadiran korporasi.
        * **Matriks Eskalasi (Dependen):** Kehadiran status represi dan terjadinya jatuhnya korban nyawa (Boolean dikonversi ke kategori).
    4. **Dataset & File:**
        * Base Data Cross-Section: `data/processed/sulawesi_konflik_agraria_tanahkita.csv`
    """)

st.markdown("""
Hipotesis utama dalam evaluasi ini adalah bahwa **industrialisasi dan ekspansi korporasi** berbanding lurus dengan **eskalasi konflik dan represi** terhadap masyarakat. 
Untuk mengujinya secara statistik sesuai pedoman D3TLH, analisis dibagi menjadi dua bagian: (1) Komparasi metrik Before-After, dan (2) Uji signifikansi Crosstab Chi-Square. Unit observasinya adalah catatan kejadian letupan konflik historis.
""")

st.markdown("#### A. Analisis Komparatif Before-After (Pra vs Era Hilirisasi)")
st.markdown("Perbandingan absolut eskalasi konflik agraria sebelum dan sesudah rezim hilirisasi masif dimulai (cut-off tahun 2014).")

# Kalkulasi
df_ba = df_dampak[df_dampak['tahun'] >= 1990].copy()
df_pra = df_ba[df_ba['tahun'] < 2014]
df_pasca = df_ba[df_ba['tahun'] >= 2014]

tahun_pra = max(1, 2014 - int(df_pra['tahun'].min())) if not df_pra.empty else 24
tahun_pasca = max(1, int(df_pasca['tahun'].max()) - 2013) if not df_pasca.empty else 11

avg_pra = len(df_pra) / tahun_pra
avg_pasca = len(df_pasca) / tahun_pasca

col_ba1, col_ba2 = st.columns(2)

with col_ba1:
    st.markdown(f"""
    <div style="background:#1E1E1E; padding:20px; border-radius:10px; border-top:4px solid #9E9E9E;">
        <h4 style="margin-top:0; color:#9E9E9E;">Pra-Ekspansi (1990 - 2013)</h4>
        <h1 style="color:#FFF; font-size: 2.5rem; margin: 10px 0;">{avg_pra:.1f} <span style="font-size: 1rem; color:#AAA;">Kasus/Tahun</span></h1>
        <hr style="border-color: #333; margin: 15px 0;">
        <p style="margin: 5px 0;">Total Letupan Konflik: <b>{len(df_pra)}</b> kejadian</p>
        <p style="margin: 5px 0;">Total Warga Ditangkap: <b>{int(df_pra['jumlah_ditangkap'].sum())}</b> jiwa</p>
        <p style="margin: 5px 0; color:#FF8A80;">Total Korban Tewas: <b>{int(df_pra['jumlah_tewas'].sum())}</b> jiwa</p>
    </div>
    """, unsafe_allow_html=True)

with col_ba2:
    st.markdown(f"""
    <div style="background:#1E1E1E; padding:20px; border-radius:10px; border-top:4px solid #E53935;">
        <h4 style="margin-top:0; color:#E53935;">Pasca-Ekspansi (2014 - 2024)</h4>
        <h1 style="color:#FFF; font-size: 2.5rem; margin: 10px 0;">{avg_pasca:.1f} <span style="font-size: 1rem; color:#AAA;">Kasus/Tahun</span></h1>
        <hr style="border-color: #333; margin: 15px 0;">
        <p style="margin: 5px 0;">Total Letupan Konflik: <b>{len(df_pasca)}</b> kejadian</p>
        <p style="margin: 5px 0;">Total Warga Ditangkap: <b>{int(df_pasca['jumlah_ditangkap'].sum())}</b> jiwa</p>
        <p style="margin: 5px 0; color:#FF5252;">Total Korban Tewas: <b>{int(df_pasca['jumlah_tewas'].sum())}</b> jiwa</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("#### B. Uji Statistik Crosstab (Chi-Square)")

import scipy.stats as stats

# Data Preparation (Menggunakan Skala Nasional agar sampel N memadai untuk Uji Chi-Square)
df_crosstab = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'processed', 'sulawesi_konflik_agraria_tanahkita.csv'))
df_crosstab['tahun'] = pd.to_numeric(df_crosstab['tahun'], errors='coerce')
df_crosstab = df_crosstab[df_crosstab['tahun'] >= 1990]

# Define columns for X
df_crosstab['Periode_Ekspansi'] = df_crosstab['tahun'].apply(lambda x: 'Pasca-ekspansi (≥ 2014)' if x >= 2014 else 'Pra-ekspansi (< 2014)')
df_crosstab['Sektor_Tambang'] = df_crosstab['status'].str.contains('Tambang|Pertambangan', case=False, na=False).apply(lambda x: 'Sektor Pertambangan' if x else 'Sektor Non-Tambang')
df_crosstab['Keterlibatan_Pemerintah'] = df_crosstab['keterlibatan_pemerintah'].notna().apply(lambda x: 'Terlibat Aparat/Negara' if x else 'Tanpa Keterlibatan Negara')

# Define columns for Y
df_crosstab['Indikasi_Kriminalisasi'] = df_crosstab['indikasi_kriminalisasi'].fillna(False).astype(bool).apply(lambda x: 'Ada Represi/Kriminalisasi' if x else 'Baseline (Tanpa Kriminalisasi)')
df_crosstab['Status_Penyelesaian'] = df_crosstab['status_konflik'].str.contains('Belum Ditangani', na=False).apply(lambda x: 'Konflik Dibiarkan Terlantar' if x else 'Konflik Selesai/Diproses')

has_luka = pd.to_numeric(df_crosstab['jumlah_luka'], errors='coerce').fillna(0) > 0
has_tewas = pd.to_numeric(df_crosstab['jumlah_tewas'], errors='coerce').fillna(0) > 0
has_tangkap = pd.to_numeric(df_crosstab['jumlah_ditangkap'], errors='coerce').fillna(0) > 0
df_crosstab['Dampak_Kekerasan'] = (has_luka | has_tewas | has_tangkap).apply(lambda x: 'Terjadi Kekerasan/Penangkapan' if x else 'Tanpa Insiden Fisik')

x_order = {
    "Periode_Ekspansi": ['Pra-ekspansi (< 2014)', 'Pasca-ekspansi (≥ 2014)'],
    "Sektor_Tambang": ['Sektor Non-Tambang', 'Sektor Pertambangan'],
    "Keterlibatan_Pemerintah": ['Tanpa Keterlibatan Negara', 'Terlibat Aparat/Negara']
}
y_order = {
    "Indikasi_Kriminalisasi": ['Baseline (Tanpa Kriminalisasi)', 'Ada Represi/Kriminalisasi'],
    "Dampak_Kekerasan": ['Tanpa Insiden Fisik', 'Terjadi Kekerasan/Penangkapan'],
    "Status_Penyelesaian": ['Konflik Selesai/Diproses', 'Konflik Dibiarkan Terlantar']
}

col_sel1, col_sel2 = st.columns(2)

with col_sel1:
    st.markdown("##### Variabel Independen (X) - Kondisi Ekspansi")
    x_options = {
        "Periode_Ekspansi": "Periode Ekspansi Industri",
        "Sektor_Tambang": "Tipe Sektor (Tambang vs Non-Tambang)",
        "Keterlibatan_Pemerintah": "Keterlibatan Aparat/Pemerintah"
    }
    x_col = st.selectbox("Pilih Indikator Ekspansi (X):", list(x_options.keys()), format_func=lambda x: x_options[x])

with col_sel2:
    st.markdown("##### Variabel Dependen (Y) - Eskalasi Konflik")
    y_options = {
        "Indikasi_Kriminalisasi": "Tingkat Represi & Kriminalisasi",
        "Status_Penyelesaian": "Tingkat Penelantaran Kasus",
        "Dampak_Kekerasan": "Tingkat Insiden Fisik (Luka/Tewas/Ditangkap)"
    }
    y_col = st.selectbox("Pilih Indikator Eskalasi (Y):", list(y_options.keys()), format_func=lambda x: y_options[x])

df_crosstab["X_Label"] = df_crosstab[x_col]
df_crosstab["Y_Label"] = df_crosstab[y_col]

cats_x = x_order[x_col]
cats_y = y_order[y_col]

crosstab = pd.crosstab(df_crosstab["X_Label"], df_crosstab["Y_Label"]).reindex(index=cats_x, columns=cats_y, fill_value=0)

try:
    chi2, p, dof, expected = stats.chi2_contingency(crosstab)
    expected_df = pd.DataFrame(expected, index=crosstab.index, columns=crosstab.columns)
except Exception:
    chi2, p, dof, expected_df = 0, 1, 0, pd.DataFrame(0, index=cats_x, columns=cats_y)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
st.markdown("### Detail Uji Statistik (Chi-Square & Odds Ratio)")
st.caption("Tabel-tabel di bawah ini menyajikan bukti statistik formal: Case Processing → Crosstabulation → Chi-Square Tests → Ringkasan Hipotesis.")

# --- A. Case Processing Summary ---
st.markdown("##### Case Processing Summary")
total_cases = len(df_crosstab)
valid_cases = len(df_crosstab.dropna(subset=['X_Label', 'Y_Label']))
missing_cases = total_cases - valid_cases

columns_case = pd.MultiIndex.from_product([["Cases"], ["Valid", "Missing", "Total"], ["N", "Percent"]])
interaction_label = f"{x_options[x_col]} * {y_options[y_col]}"
row_data = [
    valid_cases, f"{valid_cases/total_cases*100:.1f}%" if total_cases > 0 else "0%",
    missing_cases, f"{missing_cases/total_cases*100:.1f}%" if total_cases > 0 else "0%",
    total_cases, "100.0%"
]
case_summary = pd.DataFrame([row_data], index=[interaction_label], columns=columns_case)
st.table(case_summary)

# --- B. Crosstabulation ---
st.markdown(f"##### {interaction_label} Crosstabulation")
row_indices = []
for x_cat in cats_x:
    row_indices.extend([(x_cat, "Count"), (x_cat, "Expected Count")])
row_indices.extend([("Total", "Count"), ("Total", "Expected Count")])

rows = []
for x_cat in cats_x:
    counts = crosstab.loc[x_cat].tolist()
    exps = expected_df.loc[x_cat].tolist()
    rows.append(counts + [sum(counts)])
    rows.append([f"{v:.1f}" for v in exps] + [f"{sum(exps):.1f}"])

total_counts = crosstab.sum().tolist()
total_exps = expected_df.sum().tolist()
rows.append(total_counts + [sum(total_counts)])
rows.append([f"{v:.1f}" for v in total_exps] + [f"{sum(total_exps):.1f}"])

multi_index = pd.MultiIndex.from_tuples(row_indices, names=[x_options[x_col], ""])
spss_crosstab = pd.DataFrame(rows, index=multi_index, columns=cats_y + ["Total"])
st.table(spss_crosstab)

# --- C. Chi-Square Tests ---
st.markdown("##### Chi-Square Tests")
try:
    g, p_g, dof_g, exp_g = stats.chi2_contingency(crosstab, lambda_="log-likelihood")
except:
    g, p_g = 0, 1
x_codes = df_crosstab["X_Label"].replace({cats_x[0]: 0, cats_x[1]: 1})
y_codes = df_crosstab["Y_Label"].replace({cats_y[0]: 0, cats_y[1]: 1})
try:
    r, p_corr = stats.pearsonr(list(x_codes), list(y_codes))
    lbl_val = (valid_cases - 1) * (r**2)
except:
    r, p_corr, lbl_val = 0, 1, 0

chi_data = [
    [f"{chi2:.3f}", str(dof), f"{p:.3f}"],
    [f"{g:.3f}", str(dof), f"{p_g:.3f}"],
    [f"{lbl_val:.3f}", "1", f"{p_corr:.3f}"],
    [str(valid_cases), "", ""]
]
chi_df = pd.DataFrame(chi_data, index=["Pearson Chi-Square", "Likelihood Ratio", "Linear-by-Linear Association", "N of Valid Cases"], columns=["Value", "df", "Asymp. Sig. (2-sided)"])
st.markdown(f"**{interaction_label}**")
st.table(chi_df)

# --- D. Hypothesis & Risk Summary ---
st.markdown("### Ringkasan Uji Hipotesis")
is_significant = p < 0.05
status_text = "SIGNIFIKAN (Ada Hubungan)" if is_significant else "TIDAK SIGNIFIKAN"
order_color = "#4CAF50" if is_significant else "#F44336" 
bg_color = "rgba(76, 175, 80, 0.1)" if is_significant else "rgba(244, 67, 54, 0.1)"

try:
    a = crosstab.loc[cats_x[0], cats_y[0]]
    b = crosstab.loc[cats_x[0], cats_y[1]]
    c = crosstab.loc[cats_x[1], cats_y[0]]
    d = crosstab.loc[cats_x[1], cats_y[1]]
    odds_ratio = (a * d) / (b * c) if (b * c) > 0 else 0
except:
    odds_ratio = 0

col_res1, col_res2 = st.columns([1, 1.5])
with col_res1:
    st.markdown(f"""
    <div style="border: 2px solid {order_color}; padding: 15px; border-radius: 5px; background-color: {bg_color}; margin-bottom: 10px;">
        <h4 style="color: {order_color}; margin: 0 0 10px 0; text-transform: uppercase;">Result: {status_text}</h4>
        <p style="margin: 0; font-family: monospace;">
            P-Value    : {p:.4f}<br>
            Chi-Square : {chi2:.3f}<br>
            df         : {dof}
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"**Odds Ratio (Risk Estimate):** `{odds_ratio:.3f}`")

with col_res2:
    if is_significant:
        interp_text = f"Hasil pengujian statistik menunjukkan: <b>{x_options[x_col]}</b> terbukti **berkorelasi signifikan** dengan <b>{y_options[y_col]}</b> (P < 0.05, OR: {odds_ratio:.3f}). Temuan ini mengindikasikan bahwa dinamika ekspansi wilayah industri berasosiasi dengan peningkatan risiko konflik lahan."
    else:
        interp_text = f"Secara agregat, hubungan antara <b>{x_options[x_col]}</b> dan <b>{y_options[y_col]}</b> **tidak menunjukkan perbedaan yang signifikan** secara statistik (P ≥ 0.05). Hal ini mengindikasikan bahwa dinamika konflik terjadi di berbagai periode dan sektor secara merata."
    
    st.markdown(f"""
    <div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid {order_color}; height: 100%;">
        <b>Interpretasi Analisis Sosial:</b><br><br>
        {interp_text}
    </div>
    """, unsafe_allow_html=True)

# --- E. Executive Summary of All Combinations ---
st.markdown("---")
st.markdown("### Ringkasan Eksekutif Seluruh Skenario Crosstab")
st.markdown("Tabel di bawah ini merangkum hasil pengujian statistik (Chi-Square) untuk semua kemungkinan kombinasi antara indikator Ekspansi (X) dan Eskalasi Konflik (Y) pada panel data yang sama.")

summary_data = []
for k_x, v_x in x_options.items():
    for k_y, v_y in y_options.items():
        cx = x_order[k_x]
        cy = y_order[k_y]
        
        s_x = df_crosstab[k_x]
        s_y = df_crosstab[k_y]
        
        ct = pd.crosstab(s_x, s_y).reindex(index=cx, columns=cy, fill_value=0)
        try:
            c2_val, pv_val, dof_val, exp_val = stats.chi2_contingency(ct)
        except:
            c2_val, pv_val, dof_val = 0, 1, 0
            
        try:
            aa = ct.loc[cx[0], cy[0]]
            bb = ct.loc[cx[0], cy[1]]
            cc = ct.loc[cx[1], cy[0]]
            dd = ct.loc[cx[1], cy[1]]
            or_v = (aa * dd) / (bb * cc) if (bb * cc) > 0 else 0
        except:
            or_v = 0
            
        sig_status = "🟢 SIGNIFIKAN" if pv_val < 0.05 else "🔴 TIDAK SIGNIFIKAN"
        
        summary_data.append({
            "Variabel Independen (X)": v_x,
            "Variabel Dependen (Y)": v_y,
            "Chi-Square": f"{c2_val:.3f}",
            "P-Value": f"{pv_val:.3f}",
            "Odds Ratio": f"{or_v:.2f}",
            "Kesimpulan": sig_status
        })

df_summary = pd.DataFrame(summary_data)
st.dataframe(df_summary, use_container_width=True, hide_index=True)

# Generate Dynamic Narrative for Executive Summary
sig_count = sum(1 for row in summary_data if "🟢 SIGNIFIKAN" in row["Kesimpulan"])
total_scenarios = len(summary_data)

import textwrap

if sig_count > 0:
    exec_narrative = textwrap.dedent(f"""Dari <b>{total_scenarios} skenario pengujian</b>, terdapat <b>{sig_count} skenario yang terbukti SIGNIFIKAN</b>.<br><br>
Tingginya Odds Ratio pada skenario yang signifikan menegaskan bahwa ekspansi operasi industri berasosiasi dengan peningkatan risiko sengketa lahan.<br><br>
Skenario yang <i>TIDAK SIGNIFIKAN</i> mengindikasikan bahwa dinamika sengketa lahan tersebar secara merata di berbagai sektor dan kurun waktu.    """)
    bg_color = "rgba(229, 57, 53, 0.15)"
    border_color = "#E53935"
else:
    exec_narrative = textwrap.dedent(f"""Dari <b>{total_scenarios} skenario pengujian</b>, seluruhnya menunjukkan status <b>TIDAK SIGNIFIKAN</b>.<br><br>
Hal ini menunjukkan bahwa sengketa lahan dan tantangan penyelesaiannya terdistribusi secara konsisten di sepanjang waktu dan sektor.    """)
    bg_color = "rgba(255, 152, 0, 0.15)"
    border_color = "#FF9800"

st.markdown(f"""
<div style="background-color: {bg_color}; padding:18px; border-radius:8px; border-left:6px solid {border_color}; margin-top: 15px; margin-bottom: 25px;">
    <b style="color: {border_color}; font-size: 1.05rem;">Pembedahan Realitas Kemanusiaan:</b><br><br>
    <div style="color: #E0E0E0; font-size: 0.95rem; line-height: 1.6;">
{exec_narrative}
    </div>
</div>
""", unsafe_allow_html=True)

with st.expander("Lihat Data Panel Mentah", expanded=False):
    st.dataframe(df_crosstab[['tahun', 'sektor', 'X_Label', 'Y_Label']], use_container_width=True, hide_index=True)
    st.caption("Sumber: `sulawesi_konflik_agraria_tanahkita.csv` (Diolah secara tabulasi silang)")

# ══════════════════════════════════════════════════════════
# SUB-BAB 4.5: PETA ORKESTRASI KONFLIK: AKTOR SIPIL VS EKSTRAKTIF
# ══════════════════════════════════════════════════════════
st.markdown("---")
st.subheader("4.5 Peta Entitas Aktor: Korporasi dan Organisasi Masyarakat")
st.markdown('<span style="background:#4A148C;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Frequency Profiling (Text Parsing NLP) pada Data TanahKita</span>', unsafe_allow_html=True)
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

with st.expander("ℹ️ Metodologi: Frequency Profiling (Text Parsing NLP)"):
    st.markdown("""
    **Metode Analisis:** Sub-bab ini menggunakan teknik pemrosesan teks berbasis *Natural Language Processing* (Regex Entity Extraction) untuk membedah relasi aktor (korporasi vs sipil).

    1. **Model Ekstraksi Aktor (Entity Parsing & Text Mining):**
        * **Textual Pattern Matching:** Memindai ribuan korpus teks narasi historis menggunakan metode *Regular Expressions* (RegEx) untuk mendeteksi entitas korporasi (PT/CV) dan organisasi masyarakat sipil (CSO).
        * **Token Counting (Frequency Profiling):** Menghitung frekuensi absolut penyebutan (*mentions*) dari setiap aktor spesifik di dalam dokumentasi konflik.
        * **Pemetaan Oligarki:** Memvalidasi indikasi konsentrasi kekuasaan dan monopoli penguasaan ruang oleh segelintir konglomerasi besar melalui seberapa sering nama entitas tersebut muncul dalam sengketa tanah.
    2. **Kalkulasi/Formula Pengolahan:** Regex pattern matching and Token Counting.
        * `Count_PT = SUM(RegEx_Match(r"\\b(?:PT|CV)\\.?\\s*[A-Z][a-zA-Z]*..."))`
        * `Count_CSO = SUM(RegEx_Match(r"\\b(?:Walhi|Jatam|AMAN|Aliansi)..."))`
    3. **Variabel & Fitur Data:**
        * **Teks Korpus Historis (Independen):** Penggabungan kolom `judul`, `deskripsi`, dan `narasi` dari repositori kasus.
        * **Frekuensi Penyebutan (Dependen):** *Word counts* eksistensi entitas pada teks-teks sengketa.
    4. **Dataset & File:**
        * Teks Bebas (*Free-Text*): `data/processed/sulawesi_konflik_agraria_tanahkita.csv`
    """)

st.markdown("""
Analisis entitas aktor berbasis pemrosesan teks (*string parsing*) terhadap catatan kronologi dokumentasi TanahKita memetakan keterlibatan berbagai pihak dalam sengketa agraria. 
Hasil ekstraksi teks mengidentifikasi entitas korporasi, lembaga pemerintah, serta organisasi masyarakat sipil yang tercatat dalam dokumentasi kasus. 
Grafik frekuensi di bawah menampilkan entitas korporasi dan kelompok masyarakat yang paling sering teridentifikasi dalam catatan sengketa lahan.
""")

import re

# NLP Extraction (Regex) for Actors from Text
# Menggunakan seluruh dataset TanahKita (Nasional, 500+ kasus) untuk memetakan Modus Operandi secara utuh
df_nlp = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'processed', 'sulawesi_konflik_agraria_tanahkita.csv'))
text_corpus = " ".join((df_nlp['judul'].fillna('') + " " + df_nlp['deskripsi'].fillna('') + " " + df_nlp['narasi'].fillna('')).tolist())

# Extract Corporate Actors
pts = re.findall(r'\b(?:PT|CV)\.?\s*[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*){0,3}\b', text_corpus)
pts = [" ".join(pt.split()) for pt in pts]
# Gabungkan PTPN XIV, PTPN II, dll ke "PT Perkebunan Nusantara (PTPN)"
pts = [re.sub(r'\bPTPN(?:\s+(?:XIV|XII|VII|II|14|Unit\s*14))?\b', 'PT Perkebunan Nusantara (PTPN)', pt, flags=re.IGNORECASE) for pt in pts]
df_aktor_perusahaan = pd.Series(pts).value_counts().reset_index()
df_aktor_perusahaan.columns = ['Aktor', 'Frekuensi']

# Extract Civil Society / Vigilante Actors (Data-Driven with Stopwords Cutoff)
civils_raw = re.findall(r'\b(?:Preman|Ormas|Satgas|PAM Swakarsa|Pemuda Pancasila|GRIB|Laskar|Tandingan|Oknum|Security|Satpam|Pengamanan Swakarsa|Centeng|Beking)\b[^\.,;\!\?\(\)\[\]"\'\-]*', text_corpus, flags=re.IGNORECASE)

stopwords = {'yang', 'dan', 'di', 'dari', 'dengan', 'untuk', 'pada', 'ke', 'dalam', 'oleh', 'serta', 'sebagai', 'adalah', 'ini', 'itu', 'tersebut', 'kepada', 'saat', 'ketika', 'juga', 'mengatasnamakan', 'berjumlah', 'melarang', 'datang', 'berupaya', 'segera', 'salah', 'lainnya', 'tak', 'nya', 'sedang', 'akan', 'karena', 'sebab', 'lalu', 'kemudian', 'mereka'}

civils_clean = []
for phrase in civils_raw:
    words = phrase.split()
    clean_words = []
    for w in words:
        if w.lower() in stopwords:
            break
        clean_words.append(w.title())
    if clean_words:
        civils_clean.append(' '.join(clean_words))

df_aktor_masyarakat = pd.Series(civils_clean).value_counts().reset_index()
df_aktor_masyarakat.columns = ['Aktor', 'Frekuensi']

col_aktor_1, col_aktor_2 = st.columns(2)

with col_aktor_1:
    st.markdown("#### Top 10 Entitas Korporasi Paling Dominan")
    top_corp = df_aktor_perusahaan.head(10).sort_values(by='Frekuensi', ascending=True)
    if not top_corp.empty:
        fig_corp = px.bar(
            top_corp, 
            x='Frekuensi', y='Aktor', orientation='h',
            color_discrete_sequence=['#F57C00']
        )
        fig_corp.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ECEFF1'), margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', tickformat='d')
        )
        st.plotly_chart(fig_corp, use_container_width=True, config={'displayModeBar': False})
    top1_corp_name = df_aktor_perusahaan.iloc[0]['Aktor'] if not df_aktor_perusahaan.empty else "Korporasi"
    top1_corp_freq = df_aktor_perusahaan.iloc[0]['Frekuensi'] if not df_aktor_perusahaan.empty else 0

    st.markdown(f"""
    <div style="background:rgba(245, 124, 0, 0.1);padding:15px;border-left:3px solid #F57C00;border-radius:5px;font-size:0.9rem;">
        <b>Analisis Data:</b> Ekstraksi teks mencatat frekuensi penyebutan entitas <b>{top1_corp_name}</b> dalam <b>{top1_corp_freq} catatan kasus terpisah</b>.
    </div>
    """, unsafe_allow_html=True)

with col_aktor_2:
    st.markdown("#### Top Aktor Proksi & Vigilante Terdeteksi")
    top_civil = df_aktor_masyarakat.head(10).sort_values(by='Frekuensi', ascending=True)
    if not top_civil.empty:
        fig_civil = px.bar(
            top_civil, 
            x='Frekuensi', y='Aktor', orientation='h',
            color_discrete_sequence=['#D32F2F'] # Merah untuk bahaya/vigilante
        )
        fig_civil.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ECEFF1'), margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', tickformat='d')
        )
        st.plotly_chart(fig_civil, use_container_width=True, config={'displayModeBar': False})
        
    top1_civ_name = df_aktor_masyarakat.iloc[0]['Aktor'] if not df_aktor_masyarakat.empty else "Preman/Ormas"
    top1_civ_freq = df_aktor_masyarakat.iloc[0]['Frekuensi'] if not df_aktor_masyarakat.empty else 0

    st.markdown(f"""
    <div style="background:rgba(211, 47, 47, 0.1);padding:15px;border-left:3px solid #D32F2F;border-radius:5px;font-size:0.9rem;">
        <b>Analisis Kritis:</b> Kemunculan kelompok sipil seperti <b>{top1_civ_name}</b> (terdeteksi hingga <b>{top1_civ_freq} kali</b>) menangkap besarnya skala orkestrasi horizontal. Korporasi seringkali menggunakan jasa pengamanan swakarsa, kelompok preman, hingga ormas vigilante sebagai "bemper proksi" untuk mengintimidasi warga lokal dan memecah belah solidaritas akar rumput.
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9E9E9E; font-size: 0.9rem; margin-bottom: 5px;'><i>* Grafik di atas hanya menampilkan Top 10 entitas. Untuk melihat daftar lengkap dan detail seluruh aktor yang terdeteksi, silakan buka tabel data di bawah ini.</i></p>", unsafe_allow_html=True)
with st.expander("Lihat Data Tabel Frekuensi Aktor Lengkap (Hasil Ekstraksi NLP)"):
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("**Data Entitas Korporasi**")
        st.dataframe(df_aktor_perusahaan, use_container_width=True, hide_index=True)
    with col_t2:
        st.markdown("**Data Aktor Sipil & Organisasi**")
        st.dataframe(df_aktor_masyarakat, use_container_width=True, hide_index=True)
    st.caption("📁 **Sumber File:** <code>data/processed/sulawesi_konflik_agraria_tanahkita.csv</code> - Data diekstraksi secara dinamis menggunakan NLP Regex dari korpus narasi seluruh kasus agraria (Nasional, N=568 kasus) untuk memetakan orkestrasi struktural dan modus operandi aktor secara utuh.", unsafe_allow_html=True)
