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
st.markdown('<div class="sub-title">Membedah eskalasi konflik sosial dan perampasan ruang agraria di balik klaim keberhasilan pembangunan.</div>', unsafe_allow_html=True)

# ── Dropdown Metodologi ──
with st.expander("🔍 Metodologi", expanded=False):
    st.markdown("""
    **Alur Kausalitas (Ekonomi Politik Ekologi):** `Ekspansi Industri & Proyek Strategis` → `Perampasan Ruang Hidup & Lahan` → `Eskalasi Konflik Sosial/Agraria`
    
    Tesis dari analisis ini membantah narasi kesejahteraan dengan memperlihatkan bahwa agresivitas izin konsesi, proyek strategis nasional, hingga perluasan taman nasional dan pariwisata berbanding lurus dengan meningkatnya resistensi dan terdepaknya masyarakat lokal dari ruang kelolanya.
    
    **Variabel Dampak (Y):**
    *   **Jumlah Konflik:** Riwayat insiden letupan konflik agraria historis berdasarkan database independen masyarakat sipil.
    *   **Sektor Pemicu:** Tipologi konflik yang dipecah berdasarkan klasifikasi sektor penyebab dominan.
    
    **Metode Pengolahan Data:**
    Analisis menggunakan pendekatan *Trend Analysis* dan tabulasi silang (*Crosstabulation*). Menyandingkan matriks kejadian letupan konflik secara sektoral untuk mengekstraksi fakta episentrum sengketa berdarah.
    """)

# ── Hero Statement (Narasi Kritis Utama) ──
st.markdown(f"""
<div style="background-color: transparent; padding: 10px 0px; margin-bottom: 25px;">
    <h2 style="color: #FFFFFF; font-size: 1.8rem; margin-bottom: 15px; font-weight: 700;">Hilirisasi & Pembangunan Berlumur Konflik</h2>
    <p style="color: #CCCCCC; font-size: 1.05rem; line-height: 1.7; margin-bottom: 15px; text-align: justify;">
        Ekspansi industri ekstraktif dan proyek strategis tidak hanya menumbangkan daya dukung ekologis, tetapi secara agresif merobek tatanan kehidupan sosial masyarakat. Data empiris mencatat sejarah panjang perlawanan akar rumput dengan total terjadinya <b>{total_konflik} letupan konflik agraria</b> yang tercatat. Konflik ini bukanlah residu acak pembangunan, melainkan ekses langsung dari model ekonomi yang sangat rakus daratan. 
    </p>
    <p style="color: #CCCCCC; font-size: 1.05rem; line-height: 1.7; text-align: justify;">
        Secara mengejutkan, aktor perampas lahan utama tidak hanya didominasi oleh pertambangan dan perkebunan monokultur, namun meluas ke sekor <b>Kehutanan</b> (Hutan Lindung, Produksi, Konservasi), <b>Infrastruktur & PSN</b> (Bendungan, Transmigrasi, Kawasan Industri), hingga proyek <b>Pariwisata & Pesisir</b>. Tiga sektor utama (Perkebunan, Kehutanan, dan Pertambangan) menyumbang porsi <b>{rasio_ekstraktif:.1f}%</b> dari keseluruhan catatan konflik. Alih-alih mendapatkan kucuran kesejahteraan, warga lokal justru seringkali dikriminalisasi, direpresi, dan diusir dari atas ruang penghidupan historis mereka.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Kartu Metrik Agregat (Bento Cards) - Baris 1 (4 Kolom) ──
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Total Letupan Konflik</div>
            <div class="metric-value" style="color: #B71C1C;">{total_konflik} <span style="font-size:16px; color:#B0BEC5;">kasus</span></div>
            <div class="metric-desc">Insiden perampasan lahan dan sengketa agraria yang memicu perlawanan sipil.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Korban Terdampak (Jiwa)</div>
            <div class="metric-value" style="color: #C62828;">{total_jiwa:,} <span style="font-size:16px; color:#B0BEC5;">jiwa</span></div>
            <div class="metric-desc">Jumlah warga yang kehilangan ruang hidup, digusur, atau terpinggirkan akibat konflik lahan (bukan korban meninggal).</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Status: Belum Ditangani</div>
            <div class="metric-value" style="color: #D32F2F;">{status_belum_selesai} <span style="font-size:16px; color:#B0BEC5;">kasus</span></div>
            <div class="metric-desc">Kasus yang dibiarkan terkatung-katung tanpa resolusi berkeadilan bagi warga.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Masyarakat Melawan</div>
            <div class="metric-value" style="color: #E53935;">{libat_masyarakat} <span style="font-size:16px; color:#B0BEC5;">komunitas</span></div>
            <div class="metric-desc">Kelompok tani dan masyarakat adat yang berjuang mempertahankan ruang hidup.</div>
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
            <div class="metric-desc">Tumpang tindih Hak Guna Usaha (HGU) sawit skala masif dengan lahan rakyat.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Sektor Kehutanan</div>
            <div class="metric-value" style="color: #F4511E;">{konflik_hutan} <span style="font-size:16px; color:#B0BEC5;">kasus</span></div>
            <div class="metric-desc">Klaim sepihak hutan produksi dan konservasi yang menggusur masyarakat lokal.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col7:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Sektor Pertambangan</div>
            <div class="metric-value" style="color: #FF6F00;">{konflik_tambang} <span style="font-size:16px; color:#B0BEC5;">kasus</span></div>
            <div class="metric-desc">Operasi pengerukan lahan dan hilirisasi untuk industri mineral serta nikel.</div>
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
            <div class="metric-desc">Penggusuran proyek strategis nasional seperti bendungan dan jalan.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col9:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Pariwisata & Pesisir</div>
            <div class="metric-value" style="color: #FFAB91;">{konflik_pariwisata} <span style="font-size:16px; color:#B0BEC5;">kasus</span></div>
            <div class="metric-desc">Privatisasi pesisir dan pariwisata super-premium (KEK).</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col10:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Keterlibatan Pemerintah</div>
            <div class="metric-value" style="color: #E53935;">{libat_pemerintah} <span style="font-size:16px; color:#B0BEC5;">kasus</span></div>
            <div class="metric-desc">Andil institusi negara dan pemerintah daerah dalam sengketa warga.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col11:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Keterlibatan Korporasi</div>
            <div class="metric-value" style="color: #EF5350;">{libat_perusahaan} <span style="font-size:16px; color:#B0BEC5;">kasus</span></div>
            <div class="metric-desc">Perusahaan swasta asing maupun BUMN yang memonopoli ruang hidup.</div>
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
Visualisasi *time-series* di bawah ini memberikan bukti empiris yang tidak dapat dibantah mengenai korelasi langsung antara ekspansi industri berskala masif dengan eskalasi letupan konflik agraria di daratan Sulawesi. Secara historis, jika kita membandingkan dua periode waktu yang berbeda, lonjakan perampasan ruang hidup masyarakat terlihat sangat drastis dan tidak proporsional. Pada periode pra-2005, sistem pendataan mencatat "hanya" terdapat **{pra_2005} kasus** letupan konflik yang tereskalasi. Angka ini secara fundamental merepresentasikan dinamika agraria tradisional sebelum keran perizinan konsesi ekstraktif dibuka secara agresif oleh pemerintah daerah pasca implementasi otonomi daerah secara penuh. 

Namun, narasi harmoni pembangunan ini hancur berantakan ketika memasuki periode pasca-2005 hingga saat ini. Data empiris secara mengejutkan mencatat setidaknya **{pasca_2005} kasus** perampasan lahan yang memicu perlawanan berdarah, yang ekuivalen dengan lonjakan eskalasi raksasa sebesar **{lonjakan:,.1f}%** dibandingkan era sebelumnya. Transformasi tata ruang yang sangat brutal ini didorong oleh lahirnya rezim komodifikasi daratan, di mana penerbitan Izin Usaha Pertambangan (IUP) mineral dan batubara, serta ekspansi Hak Guna Usaha (HGU) untuk perkebunan kelapa sawit monokultur menjadi panglima pembangunan yang menggusur wilayah kelola masyarakat adat dan petani gurem. Hal ini secara faktual membuktikan bahwa model pembangunan berorientasi PDB (Produk Domestik Bruto) nyatanya beroperasi di atas kerentanan ruang hidup warga.

Lebih jauh lagi, jika membedah tren pada satu dekade terakhir (terutama puncak eskalasi masif pada tahun 2017 dan melesat pasca-2020), kita menemukan anomali yang sangat berbahaya. Tren letupan sengketa sosial ini tidak lagi sekadar didominasi oleh perambahan hutan lindung atau perluasan kebun sawit, melainkan telah bermutasi menjadi konflik struktural akibat narasi besar **Hilirisasi Nikel** dan pengadaan daratan secara darurat untuk **Proyek Strategis Nasional (Infrastruktur & PSN)**. Warga lokal dipaksa melepaskan hak atas tanah produktif mereka di wilayah-wilayah episentrum ekstraktif demi menggelar karpet merah bagi modal korporat transnasional. Fakta keras berupa **{total_ts} total insiden historis** ini secara definitif membantah klaim negara bahwa industrialisasi ekstraktif membawa efek kesejahteraan berganda (*trickle-down effect*). Sebaliknya, kawasan-kawasan investasi tersebut justru bermetamorfosis menjadi 'zona tumbal' (*sacrifice zones*) di mana laju akumulasi kapital segelintir elit korporasi harus dibayar sangat mahal dengan ongkos krisis ekologis permanen, represi aparat negara, serta hancurnya tatanan kedaulatan pangan maupun pranata sosial masyarakat lokal.
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
    title='Ledakan Konflik Agraria di Sulawesi (1990 - 2025)',
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
        text=f"Puncak Krisis:<br><b>{peak_value} Letupan ({peak_year})</b>",
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

st.plotly_chart(fig_ts, use_container_width=True)

st.markdown("""
<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #FF9800; margin-bottom: 25px;">
    <b style="color: #FF9800;">Interpretasi Ekologis dan Sosial:</b> Loncatan drastis letupan konflik terjadi beririsan dengan agresivitas rezim perizinan. Hilirisasi Nikel dan Proyek Strategis Nasional (PSN) secara faktual telah merekayasa kawasan investasi menjadi zona tumbal yang mengorbankan kedaulatan masyarakat lokal secara permanen.
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# SUB-BAB 4.2: SEBARAN SEKTORAL DAMPAK
# ══════════════════════════════════════════════════════════
st.subheader("4.2 Sebaran Sektoral: Korban Jiwa dan Monopoli Ruang")
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
Konflik agraria bukanlah sebuah insiden terisolasi yang hanya berupa sengketa batas tanah, melainkan instrumen sistematis dari akumulasi modal yang beroperasi dengan menggusur paksa kehidupan manusia. Visualisasi komparatif di bawah ini membongkar skala kehancuran sosial dan ekologis yang diakibatkan oleh masing-masing sektor industri ekstraktif. Ketika kita membedah total jumlah korban terdampak, data menunjukkan realitas yang sangat mengerikan. **Sektor Kehutanan** menjadi penyumbang terbesar krisis kemanusiaan dengan total korban mencapai **{jiwa_kehutanan:,.0f} jiwa**. Angka ini bukan sekadar statistik; ini merepresentasikan masyarakat adat dan komunitas lokal yang ruang hidup dan wilayah adatnya direnggut atas nama legalitas izin Hutan Tanaman Industri (HTI) maupun klaim sepihak kawasan lindung oleh negara.

Menyusul di posisi kedua adalah **Sektor Pertambangan** yang telah memakan korban sebanyak **{jiwa_tambang:,.0f} jiwa**. Lonjakan korban di sektor ini berhubungan langsung dengan ambisi hilirisasi mineral kritis (terutama nikel) yang memaksa warga pesisir dan petani untuk melepaskan ruang produksi mereka demi fasilitas *smelter* dan pertambangan terbuka. Masyarakat yang melawan seringkali dihadapkan pada represi berlapis, mulai dari intimidasi preman korporasi hingga kriminalisasi oleh aparat keamanan negara yang bertindak sebagai penjaga gawang investasi.

Di sisi lain, saat kita meninjau dari dimensi monopoli tata ruang (luasan hektar yang dikonflikkan), **Sektor Perkebunan**—khususnya ekspansi kelapa sawit—menjadi penguasa absolut dengan merampas lahan seluas **{ha_kebun:,.0f} Hektar**. Konsentrasi penguasaan tanah oleh segelintir korporasi perkebunan ini menghancurkan kedaulatan pangan lokal dan menciptakan ketimpangan agraria yang struktural. Disusul oleh sektor Kehutanan seluas **{ha_kehutanan:,.0f} Ha** dan Pertambangan seluas **{ha_tambang:,.0f} Ha**, trinitas sektor ekstraktif ini (Kebun, Hutan, Tambang) secara empiris membuktikan bahwa pembangunan ekonomi selama ini semata-mata bergantung pada perampasan ruang berskala masif. Tidak ada tetesan kesejahteraan (*trickle-down effect*) bagi warga tapak; yang tersisa hanyalah kemiskinan struktural, pencemaran tanah, dan hilangnya hak-hak dasar konstitusional mereka atas daratan yang telah mereka tempati secara turun-temurun.
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
        title='Ledakan Korban Terdampak (Jiwa) per Tahun',
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

    st.plotly_chart(fig_jiwa, use_container_width=True)

with col_ha:
    fig_ha = px.bar(
        df_sektor_tahun,
        x='tahun',
        y='luas_ha',
        color='Sektor_Grup',
        title='Monopoli Area Konflik (Hektar) per Tahun',
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

    st.plotly_chart(fig_ha, use_container_width=True)

st.markdown("""
<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #F44336; margin-bottom: 25px;">
    <b style="color: #F44336;">Interpretasi Ekologis dan Sosial:</b> Lonjakan luar biasa pada grafik merepresentasikan titik didih ledakan demografis dari kegagalan mutlak sistem pengaman sosial di zona investasi ekstraktif.
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
            link = top_case['detail_url'] if 'detail_url' in top_case and pd.notna(top_case['detail_url']) else '#'
            
            st.markdown(f"**Kasus Utama Pendongkrak Statistik: {judul}**")
            st.markdown(f"* **Total Korban (Kasus Ini):** {int(korban):,} Jiwa")
            st.markdown(f"* **Perusahaan Terlibat:** {pt}")
            st.markdown(f"* **Narasi Singkat:** {narasi}")
            st.markdown(f"* **Sumber Referensi:** [Lihat Detail Kasus TanahKita]({link})")

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
            link = top_case['detail_url'] if 'detail_url' in top_case and pd.notna(top_case['detail_url']) else '#'

            st.markdown(f"**Kasus Utama Pendongkrak Statistik: {judul}**")
            st.markdown(f"* **Total Daratan Dirampas (Kasus Ini):** {int(luas):,} Hektar")
            st.markdown(f"* **Perusahaan Terlibat:** {pt}")
            st.markdown(f"* **Narasi Singkat:** {narasi}")
            st.markdown(f"* **Sumber Referensi:** [Lihat Detail Kasus TanahKita]({link})")

st.subheader("4.3 Kriminalisasi Aktivis dan Resistensi Ruang Sipil")
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
Rentetan data kuantitatif di wilayah Sulawesi secara telanjang membantah klaim arus utama yang kerap didengungkan oleh pemerintah dan oligarki korporasi, bahwa ekspansi industri ekstraktif membawa kesejahteraan dan pertumbuhan inklusif bagi masyarakat lokal. Fakta empiris justru memperlihatkan bahwa tata kelola investasi di Indonesia secara struktural dibangun di atas fondasi represi dan kekerasan terhadap ruang sipil. 

Dari **{total_kriminalisasi} kasus indikasi kriminalisasi** yang berhasil didokumentasikan, tercatat sebanyak **{total_ditangkap} warga dan aktivis lingkungan yang ditangkap** secara sewenang-wenang. Angka ini bukanlah statistik hampa, melainkan representasi dari hancurnya keadilan ekologis dan perampasan ruang hidup masyarakat adat, petani, dan nelayan yang dipaksa menyerahkan tanah leluhurnya demi akumulasi kapital segelintir elit industri ekstraktif.

Jika kita membedah lebih dalam pada distribusi sektoral, **Sektor {top_sektor}** muncul sebagai aktor dominan yang paling sering menggunakan instrumen koersif negara, menyumbang total **{top_sektor_count} kasus represi**. Penggunaan aparat keamanan negara maupun preman korporasi untuk memuluskan perampasan tanah menunjukkan bahwa hukum seringkali ditundukkan pada kepentingan bisnis raksasa yang lapar lahan. Eskalasi konflik paling mematikan mencapai puncaknya pada tahun **{top_tahun}** dengan mencatatkan **{top_tahun_count} kasus secara bersamaan**. Dalam banyak peristiwa empiris, warga lokal yang sekadar mempertahankan hak konstitusional mereka atas lingkungan hidup yang baik dan sehat justru dilabeli sebagai provokator dan dijerat pasal pidana karet.

Tragedi kemanusiaan ini menjadi semakin kelam dengan hilangnya nyawa **{total_tewas} pejuang lingkungan** yang melayang sia-sia di pusaran konflik agraria. Gugurnya pahlawan-pahlawan ruang hidup ini menggarisbawahi kegagalan mutlak instrumen pengaman ekologis - seperti D3TLH maupun dokumen AMDAL - dalam menjamin keselamatan rakyat. Selama pendekatan pembangunan eksploitatif yang bertumpu pada sekuritisasi investasi ini dipertahankan, setiap hektar hutan yang dibabat akan selalu berlumuran air mata konflik.
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
    st.plotly_chart(fig_krim_tahun, use_container_width=True)
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
    st.plotly_chart(fig_krim_sektor, use_container_width=True)
    with st.expander("Lihat Data Mentah: Sektor Represif", expanded=False):
        st.dataframe(df_krim_sektor, use_container_width=True, hide_index=True)
        st.caption("📁 **Sumber File:** `data/processed/sulawesi_konflik_agraria_tanahkita.csv` - Total kasus kriminalisasi dikelompokkan per sektor.")

st.markdown(f"""
<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #E53935; margin-bottom: 25px; margin-top: 25px;">
    <b>Interpretasi Ekologis & Hak Asasi Manusia:</b> Tingginya angka kriminalisasi dan korban tewas di sekitar area konsesi (terutama {top_sektor}) membuktikan bahwa perampasan ruang selalu dibarengi dengan pendekatan represif. Ini membantah telak narasi "Hilirisasi Hijau" yang nyatanya ditebus dengan ongkos kemanusiaan yang berdarah.
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
st.markdown('<span style="background:#4A148C;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Before-After Analysis & SPSS-Style Crosstabulation</span>', unsafe_allow_html=True)
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

with st.expander("ℹ️ Metodologi: Before-After Analysis & SPSS-Style Crosstabulation"):
    st.markdown("""
    **Metode Analisis:** Sub-bab ini menggunakan Uji Chi-Square (*Crosstabulation*) gaya SPSS dan kalkulasi risiko peluang (*Odds Ratio*) untuk menguji validitas empiris secara akademis.

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
st.markdown("#### B. Uji Statistik Crosstab (Chi-Square SPSS Style)")

import scipy.stats as stats

# Data Preparation
df_crosstab = df_dampak.copy()
df_crosstab = df_crosstab[df_crosstab['tahun'] >= 1990]

# Define columns for X
df_crosstab['Periode_Ekspansi'] = df_crosstab['tahun'].apply(lambda x: 'Pasca-ekspansi (≥ 2014)' if x >= 2014 else 'Pra-ekspansi (< 2014)')
df_crosstab['Keterlibatan_Perusahaan'] = df_crosstab['keterlibatan_perusahaan'].notna().apply(lambda x: 'Terlibat Korporasi' if x else 'Tanpa Korporasi/Tidak Teridentifikasi')

# Define columns for Y
df_crosstab['Indikasi_Kriminalisasi'] = df_crosstab['indikasi_kriminalisasi'].fillna(False).astype(bool).apply(lambda x: 'Ada Represi/Kriminalisasi' if x else 'Baseline (Tanpa Kriminalisasi)')
df_crosstab['Dampak_Kematian'] = (df_crosstab['jumlah_tewas'] > 0).apply(lambda x: 'Jatuh Korban Nyawa' if x else 'Tanpa Korban Jiwa')

x_order = {
    "Periode_Ekspansi": ['Pra-ekspansi (< 2014)', 'Pasca-ekspansi (≥ 2014)'],
    "Keterlibatan_Perusahaan": ['Tanpa Korporasi/Tidak Teridentifikasi', 'Terlibat Korporasi']
}
y_order = {
    "Indikasi_Kriminalisasi": ['Baseline (Tanpa Kriminalisasi)', 'Ada Represi/Kriminalisasi'],
    "Dampak_Kematian": ['Tanpa Korban Jiwa', 'Jatuh Korban Nyawa']
}

col_sel1, col_sel2 = st.columns(2)

with col_sel1:
    st.markdown("##### Variabel Independen (X) - Kondisi Ekspansi")
    x_options = {
        "Periode_Ekspansi": "Periode Ekspansi Industri",
        "Keterlibatan_Perusahaan": "Status Keterlibatan Korporasi"
    }
    x_col = st.selectbox("Pilih Indikator Ekspansi (X):", list(x_options.keys()), format_func=lambda x: x_options[x])

with col_sel2:
    st.markdown("##### Variabel Dependen (Y) - Eskalasi Konflik")
    y_options = {
        "Indikasi_Kriminalisasi": "Tingkat Represi & Kriminalisasi",
        "Dampak_Kematian": "Tingkat Fatalitas (Korban Nyawa)"
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
        interp_text = f"Temuan ini sangat krusial: pergeseran status <b>{x_options[x_col]}</b> terbukti **berkorelasi kuat dan signifikan** dengan <b>{y_options[y_col]}</b> (P < 0.05). Angka Odds Ratio (OR: {odds_ratio:.3f}) menjadi konfirmasi empiris bahwa narasi hilirisasi dan investasi bukanlah agenda nirkekerasan—ekspansi spasial mereka mutlak mengeskalasi pelanggaran hak asasi masyarakat tapak."
    else:
        interp_text = f"Secara agregat, hubungan antara <b>{x_options[x_col]}</b> dan <b>{y_options[y_col]}</b> **tidak menunjukkan perbedaan yang signifikan** secara statistik (P ≥ 0.05). Hal ini mengindikasikan bahwa penggunaan instrumen kekerasan sudah mengakar dan sistematis di sepanjang sejarah konflik agraria tanpa memandang batas waktu rezim atau aktor yang terlihat."
    
    st.markdown(f"""
    <div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid {order_color}; height: 100%;">
        <b>Interpretasi Sosial Kritis:</b><br><br>
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
Angka-angka pada tabel di atas bukan sekadar statistik di atas kertas, melainkan <b>bukti empiris</b> dari brutalitas pembangunan. Tingginya angka kemunculan represi pada skenario yang signifikan menegaskan bahwa setiap kali wilayah operasi investasi diperlebar, probabilitas dihadapkannya moncong senjata kepada warga melonjak drastis.<br><br>
Skenario yang <i>TIDAK SIGNIFIKAN</i> tidak berarti rezim terbebas dari dosa kekerasan, melainkan bukti bahwa represi terhadap warga yang mempertahankan tanahnya telah menjadi kultur mapan yang menyebar secara sporadis melampaui sekat waktu dan korporasi.    """)
    bg_color = "rgba(229, 57, 53, 0.15)"
    border_color = "#E53935"
else:
    exec_narrative = textwrap.dedent(f"""Dari <b>{total_scenarios} skenario pengujian</b>, seluruhnya menunjukkan status <b>TIDAK SIGNIFIKAN</b>.<br><br>
Dalam kacamata ekonomi politik, ketidaksignifikanan secara agregat ini justru membuktikan bahwa aparatus represif telah dipekerjakan <i>sepanjang waktu secara stabil</i> dalam menggusur ruang hidup rakyat. Kekerasan bukanlah produk parsial satu rezim, melainkan instrumen fundamental yang menyokong eksistensi industri ekstraktif.    """)
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
st.subheader("4.5 Peta Orkestrasi Konflik: Aktor Sipil vs Aktor Ekstraktif")
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
Konflik yang membara tidak hanya melibatkan negara dan aparat, melainkan memunculkan fenomena adu domba struktural (*orkestrasi konflik horizontal*). 
Pemecahan entitas (*string parsing*) terhadap catatan kronologi advokasi TanahKita menelanjangi siapa yang sesungguhnya bermain di lapangan. 
Di satu sisi, masyarakat asli sering kali didampingi oleh organisasi struktural yang solid, namun di sisi lain, mulai muncul 
ormas-ormas, lembaga swadaya buatan, hingga institusi pseudo-adat yang digunakan sebagai proksi (*buffer*) oleh korporasi. 
Grafik frekuensi ini membongkar dominasi aktor-aktor sipil dan perusahaan tambang yang paling banyak merebut ruang hidup.
""")

import re

# NLP Extraction (Regex) for Actors from Text
text_corpus = " ".join((df_konflik['judul'].fillna('') + " " + df_konflik['deskripsi'].fillna('') + " " + df_konflik['narasi'].fillna('')).tolist())

# Extract Corporate Actors
pts = re.findall(r'\b(?:PT|CV)\.?\s*[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*){0,3}\b', text_corpus)
pts = [" ".join(pt.split()) for pt in pts]
df_aktor_perusahaan = pd.Series(pts).value_counts().reset_index()
df_aktor_perusahaan.columns = ['Aktor', 'Frekuensi']

# Extract Civil Society Actors
civils = re.findall(r'\b(?:Walhi|WALHI|Jatam|JATAM|AMAN|LBH|Aliansi|Serikat|Konsorsium|Masyarakat Adat|Warga Desa)\s*[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*){0,3}\b', text_corpus)
civils = [" ".join(cv.split()) for cv in civils]
df_aktor_masyarakat = pd.Series(civils).value_counts().reset_index()
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
        st.plotly_chart(fig_corp, use_container_width=True)
    top1_corp_name = df_aktor_perusahaan.iloc[0]['Aktor'] if not df_aktor_perusahaan.empty else "Korporasi"
    top1_corp_freq = df_aktor_perusahaan.iloc[0]['Frekuensi'] if not df_aktor_perusahaan.empty else 0

    st.markdown(f"""
    <div style="background:rgba(245, 124, 0, 0.1);padding:15px;border-left:3px solid #F57C00;border-radius:5px;font-size:0.9rem;">
        <b>Analisis Kritis:</b> Ekstraksi presisi tinggi membuktikan dominasi absolut dari entitas <b>{top1_corp_name}</b> yang terlibat dalam <b>{top1_corp_freq} catatan konflik terpisah</b>. Konsentrasi tinggi frekuensi korporasi besar ini menegaskan bahwa represi di Sulawesi bukan sekadar residu administratif, melainkan <i>modus operandi</i> struktural para penguasa modal skala masif.
    </div>
    """, unsafe_allow_html=True)

with col_aktor_2:
    st.markdown("#### Top 10 Aktor Sipil & Ormas Terlibat")
    top_civil = df_aktor_masyarakat[~df_aktor_masyarakat['Aktor'].str.contains('Masyarakat Desa|Masyarakat Kabupaten|Warga|Petani', case=False, na=False)].head(10).sort_values(by='Frekuensi', ascending=True)
    if not top_civil.empty:
        fig_civil = px.bar(
            top_civil, 
            x='Frekuensi', y='Aktor', orientation='h',
            color_discrete_sequence=['#43A047']
        )
        fig_civil.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ECEFF1'), margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', tickformat='d')
        )
        st.plotly_chart(fig_civil, use_container_width=True)
        
    top1_civ_name = df_aktor_masyarakat.iloc[0]['Aktor'] if not df_aktor_masyarakat.empty else "Masyarakat Adat"
    top1_civ_freq = df_aktor_masyarakat.iloc[0]['Frekuensi'] if not df_aktor_masyarakat.empty else 0

    st.markdown(f"""
    <div style="background:rgba(67, 160, 71, 0.1);padding:15px;border-left:3px solid #43A047;border-radius:5px;font-size:0.9rem;">
        <b>Analisis Kritis:</b> Kemunculan <b>{top1_civ_name}</b> (disebut hingga <b>{top1_civ_freq} kali</b>) serta berbagai organisasi advokasi (*Jatam, Walhi, AMAN*) menangkap besarnya skala resistensi akar rumput. Tingginya friksi pada ormas sektoral dan kelompok identitas merangkap sebagai sinyal waspada atas potensi benturan horizontal yang diorkestrasi.
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
with st.expander("Lihat Data Tabel Frekuensi Aktor Lengkap (Hasil Ekstraksi NLP)"):
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("**Data Entitas Korporasi**")
        st.dataframe(df_aktor_perusahaan, use_container_width=True, hide_index=True)
    with col_t2:
        st.markdown("**Data Aktor Sipil & Organisasi**")
        st.dataframe(df_aktor_masyarakat, use_container_width=True, hide_index=True)
    st.caption("Data di atas diekstraksi secara dinamis dengan menggunakan metode NLP Regex dari kumpulan korpus `narasi`, `deskripsi`, dan `judul` kasus TanahKita (N=95 Sulawesi-Malut).")
