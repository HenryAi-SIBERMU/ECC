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
@st.cache_data
def load_konflik_data_full():
    df_konflik = pd.read_csv('data/processed/sulawesi_konflik_agraria_tanahkita.csv')
    return df_konflik

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
            <div class="metric-value" style="color: #F44336;">{total_konflik} <span style="font-size:16px; color:#B0BEC5;">kasus</span></div>
            <div class="metric-desc">Insiden perampasan lahan dan sengketa agraria yang memicu perlawanan sipil.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Korban Terdampak (Jiwa)</div>
            <div class="metric-value" style="color: #FF5252;">{total_jiwa:,} <span style="font-size:16px; color:#B0BEC5;">jiwa</span></div>
            <div class="metric-desc">Jumlah warga yang kehilangan ruang hidup, digusur, atau terpinggirkan akibat konflik lahan (bukan korban meninggal).</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Status: Belum Ditangani</div>
            <div class="metric-value" style="color: #FF9800;">{status_belum_selesai} <span style="font-size:16px; color:#B0BEC5;">kasus</span></div>
            <div class="metric-desc">Kasus yang dibiarkan terkatung-katung tanpa resolusi berkeadilan bagi warga.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Masyarakat Melawan</div>
            <div class="metric-value" style="color: #00BCD4;">{libat_masyarakat} <span style="font-size:16px; color:#B0BEC5;">komunitas</span></div>
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
            <div class="metric-value" style="color: #FFC107;">{konflik_kebun} <span style="font-size:16px; color:#B0BEC5;">kasus</span></div>
            <div class="metric-desc">Tumpang tindih Hak Guna Usaha (HGU) sawit skala masif dengan lahan rakyat.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Sektor Kehutanan</div>
            <div class="metric-value" style="color: #8BC34A;">{konflik_hutan} <span style="font-size:16px; color:#B0BEC5;">kasus</span></div>
            <div class="metric-desc">Klaim sepihak hutan produksi dan konservasi yang menggusur masyarakat lokal.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col7:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Sektor Pertambangan</div>
            <div class="metric-value" style="color: #FF9800;">{konflik_tambang} <span style="font-size:16px; color:#B0BEC5;">kasus</span></div>
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
            <div class="metric-value" style="color: #03A9F4;">{konflik_infrastruktur} <span style="font-size:16px; color:#B0BEC5;">kasus</span></div>
            <div class="metric-desc">Penggusuran proyek strategis nasional seperti bendungan dan jalan.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col9:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Pariwisata & Pesisir</div>
            <div class="metric-value" style="color: #E91E63;">{konflik_pariwisata} <span style="font-size:16px; color:#B0BEC5;">kasus</span></div>
            <div class="metric-desc">Privatisasi pesisir dan pariwisata super-premium (KEK).</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col10:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Keterlibatan Pemerintah</div>
            <div class="metric-value" style="color: #607D8B;">{libat_pemerintah} <span style="font-size:16px; color:#B0BEC5;">kasus</span></div>
            <div class="metric-desc">Andil institusi negara dan pemerintah daerah dalam sengketa warga.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col11:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Keterlibatan Korporasi</div>
            <div class="metric-value" style="color: #795548;">{libat_perusahaan} <span style="font-size:16px; color:#B0BEC5;">kasus</span></div>
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
st.markdown('<span style="background:#5C2B6A;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Analisis Tren Time-Series (Sumber: KPA / Tanah Kita)</span><br><br>', unsafe_allow_html=True)

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
st.markdown('<span style="background:#5C2B6A;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Analisis Komparatif Dampak Sosial-Ekologis (Sumber: KPA / Tanah Kita)</span><br><br>', unsafe_allow_html=True)

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
    
    val_2012 = df_sektor_tahun[df_sektor_tahun['tahun'] == 2012]['dampak_masyarakat_jiwa'].sum()
    if val_2012 > 0:
        fig_jiwa.add_annotation(
            x=2012, y=val_2012,
            text="<a href='#anomali-1' target='_self' style='color:white;text-decoration:none;'><b>Anomali 1</b></a>",
            hovertext="<b>2012 (Pertambangan)</b><br>Klik untuk melihat detail di bawah",
            showarrow=True, arrowhead=2, arrowcolor="#FF5252", ax=0, ay=-35,
            font=dict(size=11, color="white"), bgcolor="rgba(211,47,47,0.8)", bordercolor="#FF5252"
        )
    val_2019 = df_sektor_tahun[df_sektor_tahun['tahun'] == 2019]['dampak_masyarakat_jiwa'].sum()
    if val_2019 > 0:
        fig_jiwa.add_annotation(
            x=2019, y=val_2019,
            text="<a href='#anomali-2' target='_self' style='color:white;text-decoration:none;'><b>Anomali 2</b></a>",
            hovertext="<b>2019 (PSN & Kehutanan)</b><br>Klik untuk melihat detail di bawah",
            showarrow=True, arrowhead=2, arrowcolor="#FF5252", ax=0, ay=-35,
            font=dict(size=11, color="white"), bgcolor="rgba(211,47,47,0.8)", bordercolor="#FF5252"
        )
    val_2020 = df_sektor_tahun[df_sektor_tahun['tahun'] == 2020]['dampak_masyarakat_jiwa'].sum()
    if val_2020 > 0:
        fig_jiwa.add_annotation(
            x=2020, y=val_2020,
            text="<a href='#anomali-5' target='_self' style='color:white;text-decoration:none;'><b>Anomali 5</b></a>",
            hovertext="<b>2020 (Kehutanan)</b><br>Klik untuk melihat detail di bawah",
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

    val_2010 = df_sektor_tahun[df_sektor_tahun['tahun'] == 2010]['luas_ha'].sum()
    if val_2010 > 0:
        fig_ha.add_annotation(
            x=2010, y=val_2010,
            text="<a href='#anomali-3' target='_self' style='color:#111;text-decoration:none;'><b>Anomali 3</b></a>",
            hovertext="<b>2010 (Perkebunan)</b><br>Klik untuk melihat detail di bawah",
            showarrow=True, arrowhead=2, arrowcolor="#FFC107", ax=0, ay=-35,
            font=dict(size=11, color="#111"), bgcolor="rgba(255,193,7,0.9)", bordercolor="#FFB300"
        )
    val_2014 = df_sektor_tahun[df_sektor_tahun['tahun'] == 2014]['luas_ha'].sum()
    if val_2014 > 0:
        fig_ha.add_annotation(
            x=2014, y=val_2014,
            text="<a href='#anomali-4' target='_self' style='color:#111;text-decoration:none;'><b>Anomali 4</b></a>",
            hovertext="<b>2014 (Hutan & Kebun)</b><br>Klik untuk melihat detail di bawah",
            showarrow=True, arrowhead=2, arrowcolor="#FFC107", ax=0, ay=-35,
            font=dict(size=11, color="#111"), bgcolor="rgba(255,193,7,0.9)", bordercolor="#FFB300"
        )

    st.plotly_chart(fig_ha, use_container_width=True)

st.markdown("""
<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #F44336; margin-bottom: 25px;">
    <b style="color: #F44336;">Interpretasi Ekologis dan Sosial:</b> Monopoli tanah terbesar dilakukan oleh rezim Perkebunan monokultur (Sawit), namun daya rusak kemanusiaan terburuk (pengusiran masyarakat masif) disetir oleh sektor Kehutanan dan Pertambangan (Nikel). Lonjakan luar biasa pada grafik pasca-2005 dan dekade terakhir merepresentasikan kegagalan mutlak sistem pengaman sosial di zona investasi.
</div>
""", unsafe_allow_html=True)

with st.expander("🔍 Bedah Forensik Anomali (Spike) Konflik Agraria", expanded=True):
    st.markdown("""
Berdasarkan ekstraksi dataset secara mendalam pada kolom `deskripsi`, `keterlibatan_perusahaan`, `keterlibatan_pemerintah`, dan `narasi`, berikut adalah anatomi dari lonjakan-lonjakan ekstrem (*spikes*) yang terjadi pada grafik **Ledakan Korban Terdampak (Jiwa)** dan **Monopoli Area Konflik (Hektar)**.

---

<a id="anomali-1"></a>
#### ANOMALI 1: Lonjakan Korban Jiwa Tahun 2012 (Sektor Pertambangan)
Tahun 2012 mencatatkan ledakan korban jiwa tertinggi di Sektor Pertambangan, didominasi oleh dua megaproyek yang memicu represi masif terhadap warga:

**1. Konflik Kawasan Bentang Alam Karst (KBAK) Gombong**
* **Total Korban:** 82.692 Jiwa
* **Perusahaan Terlibat:** PT Semen Gombong / Medco Group
* **Pemerintah Terlibat:** Pemkab Kebumen, Pemprov Jawa Tengah, Kementerian ESDM
* **Narasi Kasus:** Ekspansi komoditas batu gamping seluas 147,50 Ha oleh PT Medco Group mengancam ekosistem karst Gombong. Izin Usaha Pertambangan (IUP) yang terus diperpanjang memicu perlawanan besar-besaran dari masyarakat (Perpag) yang menolak pabrik semen karena mengancam sumber air dan ruang hidup puluhan ribu warga.
* **Sumber Referensi:** [Tribun Jateng (Aksi Tolak Semen)](http://jateng.tribunnews.com/2018/10/16/perpag-kebumen-akan-aksi-besar-besaran-tolak-pabrik-semen) | [LBH Semarang](http://lbhsemarang.or.id/policy-brief-lbh-semarang-menata-karst-gombong-fungsi-lindung-yang-diusung/)

**2. Konflik Gunung Tumpang Pitu, Banyuwangi**
* **Total Korban:** 13.936 Jiwa
* **Perusahaan Terlibat:** PT Bumi Suksindo (BSI) / PT. Merdeka Copper Gold
* **Pemerintah Terlibat:** Pemkab Banyuwangi, Pengadilan Negeri, Mahkamah Agung
* **Narasi Kasus:** Konsesi tambang emas seluas 4.998 Ha di wilayah Desa Sumberagung. Keputusan Bupati yang mengubah status lindung dan memberikan IUP OP memicu penolakan keras yang berujung pada bentrokan, unjuk rasa masif, serta rentetan kriminalisasi terhadap aktivis dan warga penolak tambang.
* **Sumber Referensi:** [Mongabay (Konflik Tumpang Pitu)](https://www.mongabay.co.id/2015/12/02/saat-warga-penolak-tambang-emas-tumpang-pitu-berhadapan-dengan-aparat/)

---

<a id="anomali-2"></a>
#### ANOMALI 2: Lonjakan Korban Jiwa Tahun 2019 (Infrastruktur PSN & Kehutanan)
Tahun 2019 menunjukkan eskalasi brutal pengusiran warga atas nama Proyek Strategis Nasional (PSN) dan pencaplokan hutan:

**1. Megaproyek Pelabuhan Internasional Patimban (Subang)**
* **Total Korban:** 38.951 Jiwa
* **Sektor:** Infrastruktur & PSN
* **Perusahaan Terlibat:** PT. Wijaya Karya, PT. PP, Shimizu Corporation, JICA
* **Pemerintah Terlibat:** Kemenhub, PUPR, BPN, Gubernur Jawa Barat, LMAN
* **Narasi Kasus:** Ditetapkan sebagai PSN oleh Presiden melalui Perpres 47/2016. Proyek yang didanai JICA ini memicu krisis agraria parah karena proses pembebasan lahan yang cacat, merugikan puluhan ribu nelayan dan petani yang tanahnya digusur tanpa ganti rugi yang layak hingga akhir 2019.
* **Sumber Referensi:** [Mongabay (Derita Nelayan Patimban)](https://www.mongabay.co.id/2020/12/28/derita-nelayan-terdampak-pembangunan-pelabuhan-patimban/)

**2. Penolakan Tambang Timah di Perairan Bangka**
* **Total Korban:** 13.494 Jiwa
* **Sektor:** Pertambangan
* **Perusahaan Terlibat:** PT. Timah Tbk
* **Pemerintah Terlibat:** Pemprov Kep. Bangka Belitung, Kementerian KKP, Dinas Perikanan
* **Narasi Kasus:** Nelayan pesisir Matras melakukan pengusiran terhadap Kapal Isap Produksi (KIP) milik PT Timah Tbk yang beroperasi di wilayah tangkapan nelayan. Ekspansi timah lepas pantai menghancurkan terumbu karang dan mematikan ekonomi nelayan tradisional.
* **Sumber Referensi:** [Tempo (Nelayan Matras Tolak Kapal Isap)](https://nasional.tempo.co/read/1231626/nelayan-matras-bangka-tolak-kapal-isap-timah)

**3. HTI PT Biomass Andalan Energi (Mentawai)**
* **Total Korban:** 10.395 Jiwa
* **Sektor:** Kehutanan
* **Perusahaan Terlibat:** PT. Biomass Andalan Energi
* **Pemerintah Terlibat:** KLHK, BKPM, Pemkab Mentawai, Gubernur Sumatera Barat
* **Narasi Kasus:** Penerbitan Izin Usaha Pemanfaatan Hasil Hutan Kayu pada Hutan Tanaman Industri (IUPHHK-HTI) yang mengancam ruang hidup masyarakat adat Mentawai. Koalisi masyarakat mendesak KLHK membatalkan izin tersebut karena berisiko menghabisi ekosistem pulau kecil.
* **Sumber Referensi:** [Mongabay (Warga Mentawai Tolak HTI)](https://www.mongabay.co.id/2019/08/12/kala-warga-mentawai-tolak-kehadiran-hti/)

---

<a id="anomali-3"></a>
#### ANOMALI 3: Lonjakan Area Konflik Tahun 2010 (Perkebunan)
Tahun 2010 merupakan titik nadir perampasan tanah berskala raksasa di sektor perkebunan (Agroindustri):

**1. Megaproyek MIFEE (Merauke Integrated Food and Energy Estate)**
* **Luas Area:** 1.200.000 Hektar (1,2 Juta Ha)
* **Sektor:** Perkebunan
* **Perusahaan Terlibat:** PT. Dongin Prabhawa, PT. Cendrawasih Jaya Mandiri
* **Pemerintah Terlibat:** Menteri Kehutanan, Menko Perekonomian, Menteri Pertanian, Pemprov Papua
* **Narasi Kasus:** Kebijakan *Top-Down* dari pemerintah pusat untuk menciptakan lumbung pangan dan energi memicu kanibalisme daratan seluas 1,2 juta Hektar. Suku Malind dan masyarakat adat Papua digusur dan kehilangan hak ulayatnya, sementara sungai-sungai mereka dicemari oleh pestisida dan aktivitas korporasi kelapa sawit.
* **Sumber Referensi:** [Project Multatuli (MIFEE Proyek Gagal)](https://projectmultatuli.org/mifee-proyek-pangan-raksasa-papua-yang-gagal-dan-merampas-tanah-adat/)

---

<a id="anomali-4"></a>
#### ANOMALI 4: Lonjakan Area Konflik Tahun 2014 (Kehutanan & Perkebunan)
Tahun 2014 mencatatkan lonjakan masif pada luasan area konflik, didominasi oleh pencaplokan pulau-pulau kecil untuk konsesi kehutanan dan perkebunan raksasa:

**1. Megaproyek Perkebunan Tebu PT Menara Group (Kepulauan Aru, Maluku)**
* **Luas Area:** 626.900 Hektar
* **Sektor:** Kehutanan (Dialihfungsikan ke Perkebunan)
* **Perusahaan Terlibat:** Konsorsium PT Menara Group (28 perusahaan)
* **Pemerintah Terlibat:** Menteri Kehutanan, Gubernur Maluku, Bupati Kepulauan Aru
* **Narasi Kasus:** Sebuah skandal perampasan ruang hidup yang hampir menghilangkan Kabupaten Kepulauan Aru dari peta ekologis. Pemerintah menerbitkan izin prinsip seluas lebih dari 600 ribu hektar (sebagian besar daratan Kepulauan Aru) kepada konsorsium PT Menara Group untuk perkebunan tebu. Hal ini memicu gerakan masif lokal, nasional, dan global **#SaveAru** karena proyek ini dinilai akan menghancurkan ruang hidup masyarakat adat secara total, memusnahkan keanekaragaman hayati endemis, dan menenggelamkan pulau-pulau kecil akibat eksploitasi air tanah skala industri.
* **Sumber Referensi:** [Mongabay (Gerakan #SaveAru)](https://www.mongabay.co.id/2014/04/16/save-aru-perjuangan-masyarakat-kepulauan-aru-melawan-korporasi/) | [Forest Watch Indonesia](https://fwi.or.id/publikasi/menyelamatkan-kepulauan-aru/)

**2. Sengketa Lahan PT Perkebunan Nusantara II (Langkat)**
* **Luas Area:** ~18.000 Hektar
* **Sektor:** Perkebunan
* **Perusahaan Terlibat:** PTPN II
* **Narasi Kasus:** Konflik panjang antara masyarakat adat/petani dengan PTPN II atas klaim eks-HGU dan kawasan hutan yang tak kunjung diselesaikan, memicu letupan kekerasan dan penggusuran kebun rakyat.
* **Sumber Referensi:** [Catatan KPA & KontraS]

---

<a id="anomali-5"></a>
#### ANOMALI 5: Puncak Krisis Kemanusiaan Tahun 2020 (Sektor Kehutanan)
Tahun 2020 mencatatkan anomali rekor tertinggi secara absolut untuk grafik Korban Terdampak (mencapai lebih dari 134.000 jiwa). Di tengah darurat pandemi COVID-19, pengusiran paksa dan konflik agraria justru tereskalasi dengan tingkat kebrutalan baru:

**1. Konflik PT Wirakarya Sakti (WKS) vs Masyarakat Adat (Jambi)**
* **Total Korban:** > 134.000 Jiwa
* **Sektor:** Kehutanan (Hutan Produksi)
* **Perusahaan Terlibat:** PT. Wirakarya Sakti (WKS)
* **Pemerintah Terlibat:** Polres Tebo, Pemprov Jambi, DPRD Jambi, dan lintas instansi Pemkab.
* **Narasi Kasus:** Konflik historis tak berkesudahan antara PT WKS dan warga sekitar konsesi HTI. Pada April 2020, kontraktor perusahaan secara sadar menerbangkan *drone* dan menyemprotkan cairan racun herbisida dari udara ke lahan warga (Dusun Pelayang Tebat) yang ditanami sawit dan palawija. Metode represi agrikultural udara ini mematikan sumber pangan warga secara instan dan memicu darurat sosial di ratusan ribu warga desa yang menggantungkan hidup pada lahan tersebut.
* **Sumber Referensi:** [Mongabay (WKS Semprot Racun dari Udara)](https://www.mongabay.co.id/2020/05/11/konflik-lahan-berkepanjangan-perusahaan-semprot-racun-dari-udara-ke-kebun-warga/)
""")

st.subheader("4.3 Kriminalisasi Aktivis dan Resistensi Ruang Sipil")
st.markdown('<span style="background:#E53935;color:#FFCDD2;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Analisis Agregat Kasus Represi & Pelanggaran HAM (Sumber: Database Tanah Kita)</span>', unsafe_allow_html=True)

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

Tragedi kemanusiaan ini menjadi semakin kelam dengan hilangnya nyawa **{total_tewas} pejuang lingkungan** yang melayang sia-sia di pusaran konflik agraria. Gugurnya pahlawan-pahlawan ruang hidup ini menggarisbawahi kegagalan mutlak instrumen pengaman ekologis—seperti D3TLH maupun dokumen AMDAL—dalam menjamin keselamatan rakyat. Selama pendekatan pembangunan eksploitatif yang bertumpu pada sekuritisasi investasi ini dipertahankan, setiap hektar hutan yang dibabat akan selalu berlumuran air mata konflik.
""")

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
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

st.markdown(f"""
<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #E53935; margin-bottom: 25px; margin-top: 25px;">
    <b>Interpretasi Ekologis & Hak Asasi Manusia:</b> Tingginya angka kriminalisasi dan korban tewas di sekitar area konsesi (terutama {top_sektor}) membuktikan bahwa perampasan ruang selalu dibarengi dengan pendekatan represif. Ini membantah telak narasi "Hilirisasi Hijau" yang nyatanya ditebus dengan ongkos kemanusiaan yang berdarah.
</div>
""", unsafe_allow_html=True)

st.markdown("#### 🚨 Arsip Kasus Represi dan Kekerasan Fisik Tertinggi")
st.caption("Menampilkan 10 kasus dengan jumlah korban penangkapan atau tewas terbanyak berdasarkan data yang berhasil didokumentasikan.")

df_kekerasan = df_dampak[(df_dampak['jumlah_ditangkap'] > 0) | (df_dampak['jumlah_tewas'] > 0)].sort_values(['jumlah_ditangkap', 'jumlah_tewas'], ascending=[False, False])
df_kekerasan_display = df_kekerasan[['tahun', 'Sektor_Grup', 'keterlibatan_perusahaan', 'jumlah_ditangkap', 'jumlah_tewas', 'deskripsi']].copy()
df_kekerasan_display['keterlibatan_perusahaan'] = df_kekerasan_display['keterlibatan_perusahaan'].fillna('Tidak/Belum Teridentifikasi')
df_kekerasan_display.columns = ['Tahun', 'Sektor', 'Perusahaan Terlibat', 'Ditangkap (Jiwa)', 'Tewas (Jiwa)', 'Narasi Singkat Kejadian']

st.dataframe(df_kekerasan_display.head(10), use_container_width=True, hide_index=True)
