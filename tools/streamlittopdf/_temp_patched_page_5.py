__file__ = r'C:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\pages\5_Pola_Penerbitan_Izin.py'
import streamlit as st
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats
import textwrap

st.set_page_config(page_title="CELIOS ECC", layout="wide")


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
def load_izin_data():
    return pd.read_csv('data/processed/sulawesi_izin_baru_per_tahun.csv')

@st.cache_data
def load_gfw_data():
    return pd.read_csv('data/processed/sulawesi_gfw_master_1_dekade_2014_2023.csv')

df_izin = load_izin_data()
df_gfw = load_gfw_data()

# Kalkulasi Metrik Agregat
total_izin = int(df_izin['Jumlah_Izin_Baru'].sum())
total_luas_konsesi = float(df_izin['Total_Luas_Konsesi_Baru_Ha'].sum())
total_deforestasi = float(df_gfw['Total_Deforestasi_Ha'].sum())

# Metrik tahun puncak penerbitan izin
df_izin_thn = df_izin.groupby('Tahun')['Jumlah_Izin_Baru'].sum().reset_index()
tahun_puncak = int(df_izin_thn.loc[df_izin_thn['Jumlah_Izin_Baru'].idxmax(), 'Tahun']) if not df_izin_thn.empty else 0
izin_puncak = int(df_izin_thn['Jumlah_Izin_Baru'].max()) if not df_izin_thn.empty else 0

# Kalkulasi Metrik Agregat Baru (Bento Cards - Insight Kritis)
df_panel_bento = pd.merge(df_gfw, df_izin, on=['Provinsi', 'Tahun'], how='left').fillna({'Jumlah_Izin_Baru': 0})
med_def = df_panel_bento['Total_Deforestasi_Ha'].median()
df_panel_bento['is_kritis'] = df_panel_bento['Total_Deforestasi_Ha'] > med_def

izin_kritis = int(df_panel_bento[df_panel_bento['is_kritis']]['Jumlah_Izin_Baru'].sum())
izin_total = int(df_panel_bento['Jumlah_Izin_Baru'].sum())
pct_kritis = (izin_kritis / izin_total * 100) if izin_total > 0 else 0

kritis_prov = df_panel_bento[df_panel_bento['is_kritis']].groupby('Provinsi')['Jumlah_Izin_Baru'].sum().reset_index()
top_prov_kritis = kritis_prov.loc[kritis_prov['Jumlah_Izin_Baru'].idxmax()]
nama_prov_kritis = top_prov_kritis['Provinsi']
jumlah_prov_kritis = int(top_prov_kritis['Jumlah_Izin_Baru'])

izin_pra_2020 = int(df_izin[df_izin['Tahun'] < 2020]['Jumlah_Izin_Baru'].sum())
izin_pasca_2020 = int(df_izin[df_izin['Tahun'] >= 2020]['Jumlah_Izin_Baru'].sum())
rasio_akselerasi = (izin_pasca_2020 / izin_pra_2020) if izin_pra_2020 > 0 else 0

# ---------------------------------------------------------
# HERO SECTION (EXECUTIVE SUMMARY)
# ---------------------------------------------------------
st.markdown('<div class="org-badge">CELIOS — Center of Economic and Law Studies</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">Pola Penerbitan Izin di Zona Kritis Ekologis</h1>', unsafe_allow_html=True)

# Bento Cards untuk Fakta Kritis D3TLH
st.markdown("<br>", unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    st.markdown("""
    <div style="background:#1A1A1A; padding: 20px; border-radius: 10px; border-top: 4px solid #E74C3C; height: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
        <div style="font-size:0.8rem; color:#E74C3C; font-weight:bold; letter-spacing:1px; margin-bottom:10px;">FAKTA CRI, MIGHTY EARTH, TANAHKITA.ID</div>
        <div style="color: #fff; font-size: 1.3rem; font-weight:bold; margin-bottom:12px; line-height:1.3;">Mayoritas IUP Tanpa FPIC</div>
        <div style="color:#B0BEC5; font-size:0.9rem; line-height:1.5;">
            Laporan Climate Rights International, Mighty Earth, dan Business-Human Rights Resource Centre mendokumentasikan banyak IUP tambang nikel di Sulawesi terbit <b>tanpa <i>Free, Prior, and Informed Consent</i> (FPIC)</b> dari masyarakat adat. Dokumen AMDAL kerap disusun <b>tanpa konsultasi bermakna</b> dan pelibatan masyarakat yang ruang hidupnya dirampas.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div style="background:#1A1A1A; padding: 20px; border-radius: 10px; border-top: 4px solid #F39C12; height: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
        <div style="font-size:0.8rem; color:#F39C12; font-weight:bold; letter-spacing:1px; margin-bottom:10px;">DATA BPS (SLHI)</div>
        <div style="color: #fff; font-size: 1.3rem; font-weight:bold; margin-bottom:12px; line-height:1.3;">Krisis Kualitas Air (IKA) di Bawah 55</div>
        <div style="color:#B0BEC5; font-size:0.9rem; line-height:1.5;">
            Indeks Kualitas Air (IKA) di sentra nikel seperti Sultra dan Sulteng konsisten terpuruk di level cemaran berat (46-55). Sedimentasi lumpur tambang laut menghancurkan terumbu karang dan mengusir wilayah tangkap nelayan sejauh puluhan mil.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<p class="sub-title">Evaluasi instrumen tata kelola lingkungan dan dinamika penerbitan perizinan tambang di kawasan industri.</p>', unsafe_allow_html=True)

with st.expander("Metodologi Pendekatan", expanded=False):
    st.markdown("""
    **Kerangka Logis (Alur Kausalitas):**
    Bagian ini dirancang untuk menjawab sub-pertanyaan kritis dalam studi D3TLH: *"Apakah izin baru tetap diterbitkan ketika tekanan ekologis sudah tinggi?"*
    
    1. **Variabel Dependen (Y):** Jumlah penerbitan izin tambang baru per tahun.
    2. **Variabel Konteks (X):** Status kritis ekologis (diukur dari laju deforestasi dan kerusakan eksisting).
    3. **Pendekatan Metodologis:** *Timeline Mapping* dan *Crosstabulation* untuk melihat tumpang tindih (*overlay*) temporal antara memburuknya kualitas lingkungan dengan grafik penerbitan izin.
    
    **Tujuan:**
    Membuktikan secara empiris terjadinya kegagalan tata kelola (governance failure) di mana instrumen Daya Dukung dan Daya Tampung Lingkungan Hidup (D3TLH) tidak bersifat mengikat (non-mandatory) dan mudah diabaikan demi melancarkan investasi.
    """)

# Hero Statement
st.markdown(f"""
Dokumen tata ruang dan instrumen lingkungan hidup berfungsi sebagai pedoman pengendalian perizinan investasi di bentang alam berdasarkan kapasitas daya dukung lingkungan. Penelusuran data spasial dan temporal di Sulawesi menunjukkan dinamika penerbitan izin dan perubahan tutupan hutan. Selama satu dekade terakhir, total deforestasi tercatat sebesar **{total_deforestasi:,.1f} hektar**, sementara penerbitan **{total_izin:,} izin tambang baru** mencakup luas konsesi **{total_luas_konsesi:,.1f} hektar**. Puncak penerbitan izin tercatat pada tahun **{tahun_puncak}** ({izin_puncak} izin), mengindikasikan perlunya penguatan implementasi D3TLH dalam proses pengambilan keputusan perizinan.
""")

st.markdown("<br>", unsafe_allow_html=True)

# Bento Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">PERIZINAN DI ERA DEFORESTASI KRITIS</div>
            <div class="metric-value" style="color: #B71C1C;">{pct_kritis:.1f}% <span style="font-size:1rem;color:#777;">({izin_kritis} IUP)</span></div>
            <div class="metric-desc">Proporsi izin baru yang terbit pada tahun-tahun di mana laju deforestasi provinsi berada di atas rata-rata median.</div>
        </div>
        <div class="metric-source">Sumber: Data Panel (ESDM & GFW)<br>File: sulawesi_izin_baru_per_tahun.csv</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">PROVINSI DENGAN PENERBITAN IZIN TINGGI</div>
            <div class="metric-value" style="color: #C62828;">{nama_prov_kritis} <span style="font-size:1rem;color:#777;">({jumlah_prov_kritis} IUP)</span></div>
            <div class="metric-desc">Provinsi dengan catatan penerbitan izin tertinggi pada periode laju deforestasi yang relatif tinggi.</div>
        </div>
        <div class="metric-source">Sumber: Data Panel (ESDM & GFW)<br>File: sulawesi_izin_baru_per_tahun.csv</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">PERBANDINGAN IZIN PASCA-2020</div>
            <div class="metric-value" style="color: #D32F2F;">{rasio_akselerasi:.1f}x <span style="font-size:1rem;color:#777;">Lipat</span></div>
            <div class="metric-desc">Rasio perbandingan penerbitan izin baru pada era pasca-2020 dibandingkan periode sebelumnya.</div>
        </div>
        <div class="metric-source">Sumber: Kementerian ESDM (Minerbaone)<br>File: sulawesi_izin_baru_per_tahun.csv</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><hr style='border: 1px dashed #333;'><br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# PLACEHOLDERS
# ---------------------------------------------------------

st.subheader("5.1 Fakta Penyebab: Sinkronisasi Waktu (Timeline Mapping)")
st.markdown('<span style="background:#5C2B6A;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Gantt Chart Timeline (Plotly Express)</span>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("ℹ️ Metodologi: Sinkronisasi Waktu (Timeline Mapping)"):
    st.markdown("""
    **Metode Analisis:** Sub-bab ini menggunakan visualisasi deret waktu bersilang (*Dual-Axis Combo Chart*) untuk mendeteksi korelasi visual temporal.

    1. **Model Komparasi Temporal:**
        * **Time-Series Tracking:** Mengkomparasikan secara bersamaan akumulasi hilangnya luasan hutan (deforestasi) dengan laju obral perizinan pertambangan baru dari tahun 2014-2023.
        * **Pemetaan Anomali (*Governance Failure*):** Melacak secara empiris apakah instrumen 'rem darurat' ekologis bekerja. Jika kurva perizinan terus melesat naik tepat di tahun saat grafik deforestasi menembus batas krisis, maka terjadi pengabaian tata ruang yang disengaja.
    2. **Kalkulasi/Formula Pengolahan:**
        * `Total_Deforestasi_Tahunan = SUM(Luas_Hilang_Ha) GROUP BY Tahun`
        * `Total_IUP_Baru = COUNT(Izin) GROUP BY Tahun`
    3. **Variabel & Fitur Data:**
        * **X-Axis (Waktu):** `Tahun` (2014-2023)
        * **Y-Axis Kiri (Dampak Ekologis):** `Total_Deforestasi_Ha`
        * **Y-Axis Kanan (Keputusan Aktor):** `Jumlah_Izin_Baru`
    4. **Dataset & File:**
        * `data/processed/sulawesi_izin_baru_per_tahun.csv` (Minerbaone)
        * `data/processed/sulawesi_gfw_master_1_dekade_2014_2023.csv` (GFW)
    """)



import plotly.graph_objects as go

# Data Prep for Time-Series Dual-Axis Line Chart
df_izin_thn = df_izin.groupby('Tahun')[['Jumlah_Izin_Baru', 'Total_Luas_Konsesi_Baru_Ha']].sum().reset_index()
df_gfw_thn = df_gfw.groupby('Tahun')['Total_Deforestasi_Ha'].sum().reset_index()
df_timeline = pd.merge(df_gfw_thn, df_izin_thn, on='Tahun', how='outer').fillna(0).sort_values('Tahun')
df_timeline = df_timeline[df_timeline['Tahun'] <= 2023] # Filter out 2024 karena data GFW mentok di 2023

from plotly.subplots import make_subplots

st.markdown("""
<div style="text-align: justify; line-height: 1.8; color: #E0E0E0; font-size: 1.05rem; margin-bottom: 25px;">
Visualisasi <i>Dual-Axis Combo Chart</i> di bawah ini menggambarkan pergeseran tren penerbitan perizinan dan laju deforestasi. Penelusuran data historis menunjukkan dua fase utama. Pada <b>Fase 2014-2018 (Zona Kiri)</b>, deforestasi didominasi oleh peruntukan perkebunan dan Hak Pengusahaan Hutan (HPH). Pada periode tersebut, luas konsesi pertambangan baru masih relatif terbatas.
<br><br>
Memasuki <b>Era Pasca-2019 (Zona Kanan)</b>, penerbitan izin industri pertambangan mengalami peningkatan. Kurva kuning (Area Konsesi IUP Baru) meningkat beriringan dengan dinamika perubahan tutupan hutan. Pasca-2020, luas konsesi tambang mencatatkan angka yang signifikan pada periode deforestasi yang juga meningkat.
<br><br>
Data ini menunjukkan pentingnya penguatan efektivitas instrumen Daya Dukung dan Daya Tampung Lingkungan Hidup (D3TLH) serta analisis AMDAL agar berfungsi sebagai pertimbangan utama dalam proses perizinan investasi, guna mencegah tekanan lingkungan berlebih di wilayah penyangga.
</div>
""", unsafe_allow_html=True)

# Checkbox for Time-Lag Assumption
st.markdown("<br>", unsafe_allow_html=True)
use_timelag = st.checkbox("Aktifkan Simulasi Time-Lag Deforestasi (T+1 Tahun)", help="Menggeser mundur kurva deforestasi 1 tahun untuk mensimulasikan jeda waktu antara penerbitan izin dan realisasi pembabatan hutan di lapangan.")

if use_timelag:
    # Shift deforestasi mundur 1 tahun (Deforestasi tahun T+1 ditarik ke tahun T)
    df_timeline['Total_Deforestasi_Ha_Plotted'] = df_timeline['Total_Deforestasi_Ha'].shift(-1)
    df_timeline = df_timeline.dropna(subset=['Total_Deforestasi_Ha_Plotted']) # Hapus tahun terakhir yg jadi NaN
    
    st.markdown("""
    <div style="background:rgba(231, 76, 60, 0.1);padding:15px;border-left:3px solid #E74C3C;border-radius:5px;font-size:0.95rem;margin-bottom:20px;">
        <b>Studi Kasus & Justifikasi Time-Lag:</b><br>
        Setelah korelasi digeser (time-lag 1 tahun), lonjakan obral <b>56 IUP baru dengan luas konsesi mencapai 66.000 Hektar pada tahun 2022</b> kini terlihat secara langsung memicu <b>rekor puncak deforestasi sebesar 255.000 Hektar pada tahun 2023</b>.<br><br>
        Jeda waktu ini secara empiris sangat rasional. Dalam siklus eksploitasi industri nikel (seperti eskalasi ekspansi smelter di Blok Bahodopi atau blok tambang di Morowali/Kolaka), penerbitan perizinan dan penyerahan konsesi lahan di atas kertas (Tahun T) akan selalu diikuti oleh fase mobilisasi logistik, penetrasi alat berat, dan konflik lahan yang memakan waktu berbulan-bulan sebelum aktivitas <i>land clearing</i> masif akhirnya terpotret secara fatal oleh citra satelit pada tahun berikutnya (T+1).
    </div>
    """, unsafe_allow_html=True)
else:
    df_timeline['Total_Deforestasi_Ha_Plotted'] = df_timeline['Total_Deforestasi_Ha']

# Render Combo Chart (Bar + Line) Dual Axis
fig_timeline = make_subplots(specs=[[{'secondary_y': True}]])

# 1. Bar Chart: Deforestasi (Sumbu Y Kiri)
fig_timeline.add_trace(
    go.Bar(
        x=df_timeline['Tahun'], 
        y=df_timeline['Total_Deforestasi_Ha_Plotted'], 
        name='Total Deforestasi (Hektar)', 
        marker_color='rgba(231, 76, 60, 0.7)', # Merah transparan
        marker_line_color='#C0392B',
        marker_line_width=1.5,
        text=df_timeline['Total_Deforestasi_Ha_Plotted'].apply(lambda x: f"{int(x):,} Ha"),
        textposition='auto',
        textfont=dict(color='black', size=11),
        hovertemplate="<b>Tahun %{x}</b><br>Deforestasi: %{y:,.0f} Ha<extra></extra>" if not use_timelag else "<b>Tahun Izin: %{x} (Deforestasi Tahun %{customdata})</b><br>Deforestasi: %{y:,.0f} Ha<extra></extra>",
        customdata=(df_timeline['Tahun'] + 1) if use_timelag else None
    ),
    secondary_y=False,
)

# 2. Line Chart: Izin Baru (Sumbu Y Kanan)
fig_timeline.add_trace(
    go.Scatter(
        x=df_timeline['Tahun'], 
        y=df_timeline['Total_Luas_Konsesi_Baru_Ha'], 
        name='Area Konsesi IUP (Hektar)', 
        mode='lines+markers+text',
        text=[f"{int(luas/1000)}k ({int(iup)} IUP)" if luas > 0 else "0" for luas, iup in zip(df_timeline['Total_Luas_Konsesi_Baru_Ha'], df_timeline['Jumlah_Izin_Baru'])],
        textposition='top center',
        textfont=dict(color='#F1C40F', size=11, weight='bold'),
        line=dict(color='#F1C40F', width=3),
        marker=dict(symbol='circle', size=10, color='#F1C40F', line=dict(color='#FFFFFF', width=2)),
        hovertemplate="<b>Tahun %{x}</b><br>Area Konsesi: %{y:,.0f} Ha<br>Jumlah Surat: %{customdata} IUP<extra></extra>",
        customdata=df_timeline['Jumlah_Izin_Baru']
    ),
    secondary_y=True,
)

fig_timeline.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    hovermode='x unified',
    height=500,
    margin=dict(l=0, r=20, t=10, b=40),
    xaxis=dict(
        tickformat="%Y",
        dtick="M12",
        showgrid=False,
    ),
    legend=dict(
        orientation="h", 
        yanchor="bottom", 
        y=1.05, 
        xanchor="center", 
        x=0.5,
        title=""
    )
)

fig_timeline.add_vrect(x0=2013.5, x1=2018.5, fillcolor="rgba(149, 165, 166, 0.1)", layer="below", line_width=0, annotation_text="<b>Era Ekspansi<br>Sawit & HPH</b>", annotation_position="top left", annotation_font_color="#7F8C8D")
fig_timeline.add_vrect(x0=2018.5, x1=2023.5, fillcolor="rgba(231, 76, 60, 0.05)", layer="below", line_width=0, annotation_text="<b>Era Hilirisasi<br>Nikel (Krisis)</b>", annotation_position="top left", annotation_font_color="#E74C3C")

fig_timeline.update_yaxes(title_text='Deforestasi (Hektar)', secondary_y=False, showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#E74C3C')
fig_timeline.update_yaxes(title_text='Area Konsesi (Hektar)', secondary_y=True, showgrid=False, color='#F1C40F')

st.markdown("<h4 style='margin-bottom: 10px;'>Tren Eskalasi Bersamaan: Kerusakan Hutan (Batang) vs Penerbitan Izin (Garis)</h4>", unsafe_allow_html=True)
st.plotly_chart(fig_timeline, use_container_width=True, config={'displayModeBar': False})

# Interpretation Box Ringkas (Sesuai gaya Page 4)
st.markdown("""
<div style="background:#FFFFFF; padding:15px 20px; border-radius:8px; border-left:4px solid #F57C00; margin-top: 10px; margin-bottom: 25px;">
    <span style="color: #E0E0E0; font-size: 0.95rem;">
        <b style="color:#F57C00;">Interpretasi Evaluasi Perizinan:</b> Data tren historis mengindikasikan perlunya integrasi instrumen D3TLH secara lebih mengikat dalam pertimbangan izin usaha pertambangan.
    </span>
</div>
""", unsafe_allow_html=True)

with st.expander("Lihat Data Mentah: Agregasi Waktu Historis", expanded=False):
    # Format data untuk tabel
    df_tabel = df_timeline.copy()
    df_tabel['Tahun'] = df_tabel['Tahun'].astype(int).astype(str)
    df_tabel['Total_Deforestasi_Ha'] = df_tabel['Total_Deforestasi_Ha'].apply(lambda x: f"{x:,.0f}")
    df_tabel['Jumlah_Izin_Baru'] = df_tabel['Jumlah_Izin_Baru'].astype(int)
    
    st.dataframe(df_tabel, use_container_width=True, hide_index=True)
    st.caption("**Sumber File:** Agregasi dari `sulawesi_izin_baru_per_tahun.csv` (Minerbaone) & `sulawesi_gfw_master_1_dekade_2014_2023.csv` (GFW).")

st.markdown("---")

st.subheader("5.2 Fakta Spasial: Tabrakan Tata Ruang di Kawasan Konservasi")
st.markdown('<span style="background:#5C2B6A;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Overlay Area Kawasan Lindung (GFW)</span>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("ℹ️ Metodologi: Analisis Spasial Tabrakan Tata Ruang"):
    st.markdown("""
    **Metode Analisis:** Sub-bab ini menggunakan agregasi spasial bertingkat (*Stacked Bar Chart*) untuk mendokumentasikan skala kehancuran mutlak pada wilayah yang diharamkan untuk ditambang.

    1. **Model Analisis Deforestasi Livelihood:**
        * **Geospatial Overlay:** Melakukan isolasi data *tree cover loss* (GFW) yang secara spesifik bertumpukan/beririsan dengan poligon Kawasan Livelihood (Zona Pertanian, Peternakan) dan Perkebunan Warga.
        * **Kuantifikasi Kerusakan Kumulatif:** Mengkalkulasi kehancuran agregat kawasan penyangga ekosistem esensial selama satu dekade terakhir akibat penetrasi aktivitas tambang.
    2. **Kalkulasi/Formula Pengolahan:**
        * `Luas_Hancur_Perkebunan_Warga = SUM(Loss_Ha) WHERE Cat = '2'`
        * `Luas_Hancur_Pertanian_Peternakan = SUM(Loss_Ha) WHERE Cat = '1'`
        * `Total_Kumulatif_Hancur(t) = Total_Kumulatif_Hancur(t-1) + Luas_Hancur(t)`
    3. **Variabel & Fitur Data:**
        * **Kategorisasi Spasial (X):** `Tahun`, Kategori Livelihood
        * **Besaran Destruksi (Y):** `Luas_Hilang_Kawasan_Livelihood_Ha`
    4. **Dataset & File:**
        * `data/processed/sulawesi_gfw_kawasan_lindung_loss_2014_2023.csv`
    """)



st.markdown("""
Dataset spasial menunjukkan pentingnya kepatuhan terhadap batas-batas tata ruang. Kawasan penyangga kehidupan (Hutan Produksi, Kawasan Lindung, dan Area Resapan Air) memerlukan pengawasan agar fungsi ekologisnya tetap terjaga di tengah ekspansi pertambangan.
""")

try:
    df_kawasan = pd.read_csv('data/processed/sulawesi_gfw_kawasan_lindung_loss_2014_2023.csv')
    df_kawasan = df_kawasan[(df_kawasan['wdpa_protected_areas__iucn_cat'].astype(str) != '0') & (df_kawasan['Tahun'] <= 2023)]
    
    # Pivot untuk Stacked Bar Chart
    df_pivot_chart = pd.pivot_table(
        df_kawasan, 
        values='Luas_Hilang_Kawasan_Lindung_Ha', 
        index='Tahun', 
        columns='wdpa_protected_areas__iucn_cat', 
        aggfunc='sum',
        fill_value=0
    ).reset_index()

    # Hitung nilai kumulatif (karena hutan yang hilang tidak kembali, kerusakannya permanen)
    if 1 in df_pivot_chart.columns:
        df_pivot_chart[1] = df_pivot_chart[1].cumsum()
    if 2 in df_pivot_chart.columns:
        df_pivot_chart[2] = df_pivot_chart[2].cumsum()
        
    df_pivot_chart['Total'] = df_pivot_chart.get(1, 0) + df_pivot_chart.get(2, 0)

    fig_kawasan = go.Figure()
    
    # Pertanian/Peternakan Warga (Cat 1)
    if 1 in df_pivot_chart.columns:
        fig_kawasan.add_trace(go.Bar(
            x=df_pivot_chart['Tahun'],
            y=df_pivot_chart[1],
            name='Zona Pertanian & Peternakan',
            marker_color='#E74C3C',
            text=[f"{v/1000:,.1f}k" if v > 0 else "" for v in df_pivot_chart[1]],
            textposition='outside',
            textfont=dict(color='#E74C3C', size=11),
            hovertemplate="<b>Hingga Tahun %{x}</b><br>Total Pertanian/Peternakan Hancur: %{y:,.0f} Ha<extra></extra>"
        ))
        
    # Perkebunan Warga (Cat 2)
    if 2 in df_pivot_chart.columns:
        fig_kawasan.add_trace(go.Bar(
            x=df_pivot_chart['Tahun'],
            y=df_pivot_chart[2],
            name='Perkebunan Warga',
            marker_color='#F39C12',
            text=[f"{v/1000:,.1f}k" if v > 0 else "" for v in df_pivot_chart[2]],
            textposition='outside',
            textfont=dict(color='#F39C12', size=11),
            hovertemplate="<b>Hingga Tahun %{x}</b><br>Total Perkebunan Hancur: %{y:,.0f} Ha<extra></extra>"
        ))
        
    # Hitung dan Tampilkan Garis Total
    df_pivot_chart['Total'] = df_pivot_chart.get(1, 0) + df_pivot_chart.get(2, 0)
    fig_kawasan.add_trace(go.Scatter(
        x=df_pivot_chart['Tahun'],
        y=df_pivot_chart['Total'],
        name='Total Kehancuran Kumulatif',
        mode='lines+markers+text',
        text=[f"Total: {v/1000:,.1f}k" for v in df_pivot_chart['Total']],
        textposition='top center',
        textfont=dict(color='black', size=11, weight='bold'),
        line=dict(color='black', width=2, dash='dot'),
        marker=dict(size=7, color='black'),
        hovertemplate="<b>Hingga Tahun %{x}</b><br>Total Area Hancur: %{y:,.0f} Ha<extra></extra>"
    ))

    fig_kawasan.update_layout(
        title=None,
        barmode='stack',
        template='plotly_dark',
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(title='Tahun', tickmode='linear', dtick=1, showgrid=False),
        yaxis=dict(title='Luas Area Hancur (Hektar)', showgrid=True, gridcolor='#333'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='x unified',
        height=550,
        margin=dict(l=0, r=0, t=50, b=0)
    )

    st.markdown("<h4 style='margin-bottom: 10px;'>Akumulasi Kehancuran Total: Livelihood Warga (Pertanian, Peternakan, Perkebunan) 2014-2023</h4>", unsafe_allow_html=True)
    st.plotly_chart(fig_kawasan, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("""
    <div style="background:#FFFFFF; padding:15px 20px; border-radius:8px; border-left:4px solid #3498DB; margin-top: 10px; margin-bottom: 25px;">
        <span style="color: #E0E0E0; font-size: 0.95rem;">
            <b style="color:#3498DB;">Fakta Spasial:</b> Dalam dekade terakhir, total lebih dari <b>56 ribu hektar</b> kawasan livelihood (Pertanian, Peternakan, dan Perkebunan) warga tercatat mengalami perubahan tutupan lahan yang beririsan dengan dinamika industri ekstraktif.
        </span>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Lihat Data Mentah: Rincian Kawasan Livelihood", expanded=False):
        # Buat Pivot Table agar kolomnya lebih kaya dan informatif
        df_pivot = pd.pivot_table(
            df_kawasan, 
            values='Luas_Hilang_Kawasan_Lindung_Ha', 
            index='Tahun', 
            columns='wdpa_protected_areas__iucn_cat', 
            aggfunc='sum',
            fill_value=0
        ).reset_index()
        
        # Rename kolom sesuai kategori IUCN di Indonesia
        df_pivot = df_pivot.rename(columns={
            1: "Pertanian & Peternakan (Ha)", 
            2: "Perkebunan Warga (Ha)"
        })
        
        # Tambahkan kolom Total
        df_pivot['Total Kehancuran (Ha)'] = df_pivot.get("Pertanian & Peternakan (Ha)", 0) + df_pivot.get("Perkebunan Warga (Ha)", 0)
        df_pivot['Tahun'] = df_pivot['Tahun'].astype(int).astype(str)
        
        # Formatting angka
        for col in ["Pertanian & Peternakan (Ha)", "Perkebunan Warga (Ha)", "Total Kehancuran (Ha)"]:
            if col in df_pivot.columns:
                df_pivot[col] = df_pivot[col].apply(lambda x: f"{x:,.2f}")
            
        st.dataframe(df_pivot, use_container_width=True, hide_index=True)
        st.caption("**Sumber File:** `sulawesi_gfw_kawasan_lindung_loss_2014_2023.csv` (GFW dengan overlay Livelihood Zone Proxy Kategori 1 & 2).")

except Exception as e:
    st.error(f"Gagal memuat visualisasi kawasan livelihood: {e}")

st.markdown("---")

st.subheader("5.3 Realitas Lapangan: Izin Bermasalah, FPIC Diabaikan, Masyarakat Dikorbankan")
st.markdown('<span style="background:#5C2B6A;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Cross-Dataset Integration (KPA CATAHU + Tanahkita + CRI/Mighty Earth Reports)</span>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("ℹ️ Metodologi: Ekstraksi Data Konflik Agraria & Pelanggaran HAM"):
    st.markdown("""
    **Metode Analisis:** Sub-bab ini menggunakan triangulasi data kualitatif-kuantitatif dengan mendemonstrasikan integrasi *database* konflik agraria (*Multi-source Database Profiling*).

    1. **Pemodelan Indikator Pelanggaran FPIC:**
        * **Cross-Referencing:** Memadukan repositori konflik terbuka (KPA & Tanahkita.id) dengan laporan independen lembaga HAM global (CRI, Mighty Earth, BHRRC) untuk membongkar anomali perizinan (*non-compliance*).
        * **Kuantifikasi Kriminalisasi:** Menghitung jumlah perampasan lahan tanpa persetujuan warga (Pelanggaran *Free, Prior, Informed Consent*/FPIC), tumpang tindih HGU, dan letupan represi bersenjata.
    2. **Kalkulasi/Formula Pengolahan:**
        * `Total_Pelanggaran_FPIC = COUNT(Kasus) WHERE indikasi_fpic = True`
        * `Rekam_Jejak_Oligarki = COUNT(Jenis_Masalah_Izin) GROUP BY nama_perusahaan`
    3. **Variabel & Fitur Data:**
        * **Kategori Entitas:** `nama_perusahaan`, `provinsi`, `jenis_masalah_izin`, `indikasi_fpic`
        * **Besaran Kasus:** `luas_ha`, Frekuensi kemunculan konflik.
    4. **Dataset & File:**
        * `data/processed/sulawesi_konflik_tambang_fpic.csv`
        * `data/processed/kpa_masalah_izin_perusahaan.csv`
    """)



st.markdown("""
<div style="text-align: justify; line-height: 1.8; color: #E0E0E0; font-size: 1.05rem; margin-bottom: 25px;">
Laporan dari <b>Climate Rights International (2024-2025)</b>, <b>Mighty Earth (2024)</b>, dan <b>Business & Human Rights Resource Centre</b> mendokumentasikan isu tata kelola perizinan dan pelaksanaan konsultasi publik (FPIC - <i>Free, Prior, and Informed Consent</i>) di sekitar kawasan industri nikel. Kajian-kajian tersebut menyoroti pentingnya keterlibatan masyarakat lokal dan transparansi dokumen AMDAL serta D3TLH agar proses perizinan berjalan inklusif dan akuntabel.
<br><br>
Penelusuran terhadap <b>database Konsorsium Pembaruan Agraria (KPA) CATAHU 2016-2025</b> dan <b>Tanahkita.id</b> mengidentifikasi <b>21 kasus permasalahan izin perusahaan</b>, termasuk terkait status HGU, alokasi kawasan hutan, dan penanganan klaim lahan masyarakat. Di Sulawesi, tercatat <b>12 kasus konflik pertambangan</b> dengan <b>4 kasus yang mencatatkan indikasi isu pelaksanaan FPIC</b>.
<br><br>
Data ini menggarisbawahi perlunya penguatan sistem evaluasi perizinan, pemantauan hukum secara berkala, dan penghormatan terhadap hak-hak komunitas lokal dalam setiap tahapan investasi ekstraktif.
</div>
""", unsafe_allow_html=True)

# Load datasets
@st.cache_data
def load_konflik_data():
    return pd.read_csv('data/processed/sulawesi_konflik_tambang_fpic.csv')

@st.cache_data
def load_masalah_izin_data():
    return pd.read_csv('data/processed/kpa_masalah_izin_perusahaan.csv')

df_konflik = load_konflik_data()
df_masalah = load_masalah_izin_data()

# Calculate metrics
total_konflik = len(df_konflik)
konflik_fpic = df_konflik['indikasi_fpic'].sum()
total_masalah_izin = len(df_masalah)
perusahaan_masalah_sulawesi = df_masalah[df_masalah['lokasi'].str.contains('Sulawesi', case=False, na=False)]['nama_perusahaan'].nunique()

# Bento Cards untuk Key Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">KONFLIK PERTAMBANGAN SULAWESI</div>
            <div class="metric-value" style="color: #B71C1C;">{total_konflik} <span style="font-size:1rem;color:#777;">Kasus</span></div>
            <div class="metric-desc">Total konflik pertambangan terdokumentasi di Sulawesi (1968-2023) dengan <b>{konflik_fpic} kasus pelanggaran FPIC eksplisit</b> yang melibatkan kekerasan, kriminalisasi, dan penggusuran paksa.</div>
        </div>
        <div class="metric-source">Sumber: Tanahkita.id (KPA/YLBHI)<br>File: sulawesi_konflik_tambang_fpic.csv</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">PERUSAHAAN IZIN BERMASALAH</div>
            <div class="metric-value" style="color: #F4511E;">{total_masalah_izin} <span style="font-size:1rem;color:#777;">Kasus</span></div>
            <div class="metric-desc">Kasus masalah izin perusahaan yang teridentifikasi dalam CATAHU KPA (2016-2025): HGU kadaluarsa, operasi ilegal, IUP bermasalah, dan tumpang tindih klaim lahan.</div>
        </div>
        <div class="metric-source">Sumber: KPA CATAHU 2016-2025<br>File: kpa_masalah_izin_perusahaan.csv</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">PERUSAHAAN BERMASALAH DI SULAWESI</div>
            <div class="metric-value" style="color: #FF8A65;">{perusahaan_masalah_sulawesi} <span style="font-size:1rem;color:#777;">Perusahaan</span></div>
            <div class="metric-desc">Perusahaan unik yang disebutkan dalam laporan KPA dengan lokasi operasi di Sulawesi, mayoritas terlibat dalam kasus tumpang tindih lahan dan HGU kadaluarsa.</div>
        </div>
        <div class="metric-source">Sumber: KPA CATAHU 2016-2025<br>File: kpa_masalah_izin_perusahaan.csv</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---- VISUALIZATION 1: Timeline Konflik & Masalah Izin ----
st.markdown("#### Timeline Historis: Konflik Pertambangan & Masalah Izin (2000-2025)")

# Prepare timeline data
df_konflik_timeline = df_konflik.copy()
df_konflik_timeline['kategori'] = 'Konflik Pertambangan'
df_konflik_timeline = df_konflik_timeline.rename(columns={'tahun': 'Tahun', 'judul': 'Keterangan'})
df_konflik_timeline['Keterangan'] = df_konflik_timeline['Keterangan'].str[:80] + '...'

df_masalah_timeline = df_masalah[df_masalah['lokasi'].str.contains('Sulawesi', case=False, na=False)].copy()
df_masalah_timeline['kategori'] = 'Masalah Izin (KPA)'
df_masalah_timeline['Tahun'] = df_masalah_timeline['tahun_laporan'].astype(int)
df_masalah_timeline['Keterangan'] = df_masalah_timeline['nama_perusahaan'] + ' - ' + df_masalah_timeline['jenis_masalah_izin']

# Combine
df_combined_timeline = pd.concat([
    df_konflik_timeline[['Tahun', 'kategori', 'Keterangan']],
    df_masalah_timeline[['Tahun', 'kategori', 'Keterangan']]
], ignore_index=True).sort_values('Tahun')

# Filter tahun 2000 ke atas sesuai permintaan
df_combined_timeline = df_combined_timeline[df_combined_timeline['Tahun'] >= 2000]

# Count by year and category
df_timeline_agg = df_combined_timeline.groupby(['Tahun', 'kategori']).size().reset_index(name='Jumlah')

fig_timeline_konflik = px.bar(
    df_timeline_agg,
    x='Tahun',
    y='Jumlah',
    color='kategori',
    barmode='group',
    color_discrete_map={
        'Konflik Pertambangan': '#E74C3C',
        'Masalah Izin (KPA)': '#F39C12'
    },
    title='Distribusi Temporal: Konflik Pertambangan vs Masalah Izin Perusahaan',
    labels={'Jumlah': 'Jumlah Kasus', 'Tahun': 'Tahun'},
    text='Jumlah'
)

fig_timeline_konflik.update_traces(textposition='outside', textfont_size=11)
fig_timeline_konflik.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    height=450,
    hovermode='x unified',
    xaxis=dict(tickmode='linear', tick0=1968, dtick=5, showgrid=False),
    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
    legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5, title="")
)

st.plotly_chart(fig_timeline_konflik, use_container_width=True, config={'displayModeBar': False})

st.markdown("""
<div style="background:#FFFFFF; padding:15px 20px; border-radius:8px; border-left:4px solid #E74C3C; margin-top: 10px; margin-bottom: 25px;">
    <span style="color: #E0E0E0; font-size: 0.95rem;">
        <b style="color:#E74C3C;">Temuan Kunci:</b> Peningkatan catatan konflik pertambangan pada periode 2011-2023 beriringan dengan ekspansi industri nikel di Sulawesi. Laporan mendokumentasikan isu terkait kepatuhan perizinan dan penerapan FPIC yang memerlukan perhatian tata kelola.
    </span>
</div>
""", unsafe_allow_html=True)

# ---- VISUALIZATION 2: Jenis Masalah Izin (Breakdown) ----
st.markdown("#### Breakdown Jenis Masalah Izin Perusahaan")

# Parse jenis_masalah_izin (bisa multiple, dipisah dengan semicolon)
masalah_list = []
for _, row in df_masalah.iterrows():
    masalah_str = str(row['jenis_masalah_izin'])
    for m in masalah_str.split(';'):
        masalah_list.append({
            'Jenis Masalah': m.strip(),
            'Tahun': row['tahun_laporan'],
            'Perusahaan': row['nama_perusahaan']
        })

df_masalah_breakdown = pd.DataFrame(masalah_list)
df_masalah_count = df_masalah_breakdown.groupby('Jenis Masalah').size().reset_index(name='Jumlah Kasus').sort_values('Jumlah Kasus', ascending=True)

fig_masalah = px.bar(
    df_masalah_count,
    x='Jumlah Kasus',
    y='Jenis Masalah',
    orientation='h',
    title='Jenis Masalah Izin yang Paling Sering Terjadi (KPA CATAHU 2016-2025)',
    text='Jumlah Kasus',
    color='Jumlah Kasus',
    color_continuous_scale='Reds'
)

fig_masalah.update_traces(textposition='outside', textfont_size=12)
fig_masalah.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    height=400,
    showlegend=False,
    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
    yaxis=dict(showgrid=False)
)

st.plotly_chart(fig_masalah, use_container_width=True, config={'displayModeBar': False})

st.markdown("""
<div style="background:#FFFFFF; padding:15px 20px; border-radius:8px; border-left:4px solid #F39C12; margin-top: 10px; margin-bottom: 25px;">
    <span style="color: #E0E0E0; font-size: 0.95rem;">
        <b style="color:#F39C12;">Pola Isu Dominan:</b> Sengketa klaim lahan dan penataan HGU merupakan isu yang terbanyak diidentifikasi, mengindikasikan pentingnya harmonisasi data pertanahan dan pengawasan berkala dari otoritas berwenang.
    </span>
</div>
""", unsafe_allow_html=True)

# ---- VISUALIZATION 3: Perusahaan dengan FPIC Violations ----
st.markdown("#### Perusahaan dengan Pelanggaran FPIC Eksplisit")

df_fpic_violations = df_konflik[df_konflik['indikasi_fpic'] == True].copy()
df_fpic_violations['Perusahaan'] = df_fpic_violations['nama_perusahaan'].str.split(';').str[0].str.strip()
df_fpic_violations = df_fpic_violations[['tahun', 'Perusahaan', 'provinsi', 'lokasi', 'judul', 'detail_url']].sort_values('tahun', ascending=False)

# Create expanders for each case
for idx, row in df_fpic_violations.iterrows():
    with st.expander(f"**{row['tahun']}** — {row['Perusahaan']} ({row['provinsi']})", expanded=False):
        st.markdown(f"""
        **Judul Konflik:** {row['judul']}
        
        **Komoditas:** {row['lokasi']}
        
        **Provinsi:** {row['provinsi']}
        
        **Sumber:** [Tanahkita.id]({row['detail_url']})
        """)

st.markdown("""
<div style="background:#FFFFFF; padding:15px 20px; border-radius:8px; border-left:4px solid #C0392B; margin-top: 10px; margin-bottom: 25px;">
    <span style="color: #E0E0E0; font-size: 0.95rem;">
        <b style="color:#C0392B;">Studi Kasus:</b> Kasus-kasus di Pulau Wawonii dan Minahasa Selatan menyoroti pentingnya kehati-hatian dalam proses penataan perizinan serta penyelesaian sengketa lahan masyarakat secara adil dan transparan.
    </span>
</div>
""", unsafe_allow_html=True)

# ---- VISUALIZATION 4: Data Table dengan Filter ----
st.markdown("#### Database Lengkap: Konflik & Masalah Izin di Sulawesi")

tab1, tab2 = st.tabs(["Konflik Pertambangan (Tanahkita)", "Masalah Izin Perusahaan (KPA)"])

with tab1:
    # Filter options
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        filter_provinsi = st.multiselect(
            "Filter Provinsi",
            options=['Semua'] + sorted(df_konflik['provinsi'].unique().tolist()),
            default=['Semua']
        )
    with col_filter2:
        filter_komoditas = st.multiselect(
            "Filter Komoditas",
            options=['Semua'] + sorted(df_konflik['lokasi'].unique().tolist()),
            default=['Semua']
        )
    
    # Apply filters
    df_konflik_filtered = df_konflik.copy()
    if 'Semua' not in filter_provinsi:
        df_konflik_filtered = df_konflik_filtered[df_konflik_filtered['provinsi'].isin(filter_provinsi)]
    if 'Semua' not in filter_komoditas:
        df_konflik_filtered = df_konflik_filtered[df_konflik_filtered['lokasi'].isin(filter_komoditas)]
    
    # Display table
    df_konflik_display = df_konflik_filtered[['tahun', 'judul', 'nama_perusahaan', 'provinsi', 'lokasi', 'indikasi_fpic']].copy()
    df_konflik_display = df_konflik_display.rename(columns={
        'tahun': 'Tahun',
        'judul': 'Judul Konflik',
        'nama_perusahaan': 'Perusahaan',
        'provinsi': 'Provinsi',
        'lokasi': 'Komoditas',
        'indikasi_fpic': 'Pelanggaran FPIC'
    })
    df_konflik_display['Pelanggaran FPIC'] = df_konflik_display['Pelanggaran FPIC'].map({True: '✅ YA', False: '⚠️ Tidak Eksplisit'})
    
    st.dataframe(df_konflik_display, use_container_width=True, hide_index=True, height=400)
    st.caption(f"**Total {len(df_konflik_filtered)} konflik** | Sumber: `sulawesi_konflik_tambang_fpic.csv` (Tanahkita.id)")

with tab2:
    # Filter options
    col_filter3, col_filter4 = st.columns(2)
    with col_filter3:
        filter_tahun_laporan = st.multiselect(
            "Filter Tahun Laporan",
            options=['Semua'] + sorted(df_masalah['tahun_laporan'].unique().tolist()),
            default=['Semua']
        )
    with col_filter4:
        filter_masalah = st.multiselect(
            "Filter Jenis Masalah",
            options=['Semua'] + sorted(df_masalah_breakdown['Jenis Masalah'].unique().tolist()),
            default=['Semua']
        )
    
    # Apply filters
    df_masalah_filtered = df_masalah.copy()
    if 'Semua' not in filter_tahun_laporan:
        df_masalah_filtered = df_masalah_filtered[df_masalah_filtered['tahun_laporan'].isin(filter_tahun_laporan)]
    if 'Semua' not in filter_masalah:
        # Filter rows that contain any of the selected masalah types
        df_masalah_filtered = df_masalah_filtered[df_masalah_filtered['jenis_masalah_izin'].str.contains('|'.join(filter_masalah), case=False, na=False)]
    
    # Display table
    df_masalah_display = df_masalah_filtered[['tahun_laporan', 'nama_perusahaan', 'lokasi', 'jenis_masalah_izin', 'luas_ha']].copy()
    df_masalah_display = df_masalah_display.rename(columns={
        'tahun_laporan': 'Tahun Laporan',
        'nama_perusahaan': 'Perusahaan',
        'lokasi': 'Lokasi',
        'jenis_masalah_izin': 'Jenis Masalah',
        'luas_ha': 'Luas (Ha)'
    })
    
    st.dataframe(df_masalah_display, use_container_width=True, hide_index=True, height=400)
    st.caption(f"**Total {len(df_masalah_filtered)} kasus** | Sumber: `kpa_masalah_izin_perusahaan.csv` (KPA CATAHU 2016-2025)")

st.markdown("---")

# ---- CITATION BOX ----
st.markdown("#### Referensi Utama & Verifikasi Independen")

st.markdown("""
<div style="background:#1A1A1A; padding:20px; border-radius:10px; border:1px solid #333; margin-bottom:25px;">
<h5 style="color:#66BB6A; margin-top:0;">Laporan Organisasi Internasional:</h5>
<ul style="line-height:1.8; color:#E0E0E0;">
<li><b>Climate Rights International (2024-2025)</b>: "Indonesia: Nickel Industry Harming Human Rights and the Environment" — Dokumentasi pelanggaran hak asasi dan lingkungan di industri nikel Indonesia. <a href="https://cri.org/indonesia" target="_blank" style="color:#66BB6A;">cri.org/indonesia</a></li>
<li><b>Mighty Earth (2024)</b>: "From Forests to Electric Vehicles" — Temuan: perusahaan tambang nikel secara ilegal membabat hutan lindung dan produksi, <b>tanpa menggunakan FPIC untuk konsultasi dengan komunitas lokal di Kabaena</b>. <a href="https://mightyearth.org/article/from-forests-to-electric-vehicles/" target="_blank" style="color:#66BB6A;">mightyearth.org</a></li>
<li><b>Business & Human Rights Resource Centre (2024)</b>: "Indonesia: Nickel mining levels forests without FPIC" — Dokumentasi dampak kesehatan, lingkungan, dan ekonomi yang merugikan masyarakat lokal. <a href="https://www.business-humanrights.org/" target="_blank" style="color:#66BB6A;">business-humanrights.org</a></li>
<li><b>EJAtlas</b>: "Islanders resisting nickel mining permits, Wawonii, Southeast Sulawesi" — Studi kasus Pulau Wawonii: "Meskipun konsesi mencakup area pemukiman dan tanah leluhur, <b>penduduk tidak dilibatkan dalam proses pengambilan keputusan</b>." <a href="https://www.ejatlas.org/conflict/islanders-resisting-nickel-mining-permits-wawonii-southeast-sulawesi-indonesia" target="_blank" style="color:#66BB6A;">ejatlas.org</a></li>
<li><b>Mongabay (2025)</b>: "Nickel boom on an Indonesian island brings toxic seas, lost incomes" — Temuan: "Komunitas yang terdampak melaporkan <b>perampasan lahan tanpa konsultasi atau kompensasi yang layak, partisipasi publik yang terbatas, dan kriminalisasi terhadap protes</b>, semuanya melanggar hak-hak masyarakat adat dan hukum nasional." <a href="https://news.mongabay.com/2025/07/" target="_blank" style="color:#66BB6A;">mongabay.com</a></li>
</ul>

<h5 style="color:#66BB6A; margin-top:20px;">Database Nasional:</h5>
<ul style="line-height:1.8; color:#E0E0E0;">
<li><b>Konsorsium Pembaruan Agraria (KPA)</b>: Catatan Akhir Tahun (CATAHU) 2016-2025 — 9 laporan tahunan komprehensif tentang konflik agraria dan masalah perizinan di Indonesia.</li>
<li><b>Tanahkita.id</b>: Database konflik agraria YLBHI/KPA — 568 kasus konflik nasional, 12 kasus pertambangan Sulawesi terekam.</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.subheader("5.4 Pembuktian Empiris: Uji Statistik Korelasi Penerbitan Izin & Deforestasi")
st.markdown('<span style="background:#4A148C;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Crosstabulation & Pearson Chi-Square Test</span>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

with st.expander("ℹ️ Metodologi: Uji Korelasi Penerbitan Izin & Ekstraksi Ekologis"):
    st.markdown("""
    **Metode Analisis:** Sub-bab ini menggunakan pengujian statistik inferensial (*Crosstabulation & Chi-Square Test*) untuk membuktikan secara matematis apakah besaran jumlah perizinan baru menjadi prediktor kuat terhadap tingkat kerusakan deforestasi.

    1. **Uji Signifikansi Statistik (Chi-Square):**
        * **Binning (Kategorisasi Data):** Data numerik berkelanjutan (Jumlah Izin & Luas Deforestasi) dikategorikan menjadi 2 level (Tinggi & Rendah) menggunakan ambang batas Median dari distribusi panel. `Nilai > Median = Tinggi`, `Nilai <= Median = Rendah`.
        * `H0 (Null Hypothesis): Tidak ada hubungan yang signifikan (independen) antara klasifikasi tingginya jumlah penerbitan IUP baru dengan klasifikasi tingginya luasan deforestasi pada suatu provinsi di tahun tertentu.`
        * `Decision Rule: Tolak H0 jika nilai Asymptotic Significance (P-Value) pada uji Pearson Chi-Square < 0.05 (Alpha 5%).`
    2. **Kalkulasi/Formula Pengolahan:**
        * `Chi-Square (χ²) = Σ [ (O_i - E_i)² / E_i ]`
        * `Odds Ratio = (Peluang Deforestasi Tinggi pada Izin Tinggi) / (Peluang Deforestasi Tinggi pada Izin Rendah)`
    3. **Variabel & Fitur Data:**
        * **Variabel Independen (X):** `Jumlah_Izin_Baru` atau `Total_Luas_Konsesi_Baru_Ha` (Interaktif Dropdown).
        * **Variabel Dependen (Y):** `Total_Deforestasi_Ha` atau `Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha` (Interaktif Dropdown).
    4. **Dataset & File:**
        * Panel Join dari: `sulawesi_izin_baru_per_tahun.csv` dan `sulawesi_gfw_master_1_dekade_2014_2023.csv`
    """)

# --- Data Preparation ---
df_panel = pd.merge(df_gfw, df_izin, on=['Provinsi', 'Tahun'], how='left').fillna({'Jumlah_Izin_Baru': 0, 'Total_Luas_Konsesi_Baru_Ha': 0})

col_sel1, col_sel2 = st.columns(2)

with col_sel1:
    st.markdown("##### Variabel Independen (X) - Tekanan Ekspansi")
    x_options = {
        "Jumlah_Izin_Baru": "Jumlah Izin Baru (IUP)",
        "Total_Luas_Konsesi_Baru_Ha": "Luas Konsesi Baru (Hektar)"
    }
    x_col = st.selectbox("Pilih Indikator Ekspansi (X):", list(x_options.keys()), format_func=lambda x: x_options[x])

with col_sel2:
    st.markdown("##### Variabel Dependen (Y) - Dampak Ekologis")
    y_options = {
        "Total_Deforestasi_Ha": "Total Deforestasi Alam (Hektar)",
        "Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha": "Deforestasi Komoditas Tambang/Sawit (Hektar)"
    }
    y_col = st.selectbox("Pilih Indikator Dampak (Y):", list(y_options.keys()), format_func=lambda x: y_options[x])

# --- Calculation (Binning) ---
x_median = df_panel[x_col].median()
y_median = df_panel[y_col].median()

label_x_low = f"Rendah (<{x_median:,.1f})"
label_x_high = f"Tinggi (≥{x_median:,.1f})"
label_y_low = f"Rendah (<{y_median:,.1f})"
label_y_high = f"Tinggi (≥{y_median:,.1f})"

df_panel["X_Label"] = df_panel[x_col].apply(lambda x: label_x_high if x >= x_median else label_x_low)
df_panel["Y_Label"] = df_panel[y_col].apply(lambda x: label_y_high if x >= y_median else label_y_low)

# Crosstab Base
cats_x = [label_x_low, label_x_high]
cats_y = [label_y_low, label_y_high]
crosstab = pd.crosstab(df_panel["X_Label"], df_panel["Y_Label"]).reindex(index=cats_x, columns=cats_y, fill_value=0)

chi2, p, dof, expected = stats.chi2_contingency(crosstab)
expected_df = pd.DataFrame(expected, index=crosstab.index, columns=crosstab.columns)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
st.markdown("### Detail Uji Statistik (Chi-Square & Odds Ratio)")
st.caption("Tabel-tabel di bawah ini adalah *output* statistik formal yang menyajikan bukti statistik formal: Case Processing → Crosstabulation → Chi-Square Tests → Ringkasan Hipotesis.")

# --- A. Case Processing Summary ---
st.markdown("##### Case Processing Summary")
total_cases = len(df_panel)
valid_cases = len(df_panel.dropna(subset=[x_col, y_col]))
missing_cases = total_cases - valid_cases

columns_case = pd.MultiIndex.from_product([["Cases"], ["Valid", "Missing", "Total"], ["N", "Percent"]])
interaction_label = f"{x_options[x_col]} * {y_options[y_col]}"
row_data = [
    valid_cases, f"{valid_cases/total_cases*100:.1f}%",
    missing_cases, f"{missing_cases/total_cases*100:.1f}%",
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
g, p_g, dof_g, exp_g = stats.chi2_contingency(crosstab, lambda_="log-likelihood")
x_codes = df_panel["X_Label"].replace({label_x_low: 0, label_x_high: 1})
y_codes = df_panel["Y_Label"].replace({label_y_low: 0, label_y_high: 1})
r, p_corr = stats.pearsonr(list(x_codes), list(y_codes))
lbl_val = (valid_cases - 1) * (r**2)

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
    a = crosstab.loc[label_x_low, label_y_low]
    b = crosstab.loc[label_x_low, label_y_high]
    c = crosstab.loc[label_x_high, label_y_low]
    d = crosstab.loc[label_x_high, label_y_high]
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
        interp_text = f"Hasil pengujian menunjukkan: intensitas {x_options[x_col]} terbukti **berkorelasi signifikan** dengan peningkatan {y_options[y_col]} (OR: {odds_ratio:.3f}). Temuan ini menunjukkan bahwa ekspansi perizinan berasosiasi dengan dinamika luas deforestasi."
    else:
        interp_text = f"Secara agregat, hubungan antara {x_options[x_col]} dan {y_options[y_col]} **tidak signifikan** secara statistik (P ≥ 0.05). Ini mengindikasikan bahwa laju deforestasi terdistribusi secara merata di berbagai lokasi dan kurun waktu."
    
    st.markdown(f"""
    <div style="background:#FFFFFF; padding:14px; border-radius:10px; border-left:5px solid {order_color}; height: 100%;">
        <b>Interpretasi Ekologis:</b><br><br>
        {interp_text}
    </div>
    """, unsafe_allow_html=True)

# --- E. Executive Summary of All Combinations ---
st.markdown("---")
st.markdown("### Ringkasan Eksekutif Seluruh Skenario Crosstab")
st.markdown("Tabel di bawah ini merangkum hasil pengujian statistik (Chi-Square) untuk semua kemungkinan kombinasi antara indikator Ekspansi (X) dan Dampak Ekologis (Y) pada panel data yang sama.")

summary_data = []
for k_x, v_x in x_options.items():
    for k_y, v_y in y_options.items():
        med_x = df_panel[k_x].median()
        med_y = df_panel[k_y].median()
        
        lbl_x_h = f"Tinggi (≥{med_x:,.1f})"
        lbl_x_l = f"Rendah (<{med_x:,.1f})"
        lbl_y_h = f"Tinggi (≥{med_y:,.1f})"
        lbl_y_l = f"Rendah (<{med_y:,.1f})"
        
        s_x = df_panel[k_x].apply(lambda val: lbl_x_h if val >= med_x else lbl_x_l)
        s_y = df_panel[k_y].apply(lambda val: lbl_y_h if val >= med_y else lbl_y_l)
        
        ct = pd.crosstab(s_x, s_y).reindex(index=[lbl_x_l, lbl_x_h], columns=[lbl_y_l, lbl_y_h], fill_value=0)
        try:
            c2_val, pv_val, dof_val, exp_val = stats.chi2_contingency(ct)
        except:
            c2_val, pv_val, dof_val = 0, 1, 0
            
        try:
            aa = ct.loc[lbl_x_l, lbl_y_l]
            bb = ct.loc[lbl_x_l, lbl_y_h]
            cc = ct.loc[lbl_x_h, lbl_y_l]
            dd = ct.loc[lbl_x_h, lbl_y_h]
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
    exec_narrative = textwrap.dedent(f"""\
Dari <b>{total_scenarios} skenario pengujian</b>, terdapat <b>{sig_count} skenario yang terbukti SIGNIFIKAN</b>.<br><br>
Tingginya <i>Odds Ratio</i> pada skenario yang signifikan menegaskan bahwa peningkatan penerbitan izin berasosiasi dengan risiko laju deforestasi yang lebih tinggi.<br><br>
Skenario yang <i>TIDAK SIGNIFIKAN</i> mengindikasikan bahwa dampak deforestasi juga dipengaruhi oleh faktor-faktor lain di luar jumlah izin baru.\
    """)
    bg_color = "rgba(229, 57, 53, 0.15)"
    border_color = "#E53935"
else:
    exec_narrative = textwrap.dedent(f"""\
Dari <b>{total_scenarios} skenario pengujian</b>, seluruhnya menunjukkan status <b>TIDAK SIGNIFIKAN</b>.<br><br>
Dalam kacamata analisis ekologis, ketidaksignifikanan secara agregat mengindikasikan bahwa laju deforestasi terjadi secara meluas dan konsisten di berbagai wilayah.\
    """)
    bg_color = "rgba(255, 152, 0, 0.15)"
    border_color = "#FF9800"

st.markdown(f"""
<div style="background-color: {bg_color}; padding:18px; border-radius:8px; border-left:6px solid {border_color}; margin-top: 15px; margin-bottom: 25px;">
    <b style="color: {border_color}; font-size: 1.05rem;">Pembedahan Realitas Ekologis:</b><br><br>
    <div style="color: #E0E0E0; font-size: 0.95rem; line-height: 1.6;">
{exec_narrative}
    </div>
</div>
""", unsafe_allow_html=True)

with st.expander("Lihat Data Panel Mentah (Merge Izin & GFW)", expanded=False):
    st.dataframe(df_panel[['Provinsi', 'Tahun', x_col, 'X_Label', y_col, 'Y_Label']], use_container_width=True, hide_index=True)
    st.caption("Sumber: Gabungan `sulawesi_izin_baru_per_tahun.csv` (Minerbaone) dan `sulawesi_gfw_master_1_dekade_2014_2023.csv` (GFW).")



