import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import os
import sys

# Konfigurasi path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar

st.set_page_config(
    page_title="Overview Temuan — CELIOS D3TLH",
    page_icon="refrensi/Celios China-Indonesia Energy Transition.png",
    layout="wide"
)
render_sidebar()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")

# ── Styles ──
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
.ovw-card {
    background: linear-gradient(135deg, #1A1F2B, #232B3B);
    border: 1px solid #333;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
}
.ovw-value {
    font-size: 1.5rem;
    font-weight: 700;
    line-height: 1.2;
}
.ovw-label {
    font-size: 0.78rem;
    color: #AAA;
    margin-top: 6px;
    font-weight: 600;
}
.page-block {
    background: #12161F;
    border: 1px solid #2A2F3B;
    border-radius: 12px;
    padding: 22px 26px;
    margin-bottom: 22px;
}
.page-hero {
    font-size: 1.45rem;
    font-weight: 700;
    color: #ECEFF1;
    margin-bottom: 4px;
}
.page-essence {
    font-size: 0.92rem;
    color: #B0BEC5;
    margin-bottom: 14px;
    font-style: italic;
}
.placeholder-box {
    border: 2px dashed #3A3F4B;
    border-radius: 8px;
    padding: 28px;
    text-align: center;
    color: #607D8B;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_all_page3():
    d = {}
    d['kes'] = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_kesehatan_detail_2014_2024.csv"))
    d['faskes'] = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_faskes_agregat.csv"))
    d['ika'] = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_ika_2016_2024.csv"))
    d['b3'] = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_limbah_b3.csv"))
    zoo_path = os.path.join(DATA_DIR, "zoonosis_kab_kota_2015_2024.csv")
    if os.path.exists(zoo_path):
        d['zoo'] = pd.read_csv(zoo_path)
    return d


@st.cache_data
def load_all_page2():
    d = {}
    d['ika'] = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_ika_2016_2024.csv"))
    d['iku'] = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_iku_2015_2024.csv"))
    d['gfw'] = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_gfw_master_1_dekade_2014_2023.csv"))
    d['pltu'] = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_pltu_captive.csv"))
    d['b3'] = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_limbah_b3.csv"))
    d['driver'] = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_gfw_loss_by_driver_2014_2023.csv"))
    return d


@st.cache_data
def load_biodiv():
    out = {}
    raw_path = os.path.join(BASE_DIR, "data", "raw", "gbif_sulawesi_occurrences.csv")
    if os.path.exists(raw_path):
        out['gbif'] = pd.read_csv(raw_path)
    out['iucn'] = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_biodiversitas_iucn_fase5_exploded.csv"))
    with open(os.path.join(DATA_DIR, "sulawesi_provinces.geojson"), 'r') as f:
        import json as _json
        out['geojson'] = _json.load(f)
    return out


@st.cache_data
def load_all_page5():
    d = {}
    d['izin'] = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_izin_baru_per_tahun.csv"))
    d['gfw'] = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_gfw_master_1_dekade_2014_2023.csv"))
    d['kawasan'] = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_gfw_kawasan_lindung_loss_2014_2023.csv"))
    d['konflik'] = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_konflik_tambang_fpic.csv"))
    d['masalah'] = pd.read_csv(os.path.join(DATA_DIR, "kpa_masalah_izin_perusahaan.csv"))
    return d

@st.cache_data
def load_all_page4():
    d = {}
    df_konflik = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_konflik_agraria_tanahkita.csv"))
    keywords = r'\b(sulawesi|sulsel|sulteng|sultra|sulut|sulbar|gorontalo|morowali|konawe|kolaka|bombana|poso|donggala|makassar|manado|minahasa|sangihe|mamuju|majene|polewali|halmahera|maluku utara|weda|obi|soroako|luwu|bantaeng|buton|muna|wakatobi|banggai|buol|toli-toli|parigi|luwuk|kendari|baubau|palu|bitung|tomohon|kotamobagu|gowa|takalar|jeneponto|bulukumba|sinjai|bone|maros|pangkep|barru|pinrang|enrekang|toraja|palopo)\b'
    mask = df_konflik['judul'].str.contains(keywords, case=False, na=False, regex=True) | \
           df_konflik['deskripsi'].str.contains(keywords, case=False, na=False, regex=True) | \
           df_konflik['narasi'].str.contains(keywords, case=False, na=False, regex=True) | \
           df_konflik['lokasi'].str.contains(keywords, case=False, na=False, regex=True)
    d['konflik'] = df_konflik[mask].copy()
    return d

@st.cache_data
def load_all_page7():
    d = {}
    d['izin'] = pd.read_csv(os.path.join(DATA_DIR, 'sulawesi_izin_baru_per_tahun.csv'))
    d['gfw'] = pd.read_csv(os.path.join(DATA_DIR, 'sulawesi_gfw_master_1_dekade_2014_2023.csv'))
    d['hukum'] = pd.read_csv(os.path.join(DATA_DIR, 'sulawesi_konflik_hukum.csv'))
    d['pltu'] = pd.read_csv(os.path.join(DATA_DIR, 'sulawesi_pltu_captive.csv'))
    return d

@st.cache_data
def load_all_page8():
    d = {}
    d['kesehatan'] = pd.read_csv(os.path.join(DATA_DIR, 'sulawesi_kesehatan_detail_2014_2024.csv'))
    return d

@st.cache_data
def load_all_page9():
    d = {}
    d['logistik'] = pd.read_csv(os.path.join(DATA_DIR, 'sulawesi_logistik_simpul_nikel.csv'))
    return d

@st.cache_data
def load_all_page10():
    d = {}
    d['demografi'] = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_demografi_master_fase4.csv"))
    d['shift'] = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_employment_shift_fase4.csv"))
    d['pdrb'] = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_pdrb_sektoral_2016_2024.csv"))
    return d

# ── Cached data loader (data diproses 1x, reused across blocks) ──
@st.cache_data
def load_all_page1():
    d = {}
    d['izin'] = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_izin_baru_per_tahun.csv"))
    d['pltu'] = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_pltu_captive.csv"))
    d['smelter'] = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_esdm_nikel.csv"))
    d['gfw'] = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_gfw_master_1_dekade_2014_2023.csv"))
    d['inv'] = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_investasi_pmdn_2016_2024.csv"))
    d['pad_bd'] = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_pad_breakdown_2016_2024.csv"))
    d['pad_tot'] = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_pad_2016_2024.csv"))
    d['logistik'] = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_logistik_simpul_nikel.csv"))
    return d


def metric_strip(cards):
    """Render a row of compact metric cards. cards = [(label, value, color), ...]"""
    n = len(cards)
    cols = st.columns(n)
    for col, (label, value, color) in zip(cols, cards):
        col.markdown(f"""
        <div class="ovw-card">
            <div class="ovw-value" style="color:{color};">{value}</div>
            <div class="ovw-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)


# ── Header ──
st.markdown('<div class="org-badge">CELIOS — Center of Economic and Law Studies</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Overview Temuan</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Ringkasan eksekutif lintas 10 halaman analisis — Ekspansi industri ekstraktif Sulawesi vs kebangkrutan ekologis, kesehatan, dan sosial (2014-2024).</div>', unsafe_allow_html=True)

st.markdown("""
Dashboard ini membuktikan secara empiris bahwa **ekspansi industri ekstraktif (nikel, tambang, smelter)** di 6 provinsi Sulawesi berjalan tanpa rem ekologis. Tiap blok di bawah merangkum satu halaman: **angka kunci + satu grafik utama**, dengan tautan langsung ke pembahasan penuh. Mulai dari pilot **Page 1** (lengkap); halaman lain menyusul.
""", unsafe_allow_html=True)
st.markdown("---")

# ══════════════════════════════════════════════════════════
# PAGE 1 — EKSPANSI INDUSTRI EKSTRAKTIF (PILOT, FULL 4 SUB-BAB)
# ══════════════════════════════════════════════════════════
with st.expander("1 · EKSPANSI INDUSTRI EKSTRAKTIF", expanded=True):
    d = load_all_page1()
    df_izin, df_pltu, df_smelter, df_gfw, df_inv = d['izin'], d['pltu'], d['smelter'], d['gfw'], d['inv']

    # ── Top metrics (6) ──
    tot_izin = df_izin['Jumlah_Izin_Baru'].sum()
    tot_luas_izin = df_izin['Total_Luas_Konsesi_Baru_Ha'].sum()
    tot_kapasitas_pltu = df_pltu.loc[df_pltu['Status'].str.lower() == 'operating', 'Capacity (MW)'].sum()
    tot_smelter = len(df_smelter)
    tot_deforestasi = df_gfw['Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha'].sum()
    tot_investasi_triliun = df_inv['nilai'].sum() / 1_000

    st.markdown('<div class="page-block">', unsafe_allow_html=True)
    st.markdown('<div class="page-hero">Ekspansi Industri Ekstraktif</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-essence">Smelter & izin tambang mengunci lanskap ekologis Sulawesi; ledakan izin pasca-2020 tanpa moratorium.</div>', unsafe_allow_html=True)
    st.page_link("pages/1_Ekspansi_Industri.py", label="➜ Buka halaman penuh", icon="🔗")

    metric_strip([
        ("Total Izin Baru", f"{tot_izin:,.0f} IUP", "#B71C1C"),
        ("Luas Konsesi", f"{tot_luas_izin:,.0f} Ha", "#C62828"),
        ("PLTU Captive", f"{tot_kapasitas_pltu:,.0f} MW", "#D32F2F"),
        ("Smelter", f"{tot_smelter} Unit", "#FF6F00"),
        ("Deforestasi", f"{tot_deforestasi:,.0f} Ha", "#B71C1C"),
        ("PMDN", f"{tot_investasi_triliun:,.1f} T Rp", "#D32F2F"),
    ])
    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    # ── 1.1 Tren Izin ──
    st.markdown("**1.1 Tren Pertumbuhan Izin Tambang Baru**")
    df_izin_agg = df_izin.groupby(['Tahun', 'Provinsi'])['Jumlah_Izin_Baru'].sum().reset_index()
    df_izin_total = df_izin_agg.groupby('Tahun')['Jumlah_Izin_Baru'].sum().reset_index()

    bar_izin = alt.Chart(df_izin_agg).mark_bar().encode(
        x=alt.X('Tahun:O', title='Tahun', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Jumlah_Izin_Baru:Q', title='Jumlah Izin Terbit'),
        color=alt.Color('Provinsi:N', scale=alt.Scale(scheme='set2'), legend=alt.Legend(title='Provinsi')),
        tooltip=['Tahun', 'Provinsi', alt.Tooltip('Jumlah_Izin_Baru', title='Izin Baru')]
    )
    line_izin = alt.Chart(df_izin_total).mark_line(color='#FF1744', strokeWidth=3, interpolate='monotone').encode(
        x='Tahun:O', y='Jumlah_Izin_Baru:Q'
    )
    pts_izin = alt.Chart(df_izin_total).mark_circle(color='#FF1744', size=70, opacity=1).encode(
        x='Tahun:O', y='Jumlah_Izin_Baru:Q',
        tooltip=['Tahun', alt.Tooltip('Jumlah_Izin_Baru', title='Total Izin')]
    )
    try:
        v22 = df_izin_total[df_izin_total['Tahun'] == 2022]['Jumlah_Izin_Baru'].values[0]
        v24 = df_izin_total[df_izin_total['Tahun'] == 2024]['Jumlah_Izin_Baru'].values[0]
        ann_txt = f"↑ {((v24 - v22) / v22) * 100:,.0f}% Kenaikan (2022-2024)"
    except IndexError:
        ann_txt = "Lonjakan Ekstrem"
    df_ann = pd.DataFrame({'Tahun': [2023], 'Jumlah_Izin_Baru': [df_izin_total['Jumlah_Izin_Baru'].max() * 0.95], 'text': [ann_txt]})
    ann_izin = alt.Chart(df_ann).mark_text(align='right', baseline='middle', fontSize=14, fontWeight='bold', color='#FF1744', dx=-10).encode(
        x='Tahun:O', y='Jumlah_Izin_Baru:Q', text='text'
    )
    chart_1_1 = alt.layer(bar_izin, line_izin, pts_izin, ann_izin).properties(
        height=340, title='Lonjakan Penerbitan Izin Tambang Sulawesi (2014-2024)'
    ).configure_axis(grid=True, gridOpacity=0.1)
    st.altair_chart(chart_1_1, use_container_width=True)

    # ── 1.2 PLTU Captive & Zona Tumbal ──
    st.markdown("**1.2 Agresivitas Ekspansi Kawasan Industri & PLTU Captive**")
    sentra_provs = ['Sulawesi Tengah', 'Sulawesi Tenggara']

    df_sm_prov = df_smelter.groupby('provinsi').size().reset_index(name='jumlah_iup')
    df_sm_prov['Persentase'] = (df_sm_prov['jumlah_iup'] / len(df_smelter)) * 100
    df_sm_prov['color_group'] = df_sm_prov['provinsi'].apply(lambda x: x if x in sentra_provs else 'Lainnya')
    bars_sm = alt.Chart(df_sm_prov).mark_bar(cornerRadiusEnd=2).encode(
        y=alt.Y('provinsi:N', sort='-x', title=''),
        x=alt.X('Persentase:Q', title='Porsi Izin (%)'),
        color=alt.Color('color_group:N', scale=alt.Scale(domain=['Sulawesi Tengah', 'Sulawesi Tenggara', 'Lainnya'], range=['#D32F2F', '#F57C00', '#37474F']), legend=None),
        tooltip=['provinsi', alt.Tooltip('jumlah_iup', title='Total Fasilitas'), alt.Tooltip('Persentase', format='.1f', title='Porsi (%)')]
    )
    txt_sm = bars_sm.mark_text(align='left', baseline='middle', dx=3, color='#ECEFF1', fontWeight='bold').encode(text=alt.Text('Persentase:Q', format='.1f'))
    chart_1_2 = (bars_sm + txt_sm).properties(height=300, title='Konsentrasi Smelter per Provinsi')
    st.altair_chart(chart_1_2, use_container_width=True)


    # ── 1.3 Treemap Breakdown PAD ──
    st.markdown("**1.3 Realisasi Investasi & Breakdown PAD Per Provinsi**")
    df_pad_detail = d['pad_bd'].groupby(['provinsi', 'jenis_pendapatan'])['nilai_juta_rupiah'].sum().reset_index()
    df_pad_detail.columns = ['Provinsi', 'Jenis_Pendapatan', 'Nilai_Juta_Rp']
    df_pad_detail['Nilai_Miliar_Rp'] = df_pad_detail['Nilai_Juta_Rp'] / 1_000
    df_pad_tot_agg = d['pad_tot'].groupby('provinsi')['pad_juta_rupiah'].sum().reset_index()
    df_pad_tot_agg.columns = ['Provinsi', 'Nilai_Juta_Rp']
    df_pad_tot_agg['Nilai_Miliar_Rp'] = df_pad_tot_agg['Nilai_Juta_Rp'] / 1_000
    prov_breakdown = df_pad_detail['Provinsi'].unique()
    df_pad_nb = df_pad_tot_agg[~df_pad_tot_agg['Provinsi'].isin(prov_breakdown)].copy()
    df_pad_nb['Jenis_Pendapatan'] = 'Total PAD (tanpa breakdown)'
    df_pad_nb = df_pad_nb[['Provinsi', 'Jenis_Pendapatan', 'Nilai_Juta_Rp', 'Nilai_Miliar_Rp']]
    df_pad = pd.concat([df_pad_detail, df_pad_nb], ignore_index=True)
    df_pad.loc[df_pad['Provinsi'] == 'Sulawesi Tenggara', 'Jenis_Pendapatan'] = 'PAD Kab. Buton (BPS: no data provinsi)'
    df_pad = df_pad[df_pad['Nilai_Miliar_Rp'] > 0].reset_index(drop=True)
    df_pad['Nilai_Transformed'] = df_pad['Nilai_Miliar_Rp'] ** 0.25
    df_pad.loc[df_pad['Nilai_Miliar_Rp'] < 100, 'Nilai_Transformed'] = df_pad.loc[df_pad['Nilai_Miliar_Rp'] < 100, 'Nilai_Transformed'] + 3.0

    fig_treemap = px.treemap(
        df_pad, path=['Provinsi', 'Jenis_Pendapatan'], values='Nilai_Transformed',
        hover_data={'Nilai_Miliar_Rp': ':,.2f', 'Nilai_Transformed': False},
        color='Nilai_Miliar_Rp', color_continuous_scale='RdYlGn',
        color_continuous_midpoint=df_pad['Nilai_Miliar_Rp'].median(),
        custom_data=['Nilai_Miliar_Rp']
    )
    fig_treemap.update_traces(
        texttemplate="<b>%{label}</b><br>%{customdata[0]:,.1f} M Rp",
        textposition="middle center", textfont_size=12,
        marker=dict(line=dict(width=2, color='#1E1E1E')),
        hovertemplate='<b>%{label}</b><br>Nilai: %{customdata[0]:,.2f} Miliar Rp<extra></extra>'
    )
    fig_treemap.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#B0BEC5'), margin=dict(t=30, l=5, r=5, b=5), height=480
    )
    st.plotly_chart(fig_treemap, use_container_width=True, config={'displayModeBar': False})

    # ── 1.4 Pelabuhan Ekspor Nikel ──
    st.markdown("**1.4 Pelabuhan Ekspor: Ke Mana Nikel Sulawesi Dikirim?**")
    df_log = d['logistik']
    psn_count = len(df_log[df_log['psn_status'] == 'terkonfirmasi'])
    metric_strip([
        ("Pelabuhan Nikel", f"{len(df_log)}", "#43A047"),
        ("Berlabel PSN", f"{psn_count} / {len(df_log)}", "#FFA726"),
        ("Pelabuhan Terbesar", "50.000 ton", "#42A5F5"),
    ])
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    df_ringkas = df_log[['node_label', 'anchor_entity', 'port_facility', 'psn_status', 'kawasan_industri']].copy()
    df_ringkas.columns = ['Lokasi', 'Perusahaan Utama', 'Status Pelabuhan', 'Status PSN', 'Kawasan Industri']
    st.dataframe(df_ringkas, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# PAGE 2 — KUALITAS LINGKUNGAN (5 SUB-BAB)
# ══════════════════════════════════════════════════════════
with st.expander("2 · KUALITAS LINGKUNGAN", expanded=False):
    d2 = load_all_page2()
    df_ika, df_iku, df_gfw2, df_pltu2, df_b3, df_driver = d2['ika'], d2['iku'], d2['gfw'], d2['pltu'], d2['b3'], d2['driver']

    mean_ika_2023 = df_ika[df_ika['Tahun'] == 2023]['Indeks Kualitas Air'].mean()
    mean_iku_2023 = df_iku[df_iku['Tahun'] == 2023]['IKU'].mean()
    df_b3['Estimasi Timbulan (Ton/Tahun)'] = pd.to_numeric(df_b3['Estimasi Timbulan (Ton/Tahun)'], errors='coerce')
    tot_limbah_b3_juta = df_b3['Estimasi Timbulan (Ton/Tahun)'].sum() / 1_000_000
    tot_deforestasi2 = df_gfw2['Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha'].sum()

    st.markdown('<div class="page-block">', unsafe_allow_html=True)
    st.markdown('<div class="page-hero">Kualitas Lingkungan di Kawasan Smelter</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-essence">Smelter mencekik napas & air; anjloknya IKA, IKU, dan laju deforestasi.</div>', unsafe_allow_html=True)
    st.page_link("pages/2_Kualitas_Lingkungan.py", label="➜ Buka halaman penuh", icon="🔗")

    metric_strip([
        ("IKA 2023", f"{mean_ika_2023:.1f} Poin", "#D32F2F"),
        ("IKU 2023", f"{mean_iku_2023:.1f} Poin", "#F57C00"),
        ("Limbah B3", f"{tot_limbah_b3_juta:,.1f} Jt Ton", "#D32F2F"),
        ("Deforestasi", f"{tot_deforestasi2:,.0f} Ha", "#F57C00"),
    ])
    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    # ── 2.1 Choropleth IKA per Provinsi ──
    st.markdown("**2.1 Dampak Limbah Tailing: Konsentrasi Smelter vs IKA**")
    df_ika_2023 = df_ika[df_ika['Tahun'] == 2023].copy()
    bd = load_biodiv()
    fig_ika = px.choropleth_mapbox(
        df_ika_2023, geojson=bd['geojson'], locations='Provinsi', featureidkey='properties.Provinsi',
        color='Indeks Kualitas Air',
        color_continuous_scale=[[0.0, '#8B4513'], [0.3, '#D2691E'], [0.5, '#F4A460'], [0.7, '#87CEEB'], [1.0, '#1E90FF']],
        zoom=4.5, center={"lat": -1.8, "lon": 120.5}, opacity=0.75,
        hover_name="Provinsi", hover_data={"Indeks Kualitas Air": ':.1f'},
        mapbox_style="carto-darkmatter"
    )
    fig_ika.update_layout(margin={"r":0,"t":30,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ECEFF1'), height=420)
    st.plotly_chart(fig_ika, use_container_width=True, config={'displayModeBar': False})

    # ── 2.2 Dual-axis: PLTU stacked area + IKU line ──
    st.markdown("**2.2 Kepungan Asap: PLTU Captive vs IKU**")
    prov_map = {'North Sulawesi': 'Sulawesi Utara', 'South Sulawesi': 'Sulawesi Selatan', 'Southeast Sulawesi': 'Sulawesi Tenggara', 'Central Sulawesi': 'Sulawesi Tengah', 'Gorontalo': 'Gorontalo', 'West Sulawesi': 'Sulawesi Barat'}
    df_pltu2['Provinsi'] = df_pltu2['Subnational unit (province, state)'].replace(prov_map)
    years = list(range(2010, 2025))
    df_pltu_op = df_pltu2[(df_pltu2['Status'].str.lower() == 'operating') & df_pltu2['Start year'].notna()]
    rows_pltu = []
    for y in years:
        for prov in prov_map.values():
            cap = df_pltu_op[(df_pltu_op['Provinsi'] == prov) & (df_pltu_op['Start year'] <= y)]['Capacity (MW)'].sum()
            rows_pltu.append({'Tahun': y, 'Provinsi': prov, 'Kapasitas_PLTU_MW': cap})
    df_pltu_trend = pd.DataFrame(rows_pltu)
    df_iku_avg = df_iku[df_iku['Tahun'].between(2010, 2024)].groupby('Tahun')['IKU'].mean().reset_index()

    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    owid_colors = ['#9B5A40', '#E58872', '#5E85B4', '#A09CAE', '#82B989', '#E3D7A4']
    fig_2_2 = make_subplots(specs=[[{"secondary_y": True}]])
    for i, prov in enumerate(df_pltu_trend['Provinsi'].unique()):
        dd = df_pltu_trend[df_pltu_trend['Provinsi'] == prov]
        fig_2_2.add_trace(go.Scatter(x=dd['Tahun'], y=dd['Kapasitas_PLTU_MW'], name=prov, mode='lines', stackgroup='one', line=dict(width=0.5, color='#444444'), fillcolor=owid_colors[i % len(owid_colors)], hovertemplate='%{y:.0f} MW<extra></extra>'), secondary_y=False)
    fig_2_2.add_trace(go.Scatter(x=df_iku_avg['Tahun'], y=df_iku_avg['IKU'], name="Rata-rata IKU", mode='lines+markers', marker=dict(color='#FFFFFF', size=8, line=dict(width=2, color='#D32F2F')), line=dict(color='#D32F2F', width=4), hovertemplate='IKU: %{y:.2f}<extra></extra>'), secondary_y=True)
    fig_2_2.update_layout(
        title=dict(text="Ekspansi PLTU vs Penurunan Kualitas Udara (2010-2024)", font=dict(color='#ECEFF1', size=16)),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#ECEFF1'),
        legend=dict(orientation="v", yanchor="top", y=0.98, xanchor="left", x=0.02, bgcolor='rgba(30,30,30,0.8)'), height=480
    )
    fig_2_2.update_yaxes(title_text="Kapasitas PLTU Kumulatif (MW)", secondary_y=False, color='#ECEFF1', gridcolor='#555')
    fig_2_2.update_yaxes(title_text="IKU", secondary_y=True, color='#D32F2F', showgrid=False)
    st.plotly_chart(fig_2_2, use_container_width=True, config={'displayModeBar': False})

    # ── 2.3 Bar Deforestasi per Provinsi ──
    st.markdown("**2.3 Eksekusi Ruang: Ekspansi Kawasan Industri vs Deforestasi**")
    df_def_prov = df_gfw2.groupby('Provinsi')['Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha'].sum().reset_index().sort_values('Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha', ascending=True)
    df_def_prov.columns = ['Provinsi', 'Deforestasi (Ha)']
    bar_def = alt.Chart(df_def_prov).mark_bar(cornerRadiusTopRight=5).encode(
        y=alt.Y('Provinsi:N', title=''),
        x=alt.X('Deforestasi (Ha):Q', title='Deforestasi Komoditas (Ha)'),
        color=alt.condition(alt.datum['Deforestasi (Ha)'] > df_def_prov['Deforestasi (Ha)'].median(), alt.value('#D32F2F'), alt.value('#F57C00')),
        tooltip=['Provinsi', alt.Tooltip('Deforestasi (Ha)', format=',.0f')]
    ).properties(height=300, title='Deforestasi Komoditas per Provinsi (2014-2023)').configure_axis(gridColor='#333')
    st.altair_chart(bar_def, use_container_width=True)

    # ── 2.4 Stacked Area Driver Deforestasi ──
    st.markdown("**2.4 Driver Deforestasi: Anatomi Pembantaian Hutan**")
    driver_mapping = {
        'Deforestasi Komoditas (Tambang/Sawit)': 'Industri Ekstraktif (Tambang/Sawit)',
        'Kehutanan': 'Kehutanan Komersial',
        'Pertanian Berpindah': 'Pertanian Berpindah (Masyarakat)',
        'Urbanisasi': 'Urbanisasi & Infrastruktur',
        'Tidak Diketahui': 'Tidak Teridentifikasi'
    }
    df_driver_clean = df_driver.copy()
    df_driver_clean['Faktor_Pendorong'] = df_driver_clean['Faktor_Pendorong'].replace(driver_mapping)
    df_driver_temporal = df_driver_clean.groupby(['Tahun', 'Faktor_Pendorong'])['Luas_Deforestasi_Ha'].sum().reset_index()
    chart_driver = alt.Chart(df_driver_temporal).mark_area(opacity=0.8).encode(
        x=alt.X('Tahun:O', title='Tahun', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Luas_Deforestasi_Ha:Q', title='Luas (Ha)', stack='normalize', axis=alt.Axis(format='%')),
        color=alt.Color('Faktor_Pendorong:N', title='Driver',
            scale=alt.Scale(domain=['Industri Ekstraktif (Tambang/Sawit)','Kehutanan Komersial','Pertanian Berpindah (Masyarakat)','Urbanisasi & Infrastruktur','Tidak Teridentifikasi'], range=['#D32F2F','#FF6F00','#FBC02D','#7CB342','#757575'])),
        tooltip=['Tahun', 'Faktor_Pendorong', alt.Tooltip('Luas_Deforestasi_Ha', format=',.0f')]
    ).properties(height=340, title='Komposisi Driver Deforestasi (2014-2023)').configure_axis(labelColor='#ECEFF1', titleColor='#ECEFF1', gridColor='#333').configure_legend(labelColor='#ECEFF1', titleColor='#ECEFF1', orient='right').configure_view(strokeWidth=0)
    st.altair_chart(chart_driver, use_container_width=True)

    # ── 2.5 Biodiversitas (GBIF + IUCN) ──
    st.markdown("**2.5 Kehancuran Biodiversitas: Satwa Endemik**")
    df_gbif = bd['gbif']
    df_iucn = bd['iucn'].drop_duplicates(subset=['Scientific Name'])
    tot_titik = len(df_gbif)
    tot_spesies = len(df_iucn)
    tot_cr = len(df_iucn[df_iucn['Status'] == 'Critically Endangered'])
    metric_strip([
        ("Titik GBIF", f"{tot_titik:,}", "#43A047"),
        ("Spesies Endemik", f"{tot_spesies}", "#FFA726"),
        ("Critically Endangered", f"{tot_cr}", "#D32F2F"),
    ])
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    fig_biodiv = px.scatter_mapbox(
        df_gbif, lat="Latitude", lon="Longitude", color="Scientific_Name", hover_name="Scientific_Name",
        hover_data={"Province": True, "Year": True, "Latitude": False, "Longitude": False},
        color_discrete_sequence=px.colors.qualitative.Bold, zoom=5, center={"lat": -1.8, "lon": 121.0}
    )
    fig_biodiv.update_layout(mapbox_style="carto-darkmatter", margin={"r":0,"t":30,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#ECEFF1'), legend=dict(orientation="v", yanchor="top", y=0.95, xanchor="left", x=0.02, bgcolor='rgba(30,30,30,0.8)'), height=450)
    st.plotly_chart(fig_biodiv, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# PAGE 3 — BEBAN KESEHATAN (7 SUB-BAB)
# ══════════════════════════════════════════════════════════
with st.expander("3 · BEBAN KESEHATAN", expanded=False):
    d3 = load_all_page3()
    df_kes, df_faskes, df_ika3, df_b3_3, df_zoo = d3['kes'], d3['faskes'], d3['ika'], d3['b3'], d3.get('zoo')

    tot_ispa = df_kes[df_kes["indikator"] == "Kasus ISPA/Pneumonia"]["nilai"].sum()
    tot_diare = df_kes[df_kes["indikator"] == "Kasus Diare Dilayani"]["nilai"].sum()
    tot_malaria = df_kes[df_kes["indikator"] == "Kasus Malaria Positif"]["nilai"].sum()
    tot_kusta = df_kes[df_kes["indikator"] == "Kasus Kusta Baru"]["nilai"].sum()
    faskes_2022 = df_faskes[df_faskes["tahun"] == 2022]
    tot_puskesmas_2022 = faskes_2022[faskes_2022["jenis"] == "Puskesmas"]["jumlah"].sum()
    tot_rs_2022 = faskes_2022[faskes_2022["jenis"] == "Rumah Sakit"]["jumlah"].sum()

    st.markdown('<div class="page-block">', unsafe_allow_html=True)
    st.markdown('<div class="page-hero">Beban Kesehatan Masyarakat Terdampak</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-essence">Hilirisasi yang membayar dengan nyawa — ledakan ISPA, diare, malaria.</div>', unsafe_allow_html=True)
    st.page_link("pages/3_Beban_Kesehatan.py", label="➜ Buka halaman penuh", icon="🔗")

    metric_strip([
        ("ISPA/Pneumonia", f"{tot_ispa:,.0f}", "#B71C1C"),
        ("Diare", f"{tot_diare:,.0f}", "#F4511E"),
        ("Malaria", f"{tot_malaria:,.0f}", "#C62828"),
        ("Kusta Baru", f"{tot_kusta:,.0f}", "#D32F2F"),
        ("Puskesmas 2022", f"{tot_puskesmas_2022:,.0f}", "#FF8A65"),
        ("RS 2022", f"{tot_rs_2022:,.0f}", "#FFAB91"),
    ])
    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    sentra = ["Sulawesi Tengah", "Sulawesi Tenggara"]
    kat_sentra = "Sentra Industri (Sulteng & Sultra)"
    kat_non = "Non-Sentra Industri (Lainnya)"

    # ── 3.1 Bar ISPA Sentra vs Non-Sentra ──
    st.markdown("**3.1 Ketimpangan Beban Penyakit: Sentra vs Non-Sentra**")
    df_kes_c = df_kes.copy()
    df_kes_c["Kategori"] = df_kes_c["provinsi"].apply(lambda x: kat_sentra if x in sentra else kat_non)
    df_filt = df_kes_c[df_kes_c["indikator"].isin(["Kasus ISPA/Pneumonia", "Kasus Diare Dilayani"])]
    df_agg31 = df_filt.groupby(["indikator", "Kategori"])["nilai"].mean().reset_index()
    fig_31 = px.bar(df_agg31, x="indikator", y="nilai", color="Kategori", barmode="group",
        color_discrete_map={kat_sentra: "#E53935", kat_non: "#546E7A"}, text_auto=".0f")
    fig_31.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig_31.update_layout(title="Rata-Rata Kasus ISPA & Diare: Sentra vs Non-Sentra", height=420,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#B0BEC5"),
        legend=dict(title=None, orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(title="Jenis Penyakit", showgrid=False), yaxis=dict(title="Rata-Rata Kasus/Tahun", showgrid=True, gridcolor="rgba(255,255,255,0.1)"))
    st.plotly_chart(fig_31, use_container_width=True, config={'displayModeBar': False})

    # ── 3.2 Bar Faskes Gap ──
    st.markdown("**3.2 Kesenjangan Fasilitas Kesehatan di Kawasan Ekstraktif**")
    df_faskes_c = df_faskes[~df_faskes["provinsi"].str.contains("Indonesia", na=False)].copy()
    df_faskes_c["Kategori"] = df_faskes_c["provinsi"].apply(lambda x: kat_sentra if x in sentra else kat_non)
    df_gap = df_faskes_c[df_faskes_c["tahun"] == 2022].groupby(["Kategori", "jenis"])["jumlah"].mean().reset_index()
    fig_32 = px.bar(df_gap, x="jumlah", y="jenis", color="Kategori", barmode="group", orientation="h",
        color_discrete_map={kat_sentra: "#E53935", kat_non: "#546E7A"}, text="jumlah")
    fig_32.update_traces(texttemplate="%{text:.0f}", textposition="outside", textfont_size=13)
    fig_32.update_layout(title="Ketimpangan Fasilitas Kesehatan (Rata-rata per Provinsi, 2022)", height=380,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#B0BEC5"),
        legend=dict(title=None, orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(title="Rata-Rata Jumlah Faskes", showgrid=True, gridcolor="rgba(255,255,255,0.1)"), yaxis=dict(title="", showgrid=False))
    st.plotly_chart(fig_32, use_container_width=True, config={'displayModeBar': False})

    # ── 3.3 Line Tren ISPA per Provinsi ──
    st.markdown("**3.3 Lintasan Waktu Ekologis & Ledakan Penyakit**")
    color_map_prov = {"Sulawesi Tengah": "#EF5350", "Sulawesi Tenggara": "#D32F2F", "Gorontalo": "#42A5F5", "Sulawesi Barat": "#1E88E5", "Sulawesi Selatan": "#1565C0", "Sulawesi Utara": "#90CAF9"}
    df_ispa_ts = df_kes[(df_kes["indikator"] == "Kasus ISPA/Pneumonia") & (df_kes["nilai"] > 0)].copy()
    fig_33 = px.line(df_ispa_ts, x="tahun", y="nilai", color="provinsi", markers=True, color_discrete_map=color_map_prov)
    for tr in fig_33.data:
        if tr.name in sentra:
            tr.line.width = 4
        else:
            tr.line.width = 2; tr.line.dash = "dot"; tr.opacity = 0.7
    fig_33.update_layout(title="Tren Historis Kasus ISPA/Pneumonia (2014-2024)", height=420,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#B0BEC5"),
        legend=dict(title="Provinsi (Merah: Sentra)", orientation="v", yanchor="top", y=1, xanchor="left", x=1.02),
        xaxis=dict(title="Tahun", showgrid=True, gridcolor="rgba(255,255,255,0.1)", dtick=1), yaxis=dict(title="Total Kasus", showgrid=True, gridcolor="rgba(255,255,255,0.1)", zeroline=False))
    st.plotly_chart(fig_33, use_container_width=True, config={'displayModeBar': False})

    # ── 3.4 Choropleth ISPA 2024 ──
    st.markdown("**3.4 Pemetaan Geospasial: Episentrum Ledakan Penyakit**")
    df_ispa_2024 = df_kes[(df_kes["tahun"] == 2024) & (df_kes["indikator"] == "Kasus ISPA/Pneumonia")].copy()
    bd3 = load_biodiv()
    fig_34 = px.choropleth_mapbox(df_ispa_2024, geojson=bd3['geojson'], locations='provinsi', featureidkey='properties.Provinsi',
        color='nilai', color_continuous_scale='YlOrRd', zoom=4.5, center={"lat": -1.8, "lon": 120.5}, opacity=0.8,
        hover_name="provinsi", hover_data={"nilai": ':,.0f'}, mapbox_style="carto-darkmatter")
    fig_34.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ECEFF1'), height=420)
    st.plotly_chart(fig_34, use_container_width=True, config={'displayModeBar': False})

    # ── 3.5 Scatter IKA vs Diare + Regression ──
    st.markdown("**3.5 Krisis Air Bersih: IKA vs Ledakan Kasus Diare**")
    import numpy as np
    from scipy import stats as scipy_stats
    df_ika_r = df_ika3.rename(columns={"Indeks Kualitas Air": "IKA"})
    df_diare_o = df_kes[df_kes["indikator"] == "Kasus Diare Dilayani"][["provinsi", "tahun", "nilai"]].copy()
    df_diare_o.columns = ["Provinsi", "Tahun", "Total_Diare"]
    df_ika_diare = pd.merge(df_ika_r, df_diare_o, left_on=["Provinsi", "Tahun"], right_on=["Provinsi", "Tahun"], how="inner").dropna()
    df_ika_diare["Kategori"] = df_ika_diare["Provinsi"].apply(lambda x: kat_sentra if x in sentra else kat_non)
    df_ika_diare["Year_Normalized"] = ((df_ika_diare["Tahun"] - df_ika_diare["Tahun"].min()) / (df_ika_diare["Tahun"].max() - df_ika_diare["Tahun"].min())) * 20 + 8
    x_vals = df_ika_diare["IKA"].values; y_vals = df_ika_diare["Total_Diare"].values
    slope, intercept, r_value, p_value, _ = scipy_stats.linregress(x_vals, y_vals)
    r_squared = r_value**2
    x_trend = np.linspace(x_vals.min(), x_vals.max(), 100); y_trend = slope * x_trend + intercept
    import plotly.graph_objects as go
    fig_35 = px.scatter(df_ika_diare, x="IKA", y="Total_Diare", color="Kategori", size="Year_Normalized",
        hover_data={"Provinsi": True, "Tahun": True, "IKA": ":.2f", "Total_Diare": ":,.0f", "Year_Normalized": False, "Kategori": False},
        color_discrete_map={kat_sentra: "#E53935", kat_non: "#546E7A"}, labels={"IKA": "Indeks Kualitas Air (IKA)", "Total_Diare": "Kasus Diare/Tahun"})
    fig_35.add_trace(go.Scatter(x=x_trend, y=y_trend, mode="lines", name=f"Trendline (R²={r_squared:.3f})", line=dict(color="#FBC02D", width=3, dash="dash")))
    fig_35.update_layout(title=f"Korelasi: IKA vs Kasus Diare (2016-2024) — {len(df_ika_diare)} Observasi", height=460,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#B0BEC5"),
        legend=dict(orientation="v", yanchor="top", y=0.98, xanchor="left", x=0.02, bgcolor="rgba(30,30,30,0.8)"),
        xaxis=dict(title="Indeks Kualitas Air (IKA)", showgrid=True, gridcolor="rgba(255,255,255,0.1)"), yaxis=dict(title="Kasus Diare/Tahun", showgrid=True, gridcolor="rgba(255,255,255,0.1)"))
    st.plotly_chart(fig_35, use_container_width=True, config={'displayModeBar': False})

    # ── 3.6a Bar B3 per Provinsi ──
    st.markdown("**3.6 Beban Limbah Beracun (B3)**")
    df_b3_3["Estimasi Timbulan (Ton/Tahun)"] = pd.to_numeric(df_b3_3["Estimasi Timbulan (Ton/Tahun)"], errors="coerce")
    df_b3_agg = df_b3_3[df_b3_3["Estimasi Timbulan (Ton/Tahun)"] > 1000].copy()
    df_b3_by_prov = df_b3_agg.groupby("Provinsi")["Estimasi Timbulan (Ton/Tahun)"].sum().reset_index().sort_values("Estimasi Timbulan (Ton/Tahun)", ascending=False)
    fig_b3 = px.bar(df_b3_by_prov, x="Estimasi Timbulan (Ton/Tahun)", y="Provinsi", orientation="h", text="Estimasi Timbulan (Ton/Tahun)", color="Estimasi Timbulan (Ton/Tahun)", color_continuous_scale="Reds")
    fig_b3.update_traces(texttemplate="%{text:,.0f} ton", textposition="outside", textfont_size=12)
    fig_b3.update_layout(title=f"Beban Limbah B3 per Provinsi ({df_b3_agg['Estimasi Timbulan (Ton/Tahun)'].sum()/1_000_000:.1f} Jt Ton/Tahun)", height=400,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#B0BEC5"),
        xaxis=dict(title="Timbulan B3 (Ton/Tahun)", showgrid=True, gridcolor="rgba(255,255,255,0.1)"), yaxis=dict(title="", showgrid=False), coloraxis_showscale=False)
    st.plotly_chart(fig_b3, use_container_width=True, config={'displayModeBar': False})

    # ── 3.6b Zoonosis DBD per Kabupaten Ekstraktif ──
    if df_zoo is not None and not df_zoo.empty:
        st.markdown("**3.6 Anomali Zoonosis: Dampak Ekspansi di Level Tapak**")
        kab_ekstr = ['Morowali', 'Morowali Utara', 'Banggai']
        df_zoo_dbd = df_zoo[(df_zoo["jenis_penyakit"] == "DBD") & (df_zoo["kabupaten_kota"].isin(kab_ekstr))].copy()
        df_zoo_dbd["Status"] = df_zoo_dbd["kabupaten_kota"].apply(lambda x: "Ekstraktif/Smelter" if x in ['Morowali', 'Morowali Utara'] else "Lainnya")
        fig_zoo = px.line(df_zoo_dbd, x="tahun", y="total_kasus", color="kabupaten_kota", markers=True, text="total_kasus",
            color_discrete_map={"Morowali": "#D50000", "Morowali Utara": "#FF3D3D", "Banggai": "#546E7A"})
        fig_zoo.update_traces(textposition="top center", textfont_size=10)
        for tr in fig_zoo.data:
            tr.mode = "lines+markers+text"
            if "Morowali" in tr.name: tr.line.width = 4
        fig_zoo.update_layout(title="Tren DBD di Kabupaten Ekstraktif Sulteng (2015-2024)", height=400,
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#B0BEC5"),
            legend=dict(title="Kabupaten", orientation="v", yanchor="top", y=1, xanchor="left", x=1.02),
            xaxis=dict(title="Tahun", showgrid=True, gridcolor="rgba(255,255,255,0.1)", dtick=1), yaxis=dict(title="Total Kasus DBD", showgrid=True, gridcolor="rgba(255,255,255,0.1)"))
        st.plotly_chart(fig_zoo, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# PAGE 4 — KONFLIK SOSIAL
# ══════════════════════════════════════════════════════════
with st.expander("4 · KONFLIK SOSIAL", expanded=False):
    d4 = load_all_page4()
    df_konflik4 = d4['konflik']
    
    # Helper & Clean
    def map_sektor(status):
        status = str(status).lower()
        if 'kebun' in status: return 'Perkebunan'
        if 'tambang' in status: return 'Pertambangan'
        if 'hutan' in status: return 'Kehutanan'
        if any(x in status for x in ['infrastruktur', 'bendungan', 'transmigrasi', 'energi', 'fasilitas', 'jalan', 'industri']): return 'Infrastruktur & PSN'
        if any(x in status for x in ['pariwisata', 'laut', 'pesisir']): return 'Pariwisata & Pesisir'
        return 'Lainnya'
    
    df_konflik4['Sektor_Grup'] = df_konflik4['status'].apply(map_sektor)
    df_konflik4['dampak_masyarakat_jiwa'] = pd.to_numeric(df_konflik4['dampak_masyarakat_jiwa'], errors='coerce').fillna(0)
    df_konflik4['jumlah_tewas'] = pd.to_numeric(df_konflik4['jumlah_tewas'], errors='coerce').fillna(0)
    df_konflik4['luas_ha'] = pd.to_numeric(df_konflik4['luas_ha'], errors='coerce').fillna(0)
    
    # Metrik
    tot_konflik = len(df_konflik4)
    tot_jiwa = int(df_konflik4['dampak_masyarakat_jiwa'].sum())
    tot_krim = df_konflik4[df_konflik4['indikasi_kriminalisasi'] == True].shape[0]
    tot_tewas = int(df_konflik4['jumlah_tewas'].sum())
    
    status_belum_selesai = len(df_konflik4[df_konflik4['status_konflik'].str.contains('Belum Ditangani', na=False)])
    konflik_kebun = len(df_konflik4[df_konflik4['status'].str.contains('Perkebunan', case=False, na=False)])
    konflik_hutan = len(df_konflik4[df_konflik4['status'].str.contains('Hutan', case=False, na=False)])
    konflik_tambang = len(df_konflik4[df_konflik4['status'].str.contains('Pertambangan', case=False, na=False)])
    konflik_infrastruktur = len(df_konflik4[df_konflik4['status'].str.contains('Infrastruktur|Bendungan|Transmigrasi|Energi|Fasilitas|Jalan', case=False, na=False)])
    libat_perusahaan = df_konflik4['keterlibatan_perusahaan'].notna().sum()
    libat_masyarakat = df_konflik4['keterlibatan_masyarakat'].notna().sum()
    
    st.markdown('<div class="page-block">', unsafe_allow_html=True)
    st.markdown('<div class="page-hero">Ruang Hidup yang Terampas</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-essence">Eskalasi konflik agraria & perampasan ruang di balik klaim pembangunan.</div>', unsafe_allow_html=True)
    st.page_link("pages/4_Konflik_Sosial.py", label="➜ Buka halaman penuh", icon="🔗")

    metric_strip([
        ("Letupan Konflik", f"{tot_konflik}", "#B71C1C"),
        ("Korban Jiwa", f"{tot_jiwa:,}", "#C62828"),
        ("Kriminalisasi", f"{tot_krim}", "#F57C00"),
        ("Belum Ditangani", f"{status_belum_selesai}", "#D32F2F"),
        ("Masy. Melawan", f"{libat_masyarakat}", "#E53935"),
        ("S. Perkebunan", f"{konflik_kebun}", "#D32F2F"),
        ("S. Kehutanan", f"{konflik_hutan}", "#F4511E"),
        ("S. Tambang", f"{konflik_tambang}", "#FF6F00"),
        ("Infrastruktur", f"{konflik_infrastruktur}", "#00ACC1"),
        ("Libat Korporasi", f"{libat_perusahaan}", "#8E24AA"),
    ])
    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
    
    color_map = {'Perkebunan': '#FFC107', 'Kehutanan': '#8BC34A', 'Pertambangan': '#FF9800', 'Infrastruktur & PSN': '#03A9F4', 'Pariwisata & Pesisir': '#E91E63', 'Lainnya': '#9E9E9E'}
    
    # ── 4.1 Tren Konflik ──
    st.markdown("**4.1 Tren Eskalasi Konflik Agraria**")
    df_ts = df_konflik4[df_konflik4['tahun'] >= 1990].groupby(['tahun', 'Sektor_Grup']).size().reset_index(name='Jumlah')
    fig_41 = px.bar(df_ts, x='tahun', y='Jumlah', color='Sektor_Grup', color_discrete_map=color_map, title='Ledakan Konflik Agraria di Sulawesi (1990-2025)')
    fig_41.update_layout(height=350, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#B0BEC5"), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, title=""))
    st.plotly_chart(fig_41, use_container_width=True, config={'displayModeBar': False})

    # ── 4.2 Monopoli Area ──
    st.markdown("**4.2 Sebaran Sektoral: Monopoli Daratan (Ha)**")
    df_ha = df_konflik4[df_konflik4['tahun'] >= 1990].groupby(['tahun', 'Sektor_Grup'])['luas_ha'].sum().reset_index()
    fig_42 = px.bar(df_ha, x='tahun', y='luas_ha', color='Sektor_Grup', color_discrete_map=color_map, title='Monopoli Area Konflik per Tahun')
    fig_42.update_layout(height=350, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#B0BEC5"), showlegend=False)
    st.plotly_chart(fig_42, use_container_width=True, config={'displayModeBar': False})

    # ── 4.3 Kriminalisasi ──
    st.markdown("**4.3 Kriminalisasi Aktivis & Warga**")
    df_krim = df_konflik4[(df_konflik4['indikasi_kriminalisasi'] == True) & (df_konflik4['tahun'] >= 2000)].groupby('tahun').size().reset_index(name='kasus')
    fig_43 = px.line(df_krim, x='tahun', y='kasus', markers=True, title='Tren Kriminalisasi & Represi (Pasca 2000)')
    fig_43.update_traces(line_color='#E53935', marker=dict(size=8, color='#B71C1C'))
    fig_43.update_layout(height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#B0BEC5"))
    st.plotly_chart(fig_43, use_container_width=True, config={'displayModeBar': False})

    # ── 4.4 Pembuktian Statistik ──
    st.markdown("**4.4 Pembuktian Statistik: Crosstab (Ekspansi vs Represi)**")
    import scipy.stats as stats
    df_crosstab4 = df_konflik4[df_konflik4['tahun'] >= 1990].copy()
    df_crosstab4['Periode'] = df_crosstab4['tahun'].apply(lambda x: 1 if x >= 2014 else 0)
    df_crosstab4['Korporasi'] = df_crosstab4['keterlibatan_perusahaan'].notna().apply(lambda x: 1 if x else 0)
    df_crosstab4['Represi'] = df_crosstab4['indikasi_kriminalisasi'].fillna(False).astype(bool).apply(lambda x: 1 if x else 0)
    df_crosstab4['Kematian'] = (df_crosstab4['jumlah_tewas'] > 0).apply(lambda x: 1 if x else 0)
    
    x_vars4 = {"Periode": "Periode Ekspansi (Pra/Pasca 2014)", "Korporasi": "Status Keterlibatan Korporasi"}
    y_vars4 = {"Represi": "Tingkat Represi & Kriminalisasi", "Kematian": "Tingkat Fatalitas (Korban Nyawa)"}
    
    sum_data4 = []
    for kx, vx in x_vars4.items():
        for ky, vy in y_vars4.items():
            ct4 = pd.crosstab(df_crosstab4[kx], df_crosstab4[ky]).reindex(index=[0, 1], columns=[0, 1], fill_value=0)
            try:
                c2_4, p_4, dof_4, exp_4 = stats.chi2_contingency(ct4)
                or_4 = (ct4.loc[0,0]*ct4.loc[1,1]) / (ct4.loc[0,1]*ct4.loc[1,0]) if (ct4.loc[0,1]*ct4.loc[1,0]) > 0 else 0
            except:
                c2_4, p_4, or_4 = 0, 1, 0
            sum_data4.append({
                "Prediktor (X)": vx, "Dampak (Y)": vy, "P-Value": f"{p_4:.3f}", 
                "Odds Ratio": f"{or_4:.2f}", "Status": "🟢 Signifikan" if p_4 < 0.05 else "🔴 Tdk Signifikan"
            })
    st.dataframe(pd.DataFrame(sum_data4), use_container_width=True, hide_index=True)

    # ── 4.5 Peta Orkestrasi Konflik (NLP) ──
    st.markdown("**4.5 Peta Orkestrasi Konflik: Aktor Sipil vs Ekstraktif**")
    import re
    text_corpus4 = " ".join((df_konflik4['judul'].fillna('') + " " + df_konflik4['deskripsi'].fillna('') + " " + df_konflik4['narasi'].fillna('')).tolist())
    pts4 = [" ".join(pt.split()) for pt in re.findall(r'\b(?:PT|CV)\.?\s*[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*){0,3}\b', text_corpus4)]
    civs4 = [" ".join(cv.split()) for cv in re.findall(r'\b(?:Walhi|WALHI|Jatam|JATAM|AMAN|LBH|Aliansi|Serikat|Konsorsium|Masyarakat Adat|Warga Desa)\s*[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*){0,3}\b', text_corpus4)]
    
    df_pts4 = pd.Series(pts4).value_counts().reset_index().head(5)
    df_pts4.columns = ['Aktor Korporasi', 'Frekuensi']
    df_civs4 = pd.Series(civs4).value_counts().reset_index().head(5)
    df_civs4.columns = ['Aktor Sipil', 'Frekuensi']
    
    df_pts4 = df_pts4.sort_values(by='Frekuensi', ascending=True)
    df_civs4 = df_civs4.sort_values(by='Frekuensi', ascending=True)

    fig_corp4 = px.bar(df_pts4, x='Frekuensi', y='Aktor Korporasi', orientation='h', color_discrete_sequence=['#F57C00'], title="Top Aktor Korporasi")
    fig_corp4.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#ECEFF1'), height=320, xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', tickformat='d'), margin=dict(l=0, r=0, t=30, b=0))
    
    fig_civs4 = px.bar(df_civs4, x='Frekuensi', y='Aktor Sipil', orientation='h', color_discrete_sequence=['#43A047'], title="Top Aktor Sipil & Ormas")
    fig_civs4.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#ECEFF1'), height=320, xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', tickformat='d'), margin=dict(l=0, r=0, t=30, b=0))
    
    col4a, col4b = st.columns(2)
    with col4a:
        st.plotly_chart(fig_corp4, use_container_width=True, config={'displayModeBar': False})
    with col4b:
        st.plotly_chart(fig_civs4, use_container_width=True, config={'displayModeBar': False})

    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# PAGE 5 — POLA PENERBITAN IZIN
# ══════════════════════════════════════════════════════════
# ══════════════════════════════════════════════════════════
with st.expander("5 · POLA PENERBITAN IZIN", expanded=False):
    d5 = load_all_page5()
    df_izin5, df_gfw5, df_kawasan5, df_konflik5 = d5['izin'], d5['gfw'], d5['kawasan'], d5['konflik']

    # Hitung metrik
    df_panel_bento = pd.merge(df_gfw5, df_izin5, on=['Provinsi', 'Tahun'], how='left').fillna({'Jumlah_Izin_Baru': 0})
    med_def = df_panel_bento['Total_Deforestasi_Ha'].median()
    df_panel_bento['is_kritis'] = df_panel_bento['Total_Deforestasi_Ha'] > med_def
    izin_kritis = int(df_panel_bento[df_panel_bento['is_kritis']]['Jumlah_Izin_Baru'].sum())
    izin_total = int(df_panel_bento['Jumlah_Izin_Baru'].sum())
    pct_kritis = (izin_kritis / izin_total * 100) if izin_total > 0 else 0

    izin_pra_2020 = int(df_izin5[df_izin5['Tahun'] < 2020]['Jumlah_Izin_Baru'].sum())
    izin_pasca_2020 = int(df_izin5[df_izin5['Tahun'] >= 2020]['Jumlah_Izin_Baru'].sum())
    rasio_akselerasi = (izin_pasca_2020 / izin_pra_2020) if izin_pra_2020 > 0 else 0
    
    total_konflik = len(df_konflik5)
    konflik_fpic = df_konflik5['indikasi_fpic'].sum()
    
    st.markdown('<div class="page-block">', unsafe_allow_html=True)
    st.markdown('<div class="page-hero">Pola Penerbitan Izin di Zona Kritis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-essence">Tata kelola gagal meredam perizinan tambang di wilayah yang telah melampaui daya dukung.</div>', unsafe_allow_html=True)
    st.page_link("pages/5_Pola_Penerbitan_Izin.py", label="➜ Buka halaman penuh", icon="🔗")

    metric_strip([
        ("Izin di Zona Kritis", f"{pct_kritis:.1f}%", "#B71C1C"),
        ("Akselerasi Pasca-2020", f"{rasio_akselerasi:.1f}x Lipat", "#C62828"),
        ("Konflik Pertambangan", f"{total_konflik}", "#F57C00"),
        ("Pelanggaran FPIC", f"{konflik_fpic}", "#D32F2F"),
    ])
    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    # ── 5.1 Dual-axis Combo Chart (Deforestasi vs Izin Baru) ──
    st.markdown("**5.1 Sinkronisasi Waktu: Deforestasi vs Laju Izin**")
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    
    df_izin_thn = df_izin5.groupby('Tahun')['Jumlah_Izin_Baru'].sum().reset_index()
    df_gfw_thn = df_gfw5.groupby('Tahun')['Total_Deforestasi_Ha'].sum().reset_index()
    df_timeline = pd.merge(df_gfw_thn, df_izin_thn, on='Tahun', how='outer').fillna(0).sort_values('Tahun')
    df_timeline = df_timeline[df_timeline['Tahun'] <= 2023]
    
    fig_51 = make_subplots(specs=[[{'secondary_y': True}]])
    fig_51.add_trace(go.Bar(
        x=df_timeline['Tahun'], y=df_timeline['Total_Deforestasi_Ha'], name='Total Deforestasi (Ha)',
        marker_color='rgba(231, 76, 60, 0.7)', marker_line_color='#C0392B', marker_line_width=1.5
    ), secondary_y=False)
    fig_51.add_trace(go.Scatter(
        x=df_timeline['Tahun'], y=df_timeline['Jumlah_Izin_Baru'], name='Izin Baru (IUP)',
        mode='lines+markers', line=dict(color='#F1C40F', width=3), marker=dict(symbol='circle', size=8)
    ), secondary_y=True)
    fig_51.update_layout(
        title='Tren Eskalasi: Kerusakan Hutan (Batang) vs Penerbitan Izin (Garis)', height=400,
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#B0BEC5"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    fig_51.update_yaxes(title_text='Deforestasi (Ha)', secondary_y=False, showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#E74C3C')
    fig_51.update_yaxes(title_text='Izin Baru', secondary_y=True, showgrid=False, color='#F1C40F')
    st.plotly_chart(fig_51, use_container_width=True, config={'displayModeBar': False})
    
    # ── 5.2 Tabrakan Tata Ruang ──
    st.markdown("**5.2 Tabrakan Tata Ruang: Deforestasi di Kawasan Konservasi**")
    df_kawasan = df_kawasan5[(df_kawasan5['wdpa_protected_areas__iucn_cat'].astype(str) != '0') & (df_kawasan5['Tahun'] <= 2023)].copy()
    df_pivot_chart = pd.pivot_table(df_kawasan, values='Luas_Hilang_Kawasan_Lindung_Ha', index='Tahun', columns='wdpa_protected_areas__iucn_cat', aggfunc='sum', fill_value=0).reset_index()
    if 1 in df_pivot_chart.columns: df_pivot_chart[1] = df_pivot_chart[1].cumsum()
    if 2 in df_pivot_chart.columns: df_pivot_chart[2] = df_pivot_chart[2].cumsum()
    
    fig_52 = go.Figure()
    if 1 in df_pivot_chart.columns:
        fig_52.add_trace(go.Bar(x=df_pivot_chart['Tahun'], y=df_pivot_chart[1], name='Cagar Alam', marker_color='#E74C3C'))
    if 2 in df_pivot_chart.columns:
        fig_52.add_trace(go.Bar(x=df_pivot_chart['Tahun'], y=df_pivot_chart[2], name='Taman Nasional', marker_color='#F39C12'))
        
    fig_52.update_layout(title='Akumulasi Kehancuran: Cagar Alam & Taman Nasional (Ha)', barmode='group', height=350, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#B0BEC5"), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
    st.plotly_chart(fig_52, use_container_width=True, config={'displayModeBar': False})

    # ── 5.3 Konflik Agraria & Pelanggaran FPIC ──
    st.markdown("**5.3 Konflik & Pelanggaran FPIC (1968-2025)**")
    d5_masalah = load_all_page5().get('masalah')
    df_konflik_tl = df_konflik5.copy()
    df_konflik_tl['kategori'] = 'Konflik Pertambangan'
    df_konflik_tl['Tahun'] = df_konflik_tl['tahun']
    df_masalah_tl = d5_masalah[d5_masalah['lokasi'].str.contains('Sulawesi', case=False, na=False)].copy()
    df_masalah_tl['kategori'] = 'Masalah Izin (KPA)'
    df_masalah_tl['Tahun'] = df_masalah_tl['tahun_laporan'].astype(int)
    
    df_cmb = pd.concat([df_konflik_tl[['Tahun', 'kategori']], df_masalah_tl[['Tahun', 'kategori']]], ignore_index=True)
    df_agg_cmb = df_cmb.groupby(['Tahun', 'kategori']).size().reset_index(name='Jumlah')
    
    fig_53 = px.bar(df_agg_cmb, x='Tahun', y='Jumlah', color='kategori', barmode='group', color_discrete_map={'Konflik Pertambangan': '#E74C3C', 'Masalah Izin (KPA)': '#F39C12'})
    fig_53.update_layout(title='Distribusi Temporal Konflik & Masalah Izin', height=350, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#B0BEC5"), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, title=""))
    st.plotly_chart(fig_53, use_container_width=True, config={'displayModeBar': False})

    # ── 5.4 Pembuktian Empiris ──
    st.markdown("**5.4 Pembuktian Empiris: Uji Statistik Crosstab**")
    import scipy.stats as stats
    x_opts = {"Jumlah_Izin_Baru": "Jumlah Izin Baru", "Total_Luas_Konsesi_Baru_Ha": "Luas Konsesi Baru"}
    y_opts = {"Total_Deforestasi_Ha": "Deforestasi Alam", "Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha": "Deforestasi Tambang/Sawit"}
    
    summary_data = []
    # Re-merge just to be safe with full columns
    df_panel_full = pd.merge(df_gfw5, df_izin5, on=['Provinsi', 'Tahun'], how='left').fillna({'Jumlah_Izin_Baru': 0, 'Total_Luas_Konsesi_Baru_Ha': 0})
    for k_x, v_x in x_opts.items():
        for k_y, v_y in y_opts.items():
            if k_x not in df_panel_full.columns or k_y not in df_panel_full.columns:
                continue
            med_x, med_y = df_panel_full[k_x].median(), df_panel_full[k_y].median()
            s_x = df_panel_full[k_x].apply(lambda val: 1 if val >= med_x else 0)
            s_y = df_panel_full[k_y].apply(lambda val: 1 if val >= med_y else 0)
            ct = pd.crosstab(s_x, s_y).reindex(index=[0, 1], columns=[0, 1], fill_value=0)
            try:
                c2_val, pv_val, dof_val, exp_val = stats.chi2_contingency(ct)
                or_v = (ct.loc[0,0]*ct.loc[1,1]) / (ct.loc[0,1]*ct.loc[1,0]) if (ct.loc[0,1]*ct.loc[1,0]) > 0 else 0
            except:
                c2_val, pv_val, or_v = 0, 1, 0
            
            summary_data.append({
                "Prediktor Ekspansi (X)": v_x,
                "Dampak Ekologis (Y)": v_y,
                "P-Value": f"{pv_val:.3f}",
                "Odds Ratio": f"{or_v:.2f}",
                "Status": "🟢 Signifikan" if pv_val < 0.05 else "🔴 Tdk Signifikan"
            })
    
    if summary_data:
        st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# PAGE 6 — AUDIT D3TLH (PLACEHOLDER)
# ══════════════════════════════════════════════════════════
with st.expander("6 · AUDIT D3TLH", expanded=False):
    st.markdown('<div class="page-block">', unsafe_allow_html=True)
    st.markdown('<div class="page-hero">Audit Forensik Metodologi D3TLH</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-essence">Pembuktian terbalik: metodologi D3TLH pemerintah vs fakta lapangan.</div>', unsafe_allow_html=True)
    st.page_link("pages/6_Audit_D3TLH.py", label="➜ Buka halaman penuh", icon="🔗")
    st.markdown(
        '<div class="placeholder-box"><b>Model Simulasi CGE & Kalkulator Ekologis</b> berada di halaman ini. Silakan langsung buka halaman penuh untuk melakukan pemodelan interaktif.</div>',
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# PAGE 7 — KEGAGALAN TATA KELOLA
# ══════════════════════════════════════════════════════════
with st.expander("7 · KEGAGALAN TATA KELOLA", expanded=False):
    d7 = load_all_page7()
    df_izin7, df_gfw7, df_hukum7, df_pltu7 = d7['izin'], d7['gfw'], d7['hukum'], d7['pltu']
    
    st.markdown('<div class="page-block">', unsafe_allow_html=True)
    st.markdown('<div class="page-hero">Kegagalan Tata Kelola & D3TLH</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-essence">Instrumen perlindungan ekologis direduksi menjadi stempel administratif.</div>', unsafe_allow_html=True)
    st.page_link("pages/7_Kegagalan_Tata_Kelola.py", label="➜ Buka halaman penuh", icon="🔗")

    metric_strip([
        ("Skor Veto D3TLH", "9.8 / 10", "#C62828"),
        ("Otoritas D3TLH", "Nihil", "#D32F2F"),
        ("Penegakan Hukum", "Pembiaran", "#F4511E"),
        ("Total Impunitas", f"{len(df_hukum7)} Kasus", "#E53935"),
        ("Unit PLTU Captive", f"{len(df_pltu7)}", "#F57C00"),
        ("Kapasitas PLTU", f"{df_pltu7['Capacity (MW)'].sum():,.0f} MW", "#FFB300"),
    ])
    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    # ── 7.1 Crosstab Status Ekologis ──
    st.markdown("**7.1 Status Ekologis vs Keputusan Izin**")
    df_panel7 = pd.merge(df_gfw7, df_izin7, on=['Provinsi', 'Tahun'], how='left').fillna({'Jumlah_Izin_Baru': 0, 'Total_Luas_Konsesi_Baru_Ha': 0})
    tertekan_th = df_panel7["Total_Deforestasi_Ha"].quantile(0.33)
    kritis_th = df_panel7["Total_Deforestasi_Ha"].quantile(0.66)
    def classify_d3tlh7(val):
        if val <= tertekan_th: return "Aman"
        elif val <= kritis_th: return "Tertekan"
        else: return "Kritis"
    df_panel7['Status_D3TLH'] = df_panel7["Total_Deforestasi_Ha"].apply(classify_d3tlh7)
    
    agg_df7 = df_panel7.groupby('Status_D3TLH').agg({'Jumlah_Izin_Baru': 'sum', 'Total_Luas_Konsesi_Baru_Ha': 'sum', "Total_Deforestasi_Ha": ['min', 'max']}).reset_index()
    agg_df7.columns = ['Status_D3TLH', 'Total_IUP', 'Total_Luas_Ha', 'Min_Def', 'Max_Def']
    agg_df7['Order'] = agg_df7['Status_D3TLH'].map({"Aman": 1, "Tertekan": 2, "Kritis": 3})
    agg_df7 = agg_df7.sort_values('Order')
    
    table_html7 = "<table style='width:100%; border-collapse: collapse; color: #FFF; font-size: 0.95rem; margin-bottom: 20px;'><tr style='background: #232B3B; text-align: left;'><th style='padding: 8px; border: 1px solid #444;'>Status Daya Dukung</th><th style='padding: 8px; border: 1px solid #444;'>Kenyataan Izin Baru</th><th style='padding: 8px; border: 1px solid #444;'>Kesimpulan</th></tr>"
    c7 = {"Aman": ("rgba(39, 174, 96, 0.05)", "#27AE60"), "Tertekan": ("rgba(241, 196, 15, 0.05)", "#F1C40F"), "Kritis": ("rgba(231, 76, 60, 0.05)", "#E74C3C")}
    for _, row in agg_df7.iterrows():
        st_ = row['Status_D3TLH']
        bg, bd = c7[st_]
        iup = int(row['Total_IUP'])
        if st_ == "Aman": kesimpulan = "Normal"
        elif st_ == "Tertekan": kesimpulan = "Anomali"
        else: kesimpulan = "BUKTI PELANGGARAN FATAL"
        table_html7 += f"<tr><td style='padding: 8px; border: 1px solid #444; background: {bg}; border-left: 4px solid {bd}; font-weight: bold;'>{st_}</td><td style='padding: 8px; border: 1px solid #444;'>{iup} Izin Keluar</td><td style='padding: 8px; border: 1px solid #444; font-weight:bold; color:{bd};'>{kesimpulan}</td></tr>"
    table_html7 += "</table>"
    st.markdown(table_html7, unsafe_allow_html=True)

    # ── 7.2 Sebaran Konflik ──
    st.markdown("**7.2 Impunitas Korporasi: Sebaran Kasus Dibiarkan**")
    prov_counts7 = df_hukum7['Provinsi'].value_counts().reset_index()
    prov_counts7.columns = ['Provinsi', 'Jumlah Kasus']
    fig_72 = px.bar(prov_counts7, x='Jumlah Kasus', y='Provinsi', orientation='h', color='Jumlah Kasus', color_continuous_scale='Reds', height=250)
    fig_72.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#ECEFF1'), margin=dict(l=0, r=0, t=10, b=0), xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'))
    st.plotly_chart(fig_72, use_container_width=True, config={'displayModeBar': False})

    # ── 7.3 PLTU Captive ──
    st.markdown("**7.3 Inkonsistensi Iklim: PLTU Captive**")
    df_pltu7['Provinsi'] = df_pltu7['Subnational unit (province, state)']
    pltu_prov7 = df_pltu7.groupby('Provinsi')['Capacity (MW)'].sum().reset_index().sort_values(by='Capacity (MW)', ascending=True)
    fig_73 = px.bar(pltu_prov7, x='Capacity (MW)', y='Provinsi', orientation='h', color='Capacity (MW)', color_continuous_scale='YlOrRd', height=250)
    fig_73.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#ECEFF1'), margin=dict(l=0, r=0, t=10, b=0), xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'))
    st.plotly_chart(fig_73, use_container_width=True, config={'displayModeBar': False})

    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# PAGE 8 — DISTRIBUSI MANFAAT
# ══════════════════════════════════════════════════════════
with st.expander("8 · DISTRIBUSI MANFAAT", expanded=False):
    d8 = load_all_page8()
    df_kesehatan8 = d8['kesehatan']
    
    st.markdown('<div class="page-block">', unsafe_allow_html=True)
    st.markdown('<div class="page-hero">Distribusi Manfaat vs Beban Ekologis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-essence">Privatisasi keuntungan ekstraktif oligarki vs sosialisasi kerugian publik.</div>', unsafe_allow_html=True)
    st.page_link("pages/8_Distribusi_Manfaat.py", label="➜ Buka halaman penuh", icon="🔗")

    metric_strip([
        ("Harta 50 Triliuner", "Rp4.651 T", "#C62828"),
        ("Proporsi Ekstraktif", "58,0%", "#FF6F00"),
        ("Laju Harian", "Rp13 Miliar", "#D32F2F"),
        ("Krisis ISPA", "117.775 Kasus", "#E53935"),
        ("Konflik Agraria", "12 Kasus Kritis", "#F4511E"),
        ("Kerugian Ekologis", "> Rp100 Triliun", "#B71C1C"),
    ])
    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    # ── 8.1 Tabel Oligarki ──
    st.markdown("**8.1 Top Penguasa Tahta Ekstraktif (Grup Taipan)**")
    html_table8 = """
<style>
.aktor-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; color: #E0E0E0; margin-bottom: 20px; }
.aktor-table th { background-color: #1A232E; color: #4DB6AC; padding: 10px; text-align: left; border-bottom: 2px solid #009688; }
.aktor-table td { padding: 10px; border-bottom: 1px solid #2D3748; background-color: #111827; vertical-align: middle; }
.aktor-table tr:hover td { background-color: #1F2937; }
.badge-rank { background-color: #FF5252; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 0.75rem; margin-right: 5px; }
.sub-text { font-size: 0.75rem; color: #9CA3AF; display: block; margin-top: 4px; }
</style>
<div style="overflow-x:auto; border-radius: 8px; border: 1px solid #374151; margin-bottom: 10px;">
<table class="aktor-table">
    <thead>
        <tr>
            <th>Grup Taipan / Konsorsium</th>
            <th>Total Harta (CELIOS)</th>
            <th>Afiliasi Blok (Sulawesi)</th>
            <th>Luas Konsesi (Aktual)</th>
        </tr>
    </thead>
    <tbody>
        <tr><td><span class="badge-rank">#1</span><b>PT Vale Indonesia</b><br><span class="sub-text">(MIND ID & Konsorsium)</span></td><td><b>Rp 259,2 T</b></td><td>Blok Sorowako, Bahodopi, Pomalaa</td><td><b style="color:#E57373;">118.017 Ha</b></td></tr>
        <tr><td><span class="badge-rank">#2</span><b>Salim Group</b><br><span class="sub-text">(Anthony Salim)</span></td><td><b>Rp 160,0 T</b></td><td>Citra Palu Minerals, Gorontalo Min.</td><td><b style="color:#E57373;">110.175 Ha</b></td></tr>
        <tr><td><span class="badge-rank">#3</span><b>Jiangsu Delong Nickel</b><br><span class="sub-text">(Tony Zhou Yuan)</span></td><td><b>Rp 45,0 T</b></td><td>PT VDNI, OSS (Konawe), GNI (Morut)</td><td><b style="color:#E57373;">2.253 Ha</b></td></tr>
        <tr><td><span class="badge-rank">#4</span><b>Tsingshan Holding</b><br><span class="sub-text">(Xiang Guangda)</span></td><td><b>Rp 163,0 T</b></td><td>Bintangdelapan, Eternal (IMIP)</td><td><b style="color:#E57373;">20.765 Ha</b></td></tr>
        <tr><td><span class="badge-rank">#5</span><b>Boy Thohir & Edwin S.</b><br><span class="sub-text">(Adaro / Saratoga)</span></td><td><b>Rp 64,1 T</b></td><td>PT Sulawesi Cahaya Mineral (SCM)</td><td><b style="color:#E57373;">21.100 Ha</b></td></tr>
    </tbody>
</table>
</div>
"""
    st.markdown(html_table8, unsafe_allow_html=True)

    # ── 8.2 Tren Beban (ISPA) ──
    st.markdown("**8.2 Tren Sosialisasi Beban Publik (Ledakan Penyakit ISPA)**")
    df_ispa8 = df_kesehatan8[df_kesehatan8['indikator'] == 'Kasus ISPA/Pneumonia']
    prov_sentra = ['Sulawesi Tengah', 'Sulawesi Tenggara']
    df_ispa_sentra8 = df_ispa8[df_ispa8['provinsi'].isin(prov_sentra)]
    df_ispa_trend8 = df_ispa_sentra8.groupby('tahun')['nilai'].sum().reset_index()
    
    import plotly.graph_objects as go
    fig_ispa8 = go.Figure()
    fig_ispa8.add_trace(go.Scatter(
        x=df_ispa_trend8['tahun'], y=df_ispa_trend8['nilai'], mode='lines+markers+text',
        name='Total Kasus ISPA', line=dict(color='#FF5252', width=4),
        marker=dict(size=10, color='#FF5252', line=dict(color='white', width=2)),
        text=df_ispa_trend8['nilai'].apply(lambda x: f"{int(x):,}"), textposition='top center',
        textfont=dict(color='#FF5252', size=11, weight='bold')
    ))
    fig_ispa8.update_layout(title='Tren Kasus ISPA/Pneumonia di Episentrum Nikel (Sulteng & Sultra)', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#ECEFF1"), height=350, margin=dict(l=0, r=0, t=30, b=0), xaxis=dict(title='', tickmode='linear', dtick=1, showgrid=False), yaxis=dict(title='Jumlah Kasus ISPA', showgrid=True, gridcolor='rgba(255,255,255,0.05)'))
    st.plotly_chart(fig_ispa8, use_container_width=True, config={'displayModeBar': False})

    # ── 8.3 Crosstab Statistik ──
    st.markdown("**8.3 Pembuktian Statistik: Oligarki Untung, Rakyat Buntung**")
    st.markdown("""
<div style="background:#1A1F2B; padding:15px 20px; border-radius:8px; border-left:4px solid #FBC02D; margin-bottom: 25px; line-height: 1.6;">
    <span style="color: #E0E0E0; font-size: 0.95rem;">
        <b>Kesimpulan Uji Statistik Signifikansi (Odds Ratio & Chi-Square):</b><br>
        Berdasarkan persilangan data, terdapat korelasi kuat dan <b>signifikan secara statistik (P < 0.05)</b>. Provinsi dengan aliran investasi PMDN (smelter & tambang) tertinggi memiliki risiko hampir <b>dua kali lipat lebih besar</b> untuk mengalami ledakan kasus Penyakit ISPA dan hilangnya hutan primer.<br><br>
        Analisis ini mendobrak ilusi efek <i>trickle-down</i>: Uang triliunan dari investasi nyatanya tidak tersirkulasi untuk memulihkan lingkungan, melainkan mengalir lari keluar (<i>capital flight</i>) ke rekening segelintir grup oligarki (Top 50 Taipan), sementara rakyat lokal hanya murni diwarisi limbah, langit yang menghitam, dan kematian.
    </span>
</div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# PAGE 9 — KORIDOR LOGISTIK (dari file 10)
# ══════════════════════════════════════════════════════════
with st.expander("9 · KORIDOR LOGISTIK", expanded=False):
    d9 = load_all_page9()
    df_logistik = d9['logistik']
    
    n_lokasi = len(df_logistik)
    n_mandiri = len(df_logistik[df_logistik["port_facility"] == "terkonfirmasi"])
    n_psn = len(df_logistik[df_logistik["psn_status"] == "terkonfirmasi"])
    total_pltu = int(df_logistik["pltu_mw"].sum())

    st.markdown('<div class="page-block">', unsafe_allow_html=True)
    st.markdown('<div class="page-hero">Ke Mana Nikel Sulawesi Mengalir</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-essence">6 titik pelabuhan ekspor nikel: siapa membangun, ke mana dikirim, dampaknya.</div>', unsafe_allow_html=True)
    st.page_link("pages/10_Koridor_Logistik.py", label="➜ Buka halaman penuh", icon="🔗")

    metric_strip([
        ("Total Lokasi", f"{n_lokasi} Klaster", "#43A047"),
        ("Status PSN", f"{n_psn} dari {n_lokasi}", "#FFA726"),
        ("Kapasitas PLTU", f"{total_pltu:,} MW", "#EF5350"),
        ("Pelabuhan Mandiri", f"{n_mandiri} Lokasi", "#42A5F5"),
        ("Jalur Kereta", "Nihil", "#9E9E9E"),
        ("Tujuan Utama", "China", "#C62828"),
    ])
    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    # ── 9.1 Peta Logistik ──
    st.markdown("**9.1 Peta Lokasi Pelabuhan Nikel di Sulawesi**")
    
    COORDS = {
        "NODE-SULTENG-MOROWALI-IMIP": {"lat": -2.19, "lon": 121.74},
        "NODE-SULTENG-MORUT-PETASIA-GNI": {"lat": -1.88, "lon": 121.62},
        "NODE-SULTRA-KONAWE-MOROSI-VDNI": {"lat": -3.72, "lon": 122.13},
        "NODE-SULTRA-KONAWE-OSS": {"lat": -3.73, "lon": 122.14},
        "NODE-SULTRA-KOLAKA-POMALAA-ANTAM": {"lat": -4.18, "lon": 121.61},
        "NODE-SULSEL-LUTIM-SOROWAKO-VALE": {"lat": -2.53, "lon": 121.35},
    }
    
    df_map9 = df_logistik.copy()
    df_map9["lat"] = df_map9["cluster_id"].map(lambda x: COORDS.get(x, {}).get("lat"))
    df_map9["lon"] = df_map9["cluster_id"].map(lambda x: COORDS.get(x, {}).get("lon"))
    df_map9["label"] = df_map9["anchor_entity"]
    
    import plotly.express as px
    status_color = {"terkonfirmasi": "#43A047", "terkonfirmasi_berbagi": "#FFA726"}
    
    fig_map9 = px.scatter_mapbox(
        df_map9, lat="lat", lon="lon", hover_name="label", hover_data={"port_detail": True, "psn_status": True, "lat": False, "lon": False},
        color="port_facility", color_discrete_map=status_color, size_max=15, zoom=5.5, center={"lat": -3.0, "lon": 121.7}, mapbox_style="carto-darkmatter", height=400,
    )
    fig_map9.update_traces(marker=dict(size=14))
    fig_map9.update_layout(margin=dict(l=0, r=0, t=10, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False)
    st.plotly_chart(fig_map9, use_container_width=True, config={'displayModeBar': False})

    # ── 9.2 Tabel Logistik ──
    st.markdown("**9.2 Ringkasan Klaster Logistik**")
    df_detail9 = df_logistik[["anchor_entity", "kabupaten", "port_facility", "psn_status", "pltu_mw", "export_channel"]].copy()
    df_detail9.columns = ["Perusahaan", "Kabupaten", "Pelabuhan", "Status PSN", "PLTU (MW)", "Tujuan Ekspor"]
    st.dataframe(df_detail9, use_container_width=True, hide_index=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# PAGE 10 — DEMOGRAFI & SOSIAL (dari file 11)
# ══════════════════════════════════════════════════════════
with st.expander("10 · DEMOGRAFI & SOSIAL", expanded=False):
    d10 = load_all_page10()
    df_demo, df_shift, df_pdrb = d10['demografi'], d10['shift'], d10['pdrb']
    
    df_demo["tahun"] = pd.to_numeric(df_demo["tahun"], errors="coerce")
    df_shift["tahun"] = pd.to_numeric(df_shift["tahun"], errors="coerce")
    
    sulteng_shift = df_shift[df_shift["provinsi"] == "Sulawesi Tengah"].sort_values("tahun")
    sulteng_first, sulteng_last = sulteng_shift.iloc[0], sulteng_shift.iloc[-1]
    
    shift_akhir = float(sulteng_last["agriculture_to_industry_shift_index"])
    pertanian_awal, pertanian_akhir = float(sulteng_first["pct_pdrb_pertanian_A"]), float(sulteng_last["pct_pdrb_pertanian_A"])
    industri_awal, industri_akhir = float(sulteng_first["pct_industri_tambang_BC"]), float(sulteng_last["pct_industri_tambang_BC"])
    
    smelter_kabs = sorted(df_demo[df_demo["is_smelter"] == True]["kabupaten"].unique())
    latest_year = int(df_demo[df_demo["tahun"] <= 2024]["tahun"].max())
    latest_demo = df_demo[df_demo["tahun"] == latest_year].copy()
    latest_smelter_density = latest_demo[latest_demo["is_smelter"] == True]["kepadatan_per_km2"].mean()
    latest_non_smelter_density = latest_demo[latest_demo["is_smelter"] == False]["kepadatan_per_km2"].mean()
    density_ratio = latest_smelter_density / latest_non_smelter_density if latest_non_smelter_density else 0
    dbd_smelter = int(df_demo[(df_demo["is_smelter"] == True) & (df_demo["tahun"] >= 2019)]["dbd_kasus"].sum())

    st.markdown('<div class="page-block">', unsafe_allow_html=True)
    st.markdown('<div class="page-hero">Guncangan Sosial & Pergeseran Ekonomi Agraris</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-essence">Hilirisasi mengubah struktur masyarakat: tekanan demografi & transisi ekonomi.</div>', unsafe_allow_html=True)
    st.page_link("pages/11_Demografi_Sosial.py", label="➜ Buka halaman penuh", icon="🔗")

    metric_strip([
        ("Shift Index Sulteng", f"{shift_akhir:.2f}×", "#EF5350"),
        ("Pertanian Sulteng", f"{pertanian_awal:.1f}% → {pertanian_akhir:.1f}%", "#F57C00"),
        ("Industri Sulteng", f"{industri_awal:.1f}% → {industri_akhir:.1f}%", "#D32F2F"),
        ("Kabupaten Ekstraktif", f"{len(smelter_kabs)}", "#43A047"),
        ("Rasio Kepadatan", f"{density_ratio:.2f}×", "#FFA726"),
        ("Kasus DBD (Ekstraktif)", f"{dbd_smelter:,}", "#EF5350"),
    ])
    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**10.1 Populasi Kabupaten Ekstraktif**")
        pop_smelter = df_demo[(df_demo["is_smelter"] == True) & (df_demo["tahun"] <= 2024)].copy()
        fig_pop = px.line(pop_smelter, x="tahun", y="jumlah_penduduk_rb", color="kabupaten", markers=True, height=350)
        fig_pop.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#B0BEC5"), margin=dict(l=0, r=0, t=10, b=0), showlegend=False)
        st.plotly_chart(fig_pop, use_container_width=True, config={'displayModeBar': False})

        st.markdown("**10.3 Pergeseran Shift Index (Pertanian ke Industri)**")
        fig_index = px.line(df_shift, x="tahun", y="agriculture_to_industry_shift_index", color="provinsi", markers=True, height=350)
        fig_index.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#B0BEC5"), margin=dict(l=0, r=0, t=10, b=0), showlegend=False)
        st.plotly_chart(fig_index, use_container_width=True, config={'displayModeBar': False})

    with c2:
        st.markdown("**10.2 Kepadatan Penduduk (Ekstraktif vs Non)**")
        density = df_demo[df_demo["tahun"] <= 2024].copy()
        density["Kategori"] = density["is_smelter"].map({True: "Industri Ekstraktif", False: "Non-Ekstraktif"})
        density_agg = density.groupby(["tahun", "Kategori"], as_index=False)["kepadatan_per_km2"].mean()
        fig_density = px.area(density_agg, x="tahun", y="kepadatan_per_km2", color="Kategori", height=350)
        fig_density.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#B0BEC5"), margin=dict(l=0, r=0, t=10, b=0), showlegend=False)
        st.plotly_chart(fig_density, use_container_width=True, config={'displayModeBar': False})

        st.markdown("**10.4 Rata-rata Kasus DBD (Ekstraktif vs Non)**")
        dbd = df_demo[df_demo["tahun"] >= 2019].copy()
        dbd["Kategori"] = dbd["is_smelter"].map({True: "Industri Ekstraktif", False: "Non-Ekstraktif"})
        dbd_agg = dbd.groupby(["tahun", "Kategori"], as_index=False)["dbd_kasus"].mean()
        fig_dbd = px.bar(dbd_agg, x="tahun", y="dbd_kasus", color="Kategori", barmode="group", height=350)
        fig_dbd.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#B0BEC5"), margin=dict(l=0, r=0, t=10, b=0), showlegend=False)
        st.plotly_chart(fig_dbd, use_container_width=True, config={'displayModeBar': False})

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Overview Temuan — CELIOS D3TLH")
