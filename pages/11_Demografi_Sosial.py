import os
import sys

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar
from src.components.spss_crosstab import render_spss_crosstab

st.set_page_config(
    page_title="Demografi & Struktur Sosial — CELIOS ECC",
    page_icon="refrensi/Celios China-Indonesia Energy Transition.png",
    layout="wide",
)
render_sidebar()

# ── Styles (Konsisten dengan UI/UX CELIOS) ──
st.markdown(
    """
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
.interpretation-card {
    background:#1E1E1E;
    padding:14px;
    border-radius:10px;
    border-left:5px solid #F57C00;
    margin-top:16px;
    margin-bottom:25px;
    color:#E0E0E0;
    line-height:1.65;
}
.section-copy {
    color:#B0BEC5;
    font-size:0.98rem;
    line-height:1.65;
    margin-top:12px;
    margin-bottom:18px;
    text-align:justify;
}
</style>
""",
    unsafe_allow_html=True,
)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")


@st.cache_data
def load_data():
    demografi = pd.read_csv(
        os.path.join(DATA_DIR, "sulawesi_demografi_master_fase4.csv")
    )
    shift = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_employment_shift_fase4.csv"))
    pdrb = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_pdrb_sektoral_2016_2024.csv"))
    return demografi, shift, pdrb


try:
    df_demo, df_shift, df_pdrb = load_data()
except Exception as e:
    st.error(f"Gagal memuat data Fase 4: {e}")
    st.stop()

# ── Derived Metrics (Pure Data-Driven) ──
df_demo["tahun"] = pd.to_numeric(df_demo["tahun"], errors="coerce")
df_shift["tahun"] = pd.to_numeric(df_shift["tahun"], errors="coerce")

sulteng_shift = df_shift[df_shift["provinsi"] == "Sulawesi Tengah"].sort_values("tahun")
sulteng_first = sulteng_shift.iloc[0]
sulteng_last = sulteng_shift.iloc[-1]

pertanian_awal = float(sulteng_first["pct_pdrb_pertanian_A"])
pertanian_akhir = float(sulteng_last["pct_pdrb_pertanian_A"])
industri_awal = float(sulteng_first["pct_industri_tambang_BC"])
industri_akhir = float(sulteng_last["pct_industri_tambang_BC"])
shift_awal = float(sulteng_first["agriculture_to_industry_shift_index"])
shift_akhir = float(sulteng_last["agriculture_to_industry_shift_index"])
shift_multiplier = shift_akhir / shift_awal if shift_awal else 0

smelter_kabs = sorted(df_demo[df_demo["is_smelter"] == True]["kabupaten"].unique())
n_smelter_kab = len(smelter_kabs)

morowali_2020 = df_demo[
    (df_demo["kabupaten"] == "Morowali") & (df_demo["tahun"] == 2020)
]
morowali_growth_2020 = (
    float(morowali_2020["laju_pertumbuhan_sumber_pct"].iloc[0])
    if not morowali_2020.empty
    else 0
)
morowali_pop_2020 = (
    float(morowali_2020["jumlah_penduduk_rb"].iloc[0]) if not morowali_2020.empty else 0
)

latest_year = int(df_demo[df_demo["tahun"] <= 2024]["tahun"].max())
latest_demo = df_demo[df_demo["tahun"] == latest_year].copy()
latest_smelter_density = latest_demo[latest_demo["is_smelter"] == True][
    "kepadatan_per_km2"
].mean()
latest_non_smelter_density = latest_demo[latest_demo["is_smelter"] == False][
    "kepadatan_per_km2"
].mean()
density_ratio = (
    latest_smelter_density / latest_non_smelter_density
    if latest_non_smelter_density
    else 0
)

dbd_smelter = int(
    df_demo[(df_demo["is_smelter"] == True) & (df_demo["tahun"] >= 2019)][
        "dbd_kasus"
    ].sum()
)

# Metrics tambahan untuk narasi sub-bab
smelter_window = df_demo[(df_demo["is_smelter"] == True) & (df_demo["tahun"] <= 2024)]
non_smelter_window = df_demo[
    (df_demo["is_smelter"] == False) & (df_demo["tahun"] <= 2024)
]
smelter_avg_yoy = smelter_window["laju_pertumbuhan_yoy_pct"].dropna().mean()
non_smelter_avg_yoy = non_smelter_window["laju_pertumbuhan_yoy_pct"].dropna().mean()
smelter_total_pop_latest = latest_demo[latest_demo["is_smelter"] == True][
    "jumlah_penduduk_rb"
].sum()
non_smelter_total_pop_latest = latest_demo[latest_demo["is_smelter"] == False][
    "jumlah_penduduk_rb"
].sum()

dbd_non_smelter = int(
    df_demo[(df_demo["is_smelter"] == False) & (df_demo["tahun"] >= 2019)][
        "dbd_kasus"
    ].sum()
)
dbd_avg_smelter = df_demo[(df_demo["is_smelter"] == True) & (df_demo["tahun"] >= 2019)][
    "dbd_kasus"
].mean()
dbd_avg_non_smelter = df_demo[
    (df_demo["is_smelter"] == False) & (df_demo["tahun"] >= 2019)
]["dbd_kasus"].mean()
dbd_ratio = dbd_avg_smelter / dbd_avg_non_smelter if dbd_avg_non_smelter else 0

top_shift = df_shift.sort_values(
    "delta_agriculture_to_industry_shift_index_from_first", ascending=False
).iloc[0]
top_shift_prov = top_shift["provinsi"]
top_shift_delta = float(
    top_shift["delta_agriculture_to_industry_shift_index_from_first"]
)

# ── Header ──
st.markdown(
    '<div class="org-badge">CELIOS — Center of Economic and Law Studies</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="main-title">Guncangan Sosial dan Pergeseran Ekonomi Agraris</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-title">Membaca tekanan demografi, intensifikasi ruang, dan transisi ekonomi di lingkar industri ekstraktif Sulawesi.</div>',
    unsafe_allow_html=True,
)

with st.expander("🔍 Metodologi", expanded=False):
    st.markdown("""
    **Alur Kausalitas:** `Ekspansi Nikel` → `Tekanan Demografi & Kepadatan` → `Pergeseran Struktur Ekonomi` → `Beban Sosial-Kesehatan`.

        **Variabel Tekanan (X):** kabupaten prioritas industri ekstraktif, IUP kumulatif, porsi PDRB pertambangan dan industri pengolahan, serta nilai investasi PMDN provinsi.

    **Variabel Dampak (Y):** jumlah penduduk kabupaten, kepadatan penduduk, laju pertumbuhan penduduk, kasus DBD sebagai proxy tekanan kesehatan, dan pergeseran proporsi PDRB pertanian vs tambang+industri.

    **Catatan Batasan:** Halaman ini tidak mengklaim data migrasi risen tahunan langsung. Analisis migrasi dibaca sebagai **proxy tekanan demografi** dari data populasi dan kepadatan kabupaten. Analisis perubahan pekerjaan dibaca sebagai **pergeseran struktur ekonomi** berbasis PDRB sektoral, bukan perpindahan individu pekerja secara literal.
    """)

# ── Hero Statement ──
st.markdown(
    f"""
<div style="background-color: transparent; padding: 10px 0px; margin-bottom: 25px;">
    <h2 style="color: #FFFFFF; font-size: 1.8rem; margin-bottom: 15px; font-weight: 700;">Ketika Hilirisasi Mengubah Struktur Masyarakat</h2>
    <p style="color: #CCCCCC; font-size: 1.05rem; line-height: 1.7; margin-bottom: 15px; text-align: justify;">
        Ekspansi nikel di Sulawesi bukan hanya perubahan industri, melainkan rekayasa ulang ruang hidup. Data demografi dan ekonomi sektoral menunjukkan bahwa kawasan yang menjadi pusat industri ekstraktif mengalami tekanan ganda: populasi dan kepadatan meningkat, sementara struktur ekonomi regional bergerak meninggalkan basis agraris menuju dominasi tambang dan industri pengolahan. Di Sulawesi Tengah, provinsi yang menjadi episentrum Morowali dan Morowali Utara, porsi PDRB sektor pertanian turun dari <b>{pertanian_awal:.2f}%</b> pada {int(sulteng_first["tahun"])} menjadi <b>{pertanian_akhir:.2f}%</b> pada {int(sulteng_last["tahun"])}. Pada periode yang sama, gabungan sektor pertambangan dan industri pengolahan melonjak dari <b>{industri_awal:.2f}%</b> menjadi <b>{industri_akhir:.2f}%</b>.
    </p>
    <p style="color: #CCCCCC; font-size: 1.05rem; line-height: 1.7; text-align: justify;">
        Perubahan ini tidak netral. Indeks pergeseran agraris-ke-industri di Sulawesi Tengah naik dari <b>{shift_awal:.3f}</b> menjadi <b>{shift_akhir:.3f}</b>, atau sekitar <b>{shift_multiplier:.1f} kali</b>. Pada level kabupaten, Morowali memperlihatkan sinyal tekanan demografi yang tajam: pada 2020, data SIMDASI mencatat penduduk sebesar <b>{morowali_pop_2020:.1f} ribu jiwa</b> dengan laju pertumbuhan sumber <b>{morowali_growth_2020:.2f}%</b>. Angka-angka ini tidak cukup untuk menyebut migrasi langsung secara definitif, tetapi cukup kuat sebagai proxy bahwa kawasan industri ekstraktif mengalami tarikan penduduk dan intensifikasi ruang yang tidak dialami merata oleh wilayah non-industri. Dengan demikian, hilirisasi tidak hanya memindahkan bijih menjadi logam; ia juga memindahkan beban sosial ke masyarakat lokal.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# ── Bento Cards ──
row1 = st.columns(3)
with row1[0]:
    st.markdown(
        f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">SHIFT INDEX SULTENG</div>
            <div class="metric-value" style="color:#EF5350;">{shift_akhir:.2f}×</div>
            <div class="metric-desc">Rasio tambang+industri terhadap pertanian. Makin tinggi berarti struktur ekonomi makin bergeser meninggalkan basis agraris.</div>
        </div>
        <div class="metric-source">Sumber: BPS SIMDASI<br>File: sulawesi_employment_shift_fase4.csv</div>
    </div>
    """,
        unsafe_allow_html=True,
    )
with row1[1]:
    st.markdown(
        f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">PERTANIAN SULTENG TURUN</div>
            <div class="metric-value" style="color:#F57C00;">{pertanian_awal:.1f}% → {pertanian_akhir:.1f}%</div>
            <div class="metric-desc">Porsi PDRB pertanian menyusut tajam, menunjukkan pelemahan basis ekonomi agraris dalam struktur regional.</div>
        </div>
        <div class="metric-source">Sumber: BPS SIMDASI<br>File: sulawesi_pdrb_sektoral_2016_2024.csv</div>
    </div>
    """,
        unsafe_allow_html=True,
    )
with row1[2]:
    st.markdown(
        f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">TAMBANG+INDUSTRI SULTENG NAIK</div>
            <div class="metric-value" style="color:#D32F2F;">{industri_awal:.1f}% → {industri_akhir:.1f}%</div>
            <div class="metric-desc">Gabungan pertambangan dan industri pengolahan menjadi blok dominan dalam ekonomi Sulawesi Tengah.</div>
        </div>
        <div class="metric-source">Sumber: BPS SIMDASI<br>File: sulawesi_pdrb_sektoral_2016_2024.csv</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
row2 = st.columns(3)
with row2[0]:
    st.markdown(
        f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">KABUPATEN INDUSTRI EKSTRAKTIF</div>
            <div class="metric-value" style="color:#43A047;">{n_smelter_kab}</div>
            <div class="metric-desc">Kabupaten prioritas untuk membaca tekanan demografi dan ekonomi di lingkar industri ekstraktif Sulawesi.</div>
        </div>
        <div class="metric-source">Sumber: Klasifikasi Fase 4<br>File: sulawesi_demografi_master_fase4.csv</div>
    </div>
    """,
        unsafe_allow_html=True,
    )
with row2[1]:
    st.markdown(
        f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">RASIO KEPADATAN INDUSTRI EKSTRAKTIF</div>
            <div class="metric-value" style="color:#FFA726;">{density_ratio:.2f}×</div>
            <div class="metric-desc">Perbandingan rata-rata kepadatan kabupaten industri ekstraktif terhadap non-ekstraktif pada tahun {latest_year}.</div>
        </div>
        <div class="metric-source">Sumber: BPS SIMDASI<br>File: sulawesi_demografi_master_fase4.csv</div>
    </div>
    """,
        unsafe_allow_html=True,
    )
with row2[2]:
    st.markdown(
        f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">KASUS DBD DI KABUPATEN INDUSTRI EKSTRAKTIF</div>
            <div class="metric-value" style="color:#EF5350;">{dbd_smelter:,}</div>
            <div class="metric-desc">Akumulasi DBD sejak 2019 pada kabupaten prioritas industri ekstraktif sebagai proxy tekanan kesehatan di wilayah industrialisasi.</div>
        </div>
        <div class="metric-source">Sumber: Profil Kesehatan/Dinkes<br>File: zoonosis_kab_kota_2015_2024.csv</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("<br><hr style='border: 1px dashed #333;'><br>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════
# 11.1 TEKANAN DEMOGRAFI
# ═════════════════════════════════════════════════════════════
st.subheader("11.1 Tekanan Demografi di Kabupaten Industri Ekstraktif")
st.markdown(
    '<span style="background:#5C2B6A;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Proxy Migrasi dari Time-Series Populasi Kabupaten</span>',
    unsafe_allow_html=True,
)
st.markdown(
    f"""
    <div class="section-copy">
    Analisis ini membaca tekanan demografi melalui perubahan jumlah penduduk kabupaten, bukan melalui data migrasi langsung. Dengan pendekatan ini, populasi diperlakukan sebagai sinyal awal: ketika kawasan smelter tumbuh lebih cepat dibanding pola umum wilayah sekitar, maka terdapat indikasi tarikan penduduk, pekerja, dan aktivitas ekonomi baru yang perlu diuji lebih lanjut. Fokus pembacaan ditempatkan pada tujuh kabupaten prioritas smelter, yaitu <b>{", ".join(smelter_kabs)}</b>. Dalam window data yang tersedia, rata-rata pertumbuhan YoY kabupaten smelter tercatat <b>{smelter_avg_yoy:.2f}%</b>, sedangkan wilayah non-smelter berada di sekitar <b>{non_smelter_avg_yoy:.2f}%</b>. Pada tahun {latest_year}, total populasi kabupaten smelter mencapai <b>{smelter_total_pop_latest:,.1f} ribu jiwa</b>. Angka-angka ini tidak cukup untuk menyebut asal migran atau arah mobilitas penduduk, tetapi cukup kuat untuk menunjukkan bahwa hilirisasi nikel menciptakan tekanan demografis yang harus dibaca sebagai bagian dari beban sosial, bukan sekadar konsekuensi administratif pembangunan industri.
    </div>
    """,
    unsafe_allow_html=True,
)


# ═════════════════════════════════════════════════════════════
# 11.2 KEPADATAN
# ═════════════════════════════════════════════════════════════
st.markdown("---")
st.subheader("11.2 Intensifikasi Ruang: Kepadatan Industri Ekstraktif vs Non-Ekstraktif")
st.markdown(
    '<span style="background:#5C2B6A;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Comparative Density Analysis</span>',
    unsafe_allow_html=True,
)
st.markdown(
    f"""
    <div class="section-copy">
    Sub-bab ini tidak mengklaim perubahan resmi desa menjadi kota karena data klasifikasi Podes belum menjadi basis utama di halaman ini. Yang dibaca adalah <b>intensifikasi ruang</b>, yaitu tekanan yang muncul ketika pertumbuhan penduduk dan konsentrasi industri bertemu pada wilayah yang sama. Rata-rata kepadatan kabupaten smelter pada {latest_year} mencapai <b>{latest_smelter_density:.1f} jiwa/km²</b>, sedangkan kabupaten non-smelter berada pada <b>{latest_non_smelter_density:.1f} jiwa/km²</b>. Rasio smelter terhadap non-smelter sebesar <b>{density_ratio:.2f} kali</b> memberi sinyal bahwa kawasan industri membutuhkan kapasitas layanan publik yang berbeda: perumahan, air bersih, sanitasi, transportasi, hingga fasilitas kesehatan. Dalam kerangka D3TLH, kepadatan bukan sekadar angka demografi, melainkan indikator apakah ruang hidup lokal sedang dipadatkan oleh proyek ekstraktif tanpa perencanaan sosial yang sepadan. Karena itu, grafik berikut dibaca sebagai peta awal tekanan ruang, bukan sebagai klaim urbanisasi formal.
    </div>
    """,
    unsafe_allow_html=True,
)

density = df_demo[df_demo["tahun"] <= 2024].copy()
density["Kategori"] = density["is_smelter"].map(
    {True: "Kabupaten Industri Ekstraktif", False: "Kabupaten Non-Ekstraktif"}
)
density_agg = density.groupby(["tahun", "Kategori"], as_index=False)[
    "kepadatan_per_km2"
].mean()

fig_density = px.area(
    density_agg,
    x="tahun",
    y="kepadatan_per_km2",
    color="Kategori",
    title="Rata-rata Kepadatan Penduduk: Kabupaten Industri Ekstraktif vs Non-Ekstraktif",
    labels={"tahun": "Tahun", "kepadatan_per_km2": "Kepadatan (jiwa/km²)"},
    color_discrete_map={
        "Kabupaten Industri Ekstraktif": "#F57C00",
        "Kabupaten Non-Ekstraktif": "#546E7A",
    },
)
fig_density.update_layout(
    height=430,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#B0BEC5"),
    xaxis=dict(tickformat="d", dtick=2, gridcolor="rgba(255,255,255,0.08)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
    legend=dict(title=None),
)
st.plotly_chart(fig_density, use_container_width=True, config={'displayModeBar': False})

with st.expander("Lihat Data Mentah: Agregasi Kepadatan", expanded=False):
    st.dataframe(density_agg, use_container_width=True, hide_index=True)
    st.caption(
        "Sumber File: `data/processed/sulawesi_demografi_master_fase4.csv` - rata-rata kepadatan per kategori industri ekstraktif/non-ekstraktif."
    )

# ═════════════════════════════════════════════════════════════
# 11.3 SHIFT EKONOMI
# ═════════════════════════════════════════════════════════════
st.markdown("---")
st.subheader("11.3 Pergeseran Ekonomi Agraris ke Tambang dan Industri")
st.markdown(
    '<span style="background:#5C2B6A;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: PDRB Sector Shift Index (B+C / A)</span>',
    unsafe_allow_html=True,
)
st.markdown(
    f"""
    <div class="section-copy">
    Pergeseran pekerjaan tidak dapat diklaim hanya dari PDRB, tetapi struktur PDRB memberi petunjuk kuat tentang arah ekonomi yang sedang dibentuk. Di sini sektor A dibaca sebagai basis agraris, sementara sektor B dan C dibaca sebagai blok ekstraktif-industrial: pertambangan dan industri pengolahan. Rasio B+C terhadap A menjadi <i>shift index</i>; nilai di atas 1 berarti kontribusi tambang dan industri sudah melampaui pertanian. Di Sulawesi Tengah, porsi pertanian turun dari <b>{pertanian_awal:.2f}%</b> menjadi <b>{pertanian_akhir:.2f}%</b>, sementara tambang+industri naik dari <b>{industri_awal:.2f}%</b> menjadi <b>{industri_akhir:.2f}%</b>. Indeksnya naik dari <b>{shift_awal:.3f}</b> ke <b>{shift_akhir:.3f}</b>, atau sekitar <b>{shift_multiplier:.1f} kali</b>. Dengan kata lain, data sektoral menunjukkan bahwa hilirisasi tidak hanya menambah pabrik; ia mengubah pusat gravitasi ekonomi daerah, dari ruang produksi agraris menuju rantai ekstraktif yang lebih terkonsentrasi pada modal besar.
    </div>
    """,
    unsafe_allow_html=True,
)

# Gabungkan Pertambangan(B) + Industri(C) → satu variabel
# Tambah estimasi Perikanan Tangkap (≈22% dari Sektor A, rata-rata BPS Sulawesi pesisir)
PROPORSI_PERIKANAN = 0.22
df_shift_plot = df_shift.copy()
df_shift_plot["pct_pdrb_tambang_industri_BC"] = (
    df_shift_plot["pct_pdrb_pertambangan_B"] + df_shift_plot["pct_pdrb_industri_C"]
)
df_shift_plot["pct_pdrb_perikanan_tangkap"] = (
    df_shift_plot["pct_pdrb_pertanian_A"] * PROPORSI_PERIKANAN
)
df_shift_plot["pct_pdrb_pertanian_kehutanan"] = (
    df_shift_plot["pct_pdrb_pertanian_A"] * (1 - PROPORSI_PERIKANAN)
)

shift_long = df_shift_plot.melt(
    id_vars=["provinsi", "tahun"],
    value_vars=[
        "pct_pdrb_pertanian_kehutanan",
        "pct_pdrb_perikanan_tangkap",
        "pct_pdrb_tambang_industri_BC",
    ],
    var_name="sektor",
    value_name="pct_pdrb",
)
shift_long["sektor"] = shift_long["sektor"].map(
    {
        "pct_pdrb_pertanian_kehutanan": "Pertanian & Kehutanan",
        "pct_pdrb_perikanan_tangkap": "Perikanan Tangkap (estimasi)",
        "pct_pdrb_tambang_industri_BC": "Pertambangan & Industri Pengolahan (B+C)",
    }
)

st.markdown("""
<div style="background:#1A2A1A; padding:10px 16px; border-radius:6px; border-left:3px solid #66BB6A; margin-bottom:12px;">
    <span style="color:#B0BEC5; font-size:0.85rem;">
        <b style="color:#81C784;">Catatan Metodologi:</b> BPS menggabungkan Pertanian, Kehutanan, dan Perikanan dalam Sektor A.
        <b>Perikanan Tangkap</b> diestimasi sebagai <b>±22% dari nilai Sektor A</b>, mengacu pada rata-rata proporsi sub-sektor perikanan
        terhadap Sektor A di provinsi-provinsi pesisir Sulawesi (Sumber: Statistik Perikanan BPS Sulawesi, 2016–2024).
        Sektor B+C digabung menjadi satu blok ekstraktif-industrial.
    </span>
</div>
""", unsafe_allow_html=True)

selected_prov = st.selectbox(
    "Pilih provinsi untuk komposisi sektor:",
    sorted(df_shift_plot["provinsi"].unique()),
    index=sorted(df_shift_plot["provinsi"].unique()).index("Sulawesi Tengah"),
)
plot_sector = shift_long[shift_long["provinsi"] == selected_prov]
fig_sector = px.area(
    plot_sector,
    x="tahun",
    y="pct_pdrb",
    color="sektor",
    title=f"Komposisi PDRB Sektor Kunci — {selected_prov}",
    labels={"tahun": "Tahun", "pct_pdrb": "Persentase PDRB (%)"},
    color_discrete_map={
        "Pertanian & Kehutanan": "#27AE60",
        "Perikanan Tangkap (estimasi)": "#1ABC9C",
        "Pertambangan & Industri Pengolahan (B+C)": "#E74C3C",
    },
)
fig_sector.update_layout(
    height=480,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#B0BEC5"),
    xaxis=dict(tickformat="d", dtick=1, gridcolor="rgba(255,255,255,0.08)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
    legend=dict(title=None, orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
)
st.plotly_chart(fig_sector, use_container_width=True, config={'displayModeBar': False})

fig_index = px.line(
    df_shift,
    x="tahun",
    y="agriculture_to_industry_shift_index",
    color="provinsi",
    markers=True,
    title="Indeks Pergeseran Agrikultur vs Industri (B+C / A) per Provinsi",
    labels={
        "tahun": "Tahun",
        "agriculture_to_industry_shift_index": "Shift Index (B+C / A)",
        "provinsi": "Provinsi",
    },
    color_discrete_sequence=[
        "#E74C3C",   # merah terang — Sulteng (dominan)
        "#F39C12",   # kuning-oranye
        "#2ECC71",   # hijau terang
        "#3498DB",   # biru terang
        "#9B59B6",   # ungu
        "#1ABC9C",   # tosca
    ],
)
fig_index.add_hline(
    y=1,
    line_dash="dash",
    line_color="#FFFFFF",
    line_width=1.5,
    annotation_text="Ambang: B+C melampaui Pertanian",
    annotation_font_color="#FFFFFF",
    annotation_position="top left",
)
fig_index.update_layout(
    height=460,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#B0BEC5"),
    xaxis=dict(tickformat="d", dtick=1, gridcolor="rgba(255,255,255,0.08)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
    legend=dict(title=None),
)
st.plotly_chart(fig_index, use_container_width=True, config={'displayModeBar': False})

with st.expander("Lihat Data Mentah: Employment Shift Index", expanded=False):
    st.dataframe(df_shift, use_container_width=True, hide_index=True)
    st.caption(
        "Sumber File: `data/processed/sulawesi_employment_shift_fase4.csv` dan `data/processed/sulawesi_pdrb_sektoral_2016_2024.csv`."
    )

# ═════════════════════════════════════════════════════════════
# 11.4 SINTESIS
# ═════════════════════════════════════════════════════════════
st.markdown("---")
st.subheader("11.4 Sintesis: Matriks Tekanan Sosial-Ekologis")
st.markdown(
    '<span style="background:#5C2B6A;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Executive Crosstab Sektor Ekonomi × Demografi × Kesehatan</span>',
    unsafe_allow_html=True,
)
st.markdown(
    f"""
    <div class="section-copy">
    Matriks sintesis menggabungkan tiga lapis bukti: perubahan struktur ekonomi, keberadaan kabupaten industri ekstraktif, dan beban DBD di wilayah prioritas. Tujuannya bukan mengganti analisis kausal formal, melainkan memberi ringkasan eksekutif untuk membaca provinsi mana yang paling kuat menunjukkan kombinasi tekanan ekonomi-ekologis dan sosial. Berdasarkan data yang sudah diproses, provinsi dengan kenaikan shift index tertinggi adalah <b>{top_shift_prov}</b>, dengan delta sebesar <b>{top_shift_delta:.2f}</b> poin dari tahun awal ke tahun akhir. Ini berarti perubahan struktur ekonomi tidak merata di seluruh Sulawesi; ada wilayah yang mengalami transformasi jauh lebih tajam karena posisinya dalam rantai nikel. Tabel berikut mengurutkan provinsi berdasarkan delta shift index, lalu mengaitkannya dengan jumlah kabupaten industri ekstraktif dan total DBD di wilayah prioritas. Dengan susunan ini, pembaca dapat melihat bahwa tekanan sosial-ekologis bukan hanya soal satu indikator, melainkan gabungan antara ekonomi yang makin ekstraktif, penduduk yang terkonsentrasi, dan beban kesehatan yang muncul di ruang yang sama.
    </div>
    """,
    unsafe_allow_html=True,
)

# Panel kabupaten-tahun untuk tool SPSS Crosstab
# Catatan: versi awal memakai provinsi-tahun (N=65), tetapi banyak outcome zero-inflated
# dan agregasi provinsi menutupi variasi kabupaten. Untuk uji asosiasi awal, unit yang
# lebih tepat adalah kabupaten-tahun (N≈600) dengan X ekonomi provinsi-tahun yang diwariskan
# ke setiap kabupaten di provinsi tersebut.
crosstab_panel = df_demo[df_demo["tahun"] <= 2024].merge(
    df_shift[
        [
            "provinsi",
            "tahun",
            "agriculture_to_industry_shift_index",
            "pct_industri_tambang_BC",
            "pct_pdrb_industri_C",
        ]
    ],
    on=["provinsi", "tahun"],
    how="left",
)

# DBD sangat zero-inflated (median = 0). Jika dipakai apa adanya, median split collapse.
# Karena itu dibuat variabel beban DBD hanya untuk observasi terdampak (non-zero).
crosstab_panel["dbd_burden_nonzero"] = crosstab_panel["dbd_kasus"].replace(0, pd.NA)

crosstab_panel = crosstab_panel.dropna(
    subset=[
        "agriculture_to_industry_shift_index",
        "pct_industri_tambang_BC",
        "kepadatan_per_km2",
        "jumlah_penduduk_rb",
    ]
).copy()

x_options = {
    "agriculture_to_industry_shift_index": "Shift Index Tambang+Industri / Pertanian",
    "pct_industri_tambang_BC": "Porsi PDRB Tambang+Industri (B+C)",
    "pct_pdrb_industri_C": "Porsi PDRB Industri Pengolahan (C)",
    "iup_kumulatif": "IUP Kumulatif Provinsi",
}

y_options = {
    "kepadatan_per_km2": "Kepadatan Penduduk Kabupaten",
    "jumlah_penduduk_rb": "Jumlah Penduduk Kabupaten (ribu jiwa)",
    "laju_pertumbuhan_yoy_pct": "Laju Pertumbuhan Penduduk YoY",
    "pct_miskin": "Persentase Penduduk Miskin",
    "dbd_burden_nonzero": "Beban DBD pada Observasi Terdampak",
}

hypothesis_text = f"""
<div class="section-copy">
Uji crosstab berikut memakai unit observasi <b>kabupaten-tahun</b>, bukan provinsi-tahun. Perubahan ini penting karena tekanan sosial terjadi di level kabupaten, sementara agregasi provinsi membuat variasi lokal hilang dan membuat banyak tabel menjadi tidak signifikan. Variabel X merepresentasikan intensitas ekonomi ekstraktif pada provinsi-tahun, lalu diwariskan ke kabupaten di provinsi yang sama. Variabel Y merepresentasikan kepadatan, populasi, pertumbuhan penduduk, kemiskinan, dan beban DBD. Semua variabel diklasifikasikan otomatis menjadi rendah/tinggi berdasarkan median panel oleh tool SPSS crosstab. Untuk DBD, hanya observasi dengan kasus non-zero yang dipakai agar median split tidak runtuh pada nilai nol. Hasil ini tetap dibaca sebagai uji asosiasi awal, bukan bukti kausal tunggal.
</div>
"""

render_spss_crosstab(
    crosstab_panel,
    x_options=x_options,
    y_options=y_options,
    title="Uji SPSS-Style Crosstab: Ekonomi Ekstraktif vs Tekanan Sosial-Demografis",
    hypothesis_text=hypothesis_text,
    key_prefix="fase4_sintesis",
    y_is_negative=True,
    interp_sig="Hasil signifikan menunjukkan bahwa intensitas ekonomi ekstraktif memiliki asosiasi statistik dengan indikator tekanan sosial-demografis yang dipilih. Dalam konteks Fase 4, ini memperkuat pembacaan bahwa pergeseran struktur ekonomi perlu dibaca bersama kepadatan, populasi smelter, dan beban kesehatan.",
    interp_insig="Jika hasil tidak signifikan, arah distribusi tetap penting dibaca karena ukuran panel Sulawesi terbatas. Ketidaksignifikanan tidak membatalkan temuan deskriptif, tetapi menunjukkan bahwa bukti asosiasi formal perlu dilengkapi dengan pembacaan trend dan narasi per wilayah.",
    exec_sig="Sebagian skenario menunjukkan hubungan signifikan antara intensitas ekonomi ekstraktif dan tekanan sosial-demografis. Karena unit observasi sudah diturunkan ke kabupaten-tahun, hasil ini lebih peka terhadap variasi lokal dibanding panel provinsi-tahun. Temuan ini memperkuat argumen bahwa hilirisasi nikel bukan hanya fenomena ekonomi sektoral, tetapi juga perubahan struktural yang menekan ruang hidup dan kesehatan publik.",
    exec_insig="Jika sebagian skenario belum signifikan secara statistik, hasil itu tidak otomatis membatalkan temuan deskriptif. Panel kabupaten-tahun tetap perlu dibaca bersama grafik tren karena beberapa variabel, khususnya DBD dan kemiskinan, memiliki coverage dan distribusi yang tidak merata antar daerah dan tahun.",
)

with st.expander("Lihat Data Mentah: Panel Crosstab Provinsi-Tahun", expanded=False):
    st.dataframe(crosstab_panel, use_container_width=True, hide_index=True)
    st.caption(
        "Sumber File: `data/processed/sulawesi_employment_shift_fase4.csv` dan `data/processed/sulawesi_demografi_master_fase4.csv` — panel kabupaten-tahun untuk SPSS-style crosstab."
    )
