import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar

st.set_page_config(
    page_title="Progress Riset D3TLH — CELIOS",
    page_icon="refrensi/Celios China-Indonesia Energy Transition.png",
    layout="wide"
)

render_sidebar()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# ─── STYLE ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }

.page-title {
    font-size: 2rem; font-weight: 800;
    background: linear-gradient(135deg, #1B5E20, #43A047, #A5D6A7);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 0;
}
.page-subtitle {
    font-size: 0.95rem; color: #757575; font-weight: 300;
    margin-top: 0.25rem; margin-bottom: 1.5rem;
}
.status-card {
    background: #FFFFFF;
    border: 1px solid #2a2f3d;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.7rem;
}
.status-card h5 { margin: 0 0 0.3rem 0; font-size: 0.85rem; color: #B0BEC5; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
.status-card p  { margin: 0; font-size: 0.92rem; color: #111111; }
.badge-ready   { color: #66BB6A; font-weight: 700; }
.badge-partial { color: #FFA726; font-weight: 700; }
.badge-missing { color: #EF5350; font-weight: 700; }
.section-header {
    font-size: 1.1rem; font-weight: 700; color: #111111;
    border-bottom: 2px solid #2E7D32;
    padding-bottom: 0.4rem; margin: 1.8rem 0 1rem 0;
}
.note-box {
    background: #1A2F1C; border: 1px solid #2E7D3250;
    border-left: 3px solid #43A047;
    border-radius: 6px; padding: 0.8rem 1rem;
    font-size: 0.82rem; color: #A5D6A7;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown('<div class="page-title">Progress Riset — Evaluasi D3TLH Sulawesi</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">CELIOS Research Division · Update status pengumpulan data dan visualisasi awal · Juni 2026</div>', unsafe_allow_html=True)
st.markdown('<div class="note-box">Halaman ini menampilkan kondisi riset yang sedang berjalan. Dataset belum lengkap — visualisasi hanya mencerminkan data yang sudah berhasil diakuisisi hingga saat ini. Analisis final akan tersedia setelah seluruh dataset selesai dikumpulkan dan dibersihkan.</div>', unsafe_allow_html=True)

# ─── STATUS DATASET ───────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Status Pengumpulan Dataset</div>', unsafe_allow_html=True)

status_data = [
    {"Modul", "Sumber", "Variabel", "Cakupan", "Status", "Keterangan"},
]

cols = st.columns([2.5, 2.5, 4, 2.5])
headers = ["Modul Riset", "Sumber", "Variabel", "Cakupan Waktu"]
for col, h in zip(cols, headers):
    col.markdown(f"**{h}**")

st.markdown("<hr style='margin:0.3rem 0 0.5rem 0; border-color:#2a2f3d'>", unsafe_allow_html=True)

rows = [
    ("Ekspansi Industri",        "ESDM/Minerbaone",  "Izin Tambang (IUP/IUPK)",                  "2009–2026",  "siap",    ""),
    ("Ekspansi Industri",        "GEM Tracker",      "Smelter Nikel & PLTU",                      "2020–2026",  "siap",    ""),
    ("Ekspansi Industri",        "BPS API",          "Investasi PMDN per Provinsi",               "2016–2026",  "siap",    "6 Provinsi Sulawesi"),
    ("Kualitas Lingkungan",      "SIPSN KLHK",       "Kualitas Air, Udara, Limbah B3",            "2016–2026",  "belum",   "Akuisisi belum dimulai"),
    ("Kualitas Lingkungan",      "Geoportal KLHK",   "Deforestasi/Tutupan Lahan",                 "2016–2026",  "belum",   "Akuisisi belum dimulai"),
    ("Beban Kesehatan",          "Kemenkes PDF",     "Kasus ISPA, Diare, Malaria, Kusta",         "2014–2024",  "siap",    "Seluruh Indonesia"),
    ("Beban Kesehatan",          "Kemenkes PDF",     "Jumlah Puskesmas & Rumah Sakit",            "2014–2024",  "siap",    "Telah diagregasi se-Sulawesi"),
    ("Beban Kesehatan",          "Kemenkes PDF",     "Penyakit Kulit",                            "–",          "belum",   "Tidak tersedia di Profil Kesehatan"),
    ("Konflik Sosial",           "KPA TanahKita",    "Konflik Agraria (nasional)",                "2015–2024",  "parsial", "34 kasus terdeteksi di Sulawesi"),
    ("Konflik Sosial",           "YLBHI",            "Kriminalisasi Warga",                       "2016–2026",  "belum",   "Belum diakuisisi"),
    ("Distribusi Manfaat",       "BPS API",          "Investasi PMDN Sulawesi",                   "2016–2026",  "siap",    ""),
    ("Distribusi Manfaat",       "BPS/Kemendag",     "Nilai Ekspor per Sektor",                   "2016–2026",  "parsial", "Hanya Sulsel — perlu provinsi lain"),
    ("Distribusi Manfaat",       "DJPK Kemenkeu",    "PAD per Kab/Kota Sulawesi",                 "2016–2024",  "parsial", "5 provinsi terkumpul, 1 belum"),
]

badge = {"siap": "badge-ready", "parsial": "badge-partial", "belum": "badge-missing"}
label = {"siap": "Siap", "parsial": "Parsial", "belum": "Belum"}

for modul, sumber, variabel, cakupan, status, ket in rows:
    c1, c2, c3, c4 = st.columns([2.5, 2.5, 4, 2.5])
    c1.markdown(f"<small>{modul}</small>", unsafe_allow_html=True)
    c2.markdown(f"<small>{sumber}</small>", unsafe_allow_html=True)
    c3.markdown(f"<small>{variabel}</small>", unsafe_allow_html=True)
    c4.markdown(f"<small>{cakupan}</small>", unsafe_allow_html=True)

st.markdown("<hr style='margin:0.5rem 0 1.5rem 0; border-color:#2a2f3d'>", unsafe_allow_html=True)

# ─── VIZ 1: ISPA SULAWESI ─────────────────────────────────────────────────────
st.markdown('<div class="section-header">Tren Kasus ISPA — 6 Provinsi Sulawesi (2014–2024)</div>', unsafe_allow_html=True)
st.caption("Sumber: Kemenkes RI — Profil Kesehatan Indonesia. Data belum dibersihkan dan divalidasi penuh.")

SULAWESI = ["Sulawesi Utara", "Sulawesi Tengah", "Sulawesi Selatan",
            "Sulawesi Tenggara", "Gorontalo", "Sulawesi Barat"]

kemenkes_path = os.path.join(BASE_DIR, "data", "processed", "kemenkes_bersih_all.csv")
if os.path.exists(kemenkes_path):
    df_kes = pd.read_csv(kemenkes_path)
    df_ispa = df_kes[
        (df_kes["indikator"] == "Kasus ISPA/Pneumonia") &
        (df_kes["provinsi"].isin(SULAWESI))
    ].copy()
    df_ispa["tahun"] = df_ispa["tahun"].astype(int)
    df_ispa = df_ispa.sort_values("tahun")

    if not df_ispa.empty:
        fig_ispa = px.line(
            df_ispa, x="tahun", y="nilai", color="provinsi",
            markers=True,
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={"tahun": "Tahun", "nilai": "Jumlah Kasus", "provinsi": "Provinsi"},
        )
        fig_ispa.update_layout(
            plot_bgcolor="#111827", paper_bgcolor="#111827",
            font_color="#ECEFF1", font_size=12,
            legend=dict(orientation="h", y=-0.2),
            xaxis=dict(gridcolor="#1F2937", tickmode="linear", dtick=1),
            yaxis=dict(gridcolor="#1F2937"),
            margin=dict(l=20, r=20, t=30, b=20),
            hovermode="x unified",
        )
        st.plotly_chart(fig_ispa, use_container_width=True, config={'displayModeBar': False})
    else:
        st.warning("Data ISPA Sulawesi tidak ditemukan setelah filtering.")
else:
    st.error(f"File tidak ditemukan: {kemenkes_path}")

# ─── VIZ 2: INVESTASI PMDN ────────────────────────────────────────────────────
st.markdown('<div class="section-header">Realisasi Investasi PMDN — 6 Provinsi Sulawesi (2016–2026)</div>', unsafe_allow_html=True)
st.caption("Sumber: BPS WebAPI — Var 793 & 794. Data diekstrak langsung via API resmi BPS.")

pmdn_path = os.path.join(BASE_DIR, "data", "raw", "bps_pmdn", "bps_investasi_pmdn_sulawesi_2016_2026.csv")
if not os.path.exists(pmdn_path):
    pmdn_path = os.path.join(BASE_DIR, "data", "raw", "bps_pad", "bps_investasi_pmdn_sulawesi_2016_2026.csv")

if os.path.exists(pmdn_path):
    df_pmdn = pd.read_csv(pmdn_path)
    # Cari kolom relevan secara fleksibel
    col_prov = next((c for c in df_pmdn.columns if "provinsi" in c.lower() or "prov" in c.lower()), None)
    col_tahun = next((c for c in df_pmdn.columns if "tahun" in c.lower() or "year" in c.lower()), None)
    col_nilai = next((c for c in df_pmdn.columns if "nilai" in c.lower() or "value" in c.lower() or "realisasi" in c.lower()), None)

    if col_prov and col_tahun and col_nilai:
        df_pmdn[col_tahun] = df_pmdn[col_tahun].astype(int)
        df_pmdn[col_nilai] = pd.to_numeric(df_pmdn[col_nilai], errors="coerce")

        fig_pmdn = px.bar(
            df_pmdn.sort_values(col_tahun),
            x=col_tahun, y=col_nilai, color=col_prov,
            barmode="group",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            labels={col_tahun: "Tahun", col_nilai: "Nilai (Rp Juta)", col_prov: "Provinsi"},
        )
        fig_pmdn.update_layout(
            plot_bgcolor="#111827", paper_bgcolor="#111827",
            font_color="#ECEFF1", font_size=12,
            legend=dict(orientation="h", y=-0.25),
            xaxis=dict(gridcolor="#1F2937", tickmode="linear", dtick=1),
            yaxis=dict(gridcolor="#1F2937"),
            margin=dict(l=20, r=20, t=30, b=20),
        )
        st.plotly_chart(fig_pmdn, use_container_width=True, config={'displayModeBar': False})
    else:
        st.warning(f"Kolom tidak sesuai. Kolom tersedia: {list(df_pmdn.columns)}")
else:
    st.warning("File investasi PMDN tidak ditemukan.")

# ─── VIZ 3: IZIN TAMBANG SULAWESI ─────────────────────────────────────────────
st.markdown('<div class="section-header">Izin Tambang Aktif di Sulawesi — Distribusi per Komoditas</div>', unsafe_allow_html=True)
st.caption("Sumber: Minerbaone OSS (ESDM). Data mencakup IUP, IUPK, dan IPP aktif. Difilter untuk wilayah Sulawesi.")

KAB_SULAWESI_KEYWORDS = [
    "SULAWESI", "SULSEL", "SULTENG", "SULTRA", "SULUT", "GORONTALO", "SULBAR",
    "KONAWE", "KOLAKA", "KENDARI", "MOROWALI", "PALU", "MAMUJU", "POSO",
    "LUWU", "BONE", "GOWA", "MAROS", "MAKASSAR", "JENEPONTO", "BULUKUMBA",
    "PANGKAJENE", "DONGGALA", "SIGI", "PARIGI", "BANGGAI", "TOLITOLI",
    "BUOL", "GORONTALO", "BONE BOLANGO", "POHUWATO", "BOALEMO", "PASANGKAYU",
    "MAMASA", "POLEWALI", "MAJENE", "MAMUJU TENGAH"
]

permits_path = os.path.join(BASE_DIR, "data", "raw", "ESDM", "minerbaone_permits.csv")
if os.path.exists(permits_path):
    try:
        df_permits = pd.read_csv(permits_path, low_memory=False)
        df_permits["lokasi_upper"] = df_permits["lokasi_perizinan"].fillna("").str.upper()
        mask_sulawesi = df_permits["lokasi_upper"].str.contains(
            "|".join(KAB_SULAWESI_KEYWORDS), na=False
        )
        df_sul = df_permits[mask_sulawesi].copy()

        if not df_sul.empty:
            col_a, col_b = st.columns(2)

            with col_a:
                # Donut chart per komoditas
                komoditas_count = (
                    df_sul["komoditas"].fillna("Tidak Tercatat")
                    .value_counts().head(10).reset_index()
                )
                komoditas_count.columns = ["Komoditas", "Jumlah Izin"]
                fig_donut = px.pie(
                    komoditas_count, names="Komoditas", values="Jumlah Izin",
                    hole=0.45,
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    title="Top 10 Komoditas — Izin Tambang Sulawesi",
                )
                fig_donut.update_layout(
                    plot_bgcolor="#111827", paper_bgcolor="#111827",
                    font_color="#ECEFF1", font_size=11,
                    margin=dict(l=10, r=10, t=40, b=10),
                )
                st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})

            with col_b:
                # Tren penerbitan izin per tahun (berdasarkan tanggal_berlaku)
                df_sul["tahun_berlaku"] = pd.to_datetime(
                    df_sul["tanggal_berlaku"], errors="coerce"
                ).dt.year
                tren_izin = (
                    df_sul[df_sul["tahun_berlaku"].between(2010, 2026)]
                    .groupby("tahun_berlaku")
                    .size().reset_index(name="Jumlah Izin Baru")
                )
                fig_bar = px.bar(
                    tren_izin, x="tahun_berlaku", y="Jumlah Izin Baru",
                    color_discrete_sequence=["#43A047"],
                    title="Tren Penerbitan Izin Tambang per Tahun — Sulawesi",
                    labels={"tahun_berlaku": "Tahun"},
                )
                fig_bar.update_layout(
                    plot_bgcolor="#111827", paper_bgcolor="#111827",
                    font_color="#ECEFF1", font_size=11,
                    xaxis=dict(gridcolor="#1F2937", tickmode="linear", dtick=2),
                    yaxis=dict(gridcolor="#1F2937"),
                    margin=dict(l=10, r=10, t=40, b=10),
                )
                st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

            # Tabel ringkas
            with st.expander("Lihat data izin tambang Sulawesi (raw, belum final)"):
                tampil = df_sul[["nomor_izin", "jenis_perizinan", "tahap_kegiatan",
                                  "komoditas", "luas_ha", "tanggal_berlaku",
                                  "tanggal_berakhir", "lokasi_perizinan", "status_cnc"]].copy()
                tampil.columns = ["No. Izin", "Jenis", "Tahap", "Komoditas",
                                   "Luas (Ha)", "Berlaku", "Berakhir", "Lokasi", "Status CNC"]
                st.dataframe(tampil, use_container_width=True, height=300)
            st.caption(f"Total izin teridentifikasi di wilayah Sulawesi: **{len(df_sul):,}** entri")
        else:
            st.warning("Tidak ada izin tambang yang teridentifikasi di wilayah Sulawesi dari dataset ini.")
    except Exception as e:
        st.error(f"Gagal membaca data izin tambang: {e}")
else:
    st.warning("File minerbaone_permits.csv tidak ditemukan.")

# ─── VIZ 4: BEBAN KESEHATAN LAINNYA ──────────────────────────────────────────
st.markdown('<div class="section-header">Beban Kesehatan Lainnya — Sulawesi (2014–2024)</div>', unsafe_allow_html=True)
st.caption("Sumber: Kemenkes RI — Kasus Diare Dilayani, Kusta Baru, dan Malaria Positif.")

if os.path.exists(kemenkes_path):
    df_kes = pd.read_csv(kemenkes_path)
    df_other_kes = df_kes[
        (df_kes["indikator"].isin(["Kasus Diare Dilayani", "Kasus Kusta Baru", "Kasus Malaria Positif"])) &
        (df_kes["provinsi"].isin(SULAWESI))
    ].copy()
    
    if not df_other_kes.empty:
        df_other_kes["tahun"] = df_other_kes["tahun"].astype(int)
        
        # Agregasi total se-Sulawesi per tahun per indikator
        df_agg = df_other_kes.groupby(["tahun", "indikator"])["nilai"].sum().reset_index()
        df_agg = df_agg.sort_values("tahun")

        fig_kes = px.line(
            df_agg, x="tahun", y="nilai", color="indikator",
            markers=True,
            color_discrete_sequence=["#EF5350", "#FFA726", "#42A5F5"],
            labels={"tahun": "Tahun", "nilai": "Total Kasus (Sulawesi)", "indikator": "Jenis Penyakit"},
        )
        fig_kes.update_layout(
            plot_bgcolor="#111827", paper_bgcolor="#111827",
            font_color="#ECEFF1", font_size=12,
            legend=dict(orientation="h", y=-0.2),
            xaxis=dict(gridcolor="#1F2937", tickmode="linear", dtick=1),
            yaxis=dict(gridcolor="#1F2937", type="log"), # Pakai skala log karena Diare jauh lebih besar dari Kusta/Malaria
            margin=dict(l=20, r=20, t=30, b=20),
            hovermode="x unified",
        )
        st.plotly_chart(fig_kes, use_container_width=True, config={'displayModeBar': False})
        st.caption("*Catatan: Sumbu Y menggunakan skala logaritmik karena rentang jumlah kasus Diare yang sangat besar dibandingkan Kusta dan Malaria.")
    else:
        st.warning("Data kesehatan lainnya tidak ditemukan.")

# ─── VIZ 5: KONFLIK AGRARIA (KPA) ──────────────────────────────────────────────
st.markdown('<div class="section-header">Konflik Agraria (Nasional & Sulawesi)</div>', unsafe_allow_html=True)
st.caption("Sumber: KPA TanahKita. Kasus 1 Dekade Terakhir (2014–2024) & filter khusus Sulawesi.")

kpa_path = os.path.join(BASE_DIR, "data", "raw", "kpa_ylbhi_tanahkita", "tanahkita_konflik.csv")
if os.path.exists(kpa_path):
    try:
        df_kpa = pd.read_csv(kpa_path)
        
        # 1. Level Nasional (1 Dekade Terakhir)
        df_kpa_recent = df_kpa[df_kpa["tahun"] >= 2014].copy()
        nas_trend = df_kpa_recent.groupby("tahun").size().reset_index(name="Jumlah Kasus")
        fig_nas = px.bar(
            nas_trend, x="tahun", y="Jumlah Kasus",
            title=f"Tren Kasus Konflik Agraria Nasional (Total: {len(df_kpa)} Kasus)",
            color_discrete_sequence=["#EF5350"]
        )
        fig_nas.update_layout(
            plot_bgcolor="#111827", paper_bgcolor="#111827",
            font_color="#ECEFF1", font_size=11,
            xaxis=dict(gridcolor="#1F2937", tickmode="linear", dtick=2),
            yaxis=dict(gridcolor="#1F2937"),
            margin=dict(l=10, r=10, t=40, b=10),
        )
        st.plotly_chart(fig_nas, use_container_width=True, config={'displayModeBar': False})
        
        # 2. Level Sulawesi
        # Deteksi keyword sulawesi di judul atau deskripsi
        mask = df_kpa['judul'].str.lower().str.contains('|'.join(KAB_SULAWESI_KEYWORDS), na=False) | \
               df_kpa['deskripsi'].str.lower().str.contains('|'.join(KAB_SULAWESI_KEYWORDS), na=False)
               
        df_kpa_sul = df_kpa[mask].copy()
        
        if not df_kpa_sul.empty:
            c1, c2 = st.columns([3, 2])
            with c1:
                st.markdown(f"**Terdapat {len(df_kpa_sul)} Kasus Konflik Spesifik di Wilayah Sulawesi**")
                tampil_kpa = df_kpa_sul[["tahun", "judul", "lokasi", "status"]].sort_values("tahun", ascending=False)
                st.dataframe(tampil_kpa, use_container_width=True, height=250)
            with c2:
                status_count = df_kpa_sul["status"].fillna("Tidak Tercatat").value_counts().reset_index()
                status_count.columns = ["Status Lahan", "Jumlah Kasus"]
                fig_kpa_sul = px.bar(
                    status_count, x="Jumlah Kasus", y="Status Lahan",
                    orientation="h",
                    color_discrete_sequence=["#FFA726"],
                    title="Konflik Sulawesi (Berdasarkan Status Lahan)"
                )
                fig_kpa_sul.update_layout(
                    plot_bgcolor="#111827", paper_bgcolor="#111827",
                    font_color="#ECEFF1", font_size=11,
                    xaxis=dict(gridcolor="#1F2937", tickmode="linear", dtick=1),
                    yaxis=dict(gridcolor="#1F2937", categoryorder="total ascending"),
                    margin=dict(l=10, r=10, t=40, b=10),
                )
                st.plotly_chart(fig_kpa_sul, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("Tidak ada konflik agraria di Sulawesi yang terdeteksi.")
    except Exception as e:
        st.error(f"Gagal membaca data KPA: {e}")
else:
    st.warning("File tanahkita_konflik.csv tidak ditemukan.")


# ─── VIZ 6: KAPASITAS FASILITAS KESEHATAN ──────────────────────────────────────
st.markdown('<div class="section-header">Kapasitas Fasilitas Kesehatan — Sulawesi (2014–2024)</div>', unsafe_allow_html=True)
st.caption("Sumber: Kemenkes RI — Jumlah Rumah Sakit dan Puskesmas.")

faskes_path = os.path.join(BASE_DIR, "data", "processed", "faskes_sulawesi_agg.csv")
if os.path.exists(faskes_path):
    df_faskes = pd.read_csv(faskes_path)
    df_f_agg = df_faskes.groupby(["tahun", "jenis"])["jumlah"].sum().reset_index()
    
    if not df_f_agg.empty:
        fig_faskes = px.bar(
            df_f_agg, x="tahun", y="jumlah", color="jenis", barmode="group",
            color_discrete_sequence=["#26A69A", "#8D6E63"],
            labels={"tahun": "Tahun", "jumlah": "Total Unit (Sulawesi)", "jenis": "Faskes"},
            title="Tren Pertumbuhan Fasilitas Kesehatan"
        )
        fig_faskes.update_layout(
            plot_bgcolor="#111827", paper_bgcolor="#111827",
            font_color="#ECEFF1", font_size=12,
            legend=dict(orientation="h", y=-0.2),
            xaxis=dict(gridcolor="#1F2937", tickmode="linear", dtick=1),
            yaxis=dict(gridcolor="#1F2937"),
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_faskes, use_container_width=True, config={'displayModeBar': False})
else:
    st.info("Data agregrasi fasilitas kesehatan sedang diproses.")

# ─── VIZ 7: KELUHAN KESEHATAN UMUM ──────────────────────────────────────────────
st.markdown('<div class="section-header">Persentase Penduduk dengan Keluhan Kesehatan (2014–2024)</div>', unsafe_allow_html=True)
st.caption("Sumber: BPS — Persentase Penduduk yang Mempunyai Keluhan Kesehatan Selama Sebulan Terakhir.")

keluhan_path = os.path.join(BASE_DIR, "data", "raw", "bps_keluhanumum", "bps_kesehatan_provinsi_2014_2024.csv")
if os.path.exists(keluhan_path):
    df_keluhan = pd.read_csv(keluhan_path)
    df_kel_sul = df_keluhan[df_keluhan["provinsi"].isin(SULAWESI)].copy()
    
    if not df_kel_sul.empty:
        fig_keluhan = px.line(
            df_kel_sul, x="tahun", y="nilai", color="provinsi",
            markers=True,
            title="Tren Keluhan Kesehatan (Sulawesi)",
            labels={"tahun": "Tahun", "nilai": "Persentase (%)", "provinsi": "Provinsi"}
        )
        fig_keluhan.update_layout(
            plot_bgcolor="#111827", paper_bgcolor="#111827",
            font_color="#ECEFF1", font_size=12,
            xaxis=dict(gridcolor="#1F2937", tickmode="linear", dtick=1),
            yaxis=dict(gridcolor="#1F2937"),
            margin=dict(l=20, r=20, t=40, b=20),
            hovermode="x unified",
        )
        st.plotly_chart(fig_keluhan, use_container_width=True, config={'displayModeBar': False})
else:
    st.info("Data keluhan kesehatan belum diekstrak.")

# ─── VIZ 8: PENDAPATAN ASLI DAERAH (PAD) ──────────────────────────────────────
st.markdown('<div class="section-header">Pendapatan Asli Daerah (PAD) — Interim</div>', unsafe_allow_html=True)
st.caption("Sumber: BPS / DJPK. Menampilkan progres tarikan data PAD awal per provinsi.")

pad_path = os.path.join(BASE_DIR, "data", "raw", "bps_pad", "bps_pad_sulawesi_2016_2026.csv")
if os.path.exists(pad_path):
    try:
        df_pad = pd.read_csv(pad_path)
        # Ambil agregat per tahun per provinsi (rata-rata atau sum)
        df_pad_agg = df_pad.groupby(["tahun", "kategori"])["nilai_rupiah"].sum().reset_index()
        
        fig_pad = px.bar(
            df_pad_agg, x="tahun", y="nilai_rupiah", color="kategori",
            barmode="group",
            title="Nilai PAD Tercatat (Berdasarkan Kategori/Provinsi)",
            labels={"tahun": "Tahun", "nilai_rupiah": "Nilai (Satuan BPS)", "kategori": "Provinsi/Kategori"}
        )
        fig_pad.update_layout(
            plot_bgcolor="#111827", paper_bgcolor="#111827",
            font_color="#ECEFF1", font_size=12,
            xaxis=dict(gridcolor="#1F2937", tickmode="linear", dtick=1),
            yaxis=dict(gridcolor="#1F2937"),
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_pad, use_container_width=True, config={'displayModeBar': False})
        st.caption("*Catatan: Data masih bersifat raw dari API BPS (satuan bervariasi Juta/Rupiah) dan sedang dalam tahap standarisasi/cleaning.")
    except Exception as e:
        st.error(f"Gagal memuat grafik PAD: {e}")
else:
    st.info("Data PAD belum tersedia.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="font-size: 0.78rem; color: #616161; text-align: center;">
Progress Riset — Evaluasi D3TLH Sulawesi &nbsp;|&nbsp; CELIOS Research Division &nbsp;|&nbsp; Juni 2026<br>
Sumber: BPS WebAPI, Kemenkes RI, ESDM/Minerbaone OSS, KPA TanahKita &nbsp;|&nbsp;
Data belum final — dalam proses pengumpulan dan validasi
</div>
""", unsafe_allow_html=True)

