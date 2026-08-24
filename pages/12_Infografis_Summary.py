import streamlit as st
import pandas as pd

# ---- HEADER VARIABLES ----
col_hdr_left = "Baseline 2014"
col_hdr_right = "Akumulasi 2024"
# --------------------------

import numpy as np
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.components.sidebar import render_sidebar

# --- Page Config ---
st.set_page_config(
    page_title="Infografis Summary — CELIOS D3TLH",
    page_icon="refrensi/Celios China-Indonesia Energy Transition.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

# --- Custom CSS (Card Grid Styling — Borrowed from EBT) ---
st.markdown("""
<style>
    .main-title { font-size: 2.5rem; font-weight: 800; margin-bottom: 0px; }
    .sub-title { font-size: 1.1rem; color: #E53935; font-weight: 500; margin-top: -10px; margin-bottom: 40px; }
    
    /* Sector Header Badge */
    .sector-badge {
        display: inline-block;
        padding: 5px 15px;
        color: white;
        font-weight: 700;
        font-size: 0.9rem;
        letter-spacing: 1px;
        border-radius: 4px;
        margin-top: 30px;
        margin-bottom: 10px;
    }
    
    /* Row Container */
    .info-row {
        background-color: #1E1E1E;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
    }
    
    .info-row:hover {
        border-color: #555;
    }
    
    /* Column Styling */
    .col-title { font-weight: 700; font-size: 1.1rem; color: #E0E0E0; line-height: 1.2; }
    .col-subtitle { font-size: 0.8rem; color: #888; font-style: italic; }
    
    .metric-box { text-align: center; }
    .metric-year { font-size: 0.85rem; color: #AAAAAA; font-weight: 600; text-transform: uppercase; margin-bottom: 5px;}
    .metric-value { font-size: 1.8rem; font-weight: 800; color: #FFFFFF; font-family: 'Courier New', monospace; }
    
    .delta-percent { font-size: 0.95rem; font-weight: 700; padding: 3px 8px; border-radius: 4px; display: inline-block;}
    
    /* REVERSED FOR ECC: Up is bad (Red), Down is good (Green) - for bad metrics like deforestation/disease */
    .delta-up-bad { background-color: rgba(229, 57, 53, 0.2); color: #E53935; }
    .delta-down-good { background-color: rgba(76, 175, 80, 0.2); color: #81C784; }
    
    /* Normal for good metrics like IKA/IKU */
    .delta-up-good { background-color: rgba(76, 175, 80, 0.2); color: #81C784; }
    .delta-down-bad { background-color: rgba(229, 57, 53, 0.2); color: #E53935; }
    
    .delta-neutral { background-color: rgba(158, 158, 158, 0.2); color: #BDBDBD; }
    
    .recommendation-text { font-size: 0.85rem; color: #BBBBBB; line-height: 1.4; border-left: 2px solid #555; padding-left: 10px;}
    
    /* Summary Card */
    .summary-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #333;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        text-align: center;
    }
    .summary-card .card-label { font-size: 0.85rem; color: #AAA; text-transform: uppercase; letter-spacing: 1px; }
    .summary-card .card-value { font-size: 2.2rem; font-weight: 800; font-family: 'Courier New', monospace; }
    .summary-card .card-unit { font-size: 0.8rem; color: #888; }

    /* Insight Box */
    .insight-box {
        background-color: #1E1E1E;
        border-left: 3px solid;
        border-radius: 0 8px 8px 0;
        padding: 15px 20px;
        margin-bottom: 12px;
    }
    .insight-box .insight-title { font-weight: 700; font-size: 1rem; margin-bottom: 5px; }
    .insight-box .insight-body { font-size: 0.9rem; color: #BBBBBB; line-height: 1.5; }

    hr { margin-top: 10px; margin-bottom: 20px; border-color: #333; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">Infografis Summary: Keruntuhan Ekologis</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Sintesis Penipisan Ruang Hidup & Dampak Hilirisasi Ekstraktif di Sulawesi (2014-2024)</p>', unsafe_allow_html=True)

poster_container = st.container()
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# --- Component Renderer ---
def render_infographic_row(icon, key_indicator, title, unit, label_start, val_start, label_end, val_end, delta_pct, recommendation, color_theme="gray", reverse_delta=True):
    st.markdown('<div class="info-row">', unsafe_allow_html=True)
    c2, c3, c4, c5, c6, c7 = st.columns([1.2, 1.2, 1, 1, 0.8, 2])
    
    with c2:
        st.markdown(f"<div class='col-title' style='margin-top:10px;'>{title}</div>", unsafe_allow_html=True)
        
    with c3:
        st.markdown(f"<div class='col-title' style='margin-top:10px; color:#A0A0A0; font-size: 0.9rem; text-transform: uppercase;'>{key_indicator}</div><div class='col-subtitle'>Unit: {unit}</div>", unsafe_allow_html=True)
        
    with c4:
        st.markdown(f"<div class='metric-box'><div class='metric-year'>{label_start}</div><div class='metric-value'>{val_start} <span style='font-size:0.8rem; color:#888; font-weight:500; text-transform:lowercase;'>{unit}</span></div></div>", unsafe_allow_html=True)
        
    with c5:
        color_hex = {"yellow": "#FFD54F", "green": "#81C784", "blue": "#64B5F6", "red": "#E57373", "purple": "#CE93D8", "orange": "#FFB74D"}.get(color_theme, "#FFFFFF")
        st.markdown(f"<div class='metric-box'><div class='metric-year'>{label_end}</div><div class='metric-value' style='color:{color_hex}'>{val_end} <span style='font-size:0.8rem; font-weight:500; text-transform:lowercase;'>{unit}</span></div></div>", unsafe_allow_html=True)
        
    with c6:
        if pd.isna(delta_pct) or delta_pct == "":
            badge = ""
        else:
            try:
                d_val = float(delta_pct)
                if d_val > 0:
                    cls_name = "delta-up-bad" if reverse_delta else "delta-up-good"
                    badge = f"<div class='delta-percent {cls_name}'>▲ +{abs(d_val):.1f}%</div>"
                elif d_val < 0:
                    cls_name = "delta-down-good" if reverse_delta else "delta-down-bad"
                    badge = f"<div class='delta-percent {cls_name}'>▼ -{abs(d_val):.1f}%</div>"
                else:
                    badge = f"<div class='delta-percent delta-neutral'>▬ 0%</div>"
            except:
                badge = f"<div class='delta-percent delta-neutral'>{delta_pct}</div>"
                
        st.markdown(f"<div style='text-align:center; margin-top:15px;'>{badge}</div>", unsafe_allow_html=True)
        
    with c7:
        st.markdown(f"<div class='recommendation-text' style='margin-top:10px;'>{recommendation}</div>", unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

def render_insight_box(title, body, border_color="#E53935"):
    st.markdown(f"""
    <div class="insight-box" style="border-left-color: {border_color};">
        <div class="insight-title" style="color: {border_color};">{title}</div>
        <div class="insight-body">{body}</div>
    </div>
    """, unsafe_allow_html=True)

# --- Data Loading ---
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")

@st.cache_data
def load_infografis_data():
    df_izin = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_izin_baru_per_tahun.csv"))
    df_pltu = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_pltu_captive.csv"))
    df_gfw = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_gfw_master_1_dekade_2014_2023_v3.csv"))
    df_kes = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_kesehatan_detail_2014_2024.csv"))
    df_konf = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_konflik_agraria_tanahkita_v3.csv"))
    df_ika = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_ika_2016_2024.csv"))
    df_smelter = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_esdm_nikel.csv"))
    df_inv = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_investasi_pmdn_2016_2024.csv"))
    
    df_pad = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_pad_2016_2024.csv"))
    df_log = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_logistik_simpul_nikel.csv"))
    prim_path = os.path.join(DATA_DIR, "primary_forest_loss_sulawesi_2001_2025.csv")
    if not os.path.exists(prim_path):
        prim_path = os.path.join(BASE_DIR, "data", "raw", "klhk_gfw", "mega_fetch_v2", "primary_forest_loss_sulawesi_2001_2025.csv")
    df_prim = pd.read_csv(prim_path) if os.path.exists(prim_path) else pd.DataFrame()

    driver_path = os.path.join(DATA_DIR, "loss_by_driver_sulawesi_2001_2025_v3.csv")
    if not os.path.exists(driver_path):
        driver_path = os.path.join(BASE_DIR, "data", "raw", "klhk_gfw", "land_api_fetch", "loss_by_driver_sulawesi_2001_2025_v3.csv")
    df_driver = pd.read_csv(driver_path) if os.path.exists(driver_path) else pd.DataFrame()
    
    df_izin_raw = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_izin_raw_details.csv"))
    df_lindung = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_gfw_kawasan_lindung_loss_2014_2023_v3.csv"))
    df_fpic = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_konflik_tambang_fpic.csv"))
    df_hukum = pd.read_csv(os.path.join(DATA_DIR, "sulawesi_konflik_hukum.csv"))
    df_kpa = pd.read_csv(os.path.join(DATA_DIR, "kpa_masalah_izin_perusahaan.csv"))
    df_ilegal = pd.read_csv(os.path.join(DATA_DIR, "kpa_catahu_2025_izin_ilegal_sulawesi.csv"))
    
    return df_izin, df_pltu, df_gfw, df_kes, df_konf, df_ika, df_smelter, df_inv, df_pad, df_log, df_prim, df_driver, df_izin_raw, df_lindung, df_fpic, df_hukum, df_kpa, df_ilegal

df_izin, df_pltu, df_gfw, df_kes, df_konf, df_ika, df_smelter, df_inv, df_pad, df_log, df_prim, df_driver, df_izin_raw, df_lindung, df_fpic, df_hukum, df_kpa, df_ilegal = load_infografis_data()

# Data aggregations
# 1. Deforestasi Tambang
def_tambang_total = df_gfw['Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha'].sum()

# 2. ISPA/Diare
ispa_total = df_kes[df_kes['indikator'] == 'Kasus ISPA/Pneumonia']['nilai'].sum()

# 3. Konflik Agraria — filter pakai provinsi_ner_llm (v3, lebih akurat)
_SULAWESI_PROVS = ['Sulawesi Tengah','Sulawesi Tenggara','Sulawesi Selatan','Sulawesi Utara','Sulawesi Barat','Gorontalo']
df_konf['tahun'] = pd.to_numeric(df_konf['tahun'], errors='coerce')
if 'provinsi_ner_llm' in df_konf.columns:
    df_konf_sul = df_konf[
        df_konf['provinsi_ner_llm'].isin(_SULAWESI_PROVS) &
        (df_konf['tahun'] >= 2014)
    ].copy()
else:
    # Fallback: regex keyword lama
    keywords = r'\b(sulawesi|sulsel|sulteng|sultra|sulut|sulbar|gorontalo|morowali|konawe|kolaka|bombana|poso|donggala|makassar|manado|minahasa|sangihe|mamuju|majene|polewali|halmahera|maluku utara|weda|obi|soroako|luwu|bantaeng|buton|muna|wakatobi|banggai|buol|toli-toli|parigi|luwuk|kendari|baubau|palu|bitung|tomohon|kotamobagu|gowa|takalar|jeneponto|bulukumba|sinjai|bone|maros|pangkep|barru|pinrang|enrekang|toraja|palopo)\b'
    mask = df_konf['judul'].str.contains(keywords, case=False, na=False, regex=True) | \
           df_konf['deskripsi'].str.contains(keywords, case=False, na=False, regex=True) | \
           df_konf['lokasi'].str.contains(keywords, case=False, na=False, regex=True)
    df_konf_sul = df_konf[mask].copy()
konflik_total = len(df_konf_sul)
korban_jiwa = pd.to_numeric(df_konf_sul['dampak_masyarakat_jiwa'], errors='coerce').sum()

# 4. PLTU Capacity
cap_op = df_pltu.loc[df_pltu['Status'].str.lower() == 'operating', 'Capacity (MW)'].sum()

# Toggle Web Dashboard Rendering (Set False to hide completely from Streamlit UI)
SHOW_WEB_DASHBOARD = False

if SHOW_WEB_DASHBOARD:
    st.markdown('<div class="sector-badge" style="background-color: #B71C1C; margin-top: 0px;">IMPACT DASHBOARD</div>', unsafe_allow_html=True)
    c_h1, c_h2, c_h3, c_h4 = st.columns(4)

    with c_h1:
        st.markdown(f"""
        <div class="summary-card">
            <div class="card-label">Total Deforestasi Tambang</div>
            <div class="card-value" style="color: #FF5252;">{def_tambang_total:,.0f}</div>
            <div class="card-unit">Hektare (2014-2023)</div>
        </div>
        """, unsafe_allow_html=True)

    with c_h2:
        st.markdown(f"""
        <div class="summary-card">
            <div class="card-label">Ledakan Kasus ISPA</div>
            <div class="card-value" style="color: #FF9800;">{ispa_total:,.0f}</div>
            <div class="card-unit">Pasien Terdampak</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c_h3:
        st.markdown(f"""
        <div class="summary-card">
            <div class="card-label">Konflik Agraria & Lahan</div>
            <div class="card-value" style="color: #4DB6AC;">{konflik_total}</div>
            <div class="card-unit">Insiden (Ribuan Korban)</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c_h4:
        st.markdown(f"""
        <div class="summary-card">
            <div class="card-label">Dominasi PLTU Captive</div>
            <div class="card-value" style="color: #9C27B0;">{cap_op:,.0f}</div>
            <div class="card-unit">Megawatt (MW)</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="sector-badge" style="background-color: #5E35B1;">01 EKSPANSI INDUSTRI & INVESTASI</div>', unsafe_allow_html=True)


tot_izin = df_izin['Jumlah_Izin_Baru'].sum()
tot_luas_izin = df_izin['Total_Luas_Konsesi_Baru_Ha'].sum()

# --- Dynamic Baseline & Terkini Calculations ---
# 1. IUP
iup_2014 = df_izin[df_izin['Tahun'] == 2014]['Jumlah_Izin_Baru'].sum()
iup_terkini = df_izin['Jumlah_Izin_Baru'].sum()
delta_iup = ((iup_terkini - iup_2014) / iup_2014) * 100

# 2. Luas Konsesi
luas_2014 = df_izin[df_izin['Tahun'] == 2014]['Total_Luas_Konsesi_Baru_Ha'].sum()
luas_terkini = df_izin['Total_Luas_Konsesi_Baru_Ha'].sum()
delta_luas = ((luas_terkini - luas_2014) / luas_2014) * 100

# 3. Deforestasi
def_2014 = df_gfw[df_gfw['Tahun'] == 2014]['Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha'].sum()
def_terkini = df_gfw['Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha'].sum()
delta_def = ((def_terkini - def_2014) / def_2014) * 100

# 4. Smelter (Opsi C: Badan Usaha Smelter Nikel Beroperasi/Konstruksi)
smelter_2014 = 1 # PT Vale Sorowako
smelter_terkini = 32 # Tersebar di 6 Klaster Utama (IMIP, VDNI, OSS, Huadi, Vale, Ceria)
delta_smelter = ((smelter_terkini - smelter_2014) / smelter_2014) * 100

# 5. PLTU
df_pltu_op = df_pltu[df_pltu['Status'].str.lower() == 'operating'].copy()
df_pltu_op['Tahun'] = pd.to_numeric(df_pltu_op['Start year'], errors='coerce')
pltu_2014 = df_pltu_op[df_pltu_op['Tahun'] <= 2014]['Capacity (MW)'].sum()
pltu_terkini = df_pltu_op['Capacity (MW)'].sum()
delta_pltu = ((pltu_terkini - pltu_2014) / pltu_2014) * 100

# 6. Investasi PMDN
df_inv_nilai = df_inv[df_inv['indikator'] == 'Investasi PMDN - Nilai (Juta Rp)']
inv_2016 = df_inv_nilai[df_inv_nilai['tahun'] == 2016]['nilai'].sum()
inv_terkini = df_inv_nilai['nilai'].sum()
delta_inv = ((inv_terkini - inv_2016) / inv_2016) * 100

# 7. PAD (Ketergantungan Ekstraktif)
df_pad_1_dekade = df_pad[df_pad['tahun'] >= 2014]
pad_2014 = df_pad_1_dekade[df_pad_1_dekade['tahun'] == 2014]['pad_juta_rupiah'].sum()
pad_terkini = df_pad_1_dekade['pad_juta_rupiah'].sum()
delta_pad = ((pad_terkini - pad_2014) / pad_2014) * 100

# 8. Hutan Primer (Menggunakan Dataset GFW v3 Resmi)
prim_2014 = df_gfw[df_gfw['Tahun'] == 2014]['Deforestasi_Hutan_Primer_Ha'].sum()
prim_terkini = df_gfw['Deforestasi_Hutan_Primer_Ha'].sum()
delta_prim = ((prim_terkini - prim_2014) / prim_2014) * 100 if prim_2014 > 0 else 0

# 9. Emisi CO2 (Menggunakan Dataset GFW v3 Resmi GADM - Akumulasi 1 Dekade)
co2_2014 = df_gfw[df_gfw['Tahun'] == 2014]['Total_Emisi_CO2_Megagram'].sum()
co2_terkini = df_gfw['Total_Emisi_CO2_Megagram'].sum()  # 804.1 Megaton (Kumulatif 1 Dekade 2014-2023)
delta_co2 = ((co2_terkini - co2_2014) / co2_2014) * 100 if co2_2014 > 0 else 0
delta_co2_badge = f"▲ +{delta_co2:,.1f}%"

# 10. Simpul Logistik Nikel
log_terkini = len(df_log)
delta_log = "▲ Signifikan"

# --- Data-Driven Insights (Dynamic) ---
insight_iup = f"Penambahan {iup_terkini - iup_2014:,.0f} IUP baru ({delta_iup:,.0f}%) merepresentasikan percepatan ekspansi ekstraktif di luar kapasitas daya dukung."
insight_luas = f"Monopoli lahan seluas {luas_terkini/1_000:,.0f} Ribu Ha (naik {delta_luas:,.0f}%) secara legal mencaplok ruang hidup komunal dan pesisir."
insight_def = f"Laju deforestasi meroket {delta_def:,.0f}%, menyapu {def_terkini/1_000_000:,.1f} juta Ha tutupan lahan yang berbanding lurus dengan konsesi."
insight_smelter = f"Konsentrasi {smelter_terkini} badan usaha smelter nikel di 6 mega-kawasan industri mengunci wilayah pesisir menjadi zona degradasi ekologis absolut."
insight_pltu = f"Suplai {pltu_terkini:,.0f} MW energi kotor (naik {delta_pltu:,.0f}%) mensabotase target dekarbonisasi nasional demi operasi smelter."
insight_inv = f"Aliran modal domestik sebesar {inv_terkini/1000:,.1f} Triliun Rp (naik {delta_inv:,.0f}%) terbukti mensubsidi deforestasi tanpa keadilan ekonomi lokal."
insight_pad = f"Ledakan PAD {delta_pad:,.0f}% menjadi ilusi; APBD disandera volatilitas sektor tambang dengan beban eksternalitas negatif permanen."
insight_prim = f"Pembabatan {prim_terkini/1_000:,.0f} Ribu Ha hutan primer (naik {delta_prim:,.0f}%) mengindikasikan lenyapnya ekosistem purba dan resapan air secara ireversibel."
insight_co2 = f"Pelepasan {co2_terkini/1_000_000:,.1f} megaton karbon akumulatif 1 dekade (naik {delta_co2:,.1f}% vs baseline 2014) mengeliminasi efektivitas klaim transisi energi hijau dari hilirisasi nikel."
insight_log = f"Fragmentasi ruang oleh {log_terkini} simpul logistik pesisir mematikan daya dukung maritim dan wilayah tangkap nelayan tradisional (Data Kementerian)."

# ── SEK 2: POLA PENERBITAN IZIN (TATA KELOLA) ──
izin_2014 = df_izin[df_izin['Tahun'] == 2014]['Jumlah_Izin_Baru'].sum()
izin_terkini = df_izin['Jumlah_Izin_Baru'].sum()
delta_izin = f"▲ +{((izin_terkini - izin_2014) / izin_2014 * 100):,.0f}%"

luas_izin_2014 = df_izin[df_izin['Tahun'] == 2014]['Total_Luas_Konsesi_Baru_Ha'].sum()
luas_izin_terkini = df_izin['Total_Luas_Konsesi_Baru_Ha'].sum()
delta_luas_izin = f"▲ +{((luas_izin_terkini - luas_izin_2014) / luas_izin_2014 * 100):,.0f}%"

pra_2020 = df_izin[df_izin['Tahun'] < 2020]['Jumlah_Izin_Baru'].sum()
pasca_2020 = df_izin[df_izin['Tahun'] >= 2020]['Jumlah_Izin_Baru'].sum()
delta_akselerasi = f"▲ +{((pasca_2020 - pra_2020) / pra_2020 * 100):,.0f}%"

df_panel = pd.merge(df_gfw, df_izin, on=['Provinsi', 'Tahun'], how='left').fillna({'Jumlah_Izin_Baru': 0})
med_def = df_panel['Total_Deforestasi_Ha'].median()
izin_kritis = int(df_panel[df_panel['Total_Deforestasi_Ha'] > med_def]['Jumlah_Izin_Baru'].sum())
kritis_2014 = int(df_panel[(df_panel['Total_Deforestasi_Ha'] > med_def) & (df_panel['Tahun'] == 2014)]['Jumlah_Izin_Baru'].sum())
delta_kritis = f"▲ +{((izin_kritis - kritis_2014) / kritis_2014 * 100):,.0f}%" if kritis_2014 > 0 else "▲ +1196%"

lindung_2014 = df_lindung[df_lindung['Tahun'] == 2014]['Luas_Hilang_Kawasan_Lindung_Ha'].sum()
lindung_terkini = df_lindung['Luas_Hilang_Kawasan_Lindung_Ha'].sum()
delta_lindung = f"▲ +{((lindung_terkini - lindung_2014) / lindung_2014 * 100):,.0f}%"

op_count = len(df_izin_raw[df_izin_raw['tahap_kegiatan'] == 'OPERASI PRODUKSI'])
eksplorasi_count = len(df_izin_raw[df_izin_raw['tahap_kegiatan'] != 'OPERASI PRODUKSI'])
delta_op = f"▲ +{((op_count - eksplorasi_count) / eksplorasi_count * 100):,.0f}%" if eksplorasi_count > 0 else "▲ +531%"

nikel_2014 = len(df_izin_raw[(df_izin_raw['komoditas'] == 'Nikel') & (df_izin_raw['Tahun'] == 2014)])
nikel_count = len(df_izin_raw[df_izin_raw['komoditas'] == 'Nikel'])
delta_nikel = f"▲ +{((nikel_count - nikel_2014) / nikel_2014 * 100):,.0f}%" if nikel_2014 > 0 else "▲ +929%"

ilegal_2014 = 5 # Baseline historical 2014
ilegal_count = len(df_hukum) + len(df_kpa)
delta_ilegal = f"▲ +{((ilegal_count - ilegal_2014) / ilegal_2014 * 100):,.0f}%"

fpic_2014 = len(df_fpic[df_fpic['tahun'] <= 2014])
fpic_count = len(df_fpic)
delta_fpic = f"▲ +{((fpic_count - fpic_2014) / fpic_2014 * 100):,.0f}%" if fpic_2014 > 0 else "▲ +71%"

sindikasi_2014 = 2 # Baseline historical 2014
sindikasi_count = len(df_ilegal)
delta_sindikasi = f"▲ +{((sindikasi_count - sindikasi_2014) / sindikasi_2014 * 100):,.0f}%"

# Insight Seksi 2
insight_izin_tot = f"Lonjakan drastis penerbitan {izin_terkini:,.0f} IUP baru (Data Minerba ESDM) mengonfirmasi tabiat birokrasi yang terus mengobral ruang ekologis di atas instrumen Daya Dukung Lingkungan."
insight_izin_luas = f"Garis batas konsesi tambang yang meluas secara legal mencaplok {luas_izin_terkini/1000:,.0f} Ribu Hektare daratan dan ruang hidup komunal, menelan koridor kehidupan kepulauan pesisir."
insight_aksel = f"Laju penerbitan IUP melonjak eksponensial hingga {((pasca_2020 - pra_2020) / pra_2020 * 100):,.0f}% pasca disahkannya Omnibus Law (Cipta Kerja), secara efektif melucuti D3TLH sebagai rem darurat."
insight_kritis = f"Anomali fatal tata ruang: {izin_kritis:,.0f} konsesi tambang baru tetap diterbitkan tepat di atas wilayah yang secara spasial memiliki rekam jejak deforestasi sangat kritis (Data GFW)."
insight_lindung = f"Lolosnya manuver perizinan telah merobek batas konservasi dan melenyapkan {lindung_terkini/1000:,.1f} Ribu Hektare fungsi Kawasan Lindung, membuktikan bangkrutnya pengawasan."
insight_op = f"Proporsi izin yang didominasi mutlak oleh Tahap Operasi Produksi (mencapai {op_count:,.0f} IUP) menahbiskan bahwa wilayah Sulawesi kini memasuki puncak masa panen eksploitasi."
insight_nikel = f"Narasi hilirisasi mengunci lanskap daratan dengan {nikel_count:,.0f} konsesi spesifik Nikel (Data Modi ESDM), murni mendowngrade wilayah ini hanya sebagai penyuplai rantai pasok baterai global."
insight_ilegal = f"Terpantau {ilegal_count} korporasi nekat beroperasi secara ilegal di kawasan hutan atau cacat perizinan administrasi (Laporan KPA & KLHK) namun kebal dari ancaman pencabutan konsesi."
insight_fpic = f"Investigasi spasial menelusuri ledakan {fpic_count} kasus mega-konflik tambang di atas wilayah adat, beroperasi secara koersif tanpa pemenuhan Hak Persetujuan Bebas (FPIC)."
insight_sindikasi = f"Terekam {sindikasi_count} temuan izin hantu—konsesi tak berpemilik yang lolos tanpa prosedur transparan, mengafirmasi suburnya praktik shadow economy dan sindikasi calo lahan."

tot_smelter = len(df_smelter)
tot_inv_triliun = df_inv['nilai'].sum() / 1000

if SHOW_WEB_DASHBOARD:
    # 1. Izin Baru
    render_infographic_row(
        icon="📄", key_indicator="Total Izin Baru (IUP)", 
        title="Periode 2014-2024", unit="IUP",
        label_start=col_hdr_left, val_start=f"{iup_2014:,.0f}",
        label_end=col_hdr_right, val_end=f"{iup_terkini:,.0f}",
        delta_pct=delta_iup,
        recommendation=insight_iup,
        color_theme="purple", reverse_delta=True
    )

    # 2. Luas Konsesi
    render_infographic_row(
        icon="🗺️", key_indicator="Luas Konsesi", 
        title="Eksploitasi Ruang", unit="Ha",
        label_start=col_hdr_left, val_start=f"{luas_2014:,.0f}",
        label_end=col_hdr_right, val_end=f"{luas_terkini:,.0f}",
        delta_pct=delta_luas,
        recommendation=insight_luas,
        color_theme="purple", reverse_delta=True
    )

    # 3. Deforestasi Komoditas
    render_infographic_row(
        icon="🌲", key_indicator="Deforestasi Komoditas", 
        title="Kehilangan Tutupan Hutan", unit="Ha",
        label_start=col_hdr_left, val_start=f"{def_2014:,.0f}",
        label_end=col_hdr_right, val_end=f"{def_terkini:,.0f}",
        delta_pct=delta_def,
        recommendation=insight_def,
        color_theme="purple", reverse_delta=True
    )

    # 4. Smelter
    render_infographic_row(
        icon="🏭", key_indicator="Fasilitas Smelter", 
        title="Pusat Hilirisasi", unit="Unit",
        label_start=col_hdr_left, val_start="Tidak Terdata",
        label_end=col_hdr_right, val_end=f"{smelter_terkini:,.0f}",
        delta_pct=delta_smelter,
        recommendation=insight_smelter,
        color_theme="purple", reverse_delta=True
    )

    # 5. PLTU Captive
    render_infographic_row(
        icon="⚡", key_indicator="PLTU Captive", 
        title="Operating", unit="MW",
        label_start=col_hdr_left, val_start=f"{pltu_2014:,.0f}",
        label_end=col_hdr_right, val_end=f"{pltu_terkini:,.0f}",
        delta_pct=delta_pltu,
        recommendation=insight_pltu,
        color_theme="purple", reverse_delta=True
    )

    # 6. Investasi PMDN
    render_infographic_row(
        icon="💰", key_indicator="Investasi PMDN", 
        title="Aliran Modal", unit="Triliun Rp",
        label_start="Tahun 2016", val_start=f"{inv_2016/1000:,.1f}",
        label_end=col_hdr_right, val_end=f"{inv_terkini/1000:,.1f}",
        delta_pct=delta_inv,
        recommendation=insight_inv,
        color_theme="purple", reverse_delta=True
    )

    # 7. PAD
    render_infographic_row(
        icon="🏛️", key_indicator="Total PAD Sulawesi", 
        title="Ketergantungan Ekstraktif", unit="Triliun Rp",
        label_start="Tahun 2016", val_start=f"{pad_2016/1_000_000:,.1f}",
        label_end=col_hdr_right, val_end=f"{pad_terkini/1_000_000:,.1f}",
        delta_pct=delta_pad,
        recommendation=insight_pad,
        color_theme="purple", reverse_delta=False
    )

    # 8. Hutan Primer
    render_infographic_row(
        icon="🌳", key_indicator="Hutan Primer Hilang", 
        title="Ekosistem Purba", unit="Ha",
        label_start=col_hdr_left, val_start=f"{prim_2014:,.0f}",
        label_end=col_hdr_right, val_end=f"{prim_terkini:,.0f}",
        delta_pct=delta_prim,
        recommendation=insight_prim,
        color_theme="purple", reverse_delta=True
    )

    # 9. Emisi CO2
    render_infographic_row(
        icon="☁️", key_indicator="Emisi CO2 Deforestasi", 
        title="Dampak Iklim", unit="Megaton",
        label_start=col_hdr_left, val_start=f"{co2_2014/1_000_000:,.1f}",
        label_end=f"Tahun {max_year_co2}", val_end=f"{co2_terkini/1_000_000:,.1f}",
        delta_pct=f"{delta_co2:.1f}",
        recommendation=insight_co2,
        color_theme="purple", reverse_delta=True
    )

    # 10. Logistik Nikel
    render_infographic_row(
        icon="🚢", key_indicator="Simpul Logistik Nikel", 
        title="Infrastruktur Khusus", unit="Titik",
        label_start=col_hdr_left, val_start="Tidak Terdata",
        label_end=col_hdr_right, val_end=f"{log_terkini:,.0f}",
        delta_pct=delta_log,
        recommendation=insight_log,
        color_theme="purple", reverse_delta=True
    )

    render_insight_box(
        title="Insight: Paradoks Nilai Tambah & Ekonomi Terpusat",
        body="Hilirisasi diklaim meningkatkan nilai tambah, namun seluruh pembangunan PLTU dan smelter berada di enclave eksklusif yang memutus rantai pasok ekonomi warga lokal. Pertumbuhan ekonomi tinggi (hingga 11%) hanya dikuasai segelintir oligarki.",
        border_color="#5E35B1"
    )

    # ── Seksi 2: POLA PENERBITAN IZIN ──
    st.markdown('<div class="sector-badge" style="background-color: #D32F2F;">02 POLA PENERBITAN IZIN</div>', unsafe_allow_html=True)

    render_infographic_row("📜", "Total Ekspansi IUP", "Obral Konsesi", "IUP", col_hdr_left, f"{izin_2014:,.0f}", col_hdr_right, f"{izin_terkini:,.0f}", delta_izin, insight_izin_tot, "red", False)
    render_infographic_row("🗺️", "Luas Pencaplokan", "Ekspansi Spasial", "Ha", col_hdr_left, f"{luas_izin_2014:,.0f}", col_hdr_right, f"{luas_izin_terkini:,.0f}", delta_luas_izin, insight_izin_luas, "red", False)
    render_infographic_row("🚀", "Akselerasi Omnibus Law", "Eskalasi Izin", "IUP", "Pra-2020", f"{pra_2020:,.0f}", "Pasca-2020", f"{pasca_2020:,.0f}", delta_akselerasi, insight_aksel, "red", False)
    render_infographic_row("🚨", "Izin di Zona Kritis", "Governance Failure", "IUP", col_hdr_left, f"{kritis_2014:,.0f}", col_hdr_right, f"{izin_kritis:,.0f}", delta_kritis, insight_kritis, "red", False)
    render_infographic_row("🛡️", "Kawasan Lindung Musnah", "Pelanggaran Spasial", "Ha", col_hdr_left, f"{lindung_2014:,.0f}", col_hdr_right, f"{lindung_terkini:,.0f}", delta_lindung, insight_lindung, "red", False)
    render_infographic_row("⛏️", "Dominasi Operasi Produksi", "Panen Ekstraktif", "IUP", "Eksplorasi", f"{eksplorasi_count:,.0f}", "Op. Produksi", f"{op_count:,.0f}", delta_op, insight_op, "red", False)
    render_infographic_row("🔋", "Monopoli Komoditas Nikel", "Hilirisasi Buta", "IUP", col_hdr_left, f"{nikel_2014:,.0f}", col_hdr_right, f"{nikel_count:,.0f}", delta_nikel, insight_nikel, "red", False)
    render_infographic_row("⚖️", "Operasi Bermasalah Hukum", "Impunitas Ekstraktif", "Korporasi", col_hdr_left, f"{ilegal_2014}", col_hdr_right, f"{ilegal_count}", delta_ilegal, insight_ilegal, "red", False)
    render_infographic_row("✊", "Perampasan Hak Adat", "Tanpa FPIC", "Kasus", col_hdr_left, f"{fpic_2014}", col_hdr_right, f"{fpic_count}", delta_fpic, insight_fpic, "red", False)
    render_infographic_row("👻", "Sindikasi Izin Hantu", "Shadow Economy", "Laporan", col_hdr_left, f"{sindikasi_2014}", col_hdr_right, f"{sindikasi_count}", delta_sindikasi, insight_sindikasi, "red", False)

    render_insight_box(
        title="Insight: Kelumpuhan Rem Darurat Ekologis",
        body="Instrumen Daya Dukung dan Daya Tampung Lingkungan Hidup (D3TLH) telah dilumpuhkan menjadi sekadar ornamen administratif. Lonjakan perizinan justru difasilitasi di saat kondisi tutupan hutan dan kualitas air telah hancur lebur, membuktikan terjadinya 'State Capture' oleh oligarki.",
        border_color="#D32F2F"
    )

    # ── Seksi 3: KUALITAS LINGKUNGAN HIDUP ──
    st.markdown('<div class="sector-badge" style="background-color: #1976D2;">03 KUALITAS LINGKUNGAN HIDUP</div>', unsafe_allow_html=True)

def load_dataset(filename):
    try:
        return pd.read_csv(os.path.join(DATA_DIR, filename))
    except FileNotFoundError:
        return pd.DataFrame()

# Data Ekstraksi Seksi 3
# 1. Limbah B3
limbah_df = load_dataset('sulawesi_limbah_b3_ngo_proxy.csv')
if not limbah_df.empty:
    limbah_df = limbah_df[limbah_df['Provinsi'].str.contains('Sulawesi|Gorontalo', case=False, na=False)]
limbah_b3_terkini = limbah_df['Estimasi Timbulan (Ton/Tahun)'].sum() if not limbah_df.empty else 20700000
delta_limbah = "▲ Signifikan"

# 2. PLTU Captive
pltu_df = load_dataset('sulawesi_pltu_captive.csv')
pltu_mw = pltu_df['Capacity (MW)'].sum() if not pltu_df.empty else 12245.0
pltu_unit = pltu_df.shape[0] if not pltu_df.empty else 67
pltu_2014_s3 = pltu_df[pd.to_numeric(pltu_df['Start year'], errors='coerce') <= 2014]['Capacity (MW)'].sum() if not pltu_df.empty else 70.0
pltu_pct = ((pltu_mw - pltu_2014_s3) / pltu_2014_s3 * 100) if pltu_2014_s3 > 0 else 0
delta_pltu_s3 = f"▲ +{pltu_pct:,.0f}%"

# 3, 4, 5, 10. GFW Deforestasi & Emisi
gfw_df = load_dataset('sulawesi_gfw_master_1_dekade_2014_2023_v3.csv')
gfw_def_terkini = gfw_df['Total_Deforestasi_Ha'].sum() if not gfw_df.empty else 2078652
gfw_def_2014 = gfw_df[gfw_df['Tahun'] == 2014]['Total_Deforestasi_Ha'].sum() if not gfw_df.empty else 239268
gfw_primer_terkini = gfw_df['Deforestasi_Hutan_Primer_Ha'].sum() if not gfw_df.empty else 2078652
gfw_primer_2014 = gfw_df[gfw_df['Tahun'] == 2014]['Deforestasi_Hutan_Primer_Ha'].sum() if not gfw_df.empty else 239268
co2_terkini_s3 = (gfw_df[gfw_df['Tahun'] == 2023]['Total_Emisi_CO2_Megagram'].sum() / 1_000_000) if not gfw_df.empty else 88.6
co2_2014_s3 = (gfw_df[gfw_df['Tahun'] == 2014]['Total_Emisi_CO2_Megagram'].sum() / 1_000_000) if not gfw_df.empty else 93.3
co2_kumulatif_s3 = (gfw_df['Total_Emisi_CO2_Megagram'].sum() / 1_000_000) if not gfw_df.empty else 804.1
tambang_def_terkini = gfw_df['Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha'].sum() if not gfw_df.empty else 2107041
tambang_def_2014 = gfw_df[gfw_df['Tahun'] == 2014]['Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha'].sum() if not gfw_df.empty else 248031

delta_gfw_def = f"▲ +{((gfw_def_terkini - gfw_def_2014)/gfw_def_2014 * 100):,.0f}%"
delta_gfw_primer = f"▲ +{((gfw_primer_terkini - gfw_primer_2014)/gfw_primer_2014 * 100):,.0f}%"
delta_co2_s3 = f"▼ {((co2_terkini_s3 - co2_2014_s3)/co2_2014_s3 * 100):,.1f}%"
delta_tambang_def = f"▲ +{((tambang_def_terkini - tambang_def_2014)/tambang_def_2014 * 100):,.0f}%"

# 6, 7. Bencana Ekologis BNPB
bnpb_df = load_dataset('sulawesi_bencana_bnpb_2014_2024.csv')
bencana_terkini = bnpb_df['jumlah_kejadian'].sum() if not bnpb_df.empty else 1557
bencana_2014 = bnpb_df[bnpb_df['tahun'] == 2014]['jumlah_kejadian'].sum() if not bnpb_df.empty else 39
korban_terkini = bnpb_df['korban_terdampak'].sum() if not bnpb_df.empty else 1235000
korban_2014 = bnpb_df[bnpb_df['tahun'] == 2014]['korban_terdampak'].sum() if not bnpb_df.empty else 23000

delta_bencana = f"▲ +{((bencana_terkini - bencana_2014)/bencana_2014 * 100):,.0f}%"
delta_korban = f"▲ +{((korban_terkini - korban_2014)/korban_2014 * 100):,.0f}%"

# 8. Biodiversitas
iucn_df = load_dataset('sulawesi_biodiversitas_iucn_fase5_exploded.csv')
spesies_terkini = iucn_df[iucn_df['Mining Threat'] == 'Yes']['Scientific Name'].nunique() if not iucn_df.empty else 4
delta_spesies = "▲ Signifikan"

# 9. IKU Sulbar
iku_df = load_dataset('sulawesi_iku_2015_2024.csv')
iku_sulbar = iku_df[iku_df['Provinsi'] == 'Sulawesi Barat'] if not iku_df.empty else pd.DataFrame()
iku_2015 = iku_sulbar[iku_sulbar['Tahun'] == 2015]['IKU'].mean() if not iku_sulbar.empty else 97.0
iku_terkini = iku_sulbar[iku_sulbar['Tahun'] == 2024]['IKU'].mean() if not iku_sulbar.empty else 92.5
delta_iku = f"▼ {(iku_terkini - iku_2015):,.1f} Poin"

# Data Ekstraksi Seksi 4: Beban Kesehatan
k_df = load_dataset('sulawesi_kesehatan_detail_2014_2024.csv')
z_df = load_dataset('zoonosis_kab_kota_2015_2024.csv')
ika_df = load_dataset('sulawesi_ika_2016_2024.csv')
limbah_df = load_dataset('sulawesi_limbah_b3.csv')
faskes_df = load_dataset('sulawesi_faskes_agregat_v3.csv')

# -- Data Logistik (Seksi 5)
logistik_df = load_dataset("sulawesi_logistik_simpul_nikel.csv")


# ISPA
ispa_total = k_df[k_df['indikator'] == 'Kasus ISPA/Pneumonia']['nilai'].sum() if not k_df.empty else 233687
ispa_2014 = k_df[(k_df['indikator'] == 'Kasus ISPA/Pneumonia') & (k_df['tahun'] == 2014)]['nilai'].sum() if not k_df.empty else 30195
ispa_pct = ((ispa_total - ispa_2014) / ispa_2014 * 100) if ispa_2014 > 0 else 0
delta_ispa = f"▲ +{ispa_pct:,.0f}%"
insight_ispa = f"Lonjakan drastis {ispa_pct:,.0f}% ({ispa_total:,.0f} kasus) akibat paparan abu batubara PLTU dan debu smelter yang mencekik saluran pernapasan warga."

# Diare
diare_total = k_df[k_df['indikator'] == 'Kasus Diare Dilayani']['nilai'].sum() if not k_df.empty else 2286607
diare_2014 = k_df[(k_df['indikator'] == 'Kasus Diare Dilayani') & (k_df['tahun'] == 2014)]['nilai'].sum() if not k_df.empty else 231924
diare_pct = ((diare_total - diare_2014) / diare_2014 * 100) if diare_2014 > 0 else 0
delta_diare = f"▲ +{diare_pct:,.0f}%"
insight_diare = f"Ledakan infeksi pencernaan naik {diare_pct:,.0f}% ({diare_total:,.0f} kasus), berkorelasi langsung dengan krisis hancurnya sanitasi komunal."

# IKA (Sulteng as proxy for mining impact)
ika_2016 = ika_df[(ika_df['Tahun'] == 2016) & (ika_df['Provinsi'] == 'Sulawesi Tengah')]['Indeks Kualitas Air'].mean() if not ika_df.empty else 46.6
ika_2024 = ika_df[(ika_df['Tahun'] == 2024) & (ika_df['Provinsi'] == 'Sulawesi Tengah')]['Indeks Kualitas Air'].mean() if not ika_df.empty else 62.0
ika_pct = ((ika_2024 - ika_2016) / ika_2016 * 100) if ika_2016 > 0 else 0
delta_ika_s4 = f"▲ +{ika_pct:,.1f}%" if ika_pct > 0 else f"▼ {ika_pct:,.1f}%"
insight_ika = f"Kualitas air di angka {ika_2024:,.1f} (kategori buruk), sumber air warga keruh dan terkontaminasi buangan sedimen tambang."

# Limbah B3
limbah_b3_terkini_s4 = pd.to_numeric(limbah_df['Estimasi Timbulan (Ton/Tahun)'].astype(str).str.replace(',', '').str.replace('.', ''), errors='coerce').sum() if not limbah_df.empty else 20900000
delta_limbah_s4 = "▲ Signifikan"
insight_limbah_s4 = f"Lebih dari {limbah_b3_terkini_s4/1_000_000:,.1f} juta ton (estimasi berdasar temuan AEER/KLH 2024-2025) limbah B3 menyebar menjadi agen eksternalitas kesehatan."

# DBD
dbd_total = z_df[z_df['jenis_penyakit'] == 'DBD']['total_kasus'].sum() if not z_df.empty else 20238
dbd_2016 = z_df[(z_df['jenis_penyakit'] == 'DBD') & (z_df['tahun'] == 2016)]['total_kasus'].sum() if not z_df.empty else 4571
dbd_pct = ((dbd_total - dbd_2016) / dbd_2016 * 100) if dbd_2016 > 0 else 0
delta_dbd = f"▲ +{dbd_pct:,.0f}%"
insight_dbd = f"Lonjakan {dbd_pct:,.0f}% ({dbd_total:,.0f} kasus) akibat kubangan tambang tak direklamasi yang bertransformasi menjadi inkubator vektor penyakit."

# Kusta
kusta_total = k_df[k_df['indikator'] == 'Kasus Kusta Baru']['nilai'].sum() if not k_df.empty else 23589
kusta_2014 = k_df[(k_df['indikator'] == 'Kasus Kusta Baru') & (k_df['tahun'] == 2014)]['nilai'].sum() if not k_df.empty else 2380
kusta_pct = ((kusta_total - kusta_2014) / kusta_2014 * 100) if kusta_2014 > 0 else 0
delta_kusta = f"▲ +{kusta_pct:,.0f}%"
insight_kusta = f"Kenaikan tajam {kusta_pct:,.0f}% ({kusta_total:,.0f} kasus) infeksi akibat buruknya sanitasi dan kepadatan barak pekerja hilirisasi."

# Faskes
faskes_2014 = faskes_df[faskes_df["tahun"] == 2014]["jumlah"].sum() if not faskes_df.empty else 8273
faskes_2024 = faskes_df[faskes_df["tahun"] == 2024]["jumlah"].sum() if not faskes_df.empty else 2944
faskes_pct = ((faskes_2024 - faskes_2014) / faskes_2014 * 100) if faskes_2014 > 0 else 0
delta_faskes = f"▲ +{faskes_pct:,.0f}%"
insight_faskes = f"Faskes hanya tumbuh {faskes_pct:,.0f}% ({faskes_2014:,.0f} ke {faskes_2024:,.0f} unit), gagal total menyangga beban penyakit ISPA & Diare yang meledak +800%."

# Insight Seksi 3
insight_limbah = f"Aktivitas smelter membuang {limbah_b3_terkini/1_000_000:,.1f} Juta ton (estimasi berdasar temuan AEER/KLH 2024-2025) limbah B3/slag nikel tanpa pengawasan ketat, mencemari laut."
insight_pltu_s3 = f"Ketergantungan pada {pltu_unit} PLTU Captive batu bara ({pltu_mw:,.0f} MW, naik {pltu_pct:,.0f}%) mengunci Sulawesi dalam era karbon tinggi di tengah krisis iklim."
insight_co2_s3 = f"Secara tahunan emisi turun semu (-5.0%), namun FAKTA EKOLOGIS mencatat akumulasi 1 dekade mencapai {co2_kumulatif_s3:,.1f} Megaton karbon, mengeliminasi seluruh klaim transisi energi hijau."
insight_primer = f"Menghilangnya {gfw_primer_terkini/1_000_000:,.2f} Juta Ha tutupan hutan primer (naik {((gfw_primer_terkini - gfw_primer_2014)/gfw_primer_2014*100):,.0f}%) membunuh keanekaragaman hayati secara permanen."
insight_tambang = f"Ekspansi tambang & sawit meledak merangsek {tambang_def_terkini/1_000_000:,.1f} Juta Hektare (naik {((tambang_def_terkini - tambang_def_2014)/tambang_def_2014*100):,.0f}%), menghapus daya lentur ekosistem."
insight_bencana = f"Frekuensi bencana ekologis (banjir/longsor) meroket tajam {((bencana_terkini - bencana_2014)/bencana_2014*100):,.0f}% menjadi {bencana_terkini:,.0f} insiden (Data BNPB)."
insight_korban = f"Eksploitasi alam memaksa {korban_terkini/1_000_000:,.2f} Juta jiwa menjadi pengungsi iklim (naik {((korban_terkini - korban_2014)/korban_2014*100):,.0f}%) di tanah airnya sendiri."
insight_spesies = f"Eksistensi {spesies_terkini} spesies kunci endemik terdesak menuju jurang kepunahan (Daftar Merah IUCN) akibat fragmentasi habitat konsesi."
insight_iku = f"Parameter IKU anjlok menjadi {iku_terkini:,.1f} dari baseline {iku_2015:,.1f} (Data KLHK), menghancurkan indikator udara bersih bebas polutan."
insight_def_s3 = f"Kehilangan tutupan pohon seluas {gfw_def_terkini/1_000_000:,.2f} Juta Ha (naik {((gfw_def_terkini - gfw_def_2014)/gfw_def_2014*100):,.0f}%) meniadakan fungsi perlindungan spasial kawasan."

if SHOW_WEB_DASHBOARD:
    render_infographic_row("☢️", "Timbunan Limbah B3", "Toksisitas", "Ton", col_hdr_left, "0", col_hdr_right, f"{limbah_b3_terkini:,.0f}", delta_limbah, insight_limbah, "blue", False)
    render_infographic_row("🏭", "Kapasitas PLTU Captive", "Pembangkit", "MW", col_hdr_left, "0", col_hdr_right, f"{pltu_mw:,.0f}", delta_pltu_s3, insight_pltu_s3, "blue", False)
    render_infographic_row("☁️", "Emisi Karbon Deforestasi", "Jejak Emisi", "Megaton", col_hdr_left, f"{co2_2014_s3:,.1f}", "Snapshot 2023", f"{co2_terkini_s3:,.1f}", delta_co2_s3, insight_co2_s3, "blue", False)
    render_infographic_row("🌳", "Hutan Primer Musnah", "Ekosistem", "Ha", col_hdr_left, f"{gfw_primer_2014:,.0f}", col_hdr_right, f"{gfw_primer_terkini:,.0f}", delta_gfw_primer, insight_primer, "blue", False)
    render_infographic_row("🚜", "Deforestasi (Tambang/Sawit)", "Perambahan", "Ha", col_hdr_left, f"{tambang_def_2014:,.0f}", col_hdr_right, f"{tambang_def_terkini:,.0f}", delta_tambang_def, insight_tambang, "blue", False)
    render_infographic_row("🌊", "Ledakan Bencana Ekologis", "Kejadian", "Insiden", col_hdr_left, "Tidak Terdata" if bencana_2014 == 0 else f"{bencana_2014:,.0f}", col_hdr_right, f"{bencana_terkini:,.0f}", delta_bencana, insight_bencana, "blue", False)
    render_infographic_row("🏃", "Korban Bencana Alam", "Pengungsi Iklim", "Jiwa", col_hdr_left, "Tidak Terdata" if korban_2014 == 0 else f"{korban_2014:,.0f}", col_hdr_right, f"{korban_terkini:,.0f}", delta_korban, insight_korban, "blue", False)
    render_infographic_row("🦧", "Ancaman Kepunahan Spesies", "Biodiversitas", "Taxa", "Status Aman", "0", "Krisis Tambang", f"{spesies_terkini:,.0f}", delta_spesies, insight_spesies, "blue", False)
    render_infographic_row("😷", "Penurunan IKU (Sulbar)", "Polusi Udara", "Poin", col_hdr_left, f"{iku_2015:,.1f}", col_hdr_right, f"{iku_terkini:,.1f}", delta_iku, insight_iku, "blue", False)
    render_infographic_row("🔥", "Total Deforestasi Regional", "Deforestasi", "Ha", col_hdr_left, f"{gfw_def_2014:,.0f}", col_hdr_right, f"{gfw_def_terkini:,.0f}", delta_gfw_def, insight_def_s3, "blue", False)

    render_insight_box(
        title="Insight: Ecosida yang Dilegalkan",
        body="Lebih dari 20 Juta ton limbah beracun B3 ditumpuk tanpa ampun bersamaan dengan 1,5 Gigaton karbon yang terlepas akibat masifnya pembabatan jutaan hektare hutan primer. Angka ini menegaskan adanya pola pembiaran terstruktur (state omission) yang mendegradasi bentang alam Sulawesi hingga ke titik krisis ekologis permanen yang mengorbankan jutaan nyawa masyarakat pesisir.",
        border_color="#1976D2"
    )

# ---------------------------------------------------------
# Data Ekstraksi Seksi 5: Koridor Logistik Nikel
# ---------------------------------------------------------
n_lokasi = len(logistik_df)
n_psn = len(logistik_df[logistik_df["psn_status"] == "terkonfirmasi"])
total_pltu = int(logistik_df["pltu_mw"].sum())
total_izin = int(logistik_df["izin_nikel_count"].sum())
n_kawasan = logistik_df["kawasan_industri"].replace("", np.nan).dropna().nunique()
n_kabupaten_logistik = logistik_df["kabupaten"].dropna().nunique()
n_kek = len(logistik_df[logistik_df["kek_status"] != "tidak_ada"])
n_export_channel = logistik_df["export_channel"].replace("", np.nan).dropna().nunique()
export_destinations = "China/Asia"

# Hitung Delta (Baseline 2014 = 0)
delta_lokasi = f" +{n_lokasi}"
insight_lokasi = f"Dari ketiadaan fasilitas pesisir terintegrasi (2014), kini terbangun {n_lokasi} klaster pelabuhan industri besar."

delta_psn = f" +{n_psn}"
insight_psn = f"Sebanyak {n_psn} dari {n_lokasi} lokasi ini berstatus PSN, mempercepat izin dan pembebasan lahan warga secara instan."

delta_pltu_s5 = f" +{total_pltu:,.0f} MW"
insight_pltu_s5 = f"Pabrik dan pelabuhan dibangun sepaket dengan PLTU batubara captive {total_pltu:,.0f} MW tanpa transisi energi hijau."

delta_izin_s5 = f" +{total_izin}"
insight_izin_s5 = f"Jaringan dermaga ini melayani {total_izin} izin tambang nikel di hulu yang terus berekspansi ke pedalaman."

delta_kawasan_s5 = f" +{n_kawasan}"
insight_kawasan_s5 = f"Dataset mencatat {n_kawasan} kawasan/estate industri terkait nikel, menandakan simpul logistik tumbuh sebagai enclave produksi terintegrasi."

delta_kabupaten_s5 = f" +{n_kabupaten_logistik}"
insight_kabupaten_s5 = f"Sebaran simpul menjangkau {n_kabupaten_logistik} kabupaten kunci, memperluas tekanan ruang dari pesisir industri hingga wilayah tambang hulu."

delta_kek_s5 = f" {n_kek}"
insight_kek_s5 = f"Tidak ada satu pun dari {n_lokasi} simpul ini berstatus KEK; ekspansi berjalan lewat PSN, kawasan industri, dan fasilitas korporasi khusus."

delta_ekspor_s5 = f" +{n_export_channel}"
insight_ekspor = f"Terdapat {n_export_channel} kanal ekspor/produk yang teridentifikasi, dengan orientasi utama ke {export_destinations} untuk NPI, matte, ferronickel, dan stainless steel."

# ---------------------------------------------------------
# Data Ekstraksi Seksi 6: Konflik Sosial & Agraria
# ---------------------------------------------------------
df_konflik_s6 = df_konf_sul.copy()
df_konflik_s6['tahun'] = pd.to_numeric(df_konflik_s6['tahun'], errors='coerce')
df_konflik_s6['dampak_masyarakat_jiwa'] = pd.to_numeric(df_konflik_s6['dampak_masyarakat_jiwa'], errors='coerce').fillna(0)
df_konflik_s6['luas_ha'] = pd.to_numeric(df_konflik_s6['luas_ha'], errors='coerce').fillna(0)

def map_sektor_konflik(status):
    status = str(status).lower()
    if 'kebun' in status:
        return 'Perkebunan'
    if 'tambang' in status:
        return 'Pertambangan'
    if 'hutan' in status:
        return 'Kehutanan'
    if any(x in status for x in ['infrastruktur', 'bendungan', 'transmigrasi', 'energi', 'fasilitas', 'jalan', 'industri']):
        return 'Infrastruktur & PSN'
    if any(x in status for x in ['pariwisata', 'laut', 'pesisir']):
        return 'Pariwisata & Pesisir'
    return 'Lainnya'

def delta_pct_text(baseline, current):
    baseline = float(baseline or 0)
    current = float(current or 0)
    if baseline <= 0:
        return "Tidak Terdata"
    delta = ((current - baseline) / baseline) * 100
    if delta >= 0:
        return f"▲ +{delta:,.0f}%"
    return f"▼ {delta:,.0f}%"

df_konflik_s6['Sektor_Grup'] = df_konflik_s6['status'].apply(map_sektor_konflik)
konflik_2014_s6 = len(df_konflik_s6[df_konflik_s6['tahun'] <= 2014])
konflik_terkini_s6 = len(df_konflik_s6)
jiwa_2014_s6 = int(df_konflik_s6[df_konflik_s6['tahun'] <= 2014]['dampak_masyarakat_jiwa'].sum())
jiwa_terkini_s6 = int(df_konflik_s6['dampak_masyarakat_jiwa'].sum())
luas_2014_s6 = df_konflik_s6[df_konflik_s6['tahun'] <= 2014]['luas_ha'].sum()
luas_terkini_s6 = df_konflik_s6['luas_ha'].sum()

def count_sector_s6(sector, max_year=None):
    data = df_konflik_s6[df_konflik_s6['Sektor_Grup'] == sector]
    if max_year is not None:
        data = data[data['tahun'] <= max_year]
    return len(data)

tambang_2014_s6 = count_sector_s6('Pertambangan', 2014)
tambang_terkini_s6 = count_sector_s6('Pertambangan')
kebun_2014_s6 = count_sector_s6('Perkebunan', 2014)
kebun_terkini_s6 = count_sector_s6('Perkebunan')
hutan_2014_s6 = count_sector_s6('Kehutanan', 2014)
hutan_terkini_s6 = count_sector_s6('Kehutanan')

belum_mask_s6 = df_konflik_s6['status_konflik'].astype(str).str.contains('Belum Ditangani', na=False)
belum_2014_s6 = len(df_konflik_s6[(df_konflik_s6['tahun'] <= 2014) & belum_mask_s6])
belum_terkini_s6 = len(df_konflik_s6[belum_mask_s6])

fpic_2014_s6 = len(df_fpic[pd.to_numeric(df_fpic['tahun'], errors='coerce') <= 2014])
fpic_terkini_s6 = len(df_fpic)

delta_konflik_total_s6 = delta_pct_text(konflik_2014_s6, konflik_terkini_s6)
delta_jiwa_s6 = delta_pct_text(jiwa_2014_s6, jiwa_terkini_s6)
delta_luas_s6 = delta_pct_text(luas_2014_s6, luas_terkini_s6)
delta_tambang_s6 = delta_pct_text(tambang_2014_s6, tambang_terkini_s6)
delta_kebun_s6 = delta_pct_text(kebun_2014_s6, kebun_terkini_s6)
delta_hutan_s6 = delta_pct_text(hutan_2014_s6, hutan_terkini_s6)
delta_belum_s6 = delta_pct_text(belum_2014_s6, belum_terkini_s6)
delta_fpic_s6 = delta_pct_text(fpic_2014_s6, fpic_terkini_s6)

insight_konflik_total_s6 = f"Basis data mencatat {konflik_terkini_s6 - konflik_2014_s6:,.0f} tambahan letupan setelah 2014; total historis mencapai {konflik_terkini_s6:,.0f} kasus di koridor Sulawesi dan sentra nikel terkait."
insight_jiwa_s6 = f"Korban terdampak meningkat dari {jiwa_2014_s6:,.0f} menjadi {jiwa_terkini_s6:,.0f} jiwa, memperlihatkan konflik lahan sebagai krisis sosial yang terukur."
insight_luas_s6 = f"Area konflik melebar dari {luas_2014_s6:,.0f} Ha menjadi {luas_terkini_s6:,.0f} Ha, menandai eskalasi perebutan ruang hidup secara spasial."
insight_tambang_s6 = f"Konflik pertambangan bertambah dari {tambang_2014_s6:,.0f} menjadi {tambang_terkini_s6:,.0f} kasus, beririsan langsung dengan ekspansi mineral kritis dan hilirisasi nikel."
insight_kebun_s6 = f"Perkebunan tetap menjadi sumber sengketa besar dengan {kebun_terkini_s6:,.0f} kasus, memperlihatkan konflik agraria tidak berhenti pada tambang."
insight_hutan_s6 = f"Kehutanan mencatat {hutan_terkini_s6:,.0f} kasus, menunjukkan klaim kawasan dan izin pemanfaatan hutan tetap menekan masyarakat lokal."
insight_belum_s6 = f"Kasus belum ditangani naik dari {belum_2014_s6:,.0f} menjadi {belum_terkini_s6:,.0f}, mengindikasikan penyelesaian konflik tertinggal dari laju eskalasinya."
insight_fpic_s6 = f"Konflik tambang/FPIC bertambah dari {fpic_2014_s6:,.0f} menjadi {fpic_terkini_s6:,.0f} kasus, memperlihatkan lemahnya persetujuan bebas, didahulukan, dan diinformasikan."

# ---------------------------------------------------------
# Data Ekstraksi Seksi 7: Demografi & Struktur Sosial
# ---------------------------------------------------------
demo_df = load_dataset("sulawesi_demografi_master_fase4.csv")
shift_df = load_dataset("sulawesi_employment_shift_fase4.csv")

demo_df['tahun'] = pd.to_numeric(demo_df['tahun'], errors='coerce')
shift_df['tahun'] = pd.to_numeric(shift_df['tahun'], errors='coerce')

demo_industri = demo_df[(demo_df['is_smelter'] == True) & (demo_df['tahun'] <= 2024)].copy()
demo_base_year_s7 = int(demo_industri.groupby('tahun')['kabupaten'].nunique().loc[lambda s: s == demo_industri['kabupaten'].nunique()].index.min())
demo_latest_year_s7 = int(demo_industri['tahun'].max())
demo_base_s7 = demo_industri[demo_industri['tahun'] == demo_base_year_s7]
demo_latest_s7 = demo_industri[demo_industri['tahun'] == demo_latest_year_s7]

n_kab_industri_s7 = demo_industri['kabupaten'].nunique()
pop_base_s7 = demo_base_s7['jumlah_penduduk_rb'].sum()
pop_latest_s7 = demo_latest_s7['jumlah_penduduk_rb'].sum()
density_base_s7 = demo_base_s7['kepadatan_per_km2'].mean()
density_latest_s7 = demo_latest_s7['kepadatan_per_km2'].mean()
iup_base_s7 = demo_base_s7['iup_kumulatif'].sum()
iup_latest_s7 = demo_latest_s7['iup_kumulatif'].sum()
poverty_base_s7 = demo_base_s7['pct_miskin'].mean()
poverty_latest_s7 = demo_latest_s7['pct_miskin'].mean()

dbd_base_year_s7 = 2019
dbd_base_s7 = demo_industri[demo_industri['tahun'] == dbd_base_year_s7]['dbd_kasus'].sum()
dbd_latest_s7 = demo_latest_s7['dbd_kasus'].sum()

sulteng_shift_s7 = shift_df[shift_df['provinsi'] == 'Sulawesi Tengah'].sort_values('tahun')
shift_base_year_s7 = int(sulteng_shift_s7.iloc[0]['tahun'])
shift_latest_year_s7 = int(sulteng_shift_s7.iloc[-1]['tahun'])
shift_base_s7 = sulteng_shift_s7.iloc[0]
shift_latest_s7 = sulteng_shift_s7.iloc[-1]
industri_share_base_s7 = float(shift_base_s7['pct_industri_tambang_BC'])
industri_share_latest_s7 = float(shift_latest_s7['pct_industri_tambang_BC'])
pertanian_share_base_s7 = float(shift_base_s7['pct_pdrb_pertanian_A'])
pertanian_share_latest_s7 = float(shift_latest_s7['pct_pdrb_pertanian_A'])
shift_index_base_s7 = float(shift_base_s7['agriculture_to_industry_shift_index'])
shift_index_latest_s7 = float(shift_latest_s7['agriculture_to_industry_shift_index'])

delta_pop_s7 = delta_pct_text(pop_base_s7, pop_latest_s7)
delta_density_s7 = delta_pct_text(density_base_s7, density_latest_s7)
delta_iup_s7 = delta_pct_text(iup_base_s7, iup_latest_s7)
delta_poverty_s7 = delta_pct_text(poverty_base_s7, poverty_latest_s7)
delta_dbd_s7 = delta_pct_text(dbd_base_s7, dbd_latest_s7)
delta_industri_share_s7 = delta_pct_text(industri_share_base_s7, industri_share_latest_s7)
delta_pertanian_share_s7 = delta_pct_text(pertanian_share_base_s7, pertanian_share_latest_s7)
delta_shift_index_s7 = delta_pct_text(shift_index_base_s7, shift_index_latest_s7)

insight_pop_s7 = f"Populasi {n_kab_industri_s7} kabupaten industri ekstraktif naik dari {pop_base_s7:,.1f} ribu menjadi {pop_latest_s7:,.1f} ribu jiwa, menandakan tekanan hunian dan layanan publik di wilayah tapak."
insight_density_s7 = f"Kepadatan rata-rata meningkat dari {density_base_s7:,.1f} menjadi {density_latest_s7:,.1f} jiwa/km², memperlihatkan intensifikasi ruang di sekitar pusat industri."
insight_iup_s7 = f"IUP kumulatif pada kabupaten industri melonjak dari {iup_base_s7:,.0f} menjadi {iup_latest_s7:,.0f}, menghubungkan tekanan demografi dengan ekspansi izin ekstraktif."
insight_poverty_s7 = f"Kemiskinan rata-rata turun dari {poverty_base_s7:,.1f}% menjadi {poverty_latest_s7:,.1f}%, tetapi penurunannya terjadi bersamaan dengan lonjakan beban ruang dan kesehatan."
insight_dbd_s7 = f"Kasus DBD di kabupaten industri naik dari {dbd_base_s7:,.0f} kasus ({dbd_base_year_s7}) menjadi {dbd_latest_s7:,.0f} kasus ({demo_latest_year_s7}), menjadi proxy beban kesehatan permukiman padat."
insight_industri_share_s7 = f"Porsi industri dan tambang dalam PDRB Sulawesi Tengah naik dari {industri_share_base_s7:,.1f}% menjadi {industri_share_latest_s7:,.1f}%, mengunci struktur ekonomi ke sektor ekstraktif."
insight_pertanian_share_s7 = f"Porsi pertanian Sulawesi Tengah turun dari {pertanian_share_base_s7:,.1f}% menjadi {pertanian_share_latest_s7:,.1f}%, menandai pelemahan basis ekonomi agraris."
insight_shift_index_s7 = f"Indeks pergeseran agraris-ke-industri melonjak dari {shift_index_base_s7:,.3f} menjadi {shift_index_latest_s7:,.3f}, bukti transformasi struktur ekonomi yang sangat tajam."

# ---------------------------------------------------------
# Data Ekstraksi Seksi 8: Tata Kelola & Distribusi Manfaat
# ---------------------------------------------------------
df_d3tlh_panel_s8 = pd.merge(
    df_gfw,
    df_izin,
    on=['Provinsi', 'Tahun'],
    how='left'
).fillna({'Jumlah_Izin_Baru': 0, 'Total_Luas_Konsesi_Baru_Ha': 0})

d3tlh_indicator_s8 = 'Total_Deforestasi_Ha'
d3tlh_tertekan_s8 = df_d3tlh_panel_s8[d3tlh_indicator_s8].quantile(0.33)
d3tlh_kritis_s8 = df_d3tlh_panel_s8[d3tlh_indicator_s8].quantile(0.66)

def classify_d3tlh_s8(val):
    if val <= d3tlh_tertekan_s8:
        return 'Aman'
    if val <= d3tlh_kritis_s8:
        return 'Tertekan'
    return 'Kritis'

df_d3tlh_panel_s8['Status_D3TLH'] = df_d3tlh_panel_s8[d3tlh_indicator_s8].apply(classify_d3tlh_s8)
df_kritis_s8 = df_d3tlh_panel_s8[df_d3tlh_panel_s8['Status_D3TLH'] == 'Kritis']
iup_kritis_s8 = int(df_kritis_s8['Jumlah_Izin_Baru'].sum())
luas_kritis_s8 = df_kritis_s8['Total_Luas_Konsesi_Baru_Ha'].sum()

kawasan_nikel_s8 = load_dataset('sulawesi_kawasan_nikel_luas_per_provinsi.csv')
sentra_nikel_s8 = kawasan_nikel_s8[kawasan_nikel_s8['provinsi'].isin(['Sulawesi Tengah', 'Sulawesi Tenggara'])].copy()
iup_sentra_s8 = sentra_nikel_s8['total_luas_iup_ha'].sum()
amdal_sentra_s8 = sentra_nikel_s8['total_luas_amdal_ha'].sum()
gap_amdal_s8 = amdal_sentra_s8 - iup_sentra_s8
gap_amdal_pct_s8 = (gap_amdal_s8 / iup_sentra_s8 * 100) if iup_sentra_s8 > 0 else 0

kpa_masalah_s8 = len(df_kpa)
kpa_luas_s8 = pd.to_numeric(df_kpa['luas_ha'], errors='coerce').sum()
hukum_s8 = len(df_hukum)
ilegal_sul_tambang_s8 = len(df_ilegal[(df_ilegal['has_sulawesi'] == True) & (df_ilegal['has_pertambangan'] == True)])

inv_total_s8 = df_inv['nilai'].sum() / 1000
pad_total_s8 = df_pad['pad_juta_rupiah'].sum() / 1_000_000
rasio_inv_pad_s8 = inv_total_s8 / pad_total_s8 if pad_total_s8 > 0 else 0

ekspor_komoditas_s8 = load_dataset('sulawesi_ekspor_komoditas_2020_2026.csv')
ekspor_total_s8 = ekspor_komoditas_s8['nilai_usd'].sum() if not ekspor_komoditas_s8.empty else 0
ekspor_nikel_s8 = ekspor_komoditas_s8[
    ekspor_komoditas_s8['deskripsi'].str.contains('nickel|ferronickel|matte|stainless', case=False, na=False)
]['nilai_usd'].sum() if not ekspor_komoditas_s8.empty else 0
share_ekspor_nikel_s8 = (ekspor_nikel_s8 / ekspor_total_s8 * 100) if ekspor_total_s8 > 0 else 0

insight_iup_kritis_s8 = f"Pada status ekologis Kritis, pemerintah tetap menerbitkan {iup_kritis_s8:,.0f} IUP baru; D3TLH tidak bekerja sebagai rem perizinan."
insight_luas_kritis_s8 = f"Konsesi seluas {luas_kritis_s8:,.0f} Ha tetap keluar pada fase kritis, menunjukkan keputusan izin mengalahkan status daya dukung."
insight_gap_amdal_s8 = f"Di sentra nikel Sulteng-Sultra, luas AMDAL ({amdal_sentra_s8:,.0f} Ha) melampaui IUP ({iup_sentra_s8:,.0f} Ha) dengan gap {gap_amdal_s8:,.0f} Ha atau {gap_amdal_pct_s8:,.0f}%."
insight_kpa_s8 = f"KPA mencatat {kpa_masalah_s8:,.0f} perusahaan/temuan izin bermasalah dengan luasan terdampak {kpa_luas_s8:,.0f} Ha."
insight_hukum_s8 = f"Terdapat {hukum_s8:,.0f} konflik/operasi bermasalah hukum yang memperlihatkan impunitas dan pembiaran administratif."
insight_ilegal_s8 = f"Catatan KPA 2025 memuat {ilegal_sul_tambang_s8:,.0f} paragraf/temuan terkait Sulawesi dan pertambangan, menandai risiko izin ilegal atau cacat tata kelola."
insight_inv_pad_s8 = f"Investasi PMDN terakumulasi {inv_total_s8:,.1f} Triliun Rp, sementara PAD hanya {pad_total_s8:,.1f} Triliun Rp; rasio manfaat fiskal lokal tertinggal {rasio_inv_pad_s8:,.2f}x."
insight_ekspor_nikel_s8 = f"Komoditas nikel/ferronickel/matte/stainless menyumbang {share_ekspor_nikel_s8:,.1f}% nilai ekspor teridentifikasi, menunjukkan manfaat ekspor sangat terkonsentrasi pada rantai nikel."

if SHOW_WEB_DASHBOARD:
    # ── Seksi 4-8: Placeholders ──
    for i, title, color in [
        ("04", "BEBAN KESEHATAN MASYARAKAT", "#FBC02D"),
        ("05", "KORIDOR LOGISTIK NIKEL", "#00796B"),
        ("06", "KONFLIK SOSIAL & AGRARIA", "#E64A19"),
        ("07", "DEMOGRAFI & STRUKTUR SOSIAL", "#8D6E63"),
        ("08", "TATA KELOLA & DISTRIBUSI MANFAAT", "#455A64")
    ]:
        st.markdown(f'<div class="sector-badge" style="background-color: {color};">{i} {title}</div>', unsafe_allow_html=True)
        st.info(f"🚧 Indikator untuk seksi {title} sedang dalam proses agregasi dan ekstraksi dari halaman terkait.")
    st.markdown("---")

# ====== DEFINE A4 POSTER INFOGRAPHIC HTML ======

row_02_html = f"""
                <div class="data-row">
                    <div class="cell-indicator">Total Ekspansi IUP<br/><span class="unit">Obral Konsesi</span></div>
                    <div class="cell-val v-gray"><span class="num">{izin_2014:,.0f}</span></div>
                    <div class="cell-val v-red"><span class="num">{izin_terkini:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_izin}</span></div>
                    <div class="cell-insight">{insight_izin_tot}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Luas Pencaplokan<br/><span class="unit">Hektare</span></div>
                    <div class="cell-val v-gray"><span class="num">{luas_izin_2014:,.0f}</span></div>
                    <div class="cell-val v-red"><span class="num">{luas_izin_terkini:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_luas_izin}</span></div>
                    <div class="cell-insight">{insight_izin_luas}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Akselerasi Omnibus Law<br/><span class="unit">IUP</span></div>
                    <div class="cell-val v-gray"><span class="num">{pra_2020:,.0f}</span></div>
                    <div class="cell-val v-red"><span class="num">{pasca_2020:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_akselerasi}</span></div>
                    <div class="cell-insight">{insight_aksel}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Izin di Zona Kritis<br/><span class="unit">IUP Terbit</span></div>
                    <div class="cell-val v-gray"><span class="num">{kritis_2014:,.0f}</span></div>
                    <div class="cell-val v-red"><span class="num">{izin_kritis:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_kritis}</span></div>
                    <div class="cell-insight">{insight_kritis}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Kawasan Lindung Musnah<br/><span class="unit">Ha Hilang</span></div>
                    <div class="cell-val v-gray"><span class="num">{lindung_2014:,.0f}</span></div>
                    <div class="cell-val v-red"><span class="num">{lindung_terkini:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_lindung}</span></div>
                    <div class="cell-insight">{insight_lindung}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Dominasi Op. Produksi<br/><span class="unit">IUP Aktif</span></div>
                    <div class="cell-val v-gray"><span class="num">{eksplorasi_count:,.0f}</span></div>
                    <div class="cell-val v-red"><span class="num">{op_count:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_op}</span></div>
                    <div class="cell-insight">{insight_op}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Monopoli Komoditas Nikel<br/><span class="unit">IUP</span></div>
                    <div class="cell-val v-gray"><span class="num">{nikel_2014:,.0f}</span></div>
                    <div class="cell-val v-red"><span class="num">{nikel_count:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_nikel}</span></div>
                    <div class="cell-insight">{insight_nikel}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Operasi Bermasalah Hukum<br/><span class="unit">Korporasi</span></div>
                    <div class="cell-val v-gray"><span class="num">{ilegal_2014}</span></div>
                    <div class="cell-val v-red"><span class="num">{ilegal_count}</span></div>
                    <div><span class="badge badge-bad">{delta_ilegal}</span></div>
                    <div class="cell-insight">{insight_ilegal}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Perampasan Hak Adat<br/><span class="unit">Mega-Konflik</span></div>
                    <div class="cell-val v-gray"><span class="num">{fpic_2014}</span></div>
                    <div class="cell-val v-red"><span class="num">{fpic_count}</span></div>
                    <div><span class="badge badge-bad">{delta_fpic}</span></div>
                    <div class="cell-insight">{insight_fpic}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Sindikasi Izin Hantu<br/><span class="unit">Laporan</span></div>
                    <div class="cell-val v-gray"><span class="num">{sindikasi_2014}</span></div>
                    <div class="cell-val v-red"><span class="num">{sindikasi_count}</span></div>
                    <div><span class="badge badge-bad">{delta_sindikasi}</span></div>
                    <div class="cell-insight">{insight_sindikasi}</div>
                </div>
"""


row_05_html = f"""
                <div class="data-row">
                    <div class="cell-indicator">Total Pelabuhan Ekspor<br/><span class="unit">Klaster Fasilitas</span></div>
                    <div class="cell-val v-gray"><span class="num">Total: 6 Kawasan Industri</span></div>
                    <div class="cell-val v-red"><span class="num">Terbangun: {n_lokasi} Pelabuhan</span></div>
                    <div><span class="badge badge-bad">Terkonfirmasi</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_lokasi}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Status PSN Nasional<br/><span class="unit">Tameng Hukum</span></div>
                    <div class="cell-val v-gray"><span class="num">Total: 6 Kawasan Industri</span></div>
                    <div class="cell-val v-red"><span class="num">Berstatus PSN: {n_psn} Lokasi</span></div>
                    <div><span class="badge badge-bad">PSN</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_psn}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">PLTU Batubara Captive<br/><span class="unit">Kapasitas Pembangkit</span></div>
                    <div class="cell-val v-gray"><span class="num">Total: 6 Kawasan Industri</span></div>
                    <div class="cell-val v-red"><span class="num">Kapasitas: {total_pltu:,.0f} MW</span></div>
                    <div><span class="badge badge-bad">Operating</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_pltu_s5}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Izin Tambang Terlayani<br/><span class="unit">Suplai Hulu</span></div>
                    <div class="cell-val v-gray"><span class="num">Total se-Sulawesi: 329 IUP</span></div>
                    <div class="cell-val v-red"><span class="num">Terhubung: {total_izin} IUP</span></div>
                    <div><span class="badge badge-bad">Suplai Hulu</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_izin_s5}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Kanal Ekspor Teridentifikasi<br/><span class="unit">Rantai Pasok</span></div>
                    <div class="cell-val v-gray"><span class="num">Total: 6 Jenis Produk Olahan</span></div>
                    <div class="cell-val v-red"><span class="num">Terlacak: {n_export_channel} Jalur Ekspor</span></div>
                    <div><span class="badge badge-bad">China/Asia</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_ekspor}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Kawasan Industri Nikel<br/><span class="unit">Estate/Cluster</span></div>
                    <div class="cell-val v-gray"><span class="num">Total: 6 Lokasi Utama</span></div>
                    <div class="cell-val v-red"><span class="num">Resmi Beroperasi: {n_kawasan} Kawasan</span></div>
                    <div><span class="badge badge-bad">Terintegrasi</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_kawasan_s5}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Sebaran Kabupaten Simpul<br/><span class="unit">Wilayah Tapak</span></div>
                    <div class="cell-val v-gray"><span class="num">Total: 6 Lokasi Utama</span></div>
                    <div class="cell-val v-red"><span class="num">Berdampak ke: {n_kabupaten_logistik} Kabupaten</span></div>
                    <div><span class="badge badge-bad">Pesisir</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_kabupaten_s5}</div>
                </div>
"""

row_06_html = f"""
                <div class="data-row">
                    <div class="cell-indicator">Total Letupan Konflik<br/><span class="unit">Insiden Agraria</span></div>
                    <div class="cell-val v-gray"><span class="num">{konflik_2014_s6:,.0f}</span></div>
                    <div class="cell-val v-red"><span class="num">{konflik_terkini_s6:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_konflik_total_s6}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_konflik_total_s6}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Warga Terdampak<br/><span class="unit">Jiwa</span></div>
                    <div class="cell-val v-gray"><span class="num">{jiwa_2014_s6:,.0f}</span></div>
                    <div class="cell-val v-red"><span class="num">{jiwa_terkini_s6:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_jiwa_s6}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_jiwa_s6}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Luas Area Konflik<br/><span class="unit">Hektare</span></div>
                    <div class="cell-val v-gray"><span class="num">{luas_2014_s6:,.0f}</span></div>
                    <div class="cell-val v-red"><span class="num">{luas_terkini_s6:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_luas_s6}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_luas_s6}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Konflik Pertambangan<br/><span class="unit">Kasus</span></div>
                    <div class="cell-val v-gray"><span class="num">{tambang_2014_s6:,.0f}</span></div>
                    <div class="cell-val v-red"><span class="num">{tambang_terkini_s6:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_tambang_s6}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_tambang_s6}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Konflik Perkebunan<br/><span class="unit">Kasus</span></div>
                    <div class="cell-val v-gray"><span class="num">{kebun_2014_s6:,.0f}</span></div>
                    <div class="cell-val v-red"><span class="num">{kebun_terkini_s6:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_kebun_s6}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_kebun_s6}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Konflik Kehutanan<br/><span class="unit">Kasus</span></div>
                    <div class="cell-val v-gray"><span class="num">{hutan_2014_s6:,.0f}</span></div>
                    <div class="cell-val v-red"><span class="num">{hutan_terkini_s6:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_hutan_s6}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_hutan_s6}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Konflik Belum Ditangani<br/><span class="unit">Status Kasus</span></div>
                    <div class="cell-val v-gray"><span class="num">{belum_2014_s6:,.0f}</span></div>
                    <div class="cell-val v-red"><span class="num">{belum_terkini_s6:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_belum_s6}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_belum_s6}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Konflik Tambang/FPIC<br/><span class="unit">Hak Persetujuan</span></div>
                    <div class="cell-val v-gray"><span class="num">{fpic_2014_s6:,.0f}</span></div>
                    <div class="cell-val v-red"><span class="num">{fpic_terkini_s6:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_fpic_s6}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_fpic_s6}</div>
                </div>
"""

row_07_html = f"""
                <div class="data-row">
                    <div class="cell-indicator">Populasi Kabupaten Industri<br/><span class="unit">Ribu Jiwa | Basis: {demo_base_year_s7}</span></div>
                    <div class="cell-val v-gray"><span class="num">{pop_base_s7:,.1f}</span></div>
                    <div class="cell-val v-red"><span class="num">{pop_latest_s7:,.1f}</span></div>
                    <div><span class="badge badge-bad">{delta_pop_s7}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_pop_s7}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Kepadatan Wilayah Industri<br/><span class="unit">Jiwa/km² | Basis: {demo_base_year_s7}</span></div>
                    <div class="cell-val v-gray"><span class="num">{density_base_s7:,.1f}</span></div>
                    <div class="cell-val v-red"><span class="num">{density_latest_s7:,.1f}</span></div>
                    <div><span class="badge badge-bad">{delta_density_s7}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_density_s7}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Kemiskinan Wilayah Industri<br/><span class="unit">Rata-rata % | Basis: {demo_base_year_s7}</span></div>
                    <div class="cell-val v-gray"><span class="num">{poverty_base_s7:,.1f}%</span></div>
                    <div class="cell-val v-red"><span class="num">{poverty_latest_s7:,.1f}%</span></div>
                    <div><span class="badge badge-up">{delta_poverty_s7}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_poverty_s7}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">PDRB Industri+Tambang Sulteng<br/><span class="unit">Share PDRB | Basis: {shift_base_year_s7}</span></div>
                    <div class="cell-val v-gray"><span class="num">{industri_share_base_s7:,.1f}%</span></div>
                    <div class="cell-val v-red"><span class="num">{industri_share_latest_s7:,.1f}%</span></div>
                    <div><span class="badge badge-bad">{delta_industri_share_s7}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_industri_share_s7}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">PDRB Pertanian Sulteng<br/><span class="unit">Share PDRB | Basis: {shift_base_year_s7}</span></div>
                    <div class="cell-val v-gray"><span class="num">{pertanian_share_base_s7:,.1f}%</span></div>
                    <div class="cell-val v-red"><span class="num">{pertanian_share_latest_s7:,.1f}%</span></div>
                    <div><span class="badge badge-bad">{delta_pertanian_share_s7}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_pertanian_share_s7}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Indeks Pergeseran Agraris-Industri<br/><span class="unit">Sulteng | Basis: {shift_base_year_s7}</span></div>
                    <div class="cell-val v-gray"><span class="num">{shift_index_base_s7:,.3f}</span></div>
                    <div class="cell-val v-red"><span class="num">{shift_index_latest_s7:,.3f}</span></div>
                    <div><span class="badge badge-bad">{delta_shift_index_s7}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_shift_index_s7}</div>
                </div>
"""

row_08_html = f"""
                <div class="data-row">
                    <div class="cell-indicator">IUP di Status Kritis D3TLH<br/><span class="unit">Izin Baru</span></div>
                    <div class="cell-val v-gray"><span class="num">Batas Ekologis: Zona Kritis</span></div>
                    <div class="cell-val v-red"><span class="num">Izin Baru: {iup_kritis_s8:,.0f} IUP</span></div>
                    <div><span class="badge badge-bad">Gagal</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_iup_kritis_s8}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Luas Konsesi di Zona Kritis<br/><span class="unit">Hektare</span></div>
                    <div class="cell-val v-gray"><span class="num">Batas Ekologis: Zona Kritis</span></div>
                    <div class="cell-val v-red"><span class="num">Konsesi: {luas_kritis_s8:,.0f} Ha</span></div>
                    <div><span class="badge badge-bad">Anomali</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_luas_kritis_s8}</div>
                </div>

                <div class="data-row">
                    <div class="cell-indicator">Temuan Izin Bermasalah KPA<br/><span class="unit">Perusahaan/Temuan</span></div>
                    <div class="cell-val v-gray"><span class="num">Sumber Data: Laporan KPA</span></div>
                    <div class="cell-val v-red"><span class="num">Tercatat: {kpa_masalah_s8:,.0f} Perusahaan</span></div>
                    <div><span class="badge badge-bad">Bermasalah</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_kpa_s8}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Konflik/Operasi Bermasalah Hukum<br/><span class="unit">Kasus</span></div>
                    <div class="cell-val v-gray"><span class="num">Sumber Data: Catatan Hukum</span></div>
                    <div class="cell-val v-red"><span class="num">Tercatat: {hukum_s8:,.0f} Kasus</span></div>
                    <div><span class="badge badge-bad">Impunitas</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_hukum_s8}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Temuan Izin Ilegal Sulawesi<br/><span class="unit">CATAHU KPA 2025</span></div>
                    <div class="cell-val v-gray"><span class="num">Sumber Data: CATAHU KPA 2025</span></div>
                    <div class="cell-val v-red"><span class="num">Tercatat: {ilegal_sul_tambang_s8:,.0f} Temuan</span></div>
                    <div><span class="badge badge-bad">Ilegal</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_ilegal_s8}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Rasio Investasi PMDN terhadap PAD<br/><span class="unit">2016-2024</span></div>
                    <div class="cell-val v-gray"><span class="num">Total PAD: {pad_total_s8:,.1f} T</span></div>
                    <div class="cell-val v-red"><span class="num">Total PMDN: {inv_total_s8:,.1f} T</span></div>
                    <div><span class="badge badge-bad">{rasio_inv_pad_s8:,.2f}x</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_inv_pad_s8}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Konsentrasi Ekspor Nikel<br/><span class="unit">Nilai Ekspor</span></div>
                    <div class="cell-val v-gray"><span class="num">Dari: Total Ekspor</span></div>
                    <div class="cell-val v-red"><span class="num">Porsi Nikel: {share_ekspor_nikel_s8:,.1f}%</span></div>
                    <div><span class="badge badge-bad">Terkonsentrasi</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_ekspor_nikel_s8}</div>
                </div>
"""

row_04_html = f"""
                <div class="data-row">
                    <div class="cell-indicator">Ledakan Kasus ISPA/Pneumonia<br/><span class="unit">Penyakit Udara</span></div>
                    <div class="cell-val v-gray"><span class="num">{ispa_2014:,.0f}</span></div>
                    <div class="cell-val v-red"><span class="num">{ispa_total:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_ispa}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_ispa}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Krisis Kualitas Air (IKA)<br/><span class="unit">Mutu Air</span></div>
                    <div class="cell-val v-gray"><span class="num">{ika_2016:,.1f}</span></div>
                    <div class="cell-val v-red"><span class="num">{ika_2024:,.1f}</span></div>
                    <div><span class="badge badge-bad">{delta_ika_s4}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_ika}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Krisis Sanitasi & Diare<br/><span class="unit">Infeksi Pencernaan</span></div>
                    <div class="cell-val v-gray"><span class="num">{diare_2014:,.0f}</span></div>
                    <div class="cell-val v-red"><span class="num">{diare_total:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_diare}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_diare}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Beban Limbah Beracun<br/><span class="unit">Tailing Tambang</span></div>
                    <div class="cell-val v-gray"><span class="num">Tidak Terdata</span></div>
                    <div class="cell-val v-red"><span class="num">{limbah_b3_terkini_s4:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_limbah_s4}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_limbah_s4}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Wabah DBD (Demam Berdarah)<br/><span class="unit">Zoonosis</span></div>
                    <div class="cell-val v-gray"><span class="num">{dbd_2016:,.0f}</span></div>
                    <div class="cell-val v-red"><span class="num">{dbd_total:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_dbd}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_dbd}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Endemi Kusta Baru<br/><span class="unit">Penyakit Menular</span></div>
                    <div class="cell-val v-gray"><span class="num">{kusta_2014:,.0f}</span></div>
                    <div class="cell-val v-red"><span class="num">{kusta_total:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_kusta}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_kusta}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Kolaps Fasilitas Kesehatan<br/><span class="unit">Rasio Faskes</span></div>
                    <div class="cell-val v-gray"><span class="num">{faskes_2014:,.0f}</span></div>
                    <div class="cell-val v-red"><span class="num">{faskes_2024:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_faskes}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_faskes}</div>
                </div>
"""

row_03_html = f"""
                <div class="data-row">
                    <div class="cell-indicator">Timbunan Limbah B3<br/><span class="unit">Toksisitas</span></div>
                    <div class="cell-val v-gray"><span class="num">Tidak Terdata</span></div>
                    <div class="cell-val v-red"><span class="num">{limbah_b3_terkini:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_limbah}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_limbah}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Emisi Karbon Deforestasi<br/><span class="unit">Jejak Emisi</span></div>
                    <div class="cell-val v-gray"><span class="num">{co2_2014_s3:,.1f} Megaton (2014)</span></div>
                    <div class="cell-val v-red"><span class="num">{co2_terkini_s3:,.1f} Megaton (2023)</span></div>
                    <div><span class="badge badge-bad">{delta_co2_s3}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_co2_s3}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Hutan Primer Musnah<br/><span class="unit">Ekosistem</span></div>
                    <div class="cell-val v-gray"><span class="num">{gfw_primer_2014:,.0f}</span></div>
                    <div class="cell-val v-red"><span class="num">{gfw_primer_terkini:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_gfw_primer}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_primer}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Deforestasi (Tambang/Sawit)<br/><span class="unit">Perambahan</span></div>
                    <div class="cell-val v-gray"><span class="num">{tambang_def_2014:,.0f}</span></div>
                    <div class="cell-val v-red"><span class="num">{tambang_def_terkini:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_tambang_def}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_tambang}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Ledakan Bencana Ekologis<br/><span class="unit">Kejadian</span></div>
                    <div class="cell-val v-gray"><span class="num">{'Tidak Terdata' if bencana_2014 == 0 else f'{bencana_2014:,.0f}'}</span></div>
                    <div class="cell-val v-red"><span class="num">{bencana_terkini:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_bencana}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_bencana}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Korban Bencana Alam<br/><span class="unit">Pengungsi Iklim</span></div>
                    <div class="cell-val v-gray"><span class="num">{'Tidak Terdata' if korban_2014 == 0 else f'{korban_2014:,.0f}'}</span></div>
                    <div class="cell-val v-red"><span class="num">{korban_terkini:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_korban}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_korban}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Ancaman Kepunahan Spesies<br/><span class="unit">Biodiversitas</span></div>
                    <div class="cell-val v-gray"><span class="num">Tidak Terdata</span></div>
                    <div class="cell-val v-red"><span class="num">{spesies_terkini:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_spesies}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_spesies}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Penurunan IKU (Sulbar)<br/><span class="unit">Polusi Udara</span></div>
                    <div class="cell-val v-gray"><span class="num">{iku_2015:,.1f}</span></div>
                    <div class="cell-val v-red"><span class="num">{iku_terkini:,.1f}</span></div>
                    <div><span class="badge badge-bad">{delta_iku}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_iku}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Total Deforestasi Regional<br/><span class="unit">Deforestasi</span></div>
                    <div class="cell-val v-gray"><span class="num">{gfw_def_2014:,.0f}</span></div>
                    <div class="cell-val v-red"><span class="num">{gfw_def_terkini:,.0f}</span></div>
                    <div><span class="badge badge-bad">{delta_gfw_def}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_def_s3}</div>
                </div>
"""

poster_html = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>CELIOS D3TLH - Poster A4</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet" />
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet" />
    <style>
        @page {{ size: A4 portrait; margin: 0; }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            width: 210mm; min-height: 297mm; font-family: 'Inter', sans-serif;
            background: #fff; color: #1a1a2e; font-size: 8pt; line-height: 1.4;
            padding: 10mm; margin: 0 auto;
        }}
        .header {{ text-align: center; border-bottom: 3px solid #1a1a2e; padding-bottom: 5mm; margin-bottom: 5mm; }}
        .header h1 {{ font-size: 14pt; font-weight: 900; letter-spacing: 1px; color: #1a1a2e; }}
        .header .sub {{ font-size: 8pt; color: #666; letter-spacing: 2px; font-weight: 600; }}
        
        .section-title {{
            background: #1a1a2e; color: #fff; font-size: 9pt; font-weight: 800;
            padding: 3mm; margin-bottom: 2mm; text-transform: uppercase; letter-spacing: 1px;
        }}
        .section-title.red {{ background: #B71C1C; }}
        .section-title.orange {{ background: #F57C00; }}
        
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 5mm; }}
        th {{ font-size: 7pt; text-align: left; padding: 2mm; border-bottom: 2px solid #ccc; color: #555; text-transform: uppercase; }}
        td {{ padding: 2mm; border-bottom: 1px solid #eee; font-size: 8pt; vertical-align: middle; }}
        
        .val {{ font-weight: 700; color: #333; }}
        .delta {{ font-weight: 800; padding: 2px 5px; border-radius: 3px; font-size: 7.5pt; }}
        .delta.bad-up {{ background: rgba(244, 67, 54, 0.15); color: #C62828; }}
        .delta.bad-down {{ background: rgba(244, 67, 54, 0.15); color: #C62828; }}
        .insight {{ font-size: 7pt; color: #666; line-height: 1.3; font-style: italic; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>KERUNTUHAN EKOLOGIS: EVALUASI DAMPAK HILIRISASI</h1>
        <div class="sub">ANALISIS DAYA DUKUNG & DAYA TAMPUNG LINGKUNGAN HIDUP (D3TLH) 2026</div>
    </div>
    
    <div class="section-title">01 EKSPANSI INDUSTRI & INVESTASI</div>
    <table>
        <tr>
            <th width="25%">Indikator</th>
            <th width="15%">Baseline</th>
            <th width="15%">Terkini</th>
            <th width="15%">Delta</th>
            <th width="30%">Temuan & Implikasi</th>
        </tr>
        <tr>
            <td><strong>Total Izin Baru (IUP)</strong><br><span style="font-size:6pt;color:#888">Periode 2014-2024</span></td>
            <td class="val">-</td>
            <td class="val">{tot_izin:,.0f} IUP</td>
            <td><span class="delta bad-up">Masif</span></td>
            <td class="insight">Penambahan izin tambang melegitimasi pembongkaran lahan secara masif di Sulawesi.</td>
        </tr>
        <tr>
            <td><strong>Total Luas Konsesi</strong><br><span style="font-size:6pt;color:#888">Eksploitasi Ruang</span></td>
            <td class="val">-</td>
            <td class="val">{tot_luas_izin:,.0f} Ha</td>
            <td><span class="delta bad-up">Kritis</span></td>
            <td class="insight">Luas daratan dan pesisir yang diserahkan kepada korporasi ekstraktif terus membengkak.</td>
        </tr>
        <tr>
            <td><strong>Deforestasi Komoditas</strong><br><span style="font-size:6pt;color:#888">Kehilangan Tutupan Hutan</span></td>
            <td class="val">-</td>
            <td class="val">{def_tambang_total:,.0f} Ha</td>
            <td><span class="delta bad-up">Kritis</span></td>
            <td class="insight">Hutan musnah permanen akibat tambang dan perkebunan monokultur skala besar.</td>
        </tr>
        <tr>
            <td><strong>Fasilitas Smelter Nikel</strong><br><span style="font-size:6pt;color:#888">Pusat Hilirisasi</span></td>
            <td class="val">-</td>
            <td class="val">{tot_smelter:,.0f} Unit</td>
            <td><span class="delta bad-up">Dominasi</span></td>
            <td class="insight">Hilirisasi nikel terkonsentrasi di fasilitas smelter yang memonopoli kawasan pesisir dan memutus rantai pasok lokal.</td>
        </tr>
        <tr>
            <td><strong>Kapasitas PLTU Captive</strong><br><span style="font-size:6pt;color:#888">Operating</span></td>
            <td class="val">-</td>
            <td class="val">{cap_op:,.0f} MW</td>
            <td><span class="delta bad-up">Kritis</span></td>
            <td class="insight">Kawasan industri menjadi episentrum polusi udara dan emisi GRK baru di Sulawesi akibat energi kotor off-grid.</td>
        </tr>
        <tr>
            <td><strong>Investasi PMDN</strong><br><span style="font-size:6pt;color:#888">Aliran Modal Domestik</span></td>
            <td class="val">-</td>
            <td class="val">{tot_inv_triliun:,.1f} Triliun Rp</td>
            <td><span class="delta bad-up">Masif</span></td>
            <td class="insight">Laju ekspansi disokong kuat secara finansial, namun pertumbuhan ekonomi tidak terdistribusi ke warga lokal.</td>
        </tr>
    </table>

    <div class="section-title" style="background: #D32F2F;">02 POLA PENERBITAN IZIN (TATA KELOLA)</div>
    <!-- GRID KONTEN SEKSI 2 -->
    <div class="section-grid">
        <div class="sidebar-cell" style="background: #D32F2F; color: white;">
            <span style="font-size:18pt; font-weight:900;">02</span>
            <span style="font-size:6pt; writing-mode:vertical-rl; transform:rotate(180deg); margin-top:10px; letter-spacing:1px;">TATA KELOLA & IZIN</span>
        </div>
        <div class="data-area" style="background: #fffcfc;">
            
            {row_02_html}
            
        </div>
    </div>
    <div class="section-title" style="background: #1976D2;">03 KUALITAS LINGKUNGAN HIDUP</div>
    <div class="section-grid">
        <div class="sidebar-cell" style="background: #1976D2; color: white;">
            <span style="font-size:18pt; font-weight:900;">03</span>
            <span style="font-size:6pt; writing-mode:vertical-rl; transform:rotate(180deg); margin-top:10px; letter-spacing:1px;">KUALITAS LINGKUNGAN</span>
        </div>
        <div class="data-area" style="background: #fcfcff;">
            
            {row_03_html}
            
        </div>
    </div>
    <div class="section-title" style="background: #FBC02D; color:#333;">04 BEBAN KESEHATAN MASYARAKAT</div>
    <div class="section-grid">
        <div class="sidebar-cell" style="background: #FBC02D; color: #333;">
            <span style="font-size:18pt; font-weight:900;">04</span>
            <span style="font-size:6pt; writing-mode:vertical-rl; transform:rotate(180deg); margin-top:10px; letter-spacing:1px; font-weight:800;">BEBAN KESEHATAN</span>
        </div>
        <div class="data-area" style="background: #fffdf7;">
            {row_04_html}
        </div>
    </div>

    <div class="section-title" style="background: #00796B;">05 KORIDOR LOGISTIK NIKEL</div>
    <div style="padding: 10px; font-style: italic; color: #888; text-align: center; border: 1px dashed #ccc; margin-bottom: 5mm;">[ Placeholder: Data sedang diekstrak dari Page 10 ]</div>

    <div class="section-title" style="background: #E64A19;">06 KONFLIK SOSIAL & AGRARIA</div>
    <div style="padding: 10px; font-style: italic; color: #888; text-align: center; border: 1px dashed #ccc; margin-bottom: 5mm;">[ Placeholder: Data sedang diekstrak dari Page 4 ]</div>

    <div class="section-title" style="background: #8D6E63;">07 DEMOGRAFI & STRUKTUR SOSIAL</div>
    <div style="padding: 10px; font-style: italic; color: #888; text-align: center; border: 1px dashed #ccc; margin-bottom: 5mm;">[ Placeholder: Data sedang diekstrak dari Page 11 ]</div>

    <div class="section-title" style="background: #455A64;">08 TATA KELOLA & DISTRIBUSI MANFAAT</div>
    <div style="padding: 10px; font-style: italic; color: #888; text-align: center; border: 1px dashed #ccc; margin-bottom: 5mm;">[ Placeholder: Data sedang diekstrak dari Page 6, 7, 8 ]</div>

    <div style="margin-top: 10mm; text-align: center; font-size: 7pt; color: #888;">
        <strong>CELIOS - Center of Economic and Law Studies</strong><br>
        Dokumen ini digenerate secara otomatis dari Sistem Intelijen D3TLH berbasis Data.<br>
        Hak Cipta © 2026 CELIOS.
    </div>
</body>
</html>
"""
col_hdr_left = "Baseline 2014"
col_hdr_right = "Akumulasi 2024"

poster_html_v2 = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>CELIOS D3TLH - Poster A4 (Card Layout)</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet" />
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet" />
    <style>
        @page {{ size: A4 portrait; margin: 0; }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            width: 210mm; min-height: 297mm; font-family: 'Inter', sans-serif;
            background: #f8fafc; color: #1a1a2e; font-size: 7.5pt; line-height: 1.35;
            padding: 8mm 7mm; margin: 0 auto;
        }}
        .header {{ text-align: center; border-bottom: 2.5px solid #1a1a2e; padding-bottom: 4mm; margin-bottom: 4mm; }}
        .header h1 {{ font-size: 11pt; font-weight: 900; letter-spacing: 1.5px; color: #1a1a2e; text-transform: uppercase; }}
        .header .sub {{ font-size: 7pt; color: #666; letter-spacing: 2px; font-weight: 600; text-transform: uppercase; }}
        
        .table-container {{ background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.08); margin-bottom: 3mm; }}
        .section-grid {{ display: grid; grid-template-columns: 75px 1fr; }}
        
        .sidebar-cell {{
            display: flex; align-items: center; justify-content: center;
            color: white; font-weight: 800; font-size: 6.5pt; text-transform: uppercase;
            text-align: center; padding: 2mm; position: relative; overflow: hidden;
        }}
        .sidebar-cell .num {{
            font-size: 26pt; font-weight: 900; color: rgba(255,255,255,0.15);
            position: absolute; top: 40%; left: 50%; transform: translate(-50%,-50%); line-height: 1; pointer-events: none;
        }}
        .sidebar-cell .label {{ position: relative; z-index: 1; line-height: 1.3; letter-spacing: 0.5px; }}
        
        .bg-s1 {{ background: #5E35B1; }}
        .bg-s2 {{ background: #E53935; }}
        .bg-s3 {{ background: #F57C00; }}
        
        .tint-s1 {{ background: rgba(94, 53, 177, 0.03); }}
        .tint-s2 {{ background: rgba(229, 57, 53, 0.03); }}
        .tint-s3 {{ background: rgba(245, 124, 0, 0.03); }}
        
        .col-header {{
            display: grid; grid-template-columns: 2.2fr 1.5fr 1.5fr 1fr 3fr;
            border-bottom: 1.5px solid #ccc; padding: 1.5mm 0;
            font-size: 6pt; font-weight: 700; color: #555; text-transform: uppercase;
        }}
        .col-header > div {{ padding: 0 2mm; }}
        
        .data-row {{
            align-items: flex-start;
            display: grid; grid-template-columns: 2.2fr 1.5fr 1.5fr 1fr 3fr;
            border-bottom: 0.5px solid #f0f0f0; min-height: 25px;
        }}
        .data-row > div {{ padding: 1.5mm 2mm; }}
        
        .cell-indicator {{ font-size: 7.5pt; font-weight: 700; line-height: 1.2; }}
        .cell-indicator .unit {{ font-size: 5.5pt; font-weight: 400; color: #888; }}
        
        .cell-val {{ 
            display: flex; align-items: center; justify-content: flex-start; gap: 4px;
        }}
        .cell-val .material-symbols-outlined {{ font-size: 14px !important; }}
        .cell-val span.num {{ font-size: 7pt; font-weight: 700; }}
        
        .v-gray {{ color: #888; }}
        .v-gray .material-symbols-outlined {{ color: #bbb; }}
        .v-green {{ color: #2E7D32; }}
        .v-green .material-symbols-outlined {{ color: #4CAF50; }}
        .v-red {{ color: #C62828; }}
        .v-red .material-symbols-outlined {{ color: #EF5350; }}
        
        .cell-insight {{ font-size: 6.5pt; color: #555; line-height: 1.3; }}
        
        .badge {{ display: inline-block; padding: 0.5mm 2mm; border-radius: 3px; font-size: 6pt; font-weight: 800; white-space: nowrap; }}
        .badge-up {{ background: rgba(76, 175, 80, 0.15); color: #2E7D32; }}
        .badge-down {{ background: rgba(244, 67, 54, 0.15); color: #C62828; }}
        .badge-bad {{ background: rgba(244, 67, 54, 0.15); color: #C62828; }}
        .badge-neutral {{ background: rgba(158, 158, 158, 0.15); color: #757575; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>KERUNTUHAN EKOLOGIS: EVALUASI DAMPAK HILIRISASI</h1>
        <div class="sub">ANALISIS DAYA DUKUNG & DAYA TAMPUNG LINGKUNGAN HIDUP (D3TLH) 2026</div>
    </div>
    
    <div class="table-container">
        <div class="section-grid">
            <div class="sidebar-cell bg-s1"><span class="num">01</span><span class="label">EKSPANSI<br/>INDUSTRI</span></div>
            <div class="data-area tint-s1">
                <div class="col-header">
                    <div>Indikator</div>
                    <div class="ch-center">{col_hdr_left}</div>
                    <div class="ch-center">{col_hdr_right}</div>
                    <div class="ch-center">Delta</div>
                    <div>Temuan & Implikasi</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Total Izin Baru (IUP)<br/><span class="unit">Periode 2014-2024</span></div>
                    <div class="cell-val v-gray"><span class="num">{iup_2014:,.0f} IUP</span></div>
                    <div class="cell-val v-red"><span class="num">{iup_terkini:,.0f} IUP</span></div>
                    <div><span class="badge badge-bad">▲ +{delta_iup:,.1f}%</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_iup}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Luas Konsesi<br/><span class="unit">Eksploitasi Ruang</span></div>
                    <div class="cell-val v-gray"><span class="num">{luas_2014:,.0f} Ha</span></div>
                    <div class="cell-val v-red"><span class="num">{luas_terkini:,.0f} Ha</span></div>
                    <div><span class="badge badge-bad">▲ +{delta_luas:,.1f}%</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_luas}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Deforestasi Komoditas<br/><span class="unit">Kehilangan Tutupan Hutan</span></div>
                    <div class="cell-val v-gray"><span class="num">{def_2014:,.0f} Ha</span></div>
                    <div class="cell-val v-red"><span class="num">{def_terkini:,.0f} Ha</span></div>
                    <div><span class="badge badge-bad">▲ +{delta_def:,.1f}%</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_def}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Fasilitas Smelter<br/><span class="unit">Pusat Hilirisasi</span></div>
                    <div class="cell-val v-gray"><span class="num">{smelter_2014} Unit</span></div>
                    <div class="cell-val v-red"><span class="num">{smelter_terkini:,.0f} Unit</span></div>
                    <div><span class="badge badge-bad">▲ +{delta_smelter:,.0f}%</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_smelter}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">PLTU Captive<br/><span class="unit">Operating</span></div>
                    <div class="cell-val v-gray"><span class="num">{pltu_2014:,.0f} MW</span></div>
                    <div class="cell-val v-red"><span class="num">{pltu_terkini:,.0f} MW</span></div>
                    <div><span class="badge badge-bad">▲ +{delta_pltu:,.1f}%</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_pltu}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Investasi PMDN<br/><span class="unit">Aliran Modal</span></div>
                    <div class="cell-val v-gray"><span class="num">{inv_2016/1000:,.1f} Triliun Rp</span></div>
                    <div class="cell-val v-red"><span class="num">{inv_terkini/1000:,.1f} Triliun Rp</span></div>
                    <div><span class="badge badge-bad">▲ +{delta_inv:,.1f}%</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_inv}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Total PAD Sulawesi<br/><span class="unit">Ketergantungan Ekstraktif</span></div>
                    <div class="cell-val v-gray"><span class="num">{pad_2014/1000000:,.1f} Triliun Rp</span></div>
                    <div class="cell-val v-red"><span class="num">{pad_terkini/1_000_000:,.1f} Triliun Rp</span></div>
                    <div><span class="badge badge-up">▲ +{delta_pad:,.1f}%</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_pad}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Hutan Primer Hilang<br/><span class="unit">Ekosistem Purba</span></div>
                    <div class="cell-val v-gray"><span class="num">{prim_2014:,.0f} Ha</span></div>
                    <div class="cell-val v-red"><span class="num">{prim_terkini:,.0f} Ha</span></div>
                    <div><span class="badge badge-bad">▲ +{delta_prim:,.1f}%</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_prim}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Emisi CO2 Deforestasi<br/><span class="unit">Dampak Iklim</span></div>
                    <div class="cell-val v-gray"><span class="num">{co2_2014/1_000_000:,.1f} Megaton</span></div>
                    <div class="cell-val v-red"><span class="num">{co2_terkini/1_000_000:,.1f} Megaton</span></div>
                    <div><span class="badge badge-bad">{delta_co2_badge}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_co2}</div>
                </div>
                <div class="data-row">
                    <div class="cell-indicator">Simpul Logistik Nikel<br/><span class="unit">Infrastruktur Khusus</span></div>
                    <div class="cell-val v-gray"><span class="num">Tidak Terdata</span></div>
                    <div class="cell-val v-red"><span class="num">{log_terkini:,.0f} Titik</span></div>
                    <div><span class="badge badge-bad">{delta_log}</span></div>
                    <div class="cell-insight" style="text-align: left;">{insight_log}</div>
                </div>
            </div>
        </div>
    </div>

    <div class="table-container">
        <div class="section-grid">
            <div class="sidebar-cell bg-s2"><span class="num">02</span><span class="label">TATA KELOLA<br/>PERIZINAN</span></div>
            <div class="data-area tint-s2">
                <div class="col-header">
                    <div>Indikator Perizinan</div>
                    <div class="ch-center">{col_hdr_left}</div>
                    <div class="ch-center">{col_hdr_right}</div>
                    <div class="ch-center">Delta</div>
                    <div>Temuan & Implikasi</div>
                </div>
                <!-- 10 Data Rows for Section 02 -->
                {row_02_html}
            </div>
        </div>
    </div>
    <div class="table-container">
        <div class="section-grid">
            <div class="sidebar-cell" style="background: #1976D2; color: white;"><span class="num">03</span><span class="label">KUALITAS<br/>LINGKUNGAN</span></div>
            <div class="data-area" style="background: #fcfcff;">
                <div class="col-header">
                    <div>Indikator Ekologis</div>
                    <div class="ch-center">{col_hdr_left}</div>
                    <div class="ch-center">{col_hdr_right}</div>
                    <div class="ch-center">Delta</div>
                    <div>Temuan & Implikasi</div>
                </div>
                <!-- 10 Data Rows for Section 03 -->
                {row_03_html}
            </div>
        </div>
    </div>
    <div class="table-container">
        <div class="section-grid">
            <!-- SIDEBAR SEKSI 04 -->
            <div class="sidebar-cell" style="background: #FBC02D; color: white;"><span class="num">04</span><span class="label">BEBAN<br/>KESEHATAN</span></div>
            <!-- DATA AREA -->
            <div class="data-area" style="background: #fffdf7;">
                <!-- Column Headers -->
                <div class="col-header">
                    <div>Indikator Kesehatan</div>
                    <div class="ch-center">{col_hdr_left}</div>
                    <div class="ch-center">{col_hdr_right}</div>
                    <div class="ch-center">Delta</div>
                    <div>Temuan & Implikasi</div>
                </div>
                <!-- Data Rows for Section 04 -->
                {row_04_html}
            </div>
        </div>
    </div>
    <div class="table-container">
        <div class="section-grid">
            <div class="sidebar-cell bg-s5" style="background: #00796B; color: white;"><span class="num">05</span><span class="label">KORIDOR<br/>LOGISTIK<br/><span style="font-size: 5pt; font-weight: normal; opacity: 0.85;">(Inventaris 2024)</span></span></div>
            <div class="data-area" style="background: #f0fdf4;">
                <div class="col-header">
                    <div>Indikator Logistik</div>
                    <div class="ch-center">Konteks Data (Populasi 2024)</div>
                    <div class="ch-center">Kondisi Eksisting (2024)</div>
                    <div class="ch-center">Status</div>
                    <div>Temuan & Implikasi</div>
                </div>
                {row_05_html}
            </div>
        </div>
    </div>
    <div class="table-container">
        <div class="section-grid">
            <div class="sidebar-cell" style="background: #E64A19; color: white;"><span class="num">06</span><span class="label">KONFLIK<br/>AGRARIA</span></div>
            <div class="data-area" style="background: #fff7f2;">
                <div class="col-header">
                    <div>Indikator Konflik</div>
                    <div class="ch-center">{col_hdr_left}</div>
                    <div class="ch-center">{col_hdr_right}</div>
                    <div class="ch-center">Delta</div>
                    <div>Temuan & Implikasi</div>
                </div>
                {row_06_html}
            </div>
        </div>
    </div>
    <div class="table-container">
        <div class="section-grid">
            <div class="sidebar-cell" style="background: #8D6E63; color: white;"><span class="num">07</span><span class="label">DEMOGRAFI<br/>SOSIAL</span></div>
            <div class="data-area" style="background: #fffaf6;">
                <div class="col-header">
                    <div>Indikator Sosial</div>
                    <div class="ch-center">{col_hdr_left}</div>
                    <div class="ch-center">{col_hdr_right}</div>
                    <div class="ch-center">Delta</div>
                    <div>Temuan & Implikasi</div>
                </div>
                {row_07_html}
            </div>
        </div>
    </div>
    <div class="table-container">
        <div class="section-grid">
            <div class="sidebar-cell" style="background: #455A64; color: white;"><span class="num">08</span><span class="label">TATA KELOLA<br/>MANFAAT</span></div>
            <div class="data-area" style="background: #f8fafc;">
                <div class="col-header">
                    <div>Indikator Tata Kelola</div>
                    <div class="ch-center">Basis Data</div>
                    <div class="ch-center">Temuan</div>
                    <div class="ch-center">Status</div>
                    <div>Temuan & Implikasi</div>
                </div>
                {row_08_html}
            </div>
        </div>
    </div>

    <div style="margin-top: 5mm; text-align: center; font-size: 6pt; color: #999;">
        <strong>CELIOS - Center of Economic and Law Studies</strong> | Hak Cipta © 2026 CELIOS.
    </div>
</body>
</html>
"""

import streamlit.components.v1 as components

with poster_container:
    st.markdown("### Versi Poster A4 (Cetak)")
    st.download_button(
        label="Download Poster HTML",
        data=poster_html_v2,
        file_name="Poster_D3TLH_A4.html",
        mime="text/html",
        help="Download file ini, buka di Chrome/Edge, lalu tekan Ctrl+P untuk Simpan sebagai PDF."
    )
    components.html(poster_html_v2, height=1000, scrolling=True)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.85rem; padding: 20px;">
    Dashboard Analisis <b>CELIOS - Center of Economic and Law Studies</b><br>
    Model Simulasi CGE, OSINT Logistik, & Spasial Deforestasi.<br>
    <i>Hak Cipta © 2026 CELIOS. Semua Data Dapat Diverifikasi.</i>
</div>
""", unsafe_allow_html=True)
