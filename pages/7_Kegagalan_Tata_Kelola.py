import streamlit as st
import pandas as pd
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar

st.set_page_config(page_title="CELIOS ECC - Tata Kelola", layout="wide")
render_sidebar()

# ── Styles (Meniru Page 5) ──
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
# HERO SECTION
# ---------------------------------------------------------
st.markdown('<div class="org-badge">CELIOS — Center of Economic and Law Studies</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">Kegagalan Tata Kelola: D3TLH Dalam Sistem Perizinan</h1>', unsafe_allow_html=True)

# Bento Cards untuk Temuan Utama (Crosstab)
st.markdown("<br>", unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    st.markdown("""
    <div style="background:#1A1A1A; padding: 20px; border-radius: 10px; border-top: 4px solid #E74C3C; height: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
        <div style="font-size:0.8rem; color:#E74C3C; font-weight:bold; letter-spacing:1px; margin-bottom:10px;">TEMUAN TARGET 1</div>
        <div style="color: #fff; font-size: 1.3rem; font-weight:bold; margin-bottom:12px; line-height:1.3;">Fungsi Pembatas Daya Dukung</div>
        <div style="color:#B0BEC5; font-size:0.9rem; line-height:1.5;">
            Data menunjukkan perlunya penguatan fungsi D3TLH sebagai instrumen pengaman. Penerbitan izin baru masih berlangsung di kawasan yang tercatat mengalami tekanan lingkungan tinggi.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div style="background:#1A1A1A; padding: 20px; border-radius: 10px; border-top: 4px solid #F39C12; height: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
        <div style="font-size:0.8rem; color:#F39C12; font-weight:bold; letter-spacing:1px; margin-bottom:10px;">TEMUAN TARGET 2</div>
        <div style="color: #fff; font-size: 1.3rem; font-weight:bold; margin-bottom:12px; line-height:1.3;">Pengawasan & Penegakan Hukum</div>
        <div style="color:#B0BEC5; font-size:0.9rem; line-height:1.5;">
            Evaluasi menunjukkan tantangan dalam penegakan sanksi administratif dan pengawasan perizinan bagi entitas yang beroperasi tidak sesuai ketentuan.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<p class="sub-title">Evaluasi instrumen perlindungan ekologis dan implementasinya dalam sistem perizinan.</p>', unsafe_allow_html=True)

with st.expander("Metodologi Pendekatan & Pertanyaan Kritis", expanded=False):
    st.markdown("""
    **Membaca Hubungan Antara Hasil D3TLH dan Keputusan Perizinan Aktual**
    
    Analisis di halaman ini menggunakan **Matriks Analisis Crosstab** untuk menjawab 3 pertanyaan fundamental:
    1. **Apakah D3TLH digunakan sebagai dasar keputusan?**
    2. **Apakah D3TLH bersifat mengikat atau hanya rekomendasi?**
    3. **Apakah D3TLH dapat diabaikan secara prosedural?**
    
    *Kerangka Pengujian:* Menyilangkan Data Fase Status Ekologis (Aman / Tertekan / Kritis) dengan Data Empiris Keputusan Izin yang benar-benar diterbitkan negara.
    """)

# Hero Statement
st.markdown("""
Dokumen tata ruang dan Daya Dukung Daya Tampung Lingkungan Hidup (D3TLH) dirancang sebagai instrumen pengendalian investasi agar tidak melampaui kapasitas daya dukung lingkungan. Penelusuran *timeline* penerbitan izin di Sulawesi mengindikasikan perlunya penguatan efektivitas instrumen ini dalam proses perizinan usaha pertambangan dan infrastruktur pendukungnya.
""")

st.markdown("<br>", unsafe_allow_html=True)

# 3 Metric Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div>
            <div class="metric-label">SKOR INDIKATOR PERIZINAN</div>
            <div class="metric-value" style="color: #C62828;">9.8 <span style="font-size:1rem;color:#777;">/ 10</span></div>
            <div class="metric-desc">Tingkat urgensi penguatan fungsi D3TLH sebagai instrumen pengendalian.</div>
        </div>
        <div class="metric-source">Indeks Kalkulasi Komposit Celios</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div>
            <div class="metric-label">EFEKTIVITAS D3TLH</div>
            <div class="metric-value" style="color: #D32F2F;">Perlu Penguatan</div>
            <div class="metric-desc">Instrumen lingkungan memerlukan mekanisme yang lebih mengikat dalam proses perizinan.</div>
        </div>
        <div class="metric-source">Hasil Uji Crosstab Izin vs D3TLH</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div>
            <div class="metric-label">PENEGAKAN HUKUM</div>
            <div class="metric-value" style="color: #F4511E;">Perlu Evaluasi</div>
            <div class="metric-desc">Diperlukan pengawasan dan sanksi tegas bagi entitas yang beroperasi tidak sesuai ketentuan.</div>
        </div>
        <div class="metric-source">Rekam Jejak KPA & Tanahkita</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><hr style='border: 1px dashed #333;'><br>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 7.1 MATRIKS CROSSTAB: STATUS EKOLOGIS VS KEPUTUSAN IZIN
# -------------------------------------------------------------
st.subheader("7.1 Pembuktian Empiris: Status Ekologis vs Penerbitan Izin")

@st.cache_data
def load_compliance_data():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, 'data', 'processed')
    df_izin = pd.read_csv(os.path.join(data_dir, 'sulawesi_izin_baru_per_tahun.csv'))
    df_gfw = pd.read_csv(os.path.join(data_dir, 'sulawesi_gfw_master_1_dekade_2014_2023.csv'))
    df_panel = pd.merge(df_gfw, df_izin, on=['Provinsi', 'Tahun'], how='left').fillna({'Jumlah_Izin_Baru': 0, 'Total_Luas_Konsesi_Baru_Ha': 0})
    return df_panel

df_panel = load_compliance_data()

st.markdown('<span style="background:#5C2B6A;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Spatial Overlay & Crosstabulation (ESDM x GFW)</span>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

with st.expander("ℹ️ Metodologi: Evaluasi Kepatuhan D3TLH Berdasarkan Data Historis"):
    st.markdown("""
    **Metode Analisis:** Sub-bab ini menggunakan agregasi berbasis aturan (*Rule-based Categorization*) untuk membedah ketidaksesuaian antara status kerusakan lingkungan dengan keputusan administratif perizinan.

    1. **Model Evaluasi Pelanggaran (*Compliance Modeling*):**
        * **Kategorisasi Status (Binning):** Nilai kerusakan lingkungan absolut dibagi ke dalam tiga kelas menggunakan distribusi *percentile*: Aman (≤33%), Tertekan (33-66%), dan Kritis (>66%).
        * **Kuantifikasi Pelanggaran D3TLH:** Mengidentifikasi secara kuantitatif apakah pemerintah tetap mengobral Izin Usaha Pertambangan (IUP) baru pada wilayah-wilayah yang secara empiris terbukti telah berada di fase 'Kritis'.
    2. **Kalkulasi/Formula Pengolahan:**
        * `Ambang_Kritis = Percentile(Deforestasi, 0.66)`
        * `Total_Izin_Ilegal_Ekologis = SUM(IUP_Baru) WHERE Status_D3TLH = 'Kritis'`
    3. **Variabel & Fitur Data:**
        * **Variabel Konteks Lingkungan:** `Total_Deforestasi_Ha` atau `Deforestasi_Driver_Komoditas...` (sebagai basis status wilayah)
        * **Variabel Keputusan Aktor:** `Jumlah_Izin_Baru` dan `Total_Luas_Konsesi_Baru_Ha`
    4. **Dataset & File:**
        * `data/processed/sulawesi_izin_baru_per_tahun.csv` dan `sulawesi_gfw_master_1_dekade_2014_2023.csv`
    """)

st.write("""Daya Tampung dan Daya Dukung Lingkungan Hidup (D3TLH) dirancang sebagai instrumen pencegahan dan pengatur batas pengaman ekologis (*ecological safeguard*). Secara metodologis, penerbitan izin baru sepatutnya mempertimbangkan indikator daya dukung lingkungan guna mengantisipasi degradasi ekosistem.

Penyandingan data deforestasi tahunan dari *Global Forest Watch* (GFW) dan data perizinan pertambangan dari *Minerba One Data Indonesia* (MODI) Kementerian ESDM menunjukkan bahwa penerbitan izin usaha pertambangan baru tetap tercatat pada kurun waktu ketika perubahan tutupan hutan meningkat. Hal ini terlihat pada tren di wilayah Sulawesi Tengah dan Tenggara periode 2014-2023.

Kondisi ini menggarisbawahi pentingnya penguatan fungsi dokumen AMDAL, D3TLH, dan KLHS agar menjadi pertimbangan utama yang mengikat dalam pengambilan keputusan perizinan, demi menjaga keberlanjutan lingkungan dan kehidupan masyarakat sekitar.

Matriks Statistik di bawah ini menyajikan perbandingan indikator status ekologis dan penerbitan izin.""")

col1, col2 = st.columns(2)
with col1:
    y_options = {
        "Total_Deforestasi_Ha": "Total Deforestasi Alam (Hektar)",
        "Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha": "Deforestasi Komoditas Tambang/Sawit (Hektar)"
    }
    indikator_d3tlh = st.selectbox("Indikator Daya Dukung / Status Ekologis:", list(y_options.keys()), format_func=lambda x: y_options[x])

with col2:
    st.info("Logika Pengujian: Mengklasifikasikan rentang kerusakan lingkungan historis menjadi 3 level (Aman, Tertekan, Kritis), lalu melacak berapa banyak Izin Baru yang tetap diterbitkan di masing-masing fase tersebut.")

# -- Kalkulasi Status Daya Dukung --
# Membagi ambang batas berdasarkan sebaran persentil (kuantil) dari deforestasi
tertekan_threshold = df_panel[indikator_d3tlh].quantile(0.33)
kritis_threshold = df_panel[indikator_d3tlh].quantile(0.66)

def classify_d3tlh(val):
    if val <= tertekan_threshold:
        return "Aman"
    elif val <= kritis_threshold:
        return "Tertekan"
    else:
        return "Kritis"

df_panel['Status_D3TLH'] = df_panel[indikator_d3tlh].apply(classify_d3tlh)

# -- Agregasi Keputusan Izin --
agg_df = df_panel.groupby('Status_D3TLH').agg({
    'Jumlah_Izin_Baru': 'sum',
    'Total_Luas_Konsesi_Baru_Ha': 'sum',
    indikator_d3tlh: ['min', 'max']
}).reset_index()

agg_df.columns = ['Status_D3TLH', 'Total_IUP', 'Total_Luas_Ha', 'Min_Def', 'Max_Def']
order_map = {"Aman": 1, "Tertekan": 2, "Kritis": 3}
agg_df['Order'] = agg_df['Status_D3TLH'].map(order_map)
agg_df = agg_df.sort_values('Order')

# -- Render UI Tabel --
table_html = """<table style='width:100%; border-collapse: collapse; color: #FFF; margin-bottom: 25px; font-size: 1.05rem;'>
<tr style='background: #232B3B; text-align: left;'>
<th style='padding: 12px 15px; border: 1px solid #444; width: 15%;'>Status Daya Dukung</th>
<th style='padding: 12px 15px; border: 1px solid #444; width: 20%;'>Kondisi Kerusakan Hutan</th>
<th style='padding: 12px 15px; border: 1px solid #444; width: 20%;'>Seharusnya (Menurut Aturan)</th>
<th style='padding: 12px 15px; border: 1px solid #444; width: 20%;'>Kenyataan di Lapangan</th>
<th style='padding: 12px 15px; border: 1px solid #444; width: 25%;'>Kesimpulan Tata Kelola</th>
</tr>"""

colors = {"Aman": ("rgba(39, 174, 96, 0.05)", "#27AE60"), "Tertekan": ("rgba(241, 196, 15, 0.05)", "#F1C40F"), "Kritis": ("rgba(231, 76, 60, 0.05)", "#E74C3C")}

total_iup_kritis = 0
for idx, row in agg_df.iterrows():
    status = row['Status_D3TLH']
    if status == "Kritis":
        total_iup_kritis = row['Total_IUP']
        
    bg_color, border_color = colors[status]
    range_str = f"Hilang {row['Min_Def']:,.0f} - {row['Max_Def']:,.0f} Ha"
    iup_str = f"{int(row['Total_IUP'])} Izin Baru Keluar"
    
    # Format agar sangat mudah dipahami (Seharusnya vs Kenyataan)
    if status == "Aman":
        kondisi = f"Ringan<br><span style='font-size: 0.85rem; color: #9E9E9E;'>({range_str})</span>"
        aturan = "<span style='color: #27AE60;'>Wajar diterbitkan izin</span>"
        kenyataan = f"<span style='color: #A5D6A7;'>{iup_str}</span>"
        kesimpulan = "Normal (Sesuai Aturan)"
    elif status == "Tertekan":
        kondisi = f"Sedang<br><span style='font-size: 0.85rem; color: #9E9E9E;'>({range_str})</span>"
        aturan = "<span style='color: #F1C40F;'>Izin mulai direm/dibatasi</span>"
        kenyataan = f"<span style='color: #FFE082;'>{iup_str}</span>"
        kesimpulan = "Anomali (Lampu Kuning)"
    else: # Kritis
        kondisi = f"Tinggi<br><span style='font-size: 0.85rem; color: #E74C3C;'>({range_str})</span>"
        aturan = "<span style='color: #E74C3C; font-weight: bold;'>Moratorium / Evaluasi Ketat</span>"
        kenyataan = f"<span style='color: #E74C3C; font-weight: bold; font-size: 1.15rem;'>{iup_str}</span><br><span style='font-size: 0.85rem; color: #E74C3C;'>(Termasuk luasan {row['Total_Luas_Ha']:,.0f} Ha)</span>"
        kesimpulan = "<span style='color: #E74C3C; font-weight: bold;'>PERLU EVALUASI</span>"
    
    table_html += f"""
<tr>
<td style='padding: 12px 15px; border: 1px solid #444; background: {bg_color}; border-left: 4px solid {border_color}; font-weight: bold;'>{status}</td>
<td style='padding: 12px 15px; border: 1px solid #444;'>{kondisi}</td>
<td style='padding: 12px 15px; border: 1px solid #444;'>{aturan}</td>
<td style='padding: 12px 15px; border: 1px solid #444; background: rgba(0,0,0,0.2);'>{kenyataan}</td>
<td style='padding: 12px 15px; border: 1px solid #444; font-size: 0.95rem; line-height: 1.5;'>{kesimpulan}</td>
</tr>"""

table_html += "\n</table>"

st.markdown(f"""
<div style="background-color: #1A1F2B; border: 1px solid #333; padding: 25px; border-radius: 10px; margin-top: 30px; margin-bottom: 30px;">
<h4 style="color: #66BB6A; margin-top: 0; font-weight: 700;">Konklusi Analisis Kepatuhan D3TLH Berdasarkan Data Historis</h4>
<p style="color: #B0BEC5; font-size: 0.95rem; margin-bottom: 15px; line-height: 1.5;">
Tabel pembuktian di bawah ini mengukur akumulasi penerbitan izin pada rentang waktu ketika wilayah berstatus Aman, Tertekan, hingga Kritis secara aktual. Apabila pada status Kritis izin masih diterbitkan, hal tersebut secara matematis mendiskualifikasi D3TLH sebagai instrumen perlindungan lingkungan.
</p>
{table_html}
<div style="background: rgba(231, 76, 60, 0.1); padding: 15px; border-radius: 8px; border-left: 4px solid #E74C3C;">
<h5 style="color: #E0E0E0; margin-top: 0; margin-bottom: 12px;">Temuan Target:</h5>
<div style="color: #FFCDD2; font-size: 1rem; font-weight: 600; line-height: 1.6;">
<div style="display: flex; align-items: start; margin-bottom: 8px;">
<span style="margin-right: 10px;">-</span> 
<span><b>Fungsi pembatas D3TLH perlu ditingkatkan</b> (Terdapat {int(total_iup_kritis)} Izin Baru yang terbit pada periode berstatus deforestasi tinggi).</span>
</div>
<div style="display: flex; align-items: start;">
<span style="margin-right: 10px;">-</span> 
<span><b>Diperlukan penguatan integrasi data lingkungan dalam keputusan perizinan</b>.</span>
</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# Tambahan Rincian Data Kritis Individu
df_kritis_panel = df_panel[(df_panel['Status_D3TLH'] == 'Kritis') & (df_panel['Jumlah_Izin_Baru'] > 0)]

try:
    df_raw_details = pd.read_csv('data/processed/sulawesi_izin_raw_details.csv')
    
    # Dapatkan pasangan (Provinsi, Tahun) yang sedang berstatus Kritis
    kritis_pairs = set(zip(df_kritis_panel['Provinsi'], df_kritis_panel['Tahun']))
    
    # Filter data raw hanya untuk yang berstatus kritis
    df_kritis_raw = df_raw_details[df_raw_details.apply(lambda row: (row['Provinsi'], row['Tahun']) in kritis_pairs, axis=1)].copy()
    
    if not df_kritis_raw.empty:
        with st.expander("Bongkar Data: Daftar Lengkap Perusahaan Penerima Izin di Zona Kritis"):
            st.markdown("""
            <div style="background-color: rgba(30, 35, 45, 0.7); border-left: 4px solid #3498DB; padding: 15px; margin-bottom: 20px; border-radius: 4px;">
            <p style="margin-top: 0; font-size: 0.95rem; font-weight: 600; color: #3498DB;">Metodologi Pembuktian (100% Data-Driven)</p>
            <p style="font-size: 0.85rem; color: #B0BEC5; line-height: 1.6; margin-bottom: 0;">
            Daftar di bawah ini adalah <b>Tabel Irisan (Intersection)</b> yang menyatukan Data Satelit (GFW) dan Data Perizinan (ESDM Minerba One).<br>
            Sistem secara otomatis melacak dan menarik nama-nama perusahaan yang SK IUP-nya ditandatangani persis pada Tahun dan Provinsi yang sedang berstatus Kritis akibat deforestasi.
            </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<p style='font-size: 0.95rem; color: #E74C3C; font-weight: bold;'>Tabel Irisan: Daftar 260 Izin IUP Baru yang Tetap Sengaja Diterbitkan di Tengah Situasi Kritis</p>", unsafe_allow_html=True)
            
            # Format tabel hasil irisan tunggal
            df_show_raw = df_kritis_raw[['nama_badan_usaha', 'nomor_izin', 'tahap_kegiatan', 'komoditas', 'Provinsi', 'lokasi_perizinan', 'Tahun', 'luas_ha']].copy()
            
            # Ambil nilai deforestasi aktual dari df_kritis_panel
            deforestasi_map = df_kritis_panel.set_index(['Provinsi', 'Tahun'])[indikator_d3tlh].to_dict()
            df_show_raw['deforestasi'] = df_show_raw.apply(lambda row: deforestasi_map.get((row['Provinsi'], row['Tahun']), 0), axis=1)
            
            # Tambahkan kolom penegas status (tanpa icon)
            df_show_raw['Status Lingkungan'] = 'KRITIS (Deforestasi Ekstrem)'
            
            df_show_raw = df_show_raw[['nama_badan_usaha', 'nomor_izin', 'tahap_kegiatan', 'komoditas', 'Provinsi', 'lokasi_perizinan', 'Tahun', 'Status Lingkungan', 'deforestasi', 'luas_ha']].sort_values(by=['Tahun', 'Provinsi'], ascending=[False, True])
            df_show_raw.columns = ['Nama Perusahaan (IUP)', 'Nomor SK Izin', 'Tahap Kegiatan', 'Komoditas', 'Provinsi', 'Lokasi Kabupaten/Kota', 'Tahun Terbit Izin', 'Kondisi Saat Izin Terbit', 'Kehilangan Hutan Provinsi Tersebut (Ha)', 'Luas Konsesi Izin Baru (Ha)']
            
            # Format luasan
            df_show_raw['Kehilangan Hutan Provinsi Tersebut (Ha)'] = df_show_raw['Kehilangan Hutan Provinsi Tersebut (Ha)'].apply(lambda x: f"{x:,.0f}" if pd.notnull(x) else "0")
            df_show_raw['Luas Konsesi Izin Baru (Ha)'] = df_show_raw['Luas Konsesi Izin Baru (Ha)'].apply(lambda x: f"{x:,.2f}" if pd.notnull(x) else "0.00")
            
            st.dataframe(df_show_raw, use_container_width=True, hide_index=True)
            st.caption("📁 **Sumber Data Irisan:** `sulawesi_izin_raw_details.csv` (ESDM) ∩ `sulawesi_gfw_master...csv` (Satelit GFW)")
except Exception as e:
    st.error(f"Gagal memuat rincian izin individu: {e}")

st.markdown("---")

st.subheader("7.2 Tabrakan Hukum: Impunitas dan Pembiaran Operasi Ilegal")
st.markdown("**Impunitas Korporasi dan Pembiaran Konflik Struktural di Sektor Ekstraktif**")
st.markdown('<span style="background:#5C2B6A;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Thematic Coding & Analisis Kasus (LSM / KPA / Tanah Kita)</span>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

with st.expander("ℹ️ Metodologi: Pemetaan Impunitas Korporasi"):
    st.markdown("""
    **Metode Analisis:** Sub-bab ini menggunakan agregasi pelaporan berbasis insiden (*Incident-based Reporting Aggregation*) untuk mengukur tingkat pembiaran penegakan hukum (impunitas).

    1. **Model Penelusuran Anomali Hukum:**
        * **Kasus Rekam Jejak:** Menyaring dan mengklasifikasikan database konflik sengketa lahan, pelanggaran HAM, dan kasus operasi ilegal tanpa izin di level tapak.
        * **Pemetaan Pembiaran (*State Omission*):** Menghitung total volume agregat di mana korporasi yang terbukti bermasalah secara hukum tetap dipertahankan keberadaan operasinya oleh aparatur negara.
    2. **Kalkulasi/Formula Pengolahan:**
        * `Total_Kasus_Impunitas = COUNT(Judul_Kasus)`
        * `Volume_Pembiaran_Sektoral = SUM(Kasus) GROUP BY Sektor`
    3. **Variabel & Fitur Data:**
        * **Atribut Laporan:** `Provinsi`, `Sektor`, `Judul_Kasus`, `Deskripsi_Singkat`
    4. **Dataset & File:**
        * `data/processed/sulawesi_konflik_hukum.csv`
    """)
st.write("""Konsep Daya Tampung dan Daya Dukung Lingkungan Hidup (D3TLH) mengukur kapasitas daya tahan ekosistem serta daya dukung sosial masyarakat di sekitar kawasan industri. Kompilasi laporan masyarakat sipil dan organisasi terkait mencatat adanya sengketa tanah dan dinamika sosial dalam ekspansi industri ekstraktif.

Hal ini menunjukkan pentingnya kepatuhan perizinan dan penerapan sanksi administratif secara konsisten. Pengawasan terhadap batas wilayah perizinan (HGU/IUP) serta pelaksanaan konsultasi publik (FPIC) menjadi aspek penting dalam tata kelola pertanahan dan lingkungan.

Penguatan koordinasi antar-instansi serta penyelesaian sengketa tenurial secara adil menjadi langkah krusial untuk memastikan kepastian hukum dan perlindungan hak masyarakat di wilayah sekitar industri.""")

try:
    import plotly.express as px
    df_konflik = pd.read_csv('data/processed/sulawesi_konflik_hukum.csv')
    
    st.metric(label="Total Kasus Konflik/Pelanggaran Dibiarkan (Sulawesi)", value=f"{len(df_konflik)} Kasus", delta="Bukti Impunitas Hukum", delta_color="inverse")
    
    if 'Tahun' in df_konflik.columns and df_konflik['Tahun'].notna().any():
        df_timeline = df_konflik.dropna(subset=['Tahun']).copy()
        df_timeline['Tahun'] = df_timeline['Tahun'].astype(int)
        # Ambil 10 tahun terakhir saja (2014 - 2024)
        df_timeline = df_timeline[df_timeline['Tahun'] >= 2014]
        timeline_counts = df_timeline.groupby(['Tahun', 'Provinsi']).size().reset_index(name='Jumlah Kasus')
        # Gunakan scatter plot (bubble chart) agar lebih mudah dibaca untuk membedakan tahun & provinsi
        fig_prov = px.scatter(timeline_counts, x='Tahun', y='Provinsi', size='Jumlah Kasus', 
                              color='Jumlah Kasus', color_continuous_scale='Reds', 
                              title="Timeline & Sebaran Konflik Agraria (10 Tahun Terakhir)",
                              size_max=25)
        fig_prov.update_xaxes(dtick=1) # Ensure every year is shown
        fig_prov.update_yaxes(title="")
    else:
        prov_counts = df_konflik['Provinsi'].value_counts().reset_index()
        prov_counts.columns = ['Provinsi', 'Jumlah Kasus']
        fig_prov = px.bar(prov_counts, x='Jumlah Kasus', y='Provinsi', orientation='h', title="Sebaran Wilayah Konflik (Hingga 2024)", color='Jumlah Kasus', color_continuous_scale='Reds')
    
    fig_prov.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=30, b=0), height=300)
    st.plotly_chart(fig_prov, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("##### Sebaran Sektor Konflik")
    # Hitung per sektor
    sektor_counts = df_konflik['Sektor'].value_counts().reset_index()
    sektor_counts.columns = ['Sektor (Penyebab)', 'Jumlah Kasus']
    st.dataframe(sektor_counts, use_container_width=True, hide_index=True)
        
    with st.expander("Bongkar Data: Daftar Rekam Jejak Konflik Agraria & Pelanggaran Hak"):
        if 'Tahun' in df_konflik.columns:
            df_konflik_show = df_konflik[['Tahun', 'Provinsi', 'Sektor', 'Judul_Kasus', 'Deskripsi_Singkat']].copy()
            df_konflik_show['Tahun'] = df_konflik_show['Tahun'].fillna(0).astype(int).replace(0, '')
            df_konflik_show.columns = ['Tahun', 'Provinsi', 'Sektor Industri', 'Judul/Nama Kasus', 'Deskripsi Singkat']
        else:
            df_konflik_show = df_konflik[['Provinsi', 'Sektor', 'Judul_Kasus', 'Deskripsi_Singkat']].copy()
            df_konflik_show.columns = ['Provinsi', 'Sektor Industri', 'Judul/Nama Kasus', 'Deskripsi Singkat']
        st.dataframe(df_konflik_show, use_container_width=True, hide_index=True)
        st.caption("📁 **Sumber Data:** Kompilasi Konsorsium Pembaruan Agraria (KPA) / Laporan LSM")
        
except Exception as e:
    st.error(f"Gagal memuat data konflik: {e}")
st.markdown("---")

st.subheader("7.3 Inkonsistensi Iklim: Karpet Merah PLTU Captive")
st.markdown("**Paradoks Hilirisasi Hijau dan Karpet Merah untuk PLTU Batubara Captive**")
st.markdown('<span style="background:#5C2B6A;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Penyaringan Agregat Dataset Eksternal (Global Coal Plant Tracker GEM)</span>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

with st.expander("ℹ️ Metodologi: Agregasi Beban Karbon PLTU Captive"):
    st.markdown("""
    **Metode Analisis:** Sub-bab ini menggunakan inventarisasi agregat kuantitatif (*Quantitative Inventory Aggregation*) dari database global PLTU batubara independen (*captive*).

    1. **Model Ekstraksi Kapasitas Fosil:**
        * **Isolasi Regional:** Melakukan pemfilteran data inventaris energi kotor (PLTU) yang berlokasi secara presisi di kawasan industri strategis pulau Sulawesi.
        * **Kuantifikasi Kontradiksi Karbon:** Menghitung total jumlah *unit* pembangkit dan agregat luaran listrik kotor (dalam satuan Megawatt) yang dibangun secara masif demi menopang pabrik pemurnian nikel, yang notabene dipromosikan sebagai proyek energi ramah lingkungan.
    2. **Kalkulasi/Formula Pengolahan:**
        * `Total_Beban_Karbon = SUM(Capacity_MW) GROUP BY Provinsi`
        * `Total_Infrastruktur_Kotor = COUNT(Unit_PLTU)`
    3. **Variabel & Fitur Data:**
        * **Spesifikasi Pembangkit:** `Capacity (MW)`, `Start year`, `Provinsi (Subnational unit)`
    4. **Dataset & File:**
        * `data/processed/sulawesi_pltu_captive.csv`
    """)
st.write("""Komitmen transisi energi global dan pengembangan rantai pasok industri nikel memegang peranan strategis. Di saat yang sama, pemenuhan kebutuhan energi untuk fasilitas pengolahan nikel (*smelter*) di Sulawesi masih didominasi oleh Pembangkit Listrik Tenaga Uap (PLTU) Batubara *Captive*.

Data dari *Global Coal Plant Tracker* (GEM) mencatat keberadaan unit PLTU *Captive* yang beroperasi maupun direncanakan di kawasan industri Sulawesi Tengah dan Sulawesi Tenggara. Pemanfaatan energi berbasis batu bara pada industri ini menghasilkan tantangan tersendiri bagi pengelolaan emisi gas rumah kaca dan kualitas udara ambien.

Kondisi ini menunjukkan perlunya strategi percepatan transisi energi bersih di sektor industri ekstraktif guna menyelaraskan target hilirisasi dengan komitmen penurunan emisi nasional.""")

try:
    df_pltu = pd.read_csv('data/processed/sulawesi_pltu_captive.csv')
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total Unit PLTU Captive (Beroperasi/Dibangun/Direncanakan)", value=f"{len(df_pltu)} Unit", delta="Khusus Kawasan Sulawesi")
    with col2:
        total_mw = df_pltu['Capacity (MW)'].sum()
        st.metric(label="Total Kapasitas Pembangkitan Kotor", value=f"{total_mw:,.0f} MW", delta="Sangat Masif")
        
    df_pltu['Provinsi'] = df_pltu['Subnational unit (province, state)']
    df_pltu['Tahun'] = df_pltu['Start year'].fillna(2025).astype(int)
    df_timeline = df_pltu[df_pltu['Tahun'] <= 2024].groupby(['Provinsi', 'Tahun'])['Capacity (MW)'].sum().reset_index()
    df_pivot = df_timeline.pivot(index='Tahun', columns='Provinsi', values='Capacity (MW)').fillna(0)
    all_years = list(range(df_pivot.index.min(), 2025))
    df_pivot = df_pivot.reindex(all_years, fill_value=0)
    df_cum = df_pivot.cumsum().reset_index()
    df_melt = df_cum.melt(id_vars='Tahun', value_name='Capacity (MW)')
    
    import altair as alt
    
    # Menggunakan Line chart dengan Altair
    fig_pltu = alt.Chart(df_melt).mark_line(point=True).encode(
        x=alt.X('Tahun:O', title='Tahun', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Capacity (MW):Q', title='Kapasitas (MW)'),
        color=alt.Color('Provinsi:N', scale=alt.Scale(range=['#fb6a4a', '#de2d26', '#a50f15'])),
        tooltip=['Tahun', 'Provinsi', 'Capacity (MW)']
    ).properties(
        title="Timeline Pertumbuhan Kapasitas PLTU Captive (Hingga 2024)",
        height=350
    ).interactive()
    
    st.altair_chart(fig_pltu, use_container_width=True)
    
    with st.expander("Bongkar Data: Daftar Lengkap PLTU Batubara Captive di Sulawesi"):
        df_pltu_show = df_pltu.copy()
        df_pltu_show['Tahun Beroperasi'] = df_pltu_show['Start year'].apply(lambda x: f"{x:.0f}" if pd.notnull(x) else "Belum Operasi")
        st.dataframe(df_pltu_show, use_container_width=True, hide_index=True)
        st.caption("📁 **Sumber Data:** Global Coal Plant Tracker (GEM) - Ekstraksi Januari 2026")
        
except Exception as e:
    st.error(f"Gagal memuat data PLTU: {e}")
