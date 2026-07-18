import streamlit as st
import os
import sys

# Konfigurasi path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar

st.set_page_config(
    page_title="Daftar Isi — CELIOS D3TLH",
    page_icon="refrensi/Celios China-Indonesia Energy Transition.png",
    layout="wide"
)
render_sidebar()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }

.toc-header {
    font-size: 2.8rem;
    font-weight: 800;
    color: #43A047;
    margin-bottom: 0.5rem;
    border-bottom: 2px solid #2E7D32;
    padding-bottom: 10px;
}
.toc-desc {
    color: #B0BEC5;
    font-size: 1.1rem;
    margin-bottom: 2.5rem;
}
.bab-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #ECEFF1;
    margin-bottom: 8px;
    border-left: 4px solid #43A047;
    padding-left: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="toc-header">Daftar Isi Laporan</div>', unsafe_allow_html=True)
st.markdown('<div class="toc-desc">Sistem Navigasi Riset Daya Dukung Lingkungan Hidup (D3TLH) Sulawesi</div>', unsafe_allow_html=True)

import re

def get_page_url_path(page_path):
    basename = os.path.basename(page_path).replace('.py', '')
    # Menghapus angka dan underscore di awal nama file (misal 1_Ekspansi -> Ekspansi)
    return re.sub(r'^\d+_', '', basename)

def slugify(text):
    text = text.lower()
    # Streamlit mengganti . menjadi - dan & menjadi and
    text = text.replace('.', '-')
    text = text.replace('&', 'and')
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def render_bab(title, page_path, sub_items):
    with st.container():
        st.markdown(f'<div class="bab-title">{title}</div>', unsafe_allow_html=True)
        if page_path:
            # Streamlit native link untuk Halaman Utama Bab
            st.page_link(page_path, label="Buka Halaman Utama Bab", icon="🔗")
            
        if sub_items and page_path:
            page_url = get_page_url_path(page_path)
            
            for item in sub_items:
                if isinstance(item, tuple):
                    display_text, target_text = item
                else:
                    display_text = item
                    target_text = item
                    
                hash_id = slugify(target_text)
                # Gunakan standard markdown link karena Streamlit frontend akan meng-intercept 
                # link internal (dimulai dengan /) dan menangani anchor scrolling-nya secara native
                # tanpa full page reload.
                st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;▪️ [{display_text}](/{page_url}#{hash_id})")
        
        st.markdown('<hr style="border-top:1px dashed #2A2F3B; margin-top: 15px; margin-bottom: 25px;">', unsafe_allow_html=True)

# BAB 1
render_bab(
    "BAB 1: EKSPANSI INDUSTRI", 
    "pages/1_Ekspansi_Industri.py",
    [
        ("1.1 Konteks Makro", "1.1 Konteks Makro: Breakdown PDRB per Komoditas"),
        "1.2 Agresivitas Ekspansi Kawasan Industri & PLTU Captive",
        "1.3 Tren Pertumbuhan Izin Tambang Baru & Uji Signifikansi",
        "1.4 Paradoks Industri: Ekspansi Izin Tambang vs Kebangkrutan Ekologis",
        "1.5 Pelabuhan Ekspor: Ke Mana Nikel Sulawesi Dikirim?",
        "1.6 Peta Jalur Distribusi Logistik Nikel Sulawesi"
    ]
)

# BAB 2
render_bab(
    "BAB 2: KUALITAS LINGKUNGAN",
    "pages/2_Kualitas_Lingkungan.py",
    [
        ("2.1 Dampak Limbah Tailing: Konsentrasi Smelter vs IKA", "2.1. Dampak Limbah Tailing: Konsentrasi Smelter vs Indeks Kualitas Air (IKA)"),
        ("2.2 Kepungan Asap: PLTU Captive vs IKU", "2.2. Kepungan Asap: Kapasitas PLTU vs Indeks Kualitas Udara (IKU)"),
        ("2.3 Eksekusi Ruang: Ekspansi Kawasan Industri vs Deforestasi", "2.3. Eksekusi Ruang: Ekspansi Kawasan Industri vs Tekanan Ekologis (Deforestasi)"),
        ("2.4 Driver Deforestasi: Anatomi Pembantaian Hutan", "2.4. Driver Deforestasi: Anatomi Pembantaian Hutan"),
        ("2.5 Kehancuran Biodiversitas: Ekstirpasi Habitat Satwa Endemik", "2.5. Kehancuran Biodiversitas: Ekstirpasi Habitat Satwa Endemik")
    ]
)

# BAB 3
render_bab(
    "BAB 3: BEBAN KESEHATAN",
    "pages/3_Beban_Kesehatan.py",
    [
        ("3.1 Kesenjangan Fasilitas Kesehatan di Kawasan Ekstraktif", "3.1 Kesenjangan Fasilitas Kesehatan di Kawasan Ekstraktif"),
        ("3.2 Ketimpangan Beban Penyakit: Sentra Industri vs Non-Sentra", "3.2 Ketimpangan Beban Penyakit: Sentra Industri vs Non-Sentra"),
        ("3.3 Lintasan Waktu Ekologis & Ledakan Penyakit", "3.3 Lintasan Waktu Ekologis & Ledakan Penyakit di Kawasan Industri Ekstraktif"),
        ("3.4 Anomali Zoonosis: Dampak Kritis Ekspansi Industri", "3.4 Anomali Zoonosis: Dampak Kritis Ekspansi Industri di Level Tapak (Studi Kasus Sulteng)"),
        ("3.5 Pemetaan Geospasial: Episentrum Ledakan Penyakit", "3.5 Pemetaan Geospasial: Episentrum Ledakan Penyakit"),
        ("3.6 Krisis Air Bersih: Penurunan IKA & Ledakan Kasus Diare", "3.6 Krisis Air Bersih: Penurunan IKA & Ledakan Kasus Diare di Kawasan Industri Ekstraktif"),
        ("3.7 Beban Limbah Beracun (B3): Eksternalitas Kesehatan", "3.7 Beban Limbah Beracun (B3): Eksternalitas Kesehatan yang Diabaikan")
    ]
)

# BAB 4
render_bab(
    "BAB 4: KONFLIK SOSIAL",
    "pages/4_Konflik_Sosial.py",
    [
        ("4.1 Tren Eskalasi Konflik Agraria", "4.1 Tren Eskalasi Konflik Agraria Seiring Ekspansi Industri"),
        ("4.2 Sebaran Sektoral: Korban Jiwa & Monopoli", "4.2 Sebaran Sektoral: Korban Jiwa dan Monopoli Ruang"),
        ("4.3 Kriminalisasi Aktivis & Resistensi Sipil", "4.3 Kriminalisasi Aktivis dan Resistensi Ruang Sipil"),
        ("4.4 Pembuktian Statistik: Crosstab (Ekspansi vs Represi)", "4.4 Pembuktian Statistik: Ekspansi vs Eskalasi Konflik"),
        ("4.5 Peta Orkestrasi Konflik: Aktor Sipil vs Aktor Ekstraktif", "4.5 Peta Orkestrasi Konflik: Aktor Sipil vs Aktor Ekstraktif")
    ]
)

# BAB 5
render_bab(
    "BAB 5: POLA PENERBITAN IZIN",
    "pages/5_Pola_Penerbitan_Izin.py",
    [
        ("5.1 Sinkronisasi Waktu: Deforestasi vs Laju Izin", "5.1 Fakta Penyebab: Sinkronisasi Waktu (Timeline Mapping)"),
        ("5.2 Fakta Spasial: Tabrakan Tata Ruang di Kawasan Konservasi", "5.2 Fakta Spasial: Tabrakan Tata Ruang di Kawasan Konservasi"),
        ("5.3 Realitas Lapangan: Izin Bermasalah & FPIC Diabaikan", "5.3 Realitas Lapangan: Izin Bermasalah, FPIC Diabaikan, Masyarakat Dikorbankan"),
        ("5.4 Pembuktian Empiris: Uji Statistik Crosstab", "5.4 Pembuktian Empiris: Uji Statistik Korelasi Penerbitan Izin & Deforestasi")
    ]
)

# BAB 6 & 7
render_bab("BAB 6: AUDIT D3TLH", "pages/6_Audit_D3TLH.py", [])
render_bab("BAB 7: KEGAGALAN TATA KELOLA", "pages/7_Kegagalan_Tata_Kelola.py", [
    ("7.1 Status Ekologis vs Keputusan Izin", "7.1 Pembuktian Empiris: Status Ekologis vs Penerbitan Izin"),
    ("7.2 Impunitas Korporasi: Sebaran Kasus Dibiarkan", "7.2 Tabrakan Hukum: Impunitas dan Pembiaran Operasi Ilegal"),
    ("7.3 Inkonsistensi Iklim: PLTU Captive", "7.3 Inkonsistensi Iklim: Karpet Merah PLTU Captive")
])

# BAB 8
render_bab(
    "BAB 8: DISTRIBUSI MANFAAT",
    "pages/8_Distribusi_Manfaat.py",
    [
        ("8.1 Sisi Manfaat: Gurita Bisnis & Monopoli Keuntungan", "8.1 Sisi Manfaat: Gurita Bisnis & Monopoli Keuntungan Ekstraktif"),
        ("8.2 Sisi Beban: Kematian, Penyakit, dan Konflik", "8.2 Sisi Beban: Kematian, Penyakit, dan Konflik yang Disosialisasikan"),
        ("8.3 Pembuktian Statistik: Manfaat Ekonomi vs Beban Ekologis", "8.3. Pembuktian Statistik: Oligarki Untung, Rakyat Buntung")
    ]
)

# BAB 11
render_bab(
    "BAB 11: DEMOGRAFI SOSIAL", 
    "pages/11_Demografi_Sosial.py", 
    [
        ("9.1 Tekanan Demografi di Kabupaten Industri Ekstraktif", "9.1 Tekanan Demografi di Kabupaten Industri Ekstraktif"),
        ("9.2 Intensifikasi Ruang: Kepadatan Industri", "9.2 Intensifikasi Ruang: Kepadatan Industri Ekstraktif vs Non-Ekstraktif"),
        ("9.3 Pergeseran Ekonomi Agraris ke Tambang", "9.3 Pergeseran Ekonomi Agraris ke Tambang dan Industri"),
        ("9.4 Sintesis: Matriks Tekanan Sosial-Ekologis", "9.4 Sintesis: Matriks Tekanan Sosial-Ekologis")
    ]
)

# RANGKUMAN
st.markdown('<div class="toc-header" style="font-size: 2rem; margin-top: 30px;">Rangkuman & Visualisasi Data</div>', unsafe_allow_html=True)
st.markdown('<br>', unsafe_allow_html=True)

render_bab("Executive Summary (Ringkasan Laporan Utama)", "pages/0_Overview_Temuan.py", [])
render_bab("Dashboard Statistik (Summary Visual)", "pages/12_Infografis_Summary.py", [])
render_bab("Temuan Utama (Narasi Infografis)", "pages/13_Infografis_Fakta.py", [])

st.markdown("<br><br><br>", unsafe_allow_html=True)
