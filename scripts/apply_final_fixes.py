def patch_file():
    with open('pages/1_Ekspansi_Industri.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Part 1: Combine method tag and expander
    old_method = '''st.markdown('<span style="background:#4A148C;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Open Source Intelligence (OSINT)</span>', unsafe_allow_html=True)
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

with st.expander("ℹ️ Metodologi: Open Source Intelligence (OSINT)"):
    st.markdown("""
    **Metode Analisis:** Halaman ini menggunakan teknik investigasi *Open Source Intelligence* (OSINT) dan Studi Literatur Forensik untuk memetakan rantai pasok dan monopoli infrastruktur logistik pesisir.

    1. **Kurasi & Validasi Silang (Cross-Validation):** Membangun matriks relasional dari sumber-sumber publik yang berserakan.
        * **Triangulasi Data:** Mencocokkan data citra satelit, dokumen perizinan lingkungan, dan laporan pengiriman kargo (ekspor).
        * Hipotesis Kerja: Infrastruktur PSN secara eksklusif dibangun bukan untuk publik, melainkan sebagai "karpet merah" kelancaran rantai pasok oligarki nikel ke pasar global.
    2. **Kalkulasi/Formula Pengolahan:** Menghitung jumlah fasilitas pelabuhan aktif dan persentase yang terafiliasi dengan status PSN.
        * Rasio Dominasi PSN = (Fasilitas_PSN / Total_Fasilitas) * 100%
    3. **Variabel & Fitur Data (Tabular OSINT):**
        * **Nama Kawasan Industri, Pemilik/Pengelola Induk:** Identitas kawasan sentra.
        * **Provinsi, Kabupaten/Kota:** Lokasi administratif geografis.
        * **Status Pelabuhan/Dermaga Khusus:** Ada / Tidak Ada / Dalam Konstruksi.
        * **Status PSN:** Afiliasi dengan Proyek Strategis Nasional.
        * **Tujuan Ekspor Utama:** Negara tujuan pengiriman kargo (Mayoritas China).
        * **Daftar Referensi:** Tautan (URL/Link) sumber dokumen pembuktian.
    4. **Dataset & File:** Referensi tekstual sekunder dan data kompilasi manual.
        * data/processed/sulawesi_logistik_simpul_nikel.csv
    """)'''

    new_method = '''st.markdown('<span style="background:#4A148C;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: OSINT & Spatial Logistic Mapping</span>', unsafe_allow_html=True)
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

with st.expander("ℹ️ Metodologi: OSINT & Pemetaan Spasial Rantai Pasok"):
    st.markdown("""
    **Metode Analisis:** Halaman ini menggabungkan investigasi *Open Source Intelligence* (OSINT) dan *Descriptive Spatial Analysis* untuk memetakan monopoli infrastruktur logistik pesisir dan ketergantungan geografis distribusi nikel ke Asia Timur.

    1. **Kurasi & Validasi Silang (OSINT):** Membangun matriks relasional dengan mencocokkan data citra satelit, dokumen lingkungan, dan laporan kargo.
    2. **Pemetaan Kausalitas (Spasial):** Membedah asimetri penguasaan ruang antara *origin* (sumber ekstraksi) dan *destination* (pusat industrialisasi). Garis diplot menggunakan rute *Great Circle* untuk merepresentasikan jarak tempuh kapal.
    3. **Variabel & Fitur Data:**
        * **Variabel Independen (X):** Titik Koordinat Smelter Utama & Status PSN.
        * **Variabel Dependen (Y):** Titik Koordinat Pelabuhan Tujuan (China, Jepang/Korea).
    4. **Dataset & File:**
        * data/processed/sulawesi_logistik_simpul_nikel.csv
    """)'''
    
    content = content.replace(old_method, new_method)

    # Part 2: Fix MAP_ROUTES text positions entirely
    old_routes = '''MAP_ROUTES = [
    # label, src_lon, src_lat, tgt_lon, tgt_lat, hex_color, text_pos, curve_offset
    ("IMIP",         122.15, -2.82, 113.8, 22.8,  "rgb(230, 25, 25)",  "top right", 0.15),
    ("GNI",          121.32, -1.91, 113.8, 22.8,  "rgb(255, 140, 0)",  "top left", 0.02),
    ("VDNI",         122.42, -3.83, 113.8, 22.8,  "rgb(0, 112, 220)",  "middle left", -0.1),
    ("OSS",          122.48, -3.80, 113.8, 22.8,  "rgb(0, 190, 220)",  "middle right", -0.15),
    ("ANTAM",        121.60, -4.18, 135.0, 35.0,  "rgb(0, 180, 80)",   "bottom right", 0.12),
    ("PT Vale",      121.34, -2.56, 135.0, 35.0,  "rgb(180, 0, 200)",  "top left", -0.05),
]'''

    new_routes = '''MAP_ROUTES = [
    # label, src_lon, src_lat, tgt_lon, tgt_lat, hex_color, text_pos, curve_offset
    ("IMIP",         122.15, -2.82, 113.8, 22.8,  "rgb(230, 25, 25)",  "middle right", 0.15),
    ("GNI",          121.32, -1.91, 113.8, 22.8,  "rgb(255, 140, 0)",  "top center", 0.02),
    ("VDNI",         122.42, -3.83, 113.8, 22.8,  "rgb(0, 112, 220)",  "bottom left", -0.1),
    ("OSS",          122.48, -3.80, 113.8, 22.8,  "rgb(0, 190, 220)",  "bottom right", -0.15),
    ("ANTAM",        121.60, -4.18, 135.0, 35.0,  "rgb(0, 180, 80)",   "bottom center", 0.12),
    ("PT Vale",      121.34, -2.56, 135.0, 35.0,  "rgb(180, 0, 200)",  "middle left", -0.05),
]'''

    content = content.replace(old_routes, new_routes)

    with open('pages/1_Ekspansi_Industri.py', 'w', encoding='utf-8') as f:
        f.write(content)

patch_file()
print("OK")
