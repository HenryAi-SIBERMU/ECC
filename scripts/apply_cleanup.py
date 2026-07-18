def patch_file():
    with open('pages/1_Ekspansi_Industri.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Part 1: Remove the 1.6 header and its methodology
    old_header = '''st.subheader("1.6 Peta Jalur Distribusi Logistik Nikel Sulawesi")

st.markdown('<span style="background:#4A148C;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: Spatial Logistic Mapping (Analisis Spasial Ekstraktif)</span>', unsafe_allow_html=True)
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

with st.expander("ℹ️ Metodologi: Pemetaan Spasial Rantai Pasok Maritim"):
    st.markdown("""
    **Metode Analisis:** Halaman ini menggunakan pendekatan *Descriptive Spatial Analysis* untuk memetakan ketergantungan geografis distribusi nikel dari smelter utama di Sulawesi menuju pelabuhan destinasi akhir di Asia Timur.
    
    **Model Parameter / Pengujian:** 
    Pemetaan Kausalitas: Membedah asimetri penguasaan ruang antara *origin* (sumber ekstraksi) dan *destination* (pusat industrialisasi). Garis diplot menggunakan rute *Great Circle* untuk merepresentasikan jarak tempuh kapal logistik terpendek di permukaan bumi.
    
    **Identifikasi Variabel:**
    *   **Variabel Independen (X):** Titik Koordinat Smelter Utama (Sulawesi).
    *   **Variabel Dependen (Y):** Titik Koordinat Pelabuhan Tujuan Utama (China, Jepang/Korea).
    
    **Daftar Dataset:**
    data/processed/sulawesi_logistik_simpul_nikel.csv
    """)'''

    content = content.replace(old_header, '')

    # Part 2: Fix MAP_ROUTES text positions
    # User said PT Vale and VDNI are overlapping
    # VDNI: middle left -> middle left
    # PT Vale: bottom left -> top left
    old_vale = '("PT Vale",      121.34, -2.56, 135.0, 35.0,  "rgb(180, 0, 200)",  "bottom left", -0.05)'
    new_vale = '("PT Vale",      121.34, -2.56, 135.0, 35.0,  "rgb(180, 0, 200)",  "top left", -0.05)'
    content = content.replace(old_vale, new_vale)

    with open('pages/1_Ekspansi_Industri.py', 'w', encoding='utf-8') as f:
        f.write(content)

patch_file()
print("OK")
