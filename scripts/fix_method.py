import codecs
def fix():
    with codecs.open('pages/1_Ekspansi_Industri.py', 'r', 'utf-8') as f:
        content = f.read()
    
    # We will find the marker to inject the correct block
    marker1 = "st.subheader(\"1.5 Pelabuhan Ekspor: Ke Mana Nikel Sulawesi Dikirim?\")"
    marker2 = 'Ekspansi nikel di Sulawesi tidak berhenti pada izin dan pabrik smelter.'
    
    start_idx = content.find(marker1)
    end_idx = content.find(marker2)
    
    if start_idx != -1 and end_idx != -1:
        new_block = marker1 + '''\n
st.markdown('<span style="background:#4A148C;color:#E1BEE7;padding:4px 10px;border-radius:5px;font-size:0.85rem;">Metode: OSINT & Spatial Logistic Mapping</span>', unsafe_allow_html=True)
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

with st.expander("ℹ️ Metodologi: OSINT & Pemetaan Spasial Rantai Pasok"):
    st.markdown("""
    **Metode Analisis:** Halaman ini menggabungkan investigasi *Open Source Intelligence* (OSINT) dan *Descriptive Spatial Analysis* untuk memetakan monopoli infrastruktur logistik pesisir dan ketergantungan geografis distribusi nikel ke Asia Timur.

    1. **Kurasi & Validasi Silang (OSINT):** Membangun matriks relasional dengan mencocokkan data citra satelit, dokumen lingkungan, dan laporan kargo.
    2. **Pemetaan Kausalitas (Spasial):** Membedah asimetri penguasaan ruang antara *origin* (sumber ekstraksi) dan *destination* (pusat industrialisasi). Garis diplot menggunakan rute *Great Circle* untuk merepresentasikan jarak tempuh kapal logistik terpendek di permukaan bumi.
    3. **Variabel & Fitur Data:**
        * **Variabel Independen (X):** Titik Koordinat Smelter Utama & Status PSN.
        * **Variabel Dependen (Y):** Titik Koordinat Pelabuhan Tujuan (China, Jepang/Korea).
    4. **Dataset & File:**
        * data/processed/sulawesi_logistik_simpul_nikel.csv
    """)
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
'''
        content = content[:start_idx] + new_block + content[end_idx:]
    
    with codecs.open('pages/1_Ekspansi_Industri.py', 'w', 'utf-8') as f:
        f.write(content)

fix()
print("OK")
