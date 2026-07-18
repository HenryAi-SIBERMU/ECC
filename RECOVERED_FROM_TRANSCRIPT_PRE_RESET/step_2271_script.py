import sys

file_path = "pages/2_Kualitas_Lingkungan.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace Map 1 config
old_map1 = '''        color_continuous_scale=[
            [0.0, '#8B4513'], # 0 - Sangat Kurang
            [0.5, '#D2691E'], # 50 - Kurang
            [0.7, '#F4A460'], # 70 - Sedang
            [0.9, '#87CEEB'], # 90 - Baik
            [1.0, '#1E90FF']  # 100 - Sangat Baik
        ],
        range_color=[0, 100],
        zoom=3.8, center={"lat": -1.8, "lon": 120.5}, opacity=0.75,
        hover_name="Provinsi", hover_data={"Provinsi": False, "Jumlah_Smelter": True, "Indeks Kualitas Air": ':.1f'},
        mapbox_style="carto-darkmatter", title="IKA BPS (Data Resmi/Paradoks)"'''

new_map1 = '''        color_continuous_scale=[
            [0.0, '#8B4513'], # Terburuk (Coklat Tua)
            [0.5, '#D2691E'], # Sedang (Coklat)
            [1.0, '#F4A460']  # Terbaik dari yang terburuk (Coklat Muda/Kuning)
        ],
        zoom=3.8, center={"lat": -1.8, "lon": 120.5}, opacity=0.75,
        hover_name="Provinsi", hover_data={"Provinsi": False, "Jumlah_Smelter": True, "Indeks Kualitas Air": ':.1f'},
        mapbox_style="carto-darkmatter", title="IKA BPS (Data Resmi)"'''

if old_map1 in content:
    content = content.replace(old_map1, new_map1)
else:
    print("Map 1 text not found.")

# Replace the text block
old_text = '''st.markdown(f\"\"\"
<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #D32F2F; margin-bottom: 25px; line-height: 1.6;">
    <b style="color:#FF5252; font-size:1.1em;">Pembedahan Spasial (Paradoks BPS vs Realita Lapangan):</b><br>
    Ketiga peta di atas menyingkap <b>kebohongan statistik</b> dari narasi keberhasilan hilirisasi. Pada Peta BPS (kiri), jika kita menstandarkan pewarnaan pada ambang batas resmi IKA KLHK (0-100), episentrum tambang nikel seperti Sulteng dan Sultra nyatanya hanya mencetak skor 54-62 (Kategori: Kurang/Tercemar Ringan). Secara visual, warnanya langsung pudar menjadi <b>Coklat Muda/Kusam</b> (bukan biru bersih). Kehancuran ini mencapai puncaknya (Coklat Pekat) saat dihadapkan pada realita lapangan (Peta Tengah & Kanan) yang dibuktikan oleh temuan empiris lembaga independen (WALHI, JATAM, AEER):<br><br>
    <ul style="margin-top: 0; margin-bottom: 10px;">
        <li><b>Beban Limbah Fantastis (Warna Coklat Peta Tengah):</b> Wilayah yang kualitas airnya "kurang" versi BPS ini nyatanya menimbun limbah mematikan dalam skala apokaliptik. Di Sulawesi Tengah (IMIP & sekitarnya), diproduksi <b>12 Juta Ton</b> slag & tailing HPAL, ditambah <b>7 Juta Ton</b> dari PT HNC, dan <b>5,5 Juta Ton</b> dari PT QMB per tahun. Di Sulawesi Tenggara (VDNI & Konawe), timbulan slag feronikel mencapai <b>6,5 Juta Ton</b> per tahun.</li>
        <li><b>Kematian Sungai & Pencemaran Cr6+ (Warna Coklat Peta Kanan):</b> Tidak hanya volume, dampaknya langsung membunuh urat nadi ekologis. Di Sulteng, setidaknya <b>4 sungai dan pesisir (Bahodopi, Laroenai, Morowali, Fatufia)</b> tercemar berat logam beracun (Kromium Heksavalen/Cr6+).</li>
        <li><b>Bencana Ekologis & Migrasi Satwa Buas:</b> Di Sultra, pelepasan <b>800.000 Ton</b> air limbah tambang (oleh PT SCM) ke Sungai Lalindu, Lasolo, dan Konaweha menyebabkan sungai berubah keruh pekat akibat TSS (Total Suspended Solid). Hal ini memicu banjir lumpur masif dan memaksa satwa liar (buaya) bermigrasi hingga ke muara dan pemukiman karena habitat aslinya hancur.</li>
    </ul>
    Ini bukan lagi sekadar anomali indikator (IKA), melainkan penciptaan <i>Zona Tumbal Ekologis</i>. Data makro BPS jelas gagal merekam penderitaan mematikan yang tersaji dalam data mentah lapangan ini.
</div>
\"\"\", unsafe_allow_html=True)'''

new_text = '''st.markdown(f\"\"\"
<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #D32F2F; margin-bottom: 25px; line-height: 1.6;">
    <b style="color:#FF5252; font-size:1.1em;">Pembedahan Spasial (Validasi Kehancuran Ekologis):</b><br>
    Ketiga peta di atas justru saling mengkonfirmasi <b>krisis ekologis</b> yang tak terbantahkan. Pada Peta BPS (kiri), data resmi negara sendiri telah mengakui bahwa episentrum tambang nikel (Sulteng, Sultra, Sulsel) berada dalam kondisi kritis dengan skor IKA hanya 54-62 (Kategori: Kurang/Cemar). Namun, di atas ekosistem yang sudah sekarat inilah, industri dibiarkan terus membuang limbah secara ugal-ugalan (Peta Tengah & Kanan) yang dibuktikan oleh temuan empiris lembaga independen (WALHI, JATAM, AEER):<br><br>
    <ul style="margin-top: 0; margin-bottom: 10px;">
        <li><b>Beban Limbah Fantastis (Peta Tengah):</b> Di atas wilayah yang kualitas airnya sudah "Kurang" versi BPS ini, nyatanya terus ditimbun limbah mematikan dalam skala apokaliptik. Di Sulteng (IMIP & sekitarnya), diproduksi <b>12 Juta Ton</b> slag & tailing HPAL, <b>7 Juta Ton</b> dari PT HNC, dan <b>5,5 Juta Ton</b> dari PT QMB per tahun. Di Sultra (VDNI & Konawe), timbulan slag feronikel mencapai <b>6,5 Juta Ton</b> per tahun.</li>
        <li><b>Kematian Sungai & Pencemaran Cr6+ (Peta Kanan):</b> Dampaknya langsung membunuh urat nadi ekologis. Di Sulteng, setidaknya <b>4 sungai dan pesisir (Bahodopi, Laroenai, Morowali, Fatufia)</b> tercemar berat logam beracun (Kromium Heksavalen/Cr6+).</li>
        <li><b>Bencana Ekologis & Migrasi Satwa Buas:</b> Di Sultra, pelepasan <b>800.000 Ton</b> air limbah tambang (oleh PT SCM) ke Sungai Lalindu, Lasolo, dan Konaweha menyebabkan sungai berubah keruh pekat akibat TSS (Total Suspended Solid). Hal ini memicu banjir lumpur masif dan memaksa satwa liar (buaya) bermigrasi hingga ke muara dan pemukiman karena habitat aslinya hancur.</li>
    </ul>
    Tidak ada paradoks di sini; data BPS dan realita lapangan sama-sama berteriak bahwa wilayah ini telah diubah menjadi <i>Zona Tumbal Ekologis</i> demi ambisi hilirisasi industri nikel.
</div>
\"\"\", unsafe_allow_html=True)'''

if old_text in content:
    content = content.replace(old_text, new_text)
else:
    print("Narrative text not found.")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated successfully.")