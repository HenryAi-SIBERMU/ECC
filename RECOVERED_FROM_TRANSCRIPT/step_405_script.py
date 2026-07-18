import sys

file_path = "pages/2_Kualitas_Lingkungan.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_text = '''st.markdown(f\"\"\"
<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #D32F2F; margin-bottom: 25px;">
    <b style="color:#FF5252; font-size:1.1em;">Pembedahan Spasial (Paradoks BPS vs Realita Lapangan):</b><br><br>
    Ketiga peta di atas menyingkap <b>kebohongan statistik</b> dari narasi keberhasilan hilirisasi. Pada Peta BPS (kiri), episentrum tambang nikel seperti Sulawesi Tengah dan Tenggara justru dilukiskan dengan warna <b>Biru (Aman/Baik)</b>. Namun, ilusi ini runtuh seketika saat dihadapkan pada realita lapangan (tengah & kanan). Wilayah yang diklaim "biru" tersebut nyatanya berubah drastis menjadi <b>Coklat Pekat (Kritis)</b>—menandakan beban belasan juta ton limbah B3 tailing per tahun.<br><br>
    Ini bukan lagi sekadar anomali data, melainkan penciptaan <i>Zona Tumbal Ekologis</i>. Sungai-sungai urat nadi masyarakat (seperti Lalindu, Lasolo, Konaweha, dan Bahodopi) kini mati tercekik endapan lumpur beracun dan cemaran logam berat mematikan seperti <b>Kromium Heksavalen (Cr6+)</b>. Ekosistem hancur, nelayan kehilangan ruang hidup, dan satwa buas bermigrasi ke pemukiman. Data publik (BPS) jelas gagal, atau sengaja gagal, merekam penderitaan ekologis ini.
</div>
\"\"\", unsafe_allow_html=True)'''

new_text = '''st.markdown(f\"\"\"
<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #D32F2F; margin-bottom: 25px; line-height: 1.6;">
    <b style="color:#FF5252; font-size:1.1em;">Pembedahan Spasial (Paradoks BPS vs Realita Lapangan):</b><br>
    Ketiga peta di atas menyingkap <b>kebohongan statistik</b> dari narasi keberhasilan hilirisasi. Pada Peta BPS (kiri), episentrum tambang nikel seperti Sulawesi Tengah dan Tenggara justru dilukiskan dengan warna <b>Biru (Aman/Baik)</b>. Namun, ilusi ini runtuh seketika saat dihadapkan pada realita lapangan (Peta Tengah & Kanan) yang dibuktikan oleh temuan empiris lembaga independen (WALHI, JATAM, AEER):<br><br>
    <ul style="margin-top: 0; margin-bottom: 10px;">
        <li><b>Beban Limbah Fantastis (Warna Coklat Peta Tengah):</b> Wilayah yang diklaim "biru" oleh BPS ini justru menimbun limbah mematikan. Di Sulawesi Tengah (IMIP & sekitarnya), diproduksi <b>12 Juta Ton</b> slag & tailing HPAL, ditambah <b>7 Juta Ton</b> dari PT HNC, dan <b>5,5 Juta Ton</b> dari PT QMB per tahun. Di Sulawesi Tenggara (VDNI & Konawe), timbulan slag feronikel mencapai <b>6,5 Juta Ton</b> per tahun.</li>
        <li><b>Kematian Sungai & Pencemaran Cr6+ (Warna Coklat Peta Kanan):</b> Tidak hanya volume, dampaknya langsung membunuh urat nadi ekologis. Di Sulteng, setidaknya <b>4 sungai dan pesisir (Bahodopi, Laroenai, Morowali, Fatufia)</b> tercemar berat logam beracun (Kromium Heksavalen/Cr6+).</li>
        <li><b>Bencana Ekologis & Migrasi Satwa Buas:</b> Di Sultra, pelepasan <b>800.000 Ton</b> air limbah tambang (oleh PT SCM) ke Sungai Lalindu, Lasolo, dan Konaweha menyebabkan sungai berubah keruh pekat akibat TSS (Total Suspended Solid). Hal ini memicu banjir lumpur masif dan memaksa satwa liar (buaya) bermigrasi hingga ke muara dan pemukiman karena habitat aslinya hancur.</li>
    </ul>
    Ini bukan lagi sekadar anomali indikator (IKA), melainkan penciptaan <i>Zona Tumbal Ekologis</i>. Data makro BPS jelas gagal merekam penderitaan mematikan yang tersaji dalam data mentah lapangan ini.
</div>
\"\"\", unsafe_allow_html=True)'''

if old_text in content:
    content = content.replace(old_text, new_text)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Replace successful!")
else:
    print("Target text not found in file.")