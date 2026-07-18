import sys

file_path = "pages/2_Kualitas_Lingkungan.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_text = '''st.markdown(f\"\"\"
<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #D32F2F; margin-bottom: 25px;">
    <b>Pembedahan Spasial:</b> Peta geospasial di atas menyingkap realitas berdarah dari hilirisasi. Lingkaran raksasa yang berada di Sulawesi Tengah dan Sulawesi Tenggara merepresentasikan konsentrasi masif fasilitas smelter. Sangat memprihatinkan bahwa pada episentrum industri inilah, warna lingkaran berubah drastis menjadi merah pekat—menandakan skor Indeks Kualitas Air (IKA) yang terjun bebas. Ini bukan lagi sekadar penurunan indikator, melainkan penciptaan <i>zona tumbal ekologis</i> akibat pencemaran aliran sungai dan pembuangan tailing (yang mengandung logam berat mematikan seperti Kromium Heksavalen).
</div>
\"\"\", unsafe_allow_html=True)'''

new_text = '''st.markdown(f\"\"\"
<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #D32F2F; margin-bottom: 25px;">
    <b style="color:#FF5252; font-size:1.1em;">Pembedahan Spasial (Paradoks BPS vs Realita Lapangan):</b><br><br>
    Ketiga peta di atas menyingkap <b>kebohongan statistik</b> dari narasi keberhasilan hilirisasi. Pada Peta BPS (kiri), episentrum tambang nikel seperti Sulawesi Tengah dan Tenggara justru dilukiskan dengan warna <b>Biru (Aman/Baik)</b>. Namun, ilusi ini runtuh seketika saat dihadapkan pada realita lapangan (tengah & kanan). Wilayah yang diklaim "biru" tersebut nyatanya berubah drastis menjadi <b>Coklat Pekat (Kritis)</b>—menandakan beban belasan juta ton limbah B3 tailing per tahun.<br><br>
    Ini bukan lagi sekadar anomali data, melainkan penciptaan <i>Zona Tumbal Ekologis</i>. Sungai-sungai urat nadi masyarakat (seperti Lalindu, Lasolo, Konaweha, dan Bahodopi) kini mati tercekik endapan lumpur beracun dan cemaran logam berat mematikan seperti <b>Kromium Heksavalen (Cr6+)</b>. Ekosistem hancur, nelayan kehilangan ruang hidup, dan satwa buas bermigrasi ke pemukiman. Data publik (BPS) jelas gagal, atau sengaja gagal, merekam penderitaan ekologis ini.
</div>
\"\"\", unsafe_allow_html=True)'''

if old_text in content:
    content = content.replace(old_text, new_text)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Replace successful!")
else:
    print("Target text not found in file.")