import sys

file_path = "pages/2_Kualitas_Lingkungan.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. FIX SPATIAL TEXT (Use find and replace precisely based on what's there now)
old_text = '''<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #D32F2F; margin-bottom: 25px;">
    <b>Pembedahan Spasial:</b> Peta geospasial di atas menyingkap realitas berdarah dari hilirisasi. Lingkaran raksasa yang berada di Sulawesi Tengah dan Sulawesi Tenggara merepresentasikan konsentrasi masif fasilitas smelter. Sangat memprihatinkan bahwa pada episentrum industri inilah, warna lingkaran berubah drastis menjadi merah pekat—menandakan skor Indeks Kualitas Air (IKA) yang terjun bebas. Ini bukan lagi sekadar penurunan indikator, melainkan penciptaan <i>zona tumbal ekologis</i> akibat pencemaran aliran sungai dan pembuangan tailing.
</div>'''

# Handle the dash encoding issue (could be ??" or —)
start = content.find('<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #D32F2F; margin-bottom: 25px;">')
end = content.find('</div>', start) + 6
if start != -1 and end != -1:
    actual_old_text = content[start:end]
    new_text = '''<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #D32F2F; margin-bottom: 25px; line-height: 1.6;">
    <b style="color:#FF5252; font-size:1.1em;">Pembedahan Spasial (Validasi Kehancuran Ekologis):</b><br>
    Ketiga peta di atas justru saling mengkonfirmasi <b>krisis ekologis</b> yang tak terbantahkan. Pada Peta BPS (kiri), data resmi negara sendiri telah mengakui bahwa episentrum tambang nikel (Sulteng, Sultra, Sulsel) berada dalam kondisi kritis dengan skor IKA hanya 54-62 (Kategori: Kurang/Cemar). Namun, di atas ekosistem yang sudah sekarat inilah, industri dibiarkan terus membuang limbah secara ugal-ugalan (Peta Tengah & Kanan) yang dibuktikan oleh temuan empiris lembaga independen (WALHI, JATAM, AEER):<br><br>
    <ul style="margin-top: 0; margin-bottom: 10px;">
        <li><b>Beban Limbah Fantastis (Peta Tengah):</b> Di atas wilayah yang kualitas airnya sudah "Kurang" versi BPS ini, nyatanya terus ditimbun limbah mematikan dalam skala apokaliptik. Di Sulteng (IMIP & sekitarnya), diproduksi <b>12 Juta Ton</b> slag & tailing HPAL, <b>7 Juta Ton</b> dari PT HNC, dan <b>5,5 Juta Ton</b> dari PT QMB per tahun. Di Sultra (VDNI & Konawe), timbulan slag feronikel mencapai <b>6,5 Juta Ton</b> per tahun.</li>
        <li><b>Kematian Sungai & Pencemaran Cr6+ (Peta Kanan):</b> Dampaknya langsung membunuh urat nadi ekologis. Di Sulteng, setidaknya <b>4 sungai dan pesisir (Bahodopi, Laroenai, Morowali, Fatufia)</b> tercemar berat logam beracun (Kromium Heksavalen/Cr6+).</li>
        <li><b>Bencana Ekologis & Migrasi Satwa Buas:</b> Di Sultra, pelepasan <b>800.000 Ton</b> air limbah tambang (oleh PT SCM) ke Sungai Lalindu, Lasolo, dan Konaweha menyebabkan sungai berubah keruh pekat akibat TSS (Total Suspended Solid). Hal ini memicu banjir lumpur masif dan memaksa satwa liar (buaya) bermigrasi hingga ke muara dan pemukiman karena habitat aslinya hancur.</li>
    </ul>
    Tidak ada paradoks di sini; data BPS dan realita lapangan sama-sama berteriak bahwa wilayah ini telah diubah menjadi <i>Zona Tumbal Ekologis</i> demi ambisi hilirisasi industri nikel.
</div>'''
    content = content.replace(actual_old_text, new_text)
    print("Fixed spatial text.")


# 2. IKU LABEL FIX (ONLY change the label, keep the blocks exactly the same)
start_iku = content.find('colorbar=dict(')
# we need to find the specific colorbar for IKU
iku_loc = content.find('title=dict(text="IKU", font=dict(color=\'#ECEFF1\', size=12))')
if iku_loc != -1:
    actual_old_iku = content[iku_loc:iku_loc+150] # capture the text to replace
    # We replace precisely
    new_iku_title = 'title=dict(text="IKU<br>merah = buruk", font=dict(color=\'#ECEFF1\', size=12), side="right")'
    content = content.replace('title=dict(text="IKU", font=dict(color=\'#ECEFF1\', size=12))', new_iku_title)
    
    # Also replace ticktext
    content = content.replace("ticktext=['80<br>merah = buruk', '85', '90', '95']", "ticktext=['80', '85', '90', '95']")
    print("Fixed IKU label format.")
    
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
