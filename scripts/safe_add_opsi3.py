import os

filepath = r'C:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\pages\13_Infografis_Fakta.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

tabs_idx = content.find('# tab1, tab2 = st.tabs')
if tabs_idx == -1:
    tabs_idx = content.find('tab2, = st.tabs')

before_tabs = content[:tabs_idx]

html3 = """
html3 = f'''
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap" rel="stylesheet">

<style>
    .font-inter {{ font-family: 'Inter', sans-serif; }}
    
    .poster-container {{
        background-color: #215e39; /* Hijau dasar CELIOS */
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.07) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.07) 1px, transparent 1px);
        background-size: 50px 50px;
    }}
    
    .card-title-text {{
        color: #215e39;
        font-weight: 700;
        font-size: 0.95rem;
    }}
    
    .card-value-text {{
        color: #215e39;
        font-weight: 800;
        font-size: 3.5rem;
        line-height: 1.1;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }}
    
    .card-desc-text {{
        color: #555555;
        font-size: 0.75rem;
        line-height: 1.3;
        font-weight: 400;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }}
</style>

<div class="poster-container font-inter w-full min-h-screen p-8 md:p-12 lg:p-16 relative overflow-hidden">
    
    <!-- BACKGROUND ACCENTS -->
    <div class="absolute" style="top: -150px; right: -100px; width: 500px; height: 500px; border-radius: 50%; border: 40px solid rgba(255, 232, 124, 0.08); z-index: 0; pointer-events: none;"></div>
    <div class="absolute" style="bottom: 10%; left: -200px; width: 600px; height: 600px; border-radius: 50%; border: 60px solid rgba(255, 232, 124, 0.06); z-index: 0; pointer-events: none;"></div>
    <div class="absolute" style="top: 30%; left: 5%; font-size: 150px; color: rgba(255, 232, 124, 0.08); z-index: 0; font-weight: 900; line-height: 1; pointer-events: none;">+</div>
    <div class="absolute" style="bottom: 20%; right: 10%; font-size: 200px; color: rgba(255, 232, 124, 0.06); z-index: 0; font-weight: 900; line-height: 1; pointer-events: none;">+</div>
    
    <!-- MAIN CONTENT -->
    <div class="relative z-10 w-full">
        <!-- HEADER -->
    <div class="text-center mb-12 mt-4 flex flex-col items-center justify-center">
        {logo_html}
        <h1 class="text-white text-4xl md:text-5xl font-bold tracking-wide mb-3">Realita di Balik Hilirisasi</h1>
        <p style="color: rgba(255,255,255,0.75); font-size: 1rem; font-weight: 500; max-width: 600px; margin: 0 auto; letter-spacing: 0.02em;">Daya Dukung &amp; Daya Tampung Lingkungan Hidup (D3TLH) — Sulawesi 2014–2024</p>
    </div>

    <!-- SEKSI 1: ILUSI HILIRISASI & EKONOMI -->
    <div class="w-full text-center font-bold text-xl md:text-2xl py-3 rounded-full mb-8 shadow-sm" style="background-color: #FFE87C; color: #215e39;">
        Ilusi Hilirisasi &amp; Ekonomi
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-14">
        
        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Asing Berpesta, Kita Merana</div>
            <div class="card-value-text">{data['investasi_asing']}</div>
            <div class="card-desc-text">Kedaulatan tergadai! Mayoritas cuan nikel lari keluar negeri, kita cuma dapat ampasnya</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Kaya Tapi Jatuh Miskin</div>
            <div class="card-value-text">{data['pdrb']}</div>
            <div class="card-desc-text">Hanya oligarki yang untung, PDRB meroket tapi nyatanya warga lokal tetap miskin gigit jari</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Petani Digilas Tambang</div>
            <div class="card-value-text">{data['pertanian']}</div>
            <div class="card-desc-text">Lahan produktif dihancurkan, kedaulatan pangan warga tamat riwayatnya</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Hipokrisi Energi Hijau</div>
            <div class="card-value-text">{data['pltu_val']}</div>
            <div class="card-desc-text">Katanya demi transisi energi, nyatanya ditenagai ribuan Megawatt batu bara super kotor</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Nyawa Pekerja Murah</div>
            <div class="card-value-text">{data['kecelakaan_tambang']}</div>
            <div class="card-desc-text">Standar K3 diabaikan demi kejar target produksi brutal, pekerja tewas sia-sia</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Tanah Dirampas Paksa</div>
            <div class="card-value-text">{data['konflik_val']}</div>
            <div class="card-desc-text">Aparat bungkam dan gusur warga lokal yang mencoba mempertahankan ruang hidupnya</div>
        </div>
    </div>

    <!-- SEKSI 2: EKOSIDA & PENGHANCURAN ALAM -->
    <div class="w-full text-center font-bold text-xl md:text-2xl py-3 rounded-full mb-8 shadow-sm" style="background-color: #FFE87C; color: #215e39;">
        Ekosida &amp; Penghancuran Alam
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-14">
        
        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Kiamat Hutan Perawan</div>
            <div class="card-value-text">{data['hutan_primer']}</div>
            <div class="card-desc-text">Jutaan hektar kanopi hutan yang tak tergantikan hilang dan hancur selamanya</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Kawasan Suci Dibuldoser</div>
            <div class="card-value-text">{data['kawasan_lindung']}</div>
            <div class="card-desc-text">Hutan lindung yang harusnya sakral resmi 'disembelih' demi memuluskan megaproyek nikel</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Satwa Endemik Terbantai</div>
            <div class="card-value-text">{data['kepunahan']}</div>
            <div class="card-desc-text">Habitat dikeruk habis, satwa ikonik Sulawesi di ujung jurang kepunahan massal</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Gunung Tailing Mengerikan</div>
            <div class="card-value-text">{data['limbah_val']}</div>
            <div class="card-desc-text">Bom waktu jutaan ton limbah B3 beracun siap menenggelamkan ekosistem pesisir kapan saja</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Sungai Darah &amp; Laut Mati</div>
            <div class="card-value-text">{data['sungai_tercemar']}</div>
            <div class="card-desc-text">Air laut berubah merah karat beracun, lumpur nikel matikan total mata pencaharian nelayan</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Langganan Bencana Buatan</div>
            <div class="card-value-text">{data['bencana_val']}</div>
            <div class="card-desc-text">Hilangnya penahan air alami bikin jutaan jiwa terus-terusan diusir dari kampung halamannya oleh banjir dan longsor</div>
        </div>
    </div>

    <!-- SEKSI 3: TUMBAL NYAWA WARGA -->
    <div class="w-full text-center font-bold text-xl md:text-2xl py-3 rounded-full mb-8 shadow-sm" style="background-color: #FFE87C; color: #215e39;">
        Tumbal Nyawa Warga
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mb-14">
        
        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Paru-Paru Sesak</div>
            <div class="card-value-text">{data['ispa_val']}</div>
            <div class="card-desc-text">Warga dipaksa menghirup debu beracun smelter tiap kali bernapas</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Langit Pekat Kematian</div>
            <div class="card-value-text">{data['no2_val']}</div>
            <div class="card-desc-text">Satelit NASA saksi bisu langit beracun yang mengintai jutaan warga tiap hari</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Krisis Air = Krisis Nyawa</div>
            <div class="card-value-text">{data['diare_val']}</div>
            <div class="card-desc-text">Air tanah tercemar pekat, penyakit diare ganas meledak serang warga kecil</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Wabah Hutan Gundul</div>
            <div class="card-value-text">{data['zoo_val']}</div>
            <div class="card-desc-text">Hutan dibabat habis, nyamuk DBD &amp; Malaria turun gunung serang pemukiman tak berdosa</div>
        </div>
    </div>

    <!-- SEKSI 4: HUKUM TUMPUL & PERMAINAN KOTOR OLIGARKI -->
    <div class="w-full text-center font-bold text-xl md:text-2xl py-3 rounded-full mb-8 shadow-sm" style="background-color: #FFE87C; color: #215e39;">
        Hukum Tumpul &amp; Permainan Kotor Oligarki
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-3 gap-5 mb-14">
        
        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Banjir Izin Pasca Omnibus</div>
            <div class="card-value-text">{data['lonjakan_izin']}</div>
            <div class="card-desc-text">Izin tambang diobral gila-gilaan tanpa ampun dan tanpa rem pasca-Omnibus Law disahkan</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Karpet Merah Amdal Kilat</div>
            <div class="card-value-text">{data['kecepatan_izin']}</div>
            <div class="card-desc-text">Aturan ditebas: Amdal yang ketat disetujui kilat cuma hitungan hari demi muluskan investor</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Moratorium Cuma Macan Kertas</div>
            <div class="card-value-text">{data['moratorium']}</div>
            <div class="card-desc-text">Obral izin terus jalan terang-terangan di belakang layar, moratorium cuma pemanis mulut</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Bekingan Tambang Ilegal</div>
            <div class="card-value-text">{data['izin_hantu']}</div>
            <div class="card-desc-text">Korporasi 'nakal' keruk hutan seenaknya tanpa takut hukum karena dibeking orang kuat</div>
        </div>

        <div class="bg-white rounded-3xl p-6 text-center flex flex-col justify-center items-center h-full">
            <div class="card-title-text">Legalitas Merampok Tanah</div>
            <div class="card-value-text">{data['tumpang_tindih']}</div>
            <div class="card-desc-text">Pemerintah sengaja keluarkan izin tambang yang menabrak dan merampas tanah adat/warga</div>
        </div>

    </div>

    </div> <!-- END MAIN CONTENT -->

</div>
'''
"""

tabs_code = """
tab2, tab3 = st.tabs(["Opsi 2", "Opsi 3"])

with tab2:
    st.markdown(html2.replace('\\n', ''), unsafe_allow_html=True)

with tab3:
    st.markdown(html3.replace('\\n', ''), unsafe_allow_html=True)
"""

final_content = before_tabs + html3 + '\n' + tabs_code

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Applied!")
