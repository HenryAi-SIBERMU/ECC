--- BLOCK 0 ---
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

--- BLOCK 1 ---
**Alur Kausalitas (Ekonomi Politik Ekologi):** `Konsentrasi Industri Ekstraktif` → `Penurunan Kualitas Daya Dukung Lingkungan` → `Peningkatan Insidensi Penyakit (ISPA, Diare) & Ketimpangan Faskes`

    Ekspansi industri ekstraktif berpotensi memengaruhi kualitas lingkungan hidup masyarakat setempat. Pembuangan polutan ke udara ambien dan badan air berkorelasi dengan peningkatan insidensi penyakit respiratori dan infeksi saluran pencernaan, yang diperparah oleh ketimpangan distribusi fasilitas kesehatan.

    **Variabel Dampak Kesehatan (Y):**
    *   **ISPA/Pneumonia:** Penyakit pernapasan akibat paparan debu dan sulfur.
    *   **Diare & Penyakit Menular (Malaria/Kusta):** Dampak pencemaran air dan buruknya sanitasi di lingkar tambang.
    *   **Ketersediaan Fasilitas Kesehatan:** Kesenjangan infrastruktur medis (Puskesmas & Rumah Sakit) terhadap pertumbuhan beban kasus penyakit.

    **Metode Pengolahan Data:**
    Analisis menggunakan *Cross-sectional* dan *Time-Series*. Menggabungkan dataset *survey* dinas kesehatan dan ketersediaan layanan publik untuk menganalisis korelasi antara pertumbuhan kapasitas PLTU *captive* dan peningkatan beban penyakit di masyarakat dengan ketersediaan fasilitas medis yang terbatas.

--- BLOCK 2 ---
<div style="background-color: transparent; padding: 10px 0px; margin-bottom: 25px;">
    <h2 style="color: #FFFFFF; font-size: 1.8rem; margin-bottom: 15px; font-weight: 700;">Hilirisasi Nikel dan Dampak Kesehatan: Analisis Data Empiris di Kawasan Penyangga</h2>
    <p style="color: #CCCCCC; font-size: 1.05rem; line-height: 1.7; margin-bottom: 15px; text-align: justify;">
        Data empiris menggambarkan kesenjangan antara klaim pertumbuhan ekonomi dari ekspansi industri nikel dan kondisi kesehatan masyarakat di kawasan penyangga. Selama satu dekade terakhir, emisi partikulat, gas buang PLTU batu bara, dan timbulan limbah dari fasilitas ekstraktif telah memberikan tekanan signifikan terhadap kualitas lingkungan hidup masyarakat. Data empiris merekam bagaimana ekspansi kapasitas industri, yang ditopang oleh PLTU <i>captive</i> berkapasitas <b>{tot_kapasitas_pltu:,.0f} Megawatt</b>, berjalan sejajar dengan peningkatan kasus penyakit di kawasan-kawasan penyangga.
    </p>
    <p style="color: #CCCCCC; font-size: 1.05rem; line-height: 1.7; margin-bottom: 15px; text-align: justify;">
        Sepanjang 2014–2024, data agregat dinas kesehatan mencatat total <b>kasus ISPA dan Pneumonia sebanyak {tot_ispa:,.0f} kasus</b>. Sementara itu, <b>kasus Diare tercatat sebanyak {tot_diare:,.0f} kasus</b>. Peningkatan insidensi penyakit ini berkorelasi dengan penurunan Indeks Kualitas Air (IKA) secara periodik. Konversi tutupan hutan untuk perluasan konsesi tambang turut berkontribusi pada pergeseran habitat satwa liar, yang berpotensi memicu perpindahan vektor penyakit zoonosis ke permukiman warga. Secara kumulatif, <b>kasus Malaria tercatat mencapai {tot_malaria:,.0f} kasus</b>, mengindikasikan tekanan terhadap keseimbangan ekologis di wilayah tambang.
    </p>
    <p style="color: #CCCCCC; font-size: 1.05rem; line-height: 1.7; text-align: justify;">
        Distribusi infrastruktur kesehatan di wilayah industri menunjukkan kesenjangan yang perlu menjadi perhatian. Ketersediaan fasilitas layanan primer seperti <b>Puskesmas tercatat sebanyak {tot_puskesmas_2022:,.0f} unit</b> pada tahun 2022, di kawasan yang bersamaan menanggung beban penyakit di atas rata-rata. Kondisi ini mengindikasikan bahwa pertumbuhan ekonomi dari hilirisasi nikel belum diimbangi dengan distribusi infrastruktur kesehatan yang proporsional bagi masyarakat di wilayah operasi industri (<i>sacrifice zone</i>).
    </p>
</div>

--- BLOCK 3 ---
<div class="metric-card">
        <div>
            <div class="metric-label">Total Kasus ISPA/Pneumonia</div>
            <div class="metric-value" style="color: #B71C1C;">{tot_ispa:,.0f}</div>
            <div class="metric-desc">Penyakit pernapasan yang meningkat secara konsisten, seiring paparan kronis debu batu bara dan emisi SO₂ dari cerobong <i>smelter</i>.</div>
        </div>
        <div class="metric-source"><b>Sumber:</b> Data Agregat Dinas Kesehatan (2014-2024)<br/><i>File: sulawesi_kesehatan_detail_2014_2024.csv</i></div>
    </div>

--- BLOCK 4 ---
<div class="metric-card">
        <div>
            <div class="metric-label">Total Kasus Diare</div>
            <div class="metric-value" style="color: #F4511E;">{tot_diare:,.0f}</div>
            <div class="metric-desc">Infeksi saluran pencernaan yang tercatat tinggi, seiring degradasi kualitas sumber air tanah dan badan air akibat limbah tailing tambang.</div>
        </div>
        <div class="metric-source"><b>Sumber:</b> Data Agregat Dinas Kesehatan (2014-2024)<br/><i>File: sulawesi_kesehatan_detail_2014_2024.csv</i></div>
    </div>

--- BLOCK 5 ---
<div class="metric-card">
        <div>
            <div class="metric-label">Total Kasus Malaria</div>
            <div class="metric-value" style="color: #C62828;">{tot_malaria:,.0f}</div>
            <div class="metric-desc">Penyakit vektor endemis dengan kecenderungan meningkat, berkorelasi dengan keberadaan genangan air bekas galian tambang yang tidak direklamasi.</div>
        </div>
        <div class="metric-source"><b>Sumber:</b> Data Agregat Dinas Kesehatan (2014-2024)<br/><i>File: sulawesi_kesehatan_detail_2014_2024.csv</i></div>
    </div>

--- BLOCK 6 ---
<div class="metric-card">
        <div>
            <div class="metric-label">Rasio Puskesmas Terdaftar (2022)</div>
            <div class="metric-value" style="color: #FF8A65;">{tot_puskesmas_2022:,.0f} <span style="font-size:1rem;">Unit</span></div>
            <div class="metric-desc">Fasilitas primer warga yang pertumbuhannya tidak sebanding dengan peningkatan beban kasus penyakit di wilayah industri.</div>
        </div>
        <div class="metric-source"><b>Sumber:</b> BPS Ketersediaan Faskes<br/><i>File: sulawesi_faskes_agregat_v2.csv</i></div>
    </div>

--- BLOCK 7 ---
<div class="metric-card">
        <div>
            <div class="metric-label">Rasio Rumah Sakit (2022)</div>
            <div class="metric-value" style="color: #FFAB91;">{tot_rs_2022:,.0f} <span style="font-size:1rem;">Unit</span></div>
            <div class="metric-desc">Ketersediaan rumah sakit yang tidak merata di wilayah timur, mengindikasikan belum optimalnya distribusi infrastruktur medis.</div>
        </div>
        <div class="metric-source"><b>Sumber:</b> BPS Ketersediaan Faskes<br/><i>File: sulawesi_faskes_agregat_v2.csv</i></div>
    </div>

--- BLOCK 8 ---
**Metode Analisis:** Sub-bab ini menggunakan visualisasi perbandingan *Grouped Horizontal Bar Chart* pada satu periode cross-sectional (Tahun 2022) untuk mengukur ketimpangan infrastruktur kesehatan primer dan sekunder.

    1. **Analisis Ketimpangan Infrastruktur (Gap Analysis):**
        * **Segmentasi Fasilitas:** Fasilitas kesehatan dikategorikan secara hierarkis menjadi Puskesmas (Faskes Primer) dan Rumah Sakit (Faskes Sekunder) untuk dievaluasi secara spasial (Sentra vs Non-Sentra).
        * **Evaluasi Defisit:** Mengukur kesenjangan distribusi rasio fasilitas medis per provinsi menggunakan analisis komparatif absolut.
        * **Pemetaan Ketersediaan:** Membedah paradoks ketersediaan layanan kesehatan di wilayah pusat akumulasi kapital ekstraktif sebagai pembuktian defisit infrastruktur publik.
    2. **Kalkulasi/Formula Pengolahan:** Perhitungan agregat ketersediaan faskes menurut wilayah pada tahun acuan data terlengkap (2022).
        * `Rata_Rata_Faskes = MEAN(Jumlah_Faskes) GROUP BY Jenis_Faskes, Kategori_Zona`
    3. **Variabel & Fitur Data:**
        * **Jumlah & Jenis Faskes (Dependen):** Unit Rumah Sakit dan Puskesmas terdaftar (BPS).
        * **Kategori Zona (Independen):** Lokasi wilayah (Sentra vs Non-Sentra).
    4. **Dataset & File:**
        * Data Agregat Faskes: `data/processed/sulawesi_faskes_agregat_v2.csv`

--- BLOCK 9 ---
Data perbandingan distribusi fasilitas kesehatan mengindikasikan bahwa ketersediaan infrastruktur medis di provinsi sentra industri relatif tidak lebih baik dibandingkan wilayah non-sentra, meski beban penyakit di wilayah tersebut lebih tinggi.

Melalui komparasi grafik batang (*Grouped Bar Chart*) di bawah, terlihat bahwa ketersediaan Fasilitas Kesehatan di provinsi dengan konsentrasi industri tinggi justru mengalami defisit relatif. Rata-rata Rumah Sakit di Sentra Industri tercatat **{rs_sentra:.0f} unit** per provinsi, lebih rendah dari wilayah Non-Sentra yang mencapai **{rs_non:.0f} unit**. Kesenjangan distribusi fasilitas medis di area dengan beban penyakit tinggi ini perlu menjadi pertimbangan dalam perencanaan infrastruktur kesehatan ke depan.

--- BLOCK 10 ---
**Metode Analisis:** Sub-bab ini menggunakan analisis komparatif spasial (*Comparative Spatial Analysis*) untuk membandingkan rata-rata beban penyakit antara provinsi sentra ekstraktif dan non-sentra.

    1. **Model Komparasi Spasial (Comparative Analysis):**
        * **Segmentasi Wilayah (Binning):** Provinsi secara sistematis dibagi menjadi dua zona: Sentra Industri (Sulteng & Sultra) dan Non-Sentra (Sulsel, Sulut, Gorontalo, Sulbar).
        * **Kuantifikasi Kesenjangan:** Menghitung rata-rata absolut beban kesakitan (*disease burden*) per zona untuk mengukur ketimpangan kesehatan struktural antar wilayah.
        * **Pemetaan Pola:** Mengidentifikasi secara analitik apakah konsentrasi fasilitas tambang berkorespondensi langsung dengan akumulasi masif kasus epidemiologis.
    2. **Kalkulasi/Formula Pengolahan:** Perhitungan rata-rata absolut beban penyakit tahunan berdasarkan klasifikasi wilayah.
        * `Rata_Rata_Kasus_Zona = MEAN(Jumlah_Kasus) GROUP BY Kategori_Zona`
        * `Disparitas_Beban = Rata_Rata_Kasus_Sentra / Rata_Rata_Kasus_Non_Sentra`
    3. **Variabel & Fitur Data:**
        * **Kategori Zona (Independen):** Labeling spasial (Sentra vs Non-Sentra).
        * **Kasus ISPA/Pneumonia & Diare (Dependen):** Total prevalensi historis penyakit per tahun dari fasilitas kesehatan primer.
    4. **Dataset & File:**
        * Data Agregasi Kesehatan: `data/processed/sulawesi_kesehatan_detail_2014_2024.csv`

--- BLOCK 11 ---
Melalui analisis komparatif spasial, terlihat bahwa beban ekologis tidak terdistribusi secara merata di seluruh wilayah. Provinsi sentra ekspansi nikel—Sulawesi Tengah dan Sulawesi Tenggara—menunjukkan indikator penyakit yang secara konsisten lebih tinggi.

Data menunjukkan bahwa rata-rata penderita **ISPA/Pneumonia** di Sentra Industri tercatat **{ispa_sentra:,.0f} kasus per tahun**, dibandingkan provinsi Non-Sentra di angka **{ispa_non:,.0f} kasus**. Selisih sebesar **{ispa_diff:.1f} kali lipat** ini mengindikasikan beban pernapasan yang lebih berat di kawasan penyangga *smelter*. Temuan ini mendukung hipotesis kerangka riset D3TLH: wilayah dengan konsentrasi industri tinggi cenderung menanggung beban kesehatan yang lebih besar akibat tekanan terhadap daya tampung lingkungan.

--- BLOCK 12 ---
<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #FF5722; margin-bottom: 25px;">
    <b>Interpretasi Ekologis:</b> Kesenjangan statistik ini mengindikasikan bahwa manfaat ekonomi dari hilirisasi nikel belum disertai perbaikan infrastruktur kesehatan yang proporsional di wilayah operasi industri ekstraktif.
</div>

--- BLOCK 13 ---
**Metode Analisis:** Sub-bab ini menggunakan visualisasi runtut waktu (Time-Series) dan uji silang (Crosstabulation) secara interaktif untuk merunut dinamika insiden penyakit sejalan dengan akumulasi polusi tahunan.

    1. **Uji Trend Historis & Proporsi Tabulasi Silang:**
        * **Time-Series Tracking:** Mengkonversi absolute numbers ke rasio per kapita (Kasus per 10.000 Penduduk) untuk menghilangkan bias jumlah populasi antar wilayah.
        * `H0 (Null Hypothesis): Penurunan kualitas lingkungan (IKU/IKA) tidak berkorelasi dengan peningkatan insidensi penyakit pernapasan dan pencernaan.`
        * `Decision Rule: Chi-Square P-Value < 0.05 (Tolak H0) dan kalkulasi Odds Ratio.`
    2. **Kalkulasi/Formula Pengolahan:** Rasio keparahan per kapita dan agregasi tabel silang panel.
        * `Insiden_Per_10K = (Total_Kasus / Total_Populasi) * 10,000`
        * `Odds_Ratio = (A * D) / (B * C)`
    3. **Variabel & Fitur Data:**
        * **Indikator Kualitas Lingkungan (X):** IKU/IKA sebagai matriks tekanan lingkungan.
        * **Total Insiden Penyakit (Y):** Angka absolut & insiden per kapita dari beragam penyakit lingkungan (ISPA, Diare, Malaria, Kusta).
        * **Waktu (Time):** Periode longitudinal 2014-2024.
    4. **Dataset & File:**
        * Data Lingkungan & Penyakit: `data/processed/sulawesi_kesehatan_detail_2014_2024.csv`, `data/processed/sulawesi_ika_2016_2024.csv`, `data/processed/sulawesi_iku_2015_2024.csv`

--- BLOCK 14 ---
Meskipun secara akumulatif kawasan Sentra Industri menanggung beban yang lebih berat, penelusuran data secara *time-series* (historis) dari 2014 hingga 2024 memberikan wawasan tambahan mengenai fluktuasi kasus penyakit dari tahun ke tahun. Anda dapat memilih indikator penyakit pada menu di bawah untuk melihat jejak ekologis secara spesifik.

--- BLOCK 15 ---
Hipotesis utama narasi ini adalah bahwa **penurunan kualitas udara ambien (IKU)** berbanding lurus dengan **peningkatan insidensi penyakit pernapasan dan lingkungan** (seperti ISPA dan Diare).
Untuk mengujinya secara statistik di tengah keterbatasan jumlah provinsi di Sulawesi (N=6), tabel crosstab dan uji Chi-Square di bawah menggunakan unit observasi **Provinsi-Tahun** (6 provinsi × 10 tahun = 60 sampel panel).
Setiap observasi diklasifikasikan menjadi "Tinggi" atau "Rendah" berdasarkan nilai **Median panel** dari indikator yang dipilih.

--- BLOCK 16 ---
<div style="border: 2px solid {order_color}; padding: 15px; border-radius: 5px; background-color: {bg_color}; margin-bottom: 10px;">
        <h4 style="color: {order_color}; margin: 0 0 10px 0; text-transform: uppercase;">Result: {status_text}</h4>
        <p style="margin: 0; font-family: monospace;">
            P-Value    : {p:.4f}<br>
            Chi-Square : {chi2:.3f}<br>
            df         : {dof}
        </p>
    </div>

--- BLOCK 17 ---
<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid {order_color}; height: 100%;">
        <b>Interpretasi Ekologis:</b><br><br>
        {interp_text}
    </div>

--- BLOCK 18 ---
<div style="background-color: {bg_color}; padding:18px; border-radius:8px; border-left:6px solid {border_color}; margin-top: 15px; margin-bottom: 25px;">
    <b style="color: {border_color}; font-size: 1.05rem;">Pembedahan Realitas Ekologis:</b><br><br>
    <div style="color: #E0E0E0; font-size: 0.95rem; line-height: 1.6;">
{exec_narrative}
    </div>
</div>

--- BLOCK 19 ---
**Metode Analisis:** Sub-bab ini menggunakan studi kasus mendalam (*Deep Dive Case Study*) berbasis deret waktu di tingkat distrik (Kabupaten/Kota) khusus untuk endemik Sulawesi Tengah.

        1. **Model Anomali Ekologis Spesifik Distrik:**
            * **Analisis Komparatif Zoonosis:** Mengisolasi zona episentrum ekstraktif (Morowali, Morowali Utara, Banggai) dan membandingkannya secara absolut dengan kabupaten agraris/non-tambang yang difungsikan sebagai daerah kontrol.
            * **Korelasi Ekologis:** Merunut pola peningkatan prevalensi penyakit infeksi yang ditransmisikan oleh vektor di kawasan perluasan pembukaan lahan (*land clearing*).
            * **Pemetaan Risiko:** Mengukur eskalasi kerentanan populasi terhadap ancaman wabah malaria dan DBD akibat hancurnya perlindungan habitat alami.
        2. **Kalkulasi/Formula Pengolahan:** Akumulasi tren tahunan infeksi Zoonosis per Kategori Wilayah (Tambang vs Non-Tambang).
            * `Tren_Zoonosis_Distrik = Σ(Total_Kasus) GROUP BY Kategori_Wilayah, Tahun`
        3. **Variabel & Fitur Data:**
            * **Kategori Wilayah Distrik:** Label dikotomi daerah ring 1 tambang vs daerah penyangga luar ring.
            * **Total Kasus Penyakit:** Angka infeksi yang ditransmisikan vektor (Malaria, Rabies, Gigitan Hewan).
        4. **Dataset & File:**
            * Data Zoonosis: `data/processed/zoonosis_kab_kota_2015_2024.csv`

--- BLOCK 20 ---
<p style="color:#E0E0E0; font-size: 1rem; line-height: 1.6; text-align: justify; margin-top: 20px;">
        Data empiris Dinas Kesehatan mencatat total akumulasi <b>{total_kasus_tambang:,.0f} kasus</b> penyakit Zoonosis di wilayah Lingkar Tambang/Smelter Aktif Sulawesi Tengah (Morowali, Morowali Utara, Banggai) sepanjang rentang waktu pengamatan.{peak_narrative}
    </p>
    <p style="color:#E0E0E0; font-size: 1rem; line-height: 1.6; text-align: justify;">
        Peningkatan angka zoonosis ini berkorelasi dengan perubahan ekologis akibat ekspansi penggunaan lahan. Konversi tutupan hutan demi perluasan konsesi dan fasilitas pengolahan <i>smelter</i> berdampak pada pergeseran habitat alami satwa liar. Akibatnya, vektor pembawa penyakit terpaksa bermigrasi dan beririsan langsung dengan pemukiman pekerja tambang dan warga lokal. Keberadaan genangan air galian tambang yang tidak direklamasi serta kondisi sanitasi di area industri turut menjadi faktor pendukung perkembangbiakan vektor penyakit.
    </p>
    <p style="color:#E0E0E0; font-size: 1rem; line-height: 1.6; text-align: justify;">
        Pertumbuhan investasi di sektor ekstraktif belum diimbangi dengan alokasi perlindungan sosial dan lingkungan yang memadai bagi masyarakat lokal. Penduduk asli dan pekerja tambang menghadapi risiko kesehatan berlapis: paparan emisi udara dari <i>captive power plant</i> sekaligus potensi risiko penyakit menular akibat disrupsi lingkungan hidup.
    </p>

--- BLOCK 21 ---
<div style="color:#B0BEC5; font-size:0.9rem; line-height:1.5; margin: 8px 0 14px 0;">
                <b>Keterangan pembacaan grafik:</b> garis merah solid menandai kabupaten <b>Ekstraktif/Smelter</b> (Morowali, Morowali Utara, Banggai). Gradasi merah mengikuti puncak kasus pada penyakit yang dipilih: merah paling kuat = puncak tertinggi. Garis abu-abu putus-putus menandai wilayah <b>Non-Ekstraktif/Kontrol</b>. Angka di setiap titik menunjukkan total kasus absolut pada tahun tersebut.
            </div>

--- BLOCK 22 ---
<h4 style="color: #FF5722; margin-top: 10px; margin-bottom: 5px; font-size: 1.1rem;">Interpretasi Spesifik: {selected_penyakit}</h4>
            <p style="color:#B0BEC5; font-size: 0.95rem; line-height: 1.6; text-align: justify;">
                Perbandingan grafik rata-rata di samping menunjukkan bahwa beban absolut kasus <b>{selected_penyakit}</b> di wilayah Lingkar Tambang/Smelter Aktif mencapai <b>{val_tambang:,.1f} kasus/tahun</b>.
            </p>
            <p style="color:#B0BEC5; font-size: 0.95rem; line-height: 1.6; text-align: justify;">
                Meskipun populasi area tambang seringkali lebih terkonsentrasi, angka ini memberikan sinyal kuat bahwa degradasi lingkungan di sekitar smelter menciptakan ceruk ekologis baru (seperti genangan air galian) yang mempercepat siklus penularan {selected_penyakit}.
            </p>

--- BLOCK 23 ---
<div class="section-copy">
    DBD dipakai sebagai indikator proxy karena penyakit ini sensitif terhadap perubahan lingkungan permukiman, kepadatan, drainase, sanitasi, dan mobilitas penduduk. Analisis ini tidak menyatakan bahwa smelter secara tunggal menyebabkan DBD; yang diuji adalah apakah kabupaten smelter menunjukkan beban kesehatan yang perlu dibaca bersama tekanan demografi dan perubahan ruang. Sejak 2019, total kasus DBD yang tercatat di kabupaten smelter mencapai <b>{dbd_smelter:,}</b> kasus, sedangkan kabupaten non-smelter mencapai <b>{dbd_non_smelter:,}</b> kasus. Karena jumlah kabupaten dalam dua kelompok tidak sama, grafik memakai rata-rata kasus per kabupaten-tahun. Rata-rata kabupaten smelter tercatat sekitar <b>{dbd_avg_smelter:.1f}</b> kasus per observasi, sementara non-smelter sekitar <b>{dbd_avg_non_smelter:.1f}</b>. Rasio <b>{dbd_ratio:.2f} kali</b> ini harus dibaca hati-hati sebagai sinyal komparatif, bukan bukti kausal final, tetapi tetap penting untuk menilai beban sosial dari industrialisasi.
    </div>

--- BLOCK 24 ---
**Metode Analisis:** Sub-bab ini menggunakan visualisasi WebGIS (Choropleth dan Point/Bubble Mapping) berbasis Leaflet/Folium untuk menganalisis pergeseran geospasial beban penyakit secara komparatif (*Before-After Analysis*).

    1. **Pemetaan Spasial Komparatif:**
        * **Poligon (Choropleth):** Intensitas warna area mewakili tingkatan total insiden ISPA. Semakin gelap, semakin rentan.
        * **Titik (Bubble):** Ukuran/radius lingkaran merepresentasikan volume kasus Diare secara proporsional.
        * **Identifikasi Episentrum (Clustering):** Menganalisis pemusatan visual beban ganda penyakit pada koordinat geografis yang beririsan langsung dengan zona perluasan industri.
    2. **Kalkulasi/Formula Pengolahan:** Komparasi absolut lintas dekade (2015 vs 2024) dan standarisasi radius bubble.
        * `Radius_Bubble = SQRT(Kasus_Diare) / K` (K = konstanta penyesuaian visual)
        * `Growth_Rate = ((Kasus_2024 - Kasus_2015) / Kasus_2015) * 100%`
    3. **Variabel & Fitur Data:**
        * **Titik Koordinat/Poligon:** Polygon Provinsi Sulawesi (GeoJSON).
        * **Warna & Ukuran (Visual Encode):** Total ISPA dan Total Diare (Data Kesehatan).
    4. **Dataset & File:**
        * Data Spasial: `data/raw/indonesia-prov.geojson`
        * Data Penyakit: `data/processed/sulawesi_kesehatan_detail_2014_2024.csv`

--- BLOCK 25 ---
Peta interaktif di bawah ini memproyeksikan secara spasial perbandingan absolut beban kesehatan (ISPA dan Diare) antara **Awal Ekstraksi (2015)** dan **Kondisi Terkini (2024)**. Sesuai *framework Before-After Analysis*, Anda bisa melihat bagaimana distribusi beban penyakit berkembang seiring perluasan kawasan industri.

--- BLOCK 26 ---
**Metode Analisis:** Sub-bab ini menggunakan pendekatan komplementer untuk memetakan krisis air bersih dan dampaknya terhadap penyakit Diare. Keterbatasan granularitas pada data statistik agregat tingkat provinsi memerlukan validasi lapangan melalui uji laboratorium di tingkat tapak.

    1. **Tinjauan Mikro (Bukti Fisik Laboratorium):**
        * Memeriksa kadar Kromium Heksavalen (Cr6+) di muara pembuangan air dan *tailing* tambang menggunakan data uji lab lapangan.
        * `Benchmark:` Membandingkan temuan sampel dengan baku mutu air laut (0.005 mg/L) untuk menilai pelanggaran toksisitas secara absolut.
    2. **Tinjauan Makro (Analisis Panel Provinsi):**
        * **Korelasi Bivariat (Scatter Plot):** Melihat tren distribusi antara IKA dan kasus Diare untuk melihat gambaran umum regional, terlepas dari kelemahan signifikansi OLS (Ordinary Least Squares) akibat jumlah sampel yang sangat kecil (n=6 provinsi).
    3. **Variabel & Fitur Data:**
        * **Kualitas Air (Mikro):** Data konsentrasi Cr6+ dari investigasi lapangan (AEER & WALHI).
        * **IKA (Makro):** Indeks Kualitas Air (BPS/KLHK).
        * **Diare (Makro):** Kasus infeksi saluran pencernaan yang dilayani (Kemenkes).

--- BLOCK 27 ---
Sub-bab ini membedah krisis air bersih melalui **dua tingkat observasi paralel**. Pertama, tinjauan mikro spesifik di kawasan padat industri menggunakan hasil uji fisik laboratorium independen. Kedua, pemetaan tren makro di tingkat provinsi yang melihat distribusi Indeks Kualitas Air (IKA) terhadap sebaran kasus Diare.

Pendekatan komplementer ini sangat penting untuk dilakukan. **Indeks Kualitas Air (IKA)** dari pemerintah merupakan nilai rata-rata dari seluruh DAS (Daerah Aliran Sungai) di satu provinsi, sehingga tidak bisa mendeteksi pencemaran ekstrem secara spesifik di muara tambang (*point source*). Oleh karena itu, kita mendampingkan pemetaan statistik makro ini dengan bukti lab klinis (Kromium) di tingkat tapak untuk mendapatkan realita krisis secara utuh.

--- BLOCK 28 ---
Titik yang tersebar acak mengindikasikan bahwa data makro secara statistik tidak menunjukkan korelasi kausalitas yang kuat pada level agregat provinsi (R²=0.043, P=0.157). Oleh karena itu, kesimpulan pencemaran air lebih valid ditarik dari hasil uji klinis mikroskopis di tapak (Bukti Lab NGO).

--- BLOCK 29 ---
Menghadapi absennya data **"Akses Air Minum Layak"** di tingkat Kabupaten dari BPS sejak 2019, kami menggunakan **Ground Truth Data** dari pengujian laboratorium independen (AEER & WALHI) sebagai alternatif pengukur pencemaran air secara absolut.
        
        Berdasarkan hasil uji klinis dari {total_samples} titik sampel di lingkar kawasan tambang, teridentifikasi bahwa **{exceed_biota} titik ({(exceed_biota/total_samples*100):.0f}%) melampaui batas aman toksisitas biota laut** (0.005 mg/L). Konsentrasi terparah ditemukan di {max_location} dengan kadar Kromium Heksavalen mencapai **{max_cr6:.3f} mg/L**, atau {(max_cr6/0.005):.0f} kali lipat lebih tinggi dari ambang batas aman. 
        
        ⚠️ **Peringatan Klinis:** Kromium Heksavalen (Cr6+) adalah logam berat karsinogenik beracun. Paparan berulang pada air yang dikonsumsi atau digunakan mencuci memicu iritasi kulit kronis, kerusakan pernapasan, pencernaan, dan potensi kanker parah di komunitas lingkar tambang. Bukti konkret di level tapak ini mengonfirmasi asimetri dampak ekologis industri ekstraktif yang gagal ditangkap oleh agregasi data makro.

--- BLOCK 30 ---
Untuk membuktikan hubungan kausal secara statistik, crosstab Chi-Square di bawah menggunakan unit observasi **Provinsi-Tahun** (6 provinsi × 9 tahun = 54 sampel panel).
Setiap observasi diklasifikasikan menjadi "IKA Rendah/Tinggi" dan "Diare Rendah/Tinggi" berdasarkan **median panel** dari masing-masing indikator.

--- BLOCK 31 ---
<div style="border: 2px solid {order_color_ika}; padding: 15px; border-radius: 5px; background-color: {bg_color_ika}; margin-bottom: 10px;">
        <h4 style="color: {order_color_ika}; margin: 0 0 10px 0; text-transform: uppercase;">Result: {status_text_ika}</h4>
        <p style="margin: 0; font-family: monospace;">
            P-Value    : {p_ika:.4f}<br>
            Chi-Square : {chi2_ika:.3f}<br>
            df         : {dof_ika}
        </p>
    </div>

--- BLOCK 32 ---
<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid {order_color_ika}; height: 100%;">
        <b>Interpretasi Ekologis:</b><br><br>
        {interp_text_ika}
    </div>

--- BLOCK 33 ---
<div style="background-color: {bg_color_ika}; padding:18px; border-radius:8px; border-left:6px solid {border_color_ika}; margin-top: 15px; margin-bottom: 25px;">
    <b style="color: {border_color_ika}; font-size: 1.05rem;">Pembedahan Realitas Ekologis:</b><br><br>
    <div style="color: #E0E0E0; font-size: 0.95rem; line-height: 1.6;">
{exec_narrative_ika}
    </div>
</div>

--- BLOCK 34 ---
**Metode Analisis:** Sub-bab ini menggunakan agregasi statistik deskriptif dan komparasi grafik batang (*Bar Chart*) untuk merunut skala penumpukan limbah B3 sebagai pemicu (driver) racun ekosistem.

    1. **Agregasi Limpasan Limbah Industri:**
        * **Statistik Deskriptif:** Melakukan pemeringkatan dan *profiling* komposisi buangan B3 absolut dari setiap fasilitas peleburan logam berat yang beroperasi.
        * **Audit Defisit Pengelolaan:** Mengkomparasikan kapasitas pengolahan yang dilaporkan dengan estimasi empiris total emisi limbah.
        * **Pemetaan Toksisitas:** Mengidentifikasi sumber dan skala ancaman racun lingkungan berdasarkan jenis tailing dan material B3 yang dominan.
    2. **Kalkulasi/Formula Pengolahan:** Penjumlahan agregat produksi limbah kotor dari level pabrik hingga ke level regional.
        * `Total_B3_Provinsi = Σ(Timbulan_Ton) GROUP BY Provinsi`
        * `Total_B3_Jenis = Σ(Timbulan_Ton) GROUP BY Jenis_Limbah`
    3. **Variabel & Fitur Data:**
        * **Timbulan (Ton/Tahun):** Estimasi absolut volume buangan limbah (Dependen).
        * **Kawasan & Jenis Limbah:** Klasifikasi operasi dan karakter residu seperti Slag/Tailing/Air Asam Tambang (Independen).
    4. **Dataset & File:**
        * Data Audit LSM & KLHK: `data/processed/sulawesi_limbah_b3.csv`

--- BLOCK 35 ---
Jika sub-bab sebelumnya telah membedah dampak pencemaran udara (IKU → ISPA) dan air (IKA → Diare), maka sub-bab ini mengungkap **sumber polusi yang signifikan namun memerlukan perhatian khusus**: timbulan **Limbah Bahan Berbahaya dan Beracun (B3)** dari operasi smelter dan tambang nikel.

**Limbah B3** adalah residu hasil proses ekstraktif yang mengandung logam berat, senyawa kimia berbahaya, dan material berpotensi karsinogenik. Jenis limbah ini meliputi:

- **Slag & Tailing**: Material sisa pengolahan bijih nikel yang mengandung logam berat seperti Chromium, Nikel, dan Kadmium
- **Tailing HPAL**: Limbah padat hasil proses High-Pressure Acid Leaching (HPAL) yang bersifat asam dan mengandung sulfat tinggi
- **Air Limbah Tambang**: Buangan cair yang tercemar logam berat dan asam sulfat
- **Residu & DSTP**: Material beracun yang dikaji dalam opsi pembuangan laut dalam (Deep Sea Tailing Placement)

Klaim bahwa slag dapat "dimanfaatkan untuk batako dan penahan abrasi" memerlukan kajian kritis, mengingat akumulasi material ini memerlukan pengelolaan dan pemantauan risiko kesehatan yang transparan.

Data kompilasi dari laporan AEER, WALHI, JATAM, dan kajian akademis membuktikan bahwa **operasi smelter di Sulawesi menghasilkan puluhan juta ton limbah B3 per tahun**—dengan dampak kesehatan jangka panjang yang perlu dimonitor secara berkelanjutan.

--- BLOCK 36 ---
<div style="background: linear-gradient(135deg, #1E1E1E, #2C1810); padding: 20px; border-radius: 10px; border-left: 5px solid #E53935; margin-bottom: 25px;">
    <h3 style="color: #FF6F60; margin-top: 0;">Skala Ancaman Limbah Beracun</h3>
    <p style="color: #EEEEEE; font-size: 1.05rem; line-height: 1.7;">
        Data komprehensif dari berbagai sumber (AEER, WALHI, JATAM, BPLH) membuktikan bahwa industri nikel di Sulawesi menghasilkan <b>lebih dari {total_b3 / 1_000_000:.1f} juta ton limbah B3 per tahun</b>. Angka ini setara dengan menimbun <b>{total_b3 / 1000:,.0f} gedung bertingkat</b> dengan material beracun setiap tahunnya.
    </p>
    <p style="color: #EEEEEE; font-size: 1.05rem; line-height: 1.7;">
        Provinsi <b>{max_prov["Provinsi"]}</b> menanggung beban terbesar dengan <b>{max_prov["Estimasi Timbulan (Ton/Tahun)"] / 1_000_000:.1f} juta ton</b> limbah B3 per tahun, didominasi oleh operasi <b>IMIP (Indonesia Morowali Industrial Park)</b> yang menghasilkan slag dan tailing HPAL tanpa izin formal yang memadai.
    </p>
    <p style="color: #FFCCBC; font-size: 0.95rem; margin-top: 15px; border-top: 1px dotted #555; padding-top: 10px;">
        <b>Catatan Kritis:</b> Angka resmi ini kemungkinan besar <i>underestimate</i> (meremehkan) karena banyak fasilitas yang tidak melaporkan timbulan limbah secara transparan. Estimasi independen menyebutkan angka sebenarnya bisa 2-3 kali lipat lebih tinggi.
    </p>
</div>

--- BLOCK 37 ---
<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #E53935; margin-bottom: 20px; margin-top: 15px;">
    <b>Interpretasi Spasial:</b><br><br>
    Visualisasi di atas menunjukkan bahwa <b>Sulawesi Tengah dan Sulawesi Tenggara</b>—dua provinsi episentrum hilirisasi nikel—menanggung volume limbah B3 yang signifikan. <b>Sulawesi Tengah</b> menghasilkan <b>{sulteng_b3 / 1_000_000:.1f} juta ton B3/tahun</b>, terutama dari kawasan industri Morowali.<br><br>

    Ini mencerminkan <b>ketimpangan ekologis</b>: wilayah penyangga menanggung beban limbah industri yang signifikan dibandingkan manfaat ekonomi langsung yang diterima. Warga lokal beriringan dengan lokasi timbunan slag—<b>sehingga membutuhkan pengawasan proteksi kesehatan dan transparansi pengolahan</b>.
</div>

--- BLOCK 38 ---
<div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid #FF9800; margin-bottom: 20px; margin-top: 15px;">
    <b>Interpretasi Komposisi Limbah:</b><br><br>
    <b>Slag dan Tailing</b> mendominasi timbulan limbah B3 dengan total <b>{(slag_total + tailing_total) / 1_000_000:.1f} juta ton/tahun</b>. Material ini mengandung konsentrasi tinggi logam berat seperti <b>Chromium (Cr), Nikel (Ni), Kadmium (Cd), dan Arsenik (As)</b> yang bersifat karsinogenik (memicu kanker) dan neurotoksik (merusak sistem saraf).<br><br>

    Klaim industri bahwa slag "aman dimanfaatkan untuk batako" adalah <b>klaim yang perlu dikaji lebih kritis</b>. Penelitian mengindikasikan bahwa paparan jangka panjang terhadap debu slag berpotensi memicu <b>dermatitis dan gangguan pernapasan</b> pada komunitas sekitar.<br><br>

    <b>Tailing HPAL</b> (High-Pressure Acid Leaching) lebih berbahaya lagi karena mengandung <b>asam sulfat konsentrasi tinggi</b> yang dapat mencemari sungai dan laut. Proses HPAL yang digunakan PT HNC dan PT QMB di Morowali menghasilkan <b>12,5 juta ton tailing beracun per tahun</b>—setara dengan volume banjir bandang yang terjadi setiap hari.
</div>

--- BLOCK 39 ---
Meskipun data epidemiologis yang menghubungkan secara langsung antara paparan limbah B3 dengan penyakit spesifik masih terbatas (karena keengganan industri untuk melakukan kajian kesehatan independen), **bukti-bukti tidak langsung sangat kuat**:

1. **Korelasi Geografis:** Provinsi dengan timbulan B3 tertinggi (Sulteng & Sultra) adalah provinsi yang sama dengan beban ISPA dan Diare tertinggi (terbukti di sub-bab 3.1 dan 3.5)

2. **Jalur Paparan Multipel:**
   - **Paparan Inhalasi:** Debu slag yang beterbangan terhirup warga sekitar → ISPA/Pneumonia kronis
   - **Kontaminasi Air:** Lindi (leachate) dari timbunan tailing berpotensi memengaruhi sumber air → Peningkatan kasus Diare dan penyakit kulit
   - **Akumulasi Logam Berat:** Chromium dan Nikel terakumulasi dalam rantai makanan → Risiko kanker jangka panjang

3. **Temuan Lapangan dari WALHI dan JATAM:**
   - Warga Morowali melaporkan peningkatan kasus gatal-gatal kulit dan iritasi mata sejak operasi IMIP dimulai
   - Air sumur warga di sekitar kawasan smelter berubah warna menjadi kemerahan dan berbau logam
   - Ikan hasil tangkapan nelayan lokal mengalami penurunan kualitas dan kuantitas drastis

4. **Perbandingan Internasional:** Kasus pencemaran slag di Filipina (Zambales) dan Kaledonia Baru (New Caledonia) membuktikan bahwa komunitas yang hidup di sekitar fasilitas pengolahan nikel mengalami peningkatan signifikan kasus penyakit pernapasan, kanker paru-paru, dan gangguan reproduksi.

--- BLOCK 40 ---
<div style="background: linear-gradient(135deg, #1E1E1E, #2C1810); padding: 20px; border-radius: 10px; border-left: 5px solid #BF360C; margin-bottom: 25px; margin-top: 20px;">
    <h4 style="color: #FF6F60; margin-top: 0;">Kesimpulan Kritis: Beban Ganda Masyarakat Terdampak</h4>
    <p style="color: #EEEEEE; font-size: 1.05rem; line-height: 1.7;">
        Data limbah B3 di atas menegaskan bahwa masyarakat di zona penyangga smelter <b>menanggung beban ganda (double burden)</b>:
    </p>
    <ol style="color: #EEEEEE; font-size: 1rem; line-height: 1.7;">
        <li><b>Beban Polusi Aktif:</b> Paparan harian terhadap emisi SO₂, debu PM2.5, dan pencemaran air (terbukti di sub-bab 3.3 dan 3.5)</li>
        <li><b>Beban Polusi Pasif:</b> Hidup berdampingan dengan timbunan <b>{total_b3 / 1_000_000:.1f} juta ton limbah beracun</b> yang terakumulasi setiap tahun—<b>tanpa jaminan keamanan jangka panjang</b></li>
    </ol>
    <p style="color: #EEEEEE; font-size: 1.05rem; line-height: 1.7;">
        Kompleks IMIP di Morowali menghasilkan <b>{imip_b3 / 1_000_000:.1f} juta ton limbah B3/tahun</b>. Hal ini menunjukkan pentingnya evaluasi independen atas dampak lingkungan dan kesehatan dari ekspansi industri nikel bagi masyarakat sekitar.
    </p>
    <p style="color: #FFCCBC; font-size: 1rem; margin-top: 15px; border-top: 1px dotted #555; padding-top: 10px;">
        <b>Rekomendasi Kebijakan:</b> Pemerintah harus segera menghentikan ekspansi smelter baru hingga tersedia kajian risiko kesehatan independen, sistem monitoring limbah B3 yang transparan, dan skema kompensasi yang adil bagi masyarakat terdampak. <b>Hak atas lingkungan hidup yang sehat adalah hak asasi yang tidak dapat ditawar dengan pertumbuhan ekonomi semata</b>.
    </p>
</div>

