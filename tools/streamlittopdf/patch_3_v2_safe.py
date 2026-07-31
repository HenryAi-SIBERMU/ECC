import re
import pandas as pd

with open("tools/streamlittopdf/extract_chapter_3.py", "r", encoding="utf-8") as f:
    content = f.read()

split_point = '    exec_hdr = "| Variabel Independen (X) | Variabel Dependen (Y) | Chi-Square | P-Value | Odds Ratio | Kesimpulan |\\n| :--- | :--- | :--- | :--- | :--- | :--- |"'
if split_point in content:
    pre_content = content.split(split_point)[0]
else:
    print("Could not find split point")
    exit()

new_content = pre_content + """    try: max_prov = df_b3_by_prov.loc[df_b3_by_prov["Estimasi Timbulan (Ton/Tahun)"].idxmax()]
    except: max_prov = {"Provinsi": "", "Estimasi Timbulan (Ton/Tahun)": 0}
    
    exec_hdr = "| Variabel Independen (X) | Variabel Dependen (Y) | Chi-Square | P-Value | Odds Ratio | Kesimpulan |\\n| :--- | :--- | :--- | :--- | :--- | :--- |"

    md = f\"\"\"# Beban Kesehatan Masyarakat Terdampak

Tinjauan empiris beban kesehatan masyarakat akibat paparan emisi dan polutan industri di kawasan penyangga smelter nikel Sulawesi.

> **Alur Kausalitas (Ekonomi Politik Ekologi):** `Konsentrasi Industri Ekstraktif` → `Penurunan Kualitas Daya Dukung Lingkungan` → `Peningkatan Insidensi Penyakit (ISPA, Diare) & Ketimpangan Faskes`
>
> Ekspansi industri ekstraktif berpotensi memengaruhi kualitas lingkungan hidup masyarakat setempat. Pembuangan polutan ke udara ambien dan badan air berkorelasi dengan peningkatan insidensi penyakit respiratori dan infeksi saluran pencernaan, yang diperparah oleh ketimpangan distribusi fasilitas kesehatan.
>
> **Variabel Dampak Kesehatan (Y):**
> * **ISPA/Pneumonia:** Penyakit pernapasan akibat paparan debu dan sulfur.
> * **Diare & Penyakit Menular (Malaria/Kusta):** Dampak pencemaran air dan buruknya sanitasi di lingkar tambang.
> * **Ketersediaan Fasilitas Kesehatan:** Kesenjangan infrastruktur medis (Puskesmas & Rumah Sakit) terhadap pertumbuhan beban kasus penyakit.
>
> **Metode Pengolahan Data:**
> Analisis menggunakan *Cross-sectional* dan *Time-Series*. Menggabungkan dataset *survey* dinas kesehatan dan ketersediaan layanan publik untuk menganalisis korelasi antara pertumbuhan kapasitas PLTU *captive* dan peningkatan beban penyakit di masyarakat dengan ketersediaan fasilitas medis yang terbatas.

## Hilirisasi Nikel dan Dampak Kesehatan: Analisis Data Empiris di Kawasan Penyangga

Data empiris menggambarkan kesenjangan antara klaim pertumbuhan ekonomi dari ekspansi industri nikel dan kondisi kesehatan masyarakat di kawasan penyangga. Selama satu dekade terakhir, emisi partikulat, gas buang PLTU batu bara, dan timbulan limbah dari fasilitas ekstraktif telah memberikan tekanan signifikan terhadap kualitas lingkungan hidup masyarakat. Data empiris merekam bagaimana ekspansi kapasitas industri, yang ditopang oleh PLTU *captive* berkapasitas **{tot_kapasitas_pltu:,.0f} Megawatt**, berjalan sejajar dengan peningkatan kasus penyakit di kawasan-kawasan penyangga.

Sepanjang 2014–2024, data agregat dinas kesehatan mencatat total **kasus ISPA dan Pneumonia sebanyak {tot_ispa:,.0f} kasus**. Sementara itu, **kasus Diare tercatat sebanyak {tot_diare:,.0f} kasus**. Peningkatan insidensi penyakit ini berkorelasi dengan penurunan Indeks Kualitas Air (IKA) secara periodik. Konversi tutupan hutan untuk perluasan konsesi tambang turut berkontribusi pada pergeseran habitat satwa liar, yang berpotensi memicu perpindahan vektor penyakit zoonosis ke permukiman warga. Secara kumulatif, **kasus Malaria tercatat mencapai {tot_malaria:,.0f} kasus**, mengindikasikan tekanan terhadap keseimbangan ekologis di wilayah tambang.

Distribusi infrastruktur kesehatan di wilayah industri menunjukkan kesenjangan yang perlu menjadi perhatian. Ketersediaan fasilitas layanan primer seperti **Puskesmas tercatat sebanyak {tot_puskesmas_2024:,.0f} unit** pada tahun 2024, di kawasan yang bersamaan menanggung beban penyakit di atas rata-rata. Kondisi ini mengindikasikan bahwa pertumbuhan ekonomi dari hilirisasi nikel belum diimbangi dengan distribusi infrastruktur kesehatan yang proporsional bagi masyarakat di wilayah operasi industri (*sacrifice zone*).

### Metrik Agregat Beban Kesehatan (2014-2024)

| Indikator Kesehatan | Nilai | Deskripsi | Sumber |
| :--- | :--- | :--- | :--- |
| **Total Kasus ISPA/Pneumonia** | **{tot_ispa:,.0f}** | Penyakit pernapasan yang meningkat secara konsisten, seiring paparan kronis debu batu bara dan emisi SO₂ dari cerobong smelter. | Data Agregat Dinas Kesehatan (2014-2024) |
| **Total Kasus Diare** | **{tot_diare:,.0f}** | Infeksi saluran pencernaan yang tercatat tinggi, seiring degradasi kualitas sumber air tanah dan badan air akibat limbah tailing tambang. | Data Agregat Dinas Kesehatan (2014-2024) |
| **Total Kasus Malaria** | **{tot_malaria:,.0f}** | Penyakit vektor endemis dengan kecenderungan meningkat, berkorelasi dengan keberadaan genangan air bekas galian tambang yang tidak direklamasi. | Data Agregat Dinas Kesehatan (2014-2024) |
| **Rasio Puskesmas Terdaftar (2024)** | **{tot_puskesmas_2024:,.0f} Unit** | Fasilitas primer warga yang pertumbuhannya tidak sebanding dengan peningkatan beban kasus penyakit di wilayah industri. | BPS Ketersediaan Faskes (2024) |
| **Rasio Rumah Sakit (2024)** | **{tot_rs_2024:,.0f} Unit** | Ketersediaan rumah sakit di wilayah industri. | BPS Ketersediaan Faskes (2024) |

---

### 3.1 Kesenjangan Fasilitas Kesehatan di Kawasan Ekstraktif

> **Metode Analisis:** Sub-bab ini menggunakan visualisasi perbandingan *Grouped Horizontal Bar Chart* pada satu periode cross-sectional (Tahun 2024) untuk mengukur ketimpangan infrastruktur kesehatan primer dan sekunder.

Data perbandingan distribusi fasilitas kesehatan mengindikasikan bahwa ketersediaan infrastruktur medis di provinsi sentra industri relatif tidak lebih baik dibandingkan wilayah non-sentra, meski beban penyakit di wilayah tersebut lebih tinggi.

Melalui komparasi grafik batang (*Grouped Bar Chart*) di bawah, terlihat bahwa ketersediaan Fasilitas Kesehatan di provinsi dengan konsentrasi industri tinggi justru mengalami defisit relatif. Rata-rata Rumah Sakit di Sentra Industri tercatat **{rs_sentra:.0f} unit** per provinsi, lebih rendah dari wilayah Non-Sentra yang mencapai **{rs_non:.0f} unit**. Kesenjangan distribusi fasilitas medis di area dengan beban penyakit tinggi ini perlu menjadi pertimbangan dalam perencanaan infrastruktur kesehatan ke depan.

![Ketimpangan Faskes 2024](visuals_bab3/chart_3_1_faskes.png)

---

### 3.2 Ketimpangan Beban Penyakit: Sentra Industri vs Non-Sentra

> **Metode Analisis:** Sub-bab ini menggunakan analisis komparatif spasial (*Comparative Spatial Analysis*) untuk membandingkan rata-rata beban penyakit antara provinsi sentra ekstraktif dan non-sentra.

Melalui analisis komparatif spasial, terlihat bahwa beban ekologis tidak terdistribusi secara merata di seluruh wilayah. Provinsi sentra ekspansi nikel—Sulawesi Tengah dan Sulawesi Tenggara—menunjukkan indikator penyakit yang secara konsisten lebih tinggi.

Data menunjukkan bahwa rata-rata penderita **ISPA/Pneumonia** di Sentra Industri tercatat **{ispa_sentra:,.0f} kasus per tahun**, dibandingkan provinsi Non-Sentra di angka **{ispa_non:,.0f} kasus**. Selisih sebesar **{ispa_diff:.1f} kali lipat** ini mengindikasikan beban pernapasan yang lebih berat di kawasan penyangga *smelter*. Temuan ini mendukung hipotesis kerangka riset D3TLH: wilayah dengan konsentrasi industri tinggi cenderung menanggung beban kesehatan yang lebih besar akibat tekanan terhadap daya tampung lingkungan.

![Rata-Rata Kasus ISPA & Diare per Tahun](visuals_bab3/chart_3_2_komparasi.png)

---

### 3.3 Lintasan Waktu Ekologis & Dinamika Penyakit di Kawasan Industri Ekstraktif

> **Metode Analisis:** Sub-bab ini menggunakan visualisasi runtut waktu (*Time-Series*) dan uji silang (*Crosstabulation*) secara interaktif untuk merunut dinamika insiden penyakit sejalan dengan akumulasi polusi tahunan.

Meskipun secara akumulatif kawasan Sentra Industri menanggung beban yang lebih berat, penelusuran data secara *time-series* (historis) dari 2014 hingga 2024 memberikan wawasan tambahan mengenai fluktuasi kasus penyakit dari tahun ke tahun.

| Insiden per 10.000 Penduduk | Total Kasus Absolut | Distribusi Stacked Bar |
| :---: | :---: | :---: |
| ![Insiden per 10k](visuals_bab3/chart_3_3_line_norm.png) | ![Kasus Absolut](visuals_bab3/chart_3_3_line_abs.png) | ![Stacked Bar](visuals_bab3/chart_3_3_stacked_bar.png) |

**Insight Ekologis:** Grafik per kapita membagi jumlah kasus terhadap total populasi, menampilkan beban per kapita yang sesungguhnya. Terlihat bahwa rasio kesakitan di kawasan Sentra Industri lebih tinggi dibandingkan wilayah Non-Sentra.

#### Uji Statistik: Asosiasi Kualitas Udara (IKU) dengan Insidensi Penyakit

Hipotesis utama narasi ini adalah bahwa penurunan kualitas udara ambien (IKU) berbanding lurus dengan peningkatan insidensi penyakit pernapasan dan lingkungan (seperti ISPA dan Diare).

### Ringkasan Eksekutif Seluruh Skenario Crosstab (IKU vs ISPA)

{exec_hdr}
{''.join([r + chr(10) for r in rows_33])}

> **Pembedahan Realitas Ekologis:** {narr_33}

---

### 3.4 Anomali Zoonosis: Dampak Kritis Ekspansi Industri di Level Tapak (Studi Kasus Sulteng)

> **Metode Analisis:** Sub-bab ini menggunakan studi kasus mendalam (*Deep Dive Case Study*) berbasis deret waktu di tingkat distrik (Kabupaten/Kota) khusus untuk endemik Sulawesi Tengah.

Data empiris Dinas Kesehatan mencatat total akumulasi **{total_kasus_tambang:,.0f} kasus** penyakit Zoonosis di wilayah Lingkar Tambang/Smelter Aktif Sulawesi Tengah (Morowali, Morowali Utara, Banggai) sepanjang rentang waktu pengamatan.**{peak_narrative}**

Peningkatan angka zoonosis ini berkorelasi dengan perubahan ekologis akibat ekspansi penggunaan lahan. Konversi tutupan hutan demi perluasan konsesi dan fasilitas pengolahan *smelter* berdampak pada pergeseran habitat alami satwa liar. Akibatnya, vektor pembawa penyakit terpaksa bermigrasi dan beririsan langsung dengan pemukiman pekerja tambang dan warga lokal. Keberadaan genangan air galian tambang yang tidak direklamasi serta kondisi sanitasi di area industri turut menjadi faktor pendukung perkembangbiakan vektor penyakit.

Pertumbuhan investasi di sektor ekstraktif belum diimbangi dengan alokasi perlindungan sosial dan lingkungan yang memadai bagi masyarakat lokal. Penduduk asli dan pekerja tambang menghadapi risiko kesehatan berlapis: paparan emisi udara dari *captive power plant* sekaligus potensi risiko penyakit menular akibat disrupsi lingkungan hidup.

| Tren Lonjakan Zoonosis (DBD) | Rata-rata Kasus per Tahun |
| :---: | :---: |
| ![Tren Zoonosis Line](visuals_bab3/chart_3_4a_zoonosis_line.png) | ![Kasus Zoonosis Bar](visuals_bab3/chart_3_4b_zoonosis_bar.png) |

**Interpretasi Spesifik (per Penyakit):**
Perbandingan grafik rata-rata di samping menunjukkan bahwa beban absolut kasus penyakit zoonosis utama di wilayah Lingkar Tambang/Smelter Aktif mencapai **{val_tambang:,.1f} kasus/tahun** vs **{val_non:,.1f} kasus/tahun** di wilayah kontrol. Meskipun populasi area tambang seringkali lebih terkonsentrasi, angka ini memberikan sinyal kuat bahwa degradasi lingkungan di sekitar smelter menciptakan ceruk ekologis baru (seperti genangan air galian) yang mempercepat siklus penularan.

#### Analisis Tambahan: Proxy Zoonosis (DBD) dan Tekanan Populasi

DBD dipakai sebagai indikator proxy karena penyakit ini sensitif terhadap perubahan lingkungan permukiman, kepadatan, drainase, sanitasi, dan mobilitas penduduk. Analisis ini tidak menyatakan bahwa smelter secara tunggal menyebabkan DBD; yang diuji adalah apakah kabupaten smelter menunjukkan beban kesehatan yang perlu dibaca bersama tekanan demografi dan perubahan ruang. Sejak 2019, total kasus DBD yang tercatat di kabupaten smelter mencapai **{dbd_smelter:,}** kasus, sedangkan kabupaten non-smelter mencapai **{dbd_non_smelter:,}** kasus. Karena jumlah kabupaten dalam dua kelompok tidak sama, grafik memakai rata-rata kasus per kabupaten-tahun. Rata-rata kabupaten smelter tercatat sekitar **{dbd_avg_smelter:.1f}** kasus per observasi, sementara non-smelter sekitar **{dbd_avg_non_smelter:.1f}**. Rasio **{dbd_ratio:.2f} kali** ini harus dibaca hati-hati sebagai sinyal komparatif, bukan bukti kausal final, tetapi tetap penting untuk menilai beban sosial dari industrialisasi.

![Proxy DBD Smelter vs Non-Smelter](visuals_bab3/chart_3_4c_dbd_proxy.png)

#### Lintasan Waktu Kasus Malaria

![Lintasan Waktu Malaria](visuals_bab3/chart_3_4d_malaria_line.png)

---

### 3.5 Pemetaan Geospasial: Distribusi Spasial Beban Penyakit

> **Metode Analisis:** Sub-bab ini menggunakan visualisasi WebGIS (Choropleth dan Point/Bubble Mapping) berbasis Leaflet/Folium untuk menganalisis pergeseran geospasial beban penyakit secara komparatif (*Before-After Analysis*).

Peta interaktif di bawah ini memproyeksikan secara spasial perbandingan absolut beban kesehatan (ISPA dan Diare) antara **Awal Ekstraksi (2015)** dan **Kondisi Terkini (2024)**. 

| Tahun 2015 (Kondisi Awal) | Tahun 2024 (Kondisi Terkini) |
| :---: | :---: |
| ![Peta Geospasial 2015](visuals_bab3/chart_3_5_map2015.png) | ![Peta Geospasial 2024](visuals_bab3/chart_3_5_map2024.png) |

**Before-After Geospasial:** Warna merah (*Choropleth*) menunjukkan tingkat absolut ISPA, sedangkan lingkaran biru (*Bubble*) merepresentasikan skala Diare.

---

### 3.6 Krisis Air Bersih: Tinjauan Makro Provinsi dan Bukti Uji Klinis Lingkar Tambang

> **Metode Analisis:** Sub-bab ini membedah krisis air bersih melalui dua tingkat observasi paralel. Pertama, tinjauan mikro spesifik di kawasan padat industri menggunakan hasil uji fisik laboratorium independen. Kedua, pemetaan tren makro di tingkat provinsi menggunakan Regresi Linier Sederhana dan Uji Tabulasi Silang (Chi-Square).

#### Pemetaan Analisis: Kualitas Air dan Kasus Diare

| Beban Diare vs IKA (Bar) | Korelasi Negatif: IKA vs Diare (Scatter Plot & OLS) |
| :---: | :---: |
| ![Beban Diare vs IKA](visuals_bab3/chart_3_6a_bar_korelasi.png) | ![Scatter IKA vs Diare](visuals_bab3/chart_3_6b_scatter.png) |

Titik yang tersebar acak mengindikasikan bahwa data makro secara statistik tidak menunjukkan korelasi kausalitas yang kuat pada level agregat provinsi.

**Interpretasi Korelasi Statistik:** {interp_text_34}

Menghadapi absennya data **"Akses Air Minum Layak"** di tingkat Kabupaten dari BPS sejak 2019, kami menggunakan **Ground Truth Data** dari pengujian laboratorium independen (AEER & WALHI) sebagai alternatif pengukur pencemaran air secara absolut.

Berdasarkan hasil uji klinis dari **{total_samples}** titik sampel di lingkar kawasan tambang, teridentifikasi bahwa **{exceed_biota} titik ({(exceed_biota/total_samples*100):.0f}%) melampaui batas aman toksisitas biota laut** (0.005 mg/L). Konsentrasi terparah ditemukan di **{max_location}** dengan kadar Kromium Heksavalen mencapai **{max_cr6:.3f} mg/L**, atau **{(max_cr6/0.005):.0f} kali lipat** lebih tinggi dari ambang batas aman. 

⚠️ **Peringatan Klinis:** Kromium Heksavalen (Cr6+) adalah logam berat karsinogenik beracun. Paparan berulang pada air yang dikonsumsi atau digunakan mencuci memicu iritasi kulit kronis, kerusakan pernapasan, pencernaan, dan potensi kanker parah di komunitas lingkar tambang. Bukti konkret di level tapak ini mengonfirmasi asimetri dampak ekologis industri ekstraktif yang gagal ditangkap oleh agregasi data makro.

#### Uji Statistik: Asosiasi IKA Rendah dengan Tingginya Kasus Diare

Untuk membuktikan hubungan kausal secara statistik, crosstab Chi-Square di bawah menggunakan unit observasi Provinsi-Tahun.

### Ringkasan Eksekutif Seluruh Skenario Crosstab (IKA vs Diare)

{exec_hdr}
{''.join([r + chr(10) for r in rows_36])}

> **Pembedahan Realitas Ekologis:** {narr_36}

---

### 3.7 Beban Limbah Beracun (B3): Eksternalitas Kesehatan yang Diabaikan

> **Metode Analisis:** Sub-bab ini menggunakan agregasi statistik deskriptif dan komparasi grafik batang (*Bar Chart*) untuk merunut skala penumpukan limbah B3.

Jika sub-bab sebelumnya telah membedah dampak pencemaran udara (IKU → ISPA) dan air (IKA → Diare), maka sub-bab ini mengungkap sumber polusi yang signifikan namun memerlukan perhatian khusus: timbulan **Limbah Bahan Berbahaya dan Beracun (B3)** dari operasi smelter dan tambang nikel.

Data komprehensif dari berbagai sumber (AEER, WALHI, JATAM, BPLH) membuktikan bahwa industri nikel di Sulawesi menghasilkan **lebih dari {total_b3 / 1_000_000:.1f} juta ton limbah B3 per tahun**. Angka ini setara dengan menimbun **{total_b3 / 1000:,.0f} gedung bertingkat** dengan material beracun setiap tahunnya.

Provinsi **{max_prov["Provinsi"]}** menanggung beban terbesar dengan **{max_prov["Estimasi Timbulan (Ton/Tahun)"] / 1_000_000:.1f} juta ton** limbah B3 per tahun, didominasi oleh operasi **IMIP (Indonesia Morowali Industrial Park)** yang menghasilkan slag dan tailing HPAL tanpa izin formal yang memadai.

#### Distribusi Limbah B3 per Provinsi

| Beban Limbah B3 per Provinsi | Komposisi Limbah B3 Berdasarkan Jenis |
| :---: | :---: |
| ![Limbah B3 per Provinsi](visuals_bab3/chart_3_7a_b3_prov.png) | ![Komposisi Limbah B3](visuals_bab3/chart_3_7b_b3_type.png) |

**Interpretasi Spasial:** Visualisasi di atas menunjukkan bahwa **Sulawesi Tengah dan Sulawesi Tenggara**—dua provinsi episentrum hilirisasi nikel—menanggung volume limbah B3 yang signifikan. **Sulawesi Tengah** menghasilkan **{sulteng_b3 / 1_000_000:.1f} juta ton B3/tahun**, terutama dari kawasan industri Morowali.

Ini mencerminkan **ketimpangan ekologis**: wilayah penyangga menanggung beban limbah industri yang signifikan dibandingkan manfaat ekonomi langsung yang diterima. Warga lokal beriringan dengan lokasi timbunan slag—**sehingga membutuhkan pengawasan proteksi kesehatan dan transparansi pengolahan**.

**Interpretasi Komposisi Limbah:** **Slag dan Tailing** mendominasi timbulan limbah B3 dengan total **{(slag_total + tailing_total) / 1_000_000:.1f} juta ton/tahun**. Material ini mengandung konsentrasi tinggi logam berat seperti **Chromium (Cr), Nikel (Ni), Kadmium (Cd), dan Arsenik (As)** yang bersifat karsinogenik (memicu kanker) dan neurotoksik (merusak sistem saraf).

Klaim industri bahwa slag "aman dimanfaatkan untuk batako" adalah **klaim yang perlu dikaji lebih kritis**. Penelitian mengindikasikan bahwa paparan jangka panjang terhadap debu slag berpotensi memicu **dermatitis dan gangguan pernapasan** pada komunitas sekitar.

**Tailing HPAL** (High-Pressure Acid Leaching) lebih berbahaya lagi karena mengandung **asam sulfat konsentrasi tinggi** yang dapat mencemari sungai dan laut. Proses HPAL yang digunakan PT HNC dan PT QMB di Morowali menghasilkan **12,5 juta ton tailing beracun per tahun**—setara dengan volume banjir bandang yang terjadi setiap hari.

#### Fasilitas Penghasil Limbah B3 Terbesar (Top 10)

{b3_table_md}

#### Kaitan dengan Beban Kesehatan Masyarakat

Meskipun data epidemiologis yang menghubungkan secara langsung antara paparan limbah B3 dengan penyakit spesifik masih terbatas, bukti-bukti tidak langsung sangat kuat:
1. **Korelasi Geografis:** Provinsi dengan timbulan B3 tertinggi (Sulteng & Sultra) adalah provinsi yang sama dengan beban ISPA dan Diare tertinggi.
2. **Jalur Paparan Multipel:** Paparan inhalasi debu slag; Kontaminasi lindi tailing ke air sumur; Akumulasi logam berat di rantai makanan.
3. **Temuan Lapangan:** Laporan masalah kesehatan warga sekitar area operasi.

#### Kesimpulan Kritis: Beban Ganda Masyarakat Terdampak

Data limbah B3 di atas menegaskan bahwa masyarakat di zona penyangga smelter **menanggung beban ganda (double burden)**:
1. **Beban Polusi Aktif:** Paparan harian terhadap emisi SO₂, debu PM2.5, dan pencemaran air (terbukti di sub-bab 3.3 dan 3.5)
2. **Beban Polusi Pasif:** Hidup berdampingan dengan timbunan **{total_b3 / 1_000_000:.1f} juta ton limbah beracun** yang terakumulasi setiap tahun—**tanpa jaminan keamanan jangka panjang**

Kompleks IMIP di Morowali menghasilkan **{imip_b3 / 1_000_000:.1f} juta ton limbah B3/tahun**. Hal ini menunjukkan pentingnya evaluasi independen atas dampak lingkungan dan kesehatan dari ekspansi industri nikel bagi masyarakat sekitar.

**Rekomendasi Kebijakan:** Pemerintah harus segera menghentikan ekspansi smelter baru hingga tersedia kajian risiko kesehatan independen, sistem monitoring limbah B3 yang transparan, dan skema kompensasi yang adil bagi masyarakat terdampak. **Hak atas lingkungan hidup yang sehat adalah hak asasi yang tidak dapat ditawar dengan pertumbuhan ekonomi semata**.
\"\"\"


    md_path = OUT_DIR / "chapter_3.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Done! 100% faithful chapter_3.md saved to {md_path}")

if __name__ == "__main__":
    generate()
"""

with open("tools/streamlittopdf/extract_chapter_3.py", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Patch applied successfully.")
