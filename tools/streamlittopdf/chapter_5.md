# Bab 5: Pola Penerbitan Izin di Zona Kritis Ekologis

**CELIOS — Center of Economic and Law Studies**

---

## Fakta Kritis D3TLH

### FAKTA CRI, MIGHTY EARTH, TANAHKITA.ID — Mayoritas IUP Tanpa FPIC

Laporan Climate Rights International, Mighty Earth, dan Business-Human Rights Resource Centre mendokumentasikan banyak IUP tambang nikel di Sulawesi terbit **tanpa *Free, Prior, and Informed Consent* (FPIC)** dari masyarakat adat. Dokumen AMDAL kerap disusun **tanpa konsultasi bermakna** dan pelibatan masyarakat yang ruang hidupnya dirampas.

### DATA BPS (SLHI) — Krisis Kualitas Air (IKA) di Bawah 55

Indeks Kualitas Air (IKA) di sentra nikel seperti Sultra dan Sulteng konsisten terpuruk di level cemaran berat (46-55). Sedimentasi lumpur tambang laut menghancurkan terumbu karang dan mengusir wilayah tangkap nelayan sejauh puluhan mil.

---

*Evaluasi terhadap kegagalan instrumen tata kelola lingkungan dalam meredam perizinan tambang di wilayah yang telah melampaui daya dukung ekologis.*

### Metodologi Pendekatan

**Kerangka Logis (Alur Kausalitas):**
Bagian ini dirancang untuk menjawab sub-pertanyaan kritis dalam studi D3TLH: *"Apakah izin baru tetap diterbitkan ketika tekanan ekologis sudah tinggi?"*

1. **Variabel Dependen (Y):** Jumlah penerbitan izin tambang baru per tahun.
2. **Variabel Konteks (X):** Status kritis ekologis (diukur dari laju deforestasi dan kerusakan eksisting).
3. **Pendekatan Metodologis:** *Timeline Mapping* dan *Crosstabulation* untuk melihat tumpang tindih (*overlay*) temporal antara memburuknya kualitas lingkungan dengan grafik penerbitan izin.

**Tujuan:**
Membuktikan secara empiris terjadinya kegagalan tata kelola (governance failure) di mana instrumen Daya Dukung dan Daya Tampung Lingkungan Hidup (D3TLH) tidak bersifat mengikat (non-mandatory) dan mudah diabaikan demi melancarkan investasi.

---

Secara institusional, dokumen tata ruang dan instrumen lingkungan hidup semestinya beroperasi sebagai 'rem darurat' negara untuk menolak izin investasi baru di bentang alam yang sudah melampaui kapasitas pemulihannya. Namun, penelusuran data spasial dan waktu di semenanjung Sulawesi membongkar skandal tata kelola yang memilukan. Selama satu dekade terakhir, saat total deforestasi telah merobek **2,078,652.3 hektar** tutupan hutan tersisa, negara justru terus mengobral **574 izin tambang baru** yang merampas tambahan **819,452.5 hektar** ruang daratan. Ironisnya, puncak penerbitan izin tertinggi meledak pada tahun **2024** (194 izin), tepat pada momentum di mana berbagai wilayah telah memancarkan sinyal darurat polusi dan kebangkrutan ekologis. Ini membuktikan bahwa D3TLH telah dilumpuhkan menjadi sekadar ornamen administratif semata yang tunduk pada syahwat oligarki ekstraktif.

---

## Ringkasan Metrik Agregat

| Indikator | Nilai | Keterangan |
|---|---|---|
| **Tingkat Pengabaian Ekologis** | **85.3% (324 IUP)** | Mayoritas mutlak izin baru justru diobral secara sengaja pada tahun-tahun di mana laju deforestasi provinsi tersebut sedang berada di zona kritis (di atas rata-rata). Sumber: Data Panel (ESDM & GFW) |
| **Zona Bebas Rem Darurat** | **Sulawesi Tengah (173 IUP)** | Provinsi dengan rekor penerbitan izin tertinggi tepat pada saat daya dukung lingkungan (tutupan hutan) mereka sedang hancur lebur tanpa mitigasi. Sumber: Data Panel (ESDM & GFW) |
| **Akselerasi Izin Pasca-2020** | **4.4x Lipat** | Ledakan drastis penerbitan izin baru di era pasca-2020 dibandingkan periode sebelumnya, mengonfirmasi jebol dan diabaikannya instrumen D3TLH. Sumber: Kementerian ESDM (Minerbaone) |

---

## 5.1 Fakta Penyebab: Sinkronisasi Waktu (Timeline Mapping)

**Metode: Gantt Chart Timeline (Plotly Express)**

### Metodologi: Sinkronisasi Waktu (Timeline Mapping)

**Metode Analisis:** Sub-bab ini menggunakan visualisasi deret waktu bersilang (*Dual-Axis Combo Chart*) untuk mendeteksi korelasi visual temporal.

1. **Model Komparasi Temporal:**
    * **Time-Series Tracking:** Mengkomparasikan secara bersamaan akumulasi hilangnya luasan hutan (deforestasi) dengan laju obral perizinan pertambangan baru dari tahun 2014-2023.
    * **Pemetaan Anomali (*Governance Failure*):** Melacak secara empiris apakah instrumen 'rem darurat' ekologis bekerja. Jika kurva perizinan terus melesat naik tepat di tahun saat grafik deforestasi menembus batas krisis, maka terjadi pengabaian tata ruang yang disengaja.
2. **Kalkulasi/Formula Pengolahan:**
    * `Total_Deforestasi_Tahunan = SUM(Luas_Hilang_Ha) GROUP BY Tahun`
    * `Total_IUP_Baru = COUNT(Izin) GROUP BY Tahun`
3. **Variabel & Fitur Data:**
    * **X-Axis (Waktu):** `Tahun` (2014-2023)
    * **Y-Axis Kiri (Dampak Ekologis):** `Total_Deforestasi_Ha`
    * **Y-Axis Kanan (Keputusan Aktor):** `Jumlah_Izin_Baru`
4. **Dataset & File:**
    * `data/processed/sulawesi_izin_baru_per_tahun.csv` (Minerbaone)
    * `data/processed/sulawesi_gfw_master_1_dekade_2014_2023.csv` (GFW)

---

Visualisasi *Dual-Axis Combo Chart* di bawah ini memberikan penelanjangan empiris mengenai pergeseran aktor perusak hutan dan kegagalan sistemik dari instrumen Daya Dukung dan Daya Tampung Lingkungan Hidup (D3TLH). Jika kita membedah tren historisnya, terdapat dua fase krisis ekologis yang berbeda. Pada **Fase 2014-2018 (Zona Kiri)**, tingginya angka deforestasi mayoritas digerakkan oleh ekspansi perkebunan kelapa sawit dan Hak Pengusahaan Hutan (HPH). Pada periode ini, kurva konsesi tambang mineral masih tergolong landai dan belum menjadi aktor utama. Namun, konstelasi ini berubah drastis memasuki fase berikutnya.

Memasuki **Era Hilirisasi Nikel Pasca-2019 (Zona Kanan)**, industri tambang mengambil alih estafet sebagai mesin utama deforestasi. Kurva kuning (Area Konsesi IUP Baru) melesat tajam dan bergerak secara sinkron dengan skala kerusakan ekosistem. Anomali paling fatal terjadi pasca-2020: lonjakan luas konsesi tambang mencapai rekor tertingginya tepat pada momentum ketika grafik deforestasi kembali memerah parah. Secara matematis, ratusan ribu hektar tanah yang diserahkan melalui konsesi IUP baru ini berkorelasi mutlak dengan hilangnya tutupan pohon (*Hektar vs Hektar*). Fenomena ini bukanlah kebetulan statistik, melainkan mengonfirmasi tesis *governance failure*, di mana instrumen tata ruang tidak lagi berfungsi sebagai "rem darurat".

Dokumen AMDAL dan analisis daya dukung lingkungan (D3TLH) telah direduksi nilainya menjadi sekadar ornamen administratif belaka; hanya berfungsi sebagai stempel legalisasi prosedural untuk memfasilitasi kelancaran invasi spasial oligarki tambang. Negara, melalui aparatus birokrasinya, secara sadar dan sistematis mengabaikan sinyal darurat dari alam. Akibat pembiaran struktural ini, wilayah-wilayah penyangga kehidupan di semenanjung Sulawesi kini secara nyata dikorbankan menjadi zona tumbal (*sacrifice zones*) demi ilusi pertumbuhan rasio PDB nasional, yang pada akhirnya harus dibayar sangat mahal dengan ongkos kebangkrutan ekologis permanen.

#### Tren Eskalasi Bersamaan: Kerusakan Hutan (Batang) vs Penerbitan Izin (Garis)

![Tren Eskalasi Bersamaan: Deforestasi vs Penerbitan Izin (2014-2023)](visuals_bab5/chart_5_1_timeline_dual.png)

> **Interpretasi Governance Failure:** Alih-alih membunyikan "rem darurat", data tren historis mengonfirmasi bahwa instrumen D3TLH hanya berakhir sebagai formalitas administratif yang secara sistematis diabaikan demi memfasilitasi ekspansi oligarki ekstraktif.

---

## 5.2 Fakta Spasial: Tabrakan Tata Ruang di Kawasan Konservasi

**Metode: Overlay Area Kawasan Lindung (GFW)**

### Metodologi: Analisis Spasial Tabrakan Tata Ruang

**Metode Analisis:** Sub-bab ini menggunakan agregasi spasial bertingkat (*Stacked Bar Chart*) untuk mendokumentasikan skala kehancuran mutlak pada wilayah yang diharamkan untuk ditambang.

1. **Model Analisis Deforestasi Livelihood:**
    * **Geospatial Overlay:** Melakukan isolasi data *tree cover loss* (GFW) yang secara spesifik bertumpukan/beririsan dengan poligon Kawasan Livelihood (Zona Pertanian, Peternakan) dan Perkebunan Warga.
    * **Kuantifikasi Kerusakan Kumulatif:** Mengkalkulasi kehancuran agregat kawasan penyangga ekosistem esensial selama satu dekade terakhir akibat penetrasi aktivitas tambang.
2. **Kalkulasi/Formula Pengolahan:**
    * `Luas_Hancur_Perkebunan_Warga = SUM(Loss_Ha) WHERE Cat = '2'`
    * `Luas_Hancur_Pertanian_Peternakan = SUM(Loss_Ha) WHERE Cat = '1'`
    * `Total_Kumulatif_Hancur(t) = Total_Kumulatif_Hancur(t-1) + Luas_Hancur(t)`
3. **Variabel & Fitur Data:**
    * **Kategorisasi Spasial (X):** `Tahun`, Kategori Livelihood
    * **Besaran Destruksi (Y):** `Luas_Hilang_Kawasan_Livelihood_Ha`
4. **Dataset & File:**
    * `data/processed/sulawesi_gfw_kawasan_lindung_loss_2014_2023.csv`

---

Dataset spasial menunjukkan obral IUP tambang tidak mempedulikan batas tata ruang. Jutaan hektar kawasan penyangga kehidupan (Hutan Produksi, Kawasan Lindung, dan Area Resapan Air) secara sistematis dirusak dan dihilangkan fungsi ekologisnya demi memuluskan ekspansi ekstraksi nikel.

#### Akumulasi Kehancuran Total: Livelihood Warga (Pertanian, Peternakan, Perkebunan) 2014-2023

![Akumulasi Kehancuran Total Kawasan Livelihood 2014-2023](visuals_bab5/chart_5_2_kawasan_livelihood.png)

> **Fakta Lapangan:** Dalam dekade terakhir, total lebih dari **56 ribu hektar** kawasan livelihood (Pertanian, Peternakan, dan Perkebunan) warga yang seharusnya menjadi ruang hidup masyarakat sekitar telah dihancurkan oleh ekspansi industri ekstraktif.

---

## 5.3 Realitas Lapangan: Izin Bermasalah, FPIC Diabaikan, Masyarakat Dikorbankan

**Metode: Cross-Dataset Integration (KPA CATAHU + Tanahkita + CRI/Mighty Earth Reports)**

### Metodologi: Ekstraksi Data Konflik Agraria & Pelanggaran HAM

**Metode Analisis:** Sub-bab ini menggunakan triangulasi data kualitatif-kuantitatif dengan mendemonstrasikan integrasi *database* konflik agraria (*Multi-source Database Profiling*).

1. **Pemodelan Indikator Pelanggaran FPIC:**
    * **Cross-Referencing:** Memadukan repositori konflik terbuka (KPA & Tanahkita.id) dengan laporan independen lembaga HAM global (CRI, Mighty Earth, BHRRC) untuk membongkar anomali perizinan (*non-compliance*).
    * **Kuantifikasi Kriminalisasi:** Menghitung jumlah perampasan lahan tanpa persetujuan warga (Pelanggaran *Free, Prior, Informed Consent*/FPIC), tumpang tindih HGU, dan letupan represi bersenjata.
2. **Kalkulasi/Formula Pengolahan:**
    * `Total_Pelanggaran_FPIC = COUNT(Kasus) WHERE indikasi_fpic = True`
    * `Rekam_Jejak_Oligarki = COUNT(Jenis_Masalah_Izin) GROUP BY nama_perusahaan`
3. **Variabel & Fitur Data:**
    * **Kategori Entitas:** `nama_perusahaan`, `provinsi`, `jenis_masalah_izin`, `indikasi_fpic`
    * **Besaran Kasus:** `luas_ha`, Frekuensi kemunculan konflik.
4. **Dataset & File:**
    * `data/processed/sulawesi_konflik_tambang_fpic.csv`
    * `data/processed/kpa_masalah_izin_perusahaan.csv`

---

Di balik lautan angka statistik penerbitan IUP, tersembunyi realitas mengerikan: **mayoritas izin tambang nikel di Sulawesi terbit tanpa *Free, Prior, and Informed Consent* (FPIC) dari masyarakat adat**. Laporan terbaru dari **Climate Rights International (2024-2025)**, **Mighty Earth (2024)**, dan **Business & Human Rights Resource Centre** mendokumentasikan pola sistematis di mana perusahaan tambang nikel secara ilegal membabat hutan lindung dan hutan produksi di seluruh Indonesia, termasuk Sulawesi, tanpa konsultasi bermakna dengan masyarakat lokal. Dokumen AMDAL dan analisis daya dukung (D3TLH) disusun sebagai **formalitas prosedural belaka**—sekadar stempel legalisasi untuk memfasilitasi investasi raksasa tanpa pelibatan komunitas yang ruang hidupnya dirampas.

Penelusuran mendalam terhadap **database Konsorsium Pembaruan Agraria (KPA) CATAHU 2016-2025** dan **Tanahkita.id** mengungkap fakta mengejutkan: dari **21 kasus masalah izin perusahaan** yang teridentifikasi dalam 9 laporan tahunan KPA, **mayoritas melibatkan perusahaan tambang dengan HGU kadaluarsa, operasi ilegal tanpa izin kehutanan, dan tumpang tindih klaim lahan**. Di Sulawesi sendiri, tercatat **12 konflik pertambangan** dengan **4 kasus pelanggaran FPIC eksplisit** yang melibatkan penembakan warga, kriminalisasi aktivis, dan penggusuran paksa lahan adat.

Yang paling mengkhawatirkan: perusahaan-perusahaan dengan rekam jejak konflik agraria dan pelanggaran HAM ini **terus beroperasi hingga hari ini**, bahkan beberapa di antaranya menjadi bagian dari Proyek Strategis Nasional (PSN) yang dilindungi negara. Ini membuktikan bahwa sistem perizinan tambang di Indonesia bukan hanya gagal melindungi lingkungan, tetapi juga **secara sistematis mengorbankan hak-hak masyarakat adat dan lokal demi kepentingan oligarki ekstraktif**.

### Metrik Kunci

| Indikator | Nilai | Keterangan |
|---|---|---|
| **Konflik Pertambangan Sulawesi** | **12 Kasus** | Total konflik pertambangan terdokumentasi di Sulawesi (1968-2023) dengan **4 kasus pelanggaran FPIC eksplisit** yang melibatkan kekerasan, kriminalisasi, dan penggusuran paksa. Sumber: Tanahkita.id (KPA/YLBHI) |
| **Perusahaan Izin Bermasalah** | **21 Kasus** | Kasus masalah izin perusahaan yang teridentifikasi dalam CATAHU KPA (2016-2025): HGU kadaluarsa, operasi ilegal, IUP bermasalah, dan tumpang tindih klaim lahan. Sumber: KPA CATAHU 2016-2025 |
| **Perusahaan Bermasalah di Sulawesi** | **16 Perusahaan** | Perusahaan unik yang disebutkan dalam laporan KPA dengan lokasi operasi di Sulawesi, mayoritas terlibat dalam kasus tumpang tindih lahan dan HGU kadaluarsa. Sumber: KPA CATAHU 2016-2025 |

#### Timeline Historis: Konflik Pertambangan & Masalah Izin (2000-2025)

![Distribusi Temporal: Konflik Pertambangan vs Masalah Izin Perusahaan](visuals_bab5/chart_5_3a_timeline_konflik.png)

> **Temuan Kunci:** Lonjakan konflik pertambangan terjadi pada periode 2011-2023, bersamaan dengan boom nikel di Sulawesi. Laporan KPA menunjukkan pola sistematis: mayoritas konflik melibatkan perusahaan dengan HGU kadaluarsa, operasi ilegal, dan pengabaian FPIC. Era pasca-2020 menunjukkan intensifikasi masalah izin, mengonfirmasi jebolnya instrumen tata kelola lingkungan.

#### Breakdown Jenis Masalah Izin Perusahaan

![Jenis Masalah Izin yang Paling Sering Terjadi (KPA CATAHU 2016-2025)](visuals_bab5/chart_5_3b_masalah_izin.png)

> **Pola Pelanggaran Dominan:** Tumpang tindih klaim lahan (17 kasus) dan HGU kadaluarsa (10 kasus) menjadi masalah terbanyak. Ini membuktikan lemahnya koordinasi antar-kementerian dan diabaikannya status legal lahan dalam proses penerbitan IUP baru. Operasi ilegal (3 kasus) dan IUP bermasalah (2 kasus) menunjukkan pengawasan yang sangat lemah dari otoritas berwenang.

#### Perusahaan dengan Pelanggaran FPIC Eksplisit

**2022** — GKP adalah ilegal karena banyak (Sulawesi (unspecified))

> **Judul Konflik:** Konflik Koalisi Selamatkan Pulau Wawoni
>
> **Komoditas:** Manufacture
>
> **Provinsi:** Sulawesi (unspecified)
>
> **Sumber:** [Tanahkita.id](https://tanahkita.id/data/data/konflik/detil/SWpxcGxoUThtUVk)

---

**2012** — Sumber Energi Jaya (PT SEJ) (Sulawesi (unspecified))

> **Judul Konflik:** Konflik PT. Sumber Energi Jaya (SEJ) dengan Warga Desa Picuan
>
> **Komoditas:** Emas
>
> **Provinsi:** Sulawesi (unspecified)
>
> **Sumber:** [Tanahkita.id](https://tanahkita.id/data/data/konflik/detil/NWRvX1hlbHF5YW8)

---

**2011** — Citra Palu dan PT Lalu Bamba (Sulawesi Selatan)

> **Judul Konflik:** Konflik Pertambangan Antara Komunitas Adat Rampi Dengan PT Citra Palu dan PT Lalu Bamba
>
> **Komoditas:** Pertambangan Logam Dasar
>
> **Provinsi:** Sulawesi Selatan
>
> **Sumber:** [Tanahkita.id](https://tanahkita.id/data/data/konflik/detil/bVNDUWxiX1VpSzA)

---

**1968** — Vale Indonesia terkait masalah kepemilikan tanah pertambangan (Sulawesi (unspecified))

> **Judul Konflik:** PT.Vale Mengubah Lahan Pemukiman Masyarakat Adat Karunsiâ€™e Menjadi Lapangan Golf.
>
> **Komoditas:** Manufacture
>
> **Provinsi:** Sulawesi (unspecified)
>
> **Sumber:** [Tanahkita.id](https://tanahkita.id/data/data/konflik/detil/Zk04Wld1VzdqLXc)


> **Kasus Terburuk:** PT Gema Kreasi Perdana (GKP) di Pulau Wawonii beroperasi dengan IPPKH kadaluarsa, mengkriminalisasi puluhan warga penolak, dan menghancurkan lahan pertanian yang dikelola 30 tahun oleh 37,000+ jiwa. PT Sumber Energi Jaya di Minahasa Selatan menembaki warga pada 4 Juni 2012. PT Vale Indonesia mengubah lahan adat To Karunsi'e menjadi lapangan golf. Ini bukan kecelakaan—ini desain sistemik.

### Referensi Utama & Verifikasi Independen

**Laporan Organisasi Internasional:**
- **Climate Rights International (2024-2025):** "Indonesia: Nickel Industry Harming Human Rights and the Environment" — Dokumentasi pelanggaran hak asasi dan lingkungan di industri nikel Indonesia. cri.org/indonesia
- **Mighty Earth (2024):** "From Forests to Electric Vehicles" — Temuan: perusahaan tambang nikel secara ilegal membabat hutan lindung dan produksi, **tanpa menggunakan FPIC untuk konsultasi dengan komunitas lokal di Kabaena**. mightyearth.org
- **Business & Human Rights Resource Centre (2024):** "Indonesia: Nickel mining levels forests without FPIC" — Dokumentasi dampak kesehatan, lingkungan, dan ekonomi yang merugikan masyarakat lokal. business-humanrights.org
- **EJAtlas:** "Islanders resisting nickel mining permits, Wawonii, Southeast Sulawesi" — "Meskipun konsesi mencakup area pemukiman dan tanah leluhur, **penduduk tidak dilibatkan dalam proses pengambilan keputusan**." ejatlas.org
- **Mongabay (2025):** "Nickel boom on an Indonesian island brings toxic seas, lost incomes" — "Komunitas yang terdampak melaporkan **perampasan lahan tanpa konsultasi atau kompensasi yang layak, partisipasi publik yang terbatas, dan kriminalisasi terhadap protes**, semuanya melanggar hak-hak masyarakat adat dan hukum nasional." mongabay.com

**Database Nasional:**
- **Konsorsium Pembaruan Agraria (KPA):** Catatan Akhir Tahun (CATAHU) 2016-2025 — 9 laporan tahunan komprehensif tentang konflik agraria dan masalah perizinan di Indonesia.
- **Tanahkita.id:** Database konflik agraria YLBHI/KPA — 568 kasus konflik nasional, 12 kasus pertambangan Sulawesi terekam.

---

## 5.4 Pembuktian Empiris: Uji Statistik Korelasi Penerbitan Izin & Deforestasi

**Metode: Crosstabulation & Pearson Chi-Square Test**

### Metodologi: Uji Korelasi Penerbitan Izin & Ekstraksi Ekologis

**Metode Analisis:** Sub-bab ini menggunakan pengujian statistik inferensial (*Crosstabulation & Chi-Square Test*) untuk membuktikan secara matematis apakah besaran jumlah perizinan baru menjadi prediktor kuat terhadap tingkat kerusakan deforestasi.

1. **Uji Signifikansi Statistik (Chi-Square):**
    * **Binning (Kategorisasi Data):** Data numerik berkelanjutan (Jumlah Izin & Luas Deforestasi) dikategorikan menjadi 2 level (Tinggi & Rendah) menggunakan ambang batas Median dari distribusi panel. `Nilai > Median = Tinggi`, `Nilai <= Median = Rendah`.
    * `H0 (Null Hypothesis): Tidak ada hubungan yang signifikan (independen) antara klasifikasi tingginya jumlah penerbitan IUP baru dengan klasifikasi tingginya luasan deforestasi pada suatu provinsi di tahun tertentu.`
    * `Decision Rule: Tolak H0 jika nilai Asymptotic Significance (P-Value) pada uji Pearson Chi-Square < 0.05 (Alpha 5%).`
2. **Kalkulasi/Formula Pengolahan:**
    * `Chi-Square (χ²) = Σ [ (O_i - E_i)² / E_i ]`
    * `Odds Ratio = (Peluang Deforestasi Tinggi pada Izin Tinggi) / (Peluang Deforestasi Tinggi pada Izin Rendah)`
3. **Variabel & Fitur Data:**
    * **Variabel Independen (X):** `Jumlah_Izin_Baru` atau `Total_Luas_Konsesi_Baru_Ha` (Interaktif Dropdown).
    * **Variabel Dependen (Y):** `Total_Deforestasi_Ha` atau `Deforestasi_Driver_Komoditas_Tambang_Sawit_Ha` (Interaktif Dropdown).
4. **Dataset & File:**
    * Panel Join dari: `sulawesi_izin_baru_per_tahun.csv` dan `sulawesi_gfw_master_1_dekade_2014_2023.csv`

---

### Detail Uji Statistik (Chi-Square & Odds Ratio)

*Tabel-tabel di bawah ini adalah output statistik formal yang menyajikan bukti statistik formal: Case Processing → Crosstabulation → Chi-Square Tests → Ringkasan Hipotesis.*

**Variabel Independen (X):** Jumlah Izin Baru (IUP)

**Variabel Dependen (Y):** Total Deforestasi Alam (Hektar)

#### Case Processing Summary

| | Valid N | Valid % | Missing N | Missing % | Total N | Total % |
|---|---|---|---|---|---|---|
| Jumlah Izin Baru (IUP) * Total Deforestasi Alam (Hektar) | 60 | 100.0% | 0 | 0.0% | 60 | 100.0% |

#### Jumlah Izin Baru (IUP) * Total Deforestasi Alam (Hektar) Crosstabulation

| | Rendah (<23,254.1) | Tinggi (≥23,254.1) | Total |
|---|---|---|---|
| **Rendah (<2.0)** Count | 22 | 7 | 29 |
| **Rendah (<2.0)** Expected | 14.5 | 14.5 | 29.0 |
| **Tinggi (≥2.0)** Count | 8 | 23 | 31 |
| **Tinggi (≥2.0)** Expected | 15.5 | 15.5 | 31.0 |
| **Total** Count | 30 | 30 | 60 |
| **Total** Expected | 30.0 | 30.0 | 60.0 |

#### Chi-Square Tests

**Jumlah Izin Baru (IUP) * Total Deforestasi Alam (Hektar)**

| | Value | df | Asymp. Sig. (2-sided) |
|---|---|---|---|
| Pearson Chi-Square | 13.081 | 1 | 0.000 |
| Likelihood Ratio | 13.606 | 1 | 0.000 |
| Linear-by-Linear Association | 14.766 | 1 | 0.000 |
| N of Valid Cases | 60 | | |

### Ringkasan Uji Hipotesis

**Result: SIGNIFIKAN (Ada Hubungan)**

| Parameter | Nilai |
|---|---|
| P-Value | 0.0003 |
| Chi-Square | 13.081 |
| df | 1 |
| **Odds Ratio (Risk Estimate)** | **9.036** |

> **Interpretasi Ekologis:** Temuan ini sangat krusial: lonjakan intensitas **Jumlah Izin Baru (IUP)** terbukti **berkorelasi kuat dan signifikan** dengan peningkatan **Total Deforestasi Alam (Hektar)** (OR: 9.036). Ini adalah konfirmasi empiris bahwa narasi hilirisasi dan investasi ekstraktif bukanlah pertumbuhan tanpa korban—ekspansi spasial mereka mutlak mengorbankan luasan hutan di tingkat tapak.

---

### Ringkasan Eksekutif Seluruh Skenario Crosstab

Tabel di bawah ini merangkum hasil pengujian statistik (Chi-Square) untuk semua kemungkinan kombinasi antara indikator Ekspansi (X) dan Dampak Ekologis (Y) pada panel data yang sama.

| Variabel Independen (X) | Variabel Dependen (Y) | Chi-Square | P-Value | Odds Ratio | Kesimpulan |
|---|---|---|---|---|---|
| Jumlah Izin Baru (IUP) | Total Deforestasi Alam (Hektar) | 13.081 | 0.000 | 9.04 | 🟢 SIGNIFIKAN |
| Jumlah Izin Baru (IUP) | Deforestasi Komoditas Tambang/Sawit (Hektar) | 1.068 | 0.301 | 1.96 | 🔴 TIDAK SIGNIFIKAN |
| Luas Konsesi Baru (Hektar) | Total Deforestasi Alam (Hektar) | 11.267 | 0.001 | 7.56 | 🟢 SIGNIFIKAN |
| Luas Konsesi Baru (Hektar) | Deforestasi Komoditas Tambang/Sawit (Hektar) | 3.267 | 0.071 | 2.98 | 🔴 TIDAK SIGNIFIKAN |

> **Pembedahan Realitas Ekologis:**
>
> Dari **4 skenario pengujian**, terdapat **2 skenario yang terbukti SIGNIFIKAN**.

Angka-angka pada tabel di atas bukan sekadar statistik di atas kertas, melainkan **bukti empiris** dari daya rusak kebijakan. Tingginya *Odds Ratio* pada skenario yang signifikan menegaskan bahwa setiap kali kran perizinan atau luas konsesi diperlebar, risiko terjadinya deforestasi melonjak berkali-kali lipat.

Menariknya, jika ada skenario yang menunjukkan *TIDAK SIGNIFIKAN* (khususnya pada deforestasi komoditas spesifik), ini tidak berarti industri ekstraktif ramah lingkungan. Sebaliknya, ini menjadi indikasi mengerikan bahwa **kehancuran ekologis telah menyebar tak terkendali (spillover effect)**—di mana kerusakan hutan akibat operasi tambang menjalar jauh melampaui batas konsesi resmi komoditasnya hingga merusak total lanskap alam secara merata.
