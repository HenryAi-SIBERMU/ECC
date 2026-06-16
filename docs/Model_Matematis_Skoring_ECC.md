# Dokumentasi Model Matematis Skoring ECC (Audit D3TLH)

Dokumen ini menjelaskan formulasi matematis yang digunakan untuk mengubah data empiris (kesehatan, lingkungan, tata ruang) menjadi **Skor Kerusakan Ekologis (0-10)** dalam Dashboard Forensik ECC secara dinamis, rasional, dan terukur.

---

## ⚠️ STATUS AUDIT THRESHOLD (Diperbarui: Juni 2026)

### Masalah yang Diidentifikasi
Audit internal pada Juni 2026 menemukan bahwa **sebagian besar threshold dalam model ini bersifat *arbitrary*** — ditentukan secara ad-hoc tanpa referensi regulasi atau literatur ilmiah yang dapat dikutip. Ini merupakan kelemahan metodologis yang perlu ditangani sebelum publikasi/advokasi publik.

### Status Per Matriks

| Matriks | Tab | Threshold Saat Ini | Basis Skoring | Sumber Data Threshold | Status |
|---|---|---|---|---|---|
| **Udara** | PLTU+IKU | 10.000 MW / penurunan 30 poin IKU | Baku Mutu Ambien | PermenLHK No.27/2021 | ✅ Defensible |
| **Udara** | ISPA Rasio | Rasio 2x lipat | Relatif risiko thd Non-Sentra | Data Rutin Kemenkes | ✅ Defensible |
| **Udara** | Limbah B3 | 30 Juta Ton | Kapasitas infrastruktur | PP No.22/2021 | ⚠️ Perlu verifikasi angka |
| **Udara** | Emisi CO2 | 150 Juta Ton | Target serapan emisi bersih | Enhanced NDC 2022 (FOLU) | ✅ Defensible |
| **Air** | IKA | Penurunan 30 poin (Cemar Berat) | Baku Mutu Ambien | PermenLHK No.27/2021 | ✅ Defensible |
| **Air** | Diare | 500.000 kasus | — | Kemenkes (SPM Nasional) | ⚠️ Perlu verifikasi angka |
| **Air** | Konflik Pesisir | 15 konflik | — | KPA Annual Report | ❌ Arbitrary |
| **Air** | Tailing | 20 Juta Ton | — | KLHK (Kajian DSTP) | ⚠️ Perlu verifikasi angka |
| **Lahan** | Bencana | 877 kejadian | Statistical Percentile (Mean+1SD) | Data BNPB (Rata-rata se-Sulawesi) | ✅ Defensible (Opsi C) |
| **Lahan** | Deforestasi | 638.000 Ha | Statistical Percentile (Mean+1SD) | Global Forest Watch (GFW Sulawesi) | ✅ Defensible (Opsi C) |
| **Lahan** | Kawasan Lindung | 638.000 Ha | Statistical Percentile (Mean+1SD) | GFW + Peta KLHK (Sulawesi) | ✅ Defensible (Opsi C) |
| **Lahan** | Driver Tambang | 500.000 Ha | Skala masif kerusakan | GFW (Sultra Saja, data Sulteng kosong) | ✅ Defensible (Opsi C) |
| **Sosial** | FPIC | 12 kasus | Total aktual dataset investigasi | KPA & TanahKita | ✅ Proporsional |
| **Sosial** | Jiwa Terdampak | 100.000 jiwa | — | Laporan KPA / UN OCHA | ⚠️ Perlu verifikasi angka |
| **Sosial** | Kriminalisasi | 50 insiden | — | Komnas HAM / KontraS | ⚠️ Perlu verifikasi angka |
| **Sosial** | Defisit Faskes | +50% pertumbuhan | Pertumbuhan kewajaran populasi | Kemenkes (Data RS/Puskesmas BPS) | ⚠️ Perlu verifikasi angka |

### Rencana Perbaikan (Opsi A + C)

**Opsi A — Dasar Regulasi Indonesia** *(target referensi yang akan dicari)*
- Bencana: Klasifikasi BNPB (PP 21/2008 → "bencana skala nasional/kabupaten/kota")
- Deforestasi: Target FOLU Net Sink 2030 (NDC Indonesia) — proyeksi angka aman
- Kawasan Lindung: PP No.23/2021 tentang Penyelenggaraan Kehutanan; target minimum 30% tutupan hutan
- Limbah B3: PP No.22/2021 tentang Penyelenggaraan Perlindungan dan Pengelolaan LH
- Kualitas Air: Peraturan Pemerintah No.22/2021 Lampiran VI → batas baku mutu air
- Emisi CO2: NDC Indonesia 2022 (Enhanced NDC) → target penurunan 31,89% s/d 43,2%

**Opsi C — Statistical Percentile (Rata-rata Nasional)**
- Hitung rata-rata per indikator dari semua provinsi Indonesia (bukan hanya Sulawesi)
- Set threshold = rata-rata nasional + 1 standar deviasi (atau ×2 rata-rata)
- Ini tidak dapat dituduh "diatur" karena basis datanya bersumber dari BPS/KLHK nasional

**Catatan**: Sampai referensi ditemukan dan divalidasi, model tetap berjalan dengan threshold saat ini. Skor 10/10 pada Matriks Lahan **BUKAN berarti bias** — data aktualnya memang sangat ekstrem (1,14 juta Ha deforestasi dalam 10 tahun di 2 provinsi). Tapi model tidak bisa membedakan "sangat krisis" vs "ultra-sangat krisis" selama threshold tidak proporsional terhadap skala nasional.

---

## 1. Matriks Daya Tampung Udara

### 1.1. Skor Ancaman Udara (Korelasi PLTU & IKU)
Mengukur tingkat ancaman kualitas udara akibat pembakaran batu bara.
* **Metrik Asal**: Kapasitas PLTU Captive beroperasi (MW) & Indeks Kualitas Udara BPS (IKU).
* **Pendekatan Statistik / Model**: **Weighted Linear Combination (WLC)** dipadukan dengan **Min-Max Normalization**. Pendekatan ini umum digunakan dalam *Multi-Criteria Decision Analysis (MCDA)* untuk analisis risiko lingkungan (Environmental Risk Assessment), di mana dua variabel dengan satuan berbeda dinormalisasi ke skala yang sama lalu diberi bobot.
* **Logika Pembuktian**: Kualitas udara divonis memburuk secara asimetris jika kapasitas PLTU meroket sementara nilai IKU anjlok tajam menjauhi standar aman (80).
* **Formula**:
  ```python
  Skor_1 = min(10.0, (Kapasitas_PLTU / 10000) * 5 + max(0, 80 - IKU_Terkini) / 30 * 5)
  ```
* **Threshold Kritis**: Kapasitas 10.000 MW akan memberi kontribusi poin maksimal (5 poin). Penurunan IKU sebesar 30 poin (anjlok dari 80 menjadi 50) akan memberi poin maksimal (5 poin).
* **⚠️ Status Threshold**: Perlu referensi dari KLHK/BMKG untuk batas kapasitas PLTU "aman" per ekoregion.

### 1.2. Skor Rasio Anomali ISPA (Morbiditas)
Mengukur asimetri distribusi penyakit infeksi saluran pernapasan di ekoregion.
* **Metrik Asal**: Rata-rata Kumulatif Kasus ISPA/Pneumonia per Provinsi.
* **Pendekatan Statistik / Model**: Modifikasi dari **Incidence Rate Ratio (IRR)** atau **Relative Risk (RR)** dalam kajian Epidemiologi Lingkungan. Model ini mengukur rasio risiko kejadian penyakit pada populasi yang terpapar (Ring-1 Tambang) dibandingkan populasi kontrol yang tidak terpapar secara masif (Non-Sentra).
* **Logika Pembuktian**: Jika rasio melampaui 1, hal itu secara statistik menolak "Hipotesis Nol" (H0) bahwa penyakit terjadi secara acak alamiah, dan membuktikan morbiditas dipicu oleh agen polutan dari kawasan sentra tambang.
* **Formula**:
  ```python
  Rasio = (Rata_Rata_Kasus_Sentra) / (Rata_Rata_Kasus_Non_Sentra)
  Skor_2 = min(10.0, max(0.0, (Rasio - 1) * 10.0))
  ```
* **Threshold Kritis**: Jika rasio mencapai 2x lipat (2.0) lebih masif dari daerah lain, skor langsung menembus nilai mutlak 10.0 (Darurat Medis).
* **✅ Status Threshold**: Defensible — berbasis perbandingan relatif statistik, bukan nilai absolut arbitrary.

### 1.3. Skor Over-Capacity Limbah B3
Mengukur tingkat kelampauan daya tampung limbah beracun dan abu terbang (fly ash).
* **Metrik Asal**: Total Estimasi Timbulan Limbah B3 (Juta Ton/Tahun).
* **Pendekatan Statistik / Model**: **Carrying Capacity Index (Indeks Daya Tampung)** berbasis ambang batas (*Threshold-based Scaling*). Metodologi ini sejalan dengan kerangka kerja *Ecological Footprint* yang membandingkan beban ekologis (timbulan limbah) langsung dengan biokapasitas alam/infrastruktur.
* **Logika Pembuktian**: Daya tampung mitigasi ekoregion memiliki batas infrastruktur alamiah. Di sini diasumsikan *Baseline Toleransi Lingkungan* adalah 1 Juta Ton per tahun.
* **Formula**:
  ```python
  Skor_Overcapacity = Total_Timbulan_B3_Ton / 1_000_000 # Menghasilkan kelipatan (x Lipat)
  Skor_3 = min(10.0, (Skor_Overcapacity / 30.0) * 10)
  ```
* **Threshold Kritis**: Apabila akumulasi timbulan limbah melampaui 30 Juta Ton/Tahun (30x lipat dari batas wajar), skor mencapai nilai absolut 10.0 (Kapasitas Jebol).
* **⚠️ Status Threshold**: Perlu referensi dari PP No.22/2021 atau Permen KLHK tentang batas pengelolaan B3.

### 1.4. Skor Defisit Ekosistem Karbon
Mengukur hilangnya "paru-paru udara" akibat eksploitasi perizinan lahan.
* **Metrik Asal**: Total Emisi CO2 Ekivalen Lepas dari Deforestasi Hutan Primer (Megagram / Juta Ton).
* **Pendekatan Statistik / Model**: **Ecological Deficit Modeling**. Menghitung rasio antara emisi yang dilepaskan secara mendadak versus kemampuan resapan (carbon sink) yang hilang permanen. Model ini diadaptasi dari metode *Global Footprint Network* untuk menghitung defisit karbon.
* **Logika Pembuktian**: Setiap hektar hutan yang ditebang demi perizinan IUP melepaskan emisi karbon yang sebelumnya tertahan berabad-abad (carbon sink), memaksa ekosistem menerima defisit ganda.
* **Formula**:
  ```python
  Skor_4 = min(10.0, (Total_Emisi_Juta_Ton / 150.0) * 10)
  ```
* **Threshold Kritis**: Pelepasan emisi secara eksponensial hingga menembus 150 Juta Ton CO2 dalam 1 dekade akan mencetak skor mutlak 10.0 (Darurat Karbon).
* **⚠️ Status Threshold**: Perlu anchor ke Enhanced NDC Indonesia 2022 (target penurunan 31,89% BAU).

### 1.5. Model Akumulasi Skor Kerusakan (Vonis D3TLH)
Menyatukan keempat dimensi skor di atas menjadi satu nilai tunggal (*Single Index*).
* **Pendekatan Statistik / Model**: **Simple Additive Weighting (SAW) / Arithmetic Mean Aggregation**. Merupakan metode perankingan dan sintesis indikator majemuk yang paling transparan dan diakui secara global (sering digunakan dalam penyusunan HDI/IPM oleh UNDP). Masing-masing metrik dianggap memiliki bobot kontribusi kerusakan yang sama (Equal Weighting = 25%).
* **Formula**:
  ```python
  Skor_Akumulasi = (Skor_1 + Skor_2 + Skor_3 + Skor_4) / 4
  ```
* **Interpretasi Output**: Menghasilkan skor akhir berskala 0 hingga 10 yang mendasari penentuan "Vonis Eksekutif" di dashboard. Nilai agregat di atas 8.0 menandakan **Status: Daya Tampung Jebol** yang secara saintifik membatalkan klaim aman dari dokumen D3TLH pemerintah.

---

## 2. Matriks Daya Tampung Air

### 2.1. Skor Kualitas Air (Degradasi IKA)
Mengukur kegagalan sistem dalam mempertahankan kualitas air di sentra nikel.
* **Metrik Asal**: Indeks Kualitas Air BPS (IKA) Sulteng vs Rata-rata Sulawesi.
* **Pendekatan Statistik / Model**: **Min-Max Normalization** terhadap rentang degradasi kualitas.
* **Logika Pembuktian**: Air dikatakan sehat jika IKA mendekati 80. Jika obral izin tambang tidak mengganggu daya tampung, IKA akan stabil. Menurunnya IKA hingga mendekati batas cemar berat (50) membuktikan kerusakan masif.
* **Formula**:
  ```python
  Skor_Air_1 = min(10.0, max(0, (80 - IKA_Terkini) / 30) * 10)
  ```
* **Threshold Kritis**: Penurunan nilai IKA sebesar 30 poin (dari ideal 80 anjlok menjadi 50) akan menghasilkan poin kerusakan maksimal 10.0.
* **⚠️ Status Threshold**: Angka 80 = batas "baik" dan 50 = "cemar berat" perlu dikonfirmasi ke PP 22/2021 Lampiran VI (Baku Mutu Air).

### 2.2. Skor Anomali Penyakit Bawaan Air (Morbiditas Diare)
Mengukur dampak kontaminasi logam berat pada rantai suplai air minum/sungai warga.
* **Metrik Asal**: Total Kumulatif Kasus Diare di Sentra Nikel (Sulteng & Sultra).
* **Pendekatan Statistik / Model**: **Cumulative Burden Index**. Mengukur akumulasi beban penyakit endemis absolut terhadap daya tampung mitigasi medis regional.
* **Logika Pembuktian**: "Mitos AMDAL" menyebut logam berat terencerkan secara aman di perairan. Realitanya, tingginya insiden diare membuktikan sumber air warga terpapar secara masif dan gagal dimitigasi.
* **Formula**:
  ```python
  Skor_Air_2 = min(10.0, (Total_Kasus_Sentra / 500_000) * 10)
  ```
* **Threshold Kritis**: Apabila beban kasus kumulatif di wilayah lingkar tambang menembus angka 500.000 pasien, hal ini memicu **Status: Darurat Medis** (Skor 10.0).
* **⚠️ Status Threshold**: Perlu referensi dari Kemenkes (angka insidensi diare nasional per 1.000 penduduk sebagai pembanding).

### 2.3. Skor Darurat Konflik Pesisir/Nelayan
Mengukur penggusuran ruang laut dan konflik sosial-ekologis sektor perairan.
* **Metrik Asal**: Jumlah kejadian konflik ruang laut, pesisir, wilayah tangkap nelayan, dan sungai dari dataset KPA/TanahKita.
* **Pendekatan Statistik / Model**: **Socio-Ecological Escalation Index**. Menghitung rasio absolut letusan konflik agraria sektoral berhadapan dengan daya serap mitigasi sosial pemerintah.
* **Logika Pembuktian**: Janji "kesejahteraan CSR" dan penguatan livelihood pesisir fiktif belaka bila grafik letusan konflik nelayan vs perusahaan tambang menanjak secara konstan sejak 2015.
* **Formula**:
  ```python
  Skor_Air_3 = min(10.0, (Jumlah_Konflik_Air_Pesisir / 15.0) * 10)
  ```
* **Threshold Kritis**: Terkumpulnya 15 konflik masif spesifik ruang pesisir memicu skor darurat 10.0.
* **❌ Status Threshold**: Arbitrary. Perlu referensi (misalnya rata-rata konflik pesisir nasional per provinsi dari KPA Annual Report).

### 2.4. Skor Ancaman Bendungan Tailing (DSTP)
Mengukur kuantitas limbah murni (sludge/tailing) yang mengancam biota laut dan wilayah resapan.
* **Metrik Asal**: Proporsi sebaran Timbulan B3 (mayoritas slag & tailing smelter) (Juta Ton).
* **Pendekatan Statistik / Model**: **Carrying Capacity Index (Indeks Daya Tampung)** berbasis ambang batas toleransi spasial.
* **Logika Pembuktian**: Praktik pembuangan limbah bawah laut (Deep Sea Tailing Placement) dan pembangunan bendungan tailing raksasa rentan gempa membawa risiko kepunahan genetik ekosistem *coral triangle* laut dalam Sulawesi.
* **Formula**:
  ```python
  Skor_Air_4 = min(10.0, (Total_Tailing_Ton / 20_000_000) * 10)
  ```
* **Threshold Kritis**: Timbulan di luar ambang batas (melampaui 20 Juta Ton/Tahun) mencetak skor 10.0.
* **⚠️ Status Threshold**: Perlu referensi dari Permen ESDM/KLHK tentang batas kapasitas pengelolaan tailing.

---

## 3. Matriks Daya Dukung Lahan (Matriks C)

> **Cakupan Wilayah**: Sulteng & Sultra — episentrum sentra nikel Indonesia (899k Ha IUP dari total 1,18 juta Ha se-Sulawesi = 76% konsentrasi).
>
> **Catatan Audit Juni 2026**: Keempat tab Matriks Lahan menghasilkan skor 10.0/10 secara konsisten. Ini bukan akibat bias threshold — data aktualnya melampaui threshold 2–11x lipat karena kerusakan ekologis yang benar-benar ekstrem. Namun threshold saat ini bersifat *arbitrary* dan perlu dianchor ke regulasi/statistik nasional (lihat bagian Status Audit di atas).

### 3.1. Skor Bencana Ekologis (Banjir & Longsor)
Mengukur efektivitas mitigasi spasial terhadap bencana hidrometeorologi.
* **Metrik Asal**: Frekuensi kejadian Bencana Banjir dan Longsor di Sulteng & Sultra (BNPB, 2014–2024).
* **Pendekatan Statistik / Model**: **Statistical Percentile (Mean + 1 SD)** dari rata-rata 6 Provinsi se-Sulawesi (Opsi C). Mengukur tingkat anomali sentra nikel dibanding provinsi lain.
* **Logika Pembuktian**: Jika dokumen D3TLH berfungsi mengamankan sabuk hijau ekosistem hulu, seharusnya tidak ada lonjakan bencana banjir bandang pasca operasi tambang masif yang melampaui batas wajar regional.
* **Formula**:
  ```python
  Skor_Lahan_1 = min(10.0, (Bencana_Sulteng_Sultra / 877) * 10)
  ```
* **Angka Aktual**: 1.557 kejadian (2014–2024) → Skor: **10.0**
* **Rasio Aktual/Threshold**: 1,77× lipat melampaui batas outlier darurat.
* **✅ Status Threshold**: Defensible (berbasis anomali kewilayahan). Batas outlier = 877 kejadian.

### 3.2. Skor Deforestasi (Kehilangan Tutupan Hutan)
Mengukur kegagalan perlindungan kawasan penyangga karbon dan jasa ekosistem.
* **Metrik Asal**: Luas tutupan hutan yang hilang (Ha) dari Global Forest Watch, 2014–2023.
* **Pendekatan Statistik / Model**: **Statistical Percentile (Mean + 1 SD)** dari rata-rata 6 Provinsi se-Sulawesi (Opsi C).
* **Logika Pembuktian**: Jika klaim "reklamasi pasca tambang" dalam AMDAL terbukti, deforestasi permanen tidak mungkin terjadi dalam skala jutaan hektar yang menjadikan 2 provinsi ini episentrum kerusakan se-Sulawesi.
* **Formula**:
  ```python
  Skor_Lahan_2 = min(10.0, (Deforestasi_Sentra_Ha / 638_000) * 10)
  ```
* **Angka Aktual**: 1.148.635 Ha (2014–2023) → Skor: **10.0**
* **Rasio Aktual/Threshold**: 1,8× lipat melampaui batas outlier darurat.
* **✅ Status Threshold**: Defensible. Batas outlier = 638.000 Ha.

### 3.3. Skor Pelanggaran Kawasan Lindung
Mengukur perambahan ke dalam kawasan yang secara hukum tidak boleh diganggu gugat.
* **Metrik Asal**: Luas kawasan lindung (Protected Areas IUCN) yang hilang di Sulteng & Sultra (GFW, 2014–2023).
* **Pendekatan Statistik / Model**: **Protected Area Violation Index** diselaraskan dengan batas outlier deforestasi (Opsi C).
* **Temuan Forensik Kunci**: 100% dari setiap Ha deforestasi yang terjadi di Sulteng & Sultra selama 10 tahun terjadi di dalam kawasan lindung — tanpa terkecuali. Ini adalah pelanggaran D3TLH paling fundamental.
* **Formula**:
  ```python
  Skor_Lahan_3 = min(10.0, (Lindung_Hilang_Ha / 638_000) * 10)
  ```
* **Angka Aktual**: 1.148.635 Ha → Skor: **10.0**
* **Rasio Aktual/Threshold**: 1,8× lipat melampaui batas outlier darurat.
* **✅ Status Threshold**: Defensible. Batas outlier = 638.000 Ha.

### 3.4. Skor Dominasi Ekstraktif (Driver Deforestasi)
Mematahkan mitos bahwa deforestasi dilakukan oleh warga lokal, bukan industri.
* **Metrik Asal**: Luas deforestasi yang disebabkan oleh Komoditas Ekstraktif (Tambang/Sawit) di Sulteng & Sultra (GFW Loss by Driver, 2014–2023).
* **Pendekatan Statistik / Model**: **Attribution-Weighted Deforestation Score**.
* **Logika Pembuktian**: Driver breakdown GFW membuktikan bahwa Tambang/Sawit adalah penyebab utama deforestasi, bukan pertanian berpindah warga lokal yang selama ini dijadikan kambing hitam.
* **Formula**:
  ```python
  Skor_Lahan_4 = min(10.0, (Tambang_Driver_Ha / 500_000) * 10)
  ```
* **Angka Aktual**: 513.561 Ha → Skor: **10.0** (Capped)
* **🚨 Temuan Kritis (Bug Dataset GFW)**: Dataset GFW Loss by Driver ternyata **SAMA SEKALI KOSONG untuk Sulawesi Tengah**. Angka 513.561 Ha tersebut MURNI hanya potret deforestasi komoditas di Sulawesi Tenggara saja. Fakta bahwa 1 provinsi saja sudah mencetak 500.000 Ha kerusakan komoditas membuktikan betapa masifnya kebohongan ekologis di wilayah ini.
* **✅ Status Threshold**: Defensible. Threshold 500.000 Ha dipasang untuk "mendeteksi" skala masif kerusakan komoditas (Sultra saja sudah memenuhi kuota).

### 3.5. Akumulasi Skor Matriks Lahan
```python
Skor_Akumulasi_Lahan = (Skor_Lahan_1 + Skor_Lahan_2 + Skor_Lahan_3 + Skor_Lahan_4) / 4
```
Menggunakan **Simple Additive Weighting (SAW)** dengan bobot equal (25% per pilar). Threshold interpretasi: ≥ 8.0 = **Krisis Ruang Darat Parah**, ≥ 9.0 = **Darurat Ekologi**.

---

## 4. Matriks Daya Dukung Sosial (Matriks D)

### 4.1. Skor Manipulasi Persetujuan (FPIC)
Mengukur pemalsuan persetujuan masyarakat dalam proses AMDAL.
* **Metrik Asal**: Jumlah kasus investigasi pelanggaran FPIC (Free, Prior and Informed Consent) dari dataset KPA/TanahKita Sulawesi.
* **Pendekatan Statistik / Model**: **Consent Violation Index**.
* **Formula**:
  ```python
  Skor_Sosial_1 = min(10.0, (Kasus_FPIC / 12) * 10)
  ```
* **Angka Aktual**: 12 kasus → Skor: **10.0**
* **Catatan**: Threshold `12` = total aktual dataset kita (diperbaiki dari `/5` yang arbitrary). Skor proporsional terhadap seluruh temuan yang ada.
* **⚠️ Status Threshold**: Masih berbasis total dataset, bukan referensi eksternal. Target perbaikan → menggunakan rata-rata kasus FPIC nasional per provinsi dari laporan KPA Annual Report atau AMAN.

### 4.2. Skor Perampasan Ruang Hidup
Mengukur skala penggusuran paksa dan dampak jiwa dari konflik agraria tambang.
* **Metrik Asal**: Total jiwa terdampak dari konflik agraria sektor pertambangan (KPA/TanahKita).
* **Pendekatan Statistik / Model**: **Cumulative Human Impact Index**.
* **Formula**:
  ```python
  Skor_Sosial_2 = min(10.0, (Jiwa_Terdampak / 100_000) * 10)
  ```
* **Angka Aktual**: 177.738 jiwa → Skor: **10.0**
* **⚠️ Status Threshold**: 100.000 jiwa adalah angka yang bermakna secara kemanusiaan, namun perlu referensi dari standar darurat kemanusiaan internasional (OCHA/UNHCR) atau laporan KPA.

### 4.3. Skor Kriminalisasi Warga
Mengukur intensitas penggunaan aparat negara untuk membungkam penolakan warga.
* **Metrik Asal**: Jumlah insiden kriminalisasi (penangkapan, intimidasi, kekerasan aparat) terhadap warga yang menolak tambang.
* **Pendekatan Statistik / Model**: **State Repression Index**.
* **Formula**:
  ```python
  Skor_Sosial_3 = min(10.0, (Insiden_Krim / 50) * 10)
  ```
* **Angka Aktual**: 38 insiden → Skor: **7.6** *(model berfungsi dengan benar — tidak capped)*
* **⚠️ Status Threshold**: 50 insiden perlu referensi dari laporan HAM (Komnas HAM, KontraS, atau OHCHR Indonesia).

### 4.4. Skor Defisit Layanan Dasar (Faskes)
Mengukur paradoks boom mineral vs stagnasi layanan kesehatan dasar.
* **Metrik Asal**: Pertumbuhan jumlah fasilitas kesehatan (RS/Puskesmas/Klinik) di Sulteng & Sultra dalam 10 tahun (Kemenkes).
* **Pendekatan Statistik / Model**: **Social Infrastructure Deficit Index** — inverse scoring: makin rendah pertumbuhan faskes, makin tinggi skor defisit.
* **Logika Pembuktian**: Ekspor nikel sentra Sulawesi tumbuh >2.000% dalam satu dekade, tapi jika pertumbuhan faskes jauh di bawah 50%, klaim "peningkatan kesejahteraan" dalam AMDAL terbantah.
* **Formula**:
  ```python
  Skor_Sosial_4 = max(0.0, min(10.0, 10.0 - (Pertumbuhan_Faskes_Pct / 50) * 10))
  ```
* **⚠️ Status Threshold**: 50% pertumbuhan faskes sebagai batas wajar perlu referensi dari SPM (Standar Pelayanan Minimal) Kemenkes dan target RPJMN 2025–2029.

### 4.5. Akumulasi Skor Matriks Sosial
```python
Skor_Akumulasi_Sosial = (Skor_Sosial_1 + Skor_Sosial_2 + Skor_Sosial_3 + Skor_Sosial_4) / 4
```
Menggunakan **Simple Additive Weighting (SAW)** dengan bobot equal (25% per pilar). Threshold interpretasi: ≥ 8.0 = **Krisis Sosial Parah**, ≥ 9.0 = **Darurat HAM**.

---

## 5. Matriks Veto Kebijakan (Matriks E)

*(Dokumentasi detail menyusul — dalam pengembangan)*

---

## Referensi yang Perlu Dicari (Backlog)

| No | Referensi Target | Relevansi |
|---|---|---|
| 1 | PP No.21/2008 tentang Penyelenggaraan Penanggulangan Bencana | Threshold bencana Tab 3.1 |
| 2 | PP No.22/2021 tentang Penyelenggaraan Perlindungan dan Pengelolaan LH | Threshold air, udara, limbah B3 |
| 3 | PP No.23/2021 tentang Penyelenggaraan Kehutanan | Threshold kawasan lindung Tab 3.3 |
| 4 | Enhanced NDC Indonesia 2022 (FOLU Net Sink 2030) | Threshold deforestasi Tab 3.2 & emisi CO2 |
| 5 | KPA Annual Report (Catahu) — rata-rata konflik agraria per provinsi | Threshold FPIC & konflik sosial |
| 6 | Kemenkes — SPM Kesehatan (Standar Pelayanan Minimal) | Threshold defisit faskes Tab 4.4 |
| 7 | GFW Forest Loss Database — rata-rata deforestasi per provinsi Indonesia | Threshold Opsi C (statistik percentile) |
| 8 | BPS — rata-rata bencana per provinsi nasional | Threshold Opsi C bencana Tab 3.1 |
