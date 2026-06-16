# Dokumentasi Model Matematis Skoring ECC (Audit D3TLH)

Dokumen ini menjelaskan formulasi matematis yang digunakan untuk mengubah data empiris (kesehatan, lingkungan, tata ruang) menjadi **Skor Kerusakan Ekologis (0-10)** dalam Dashboard Forensik ECC secara dinamis, rasional, dan terukur.

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

### 1.5. Model Akumulasi Skor Kerusakan (Vonis D3TLH)
Menyatukan keempat dimensi skor di atas menjadi satu nilai tunggal (*Single Index*).
* **Pendekatan Statistik / Model**: **Simple Additive Weighting (SAW) / Arithmetic Mean Aggregation**. Merupakan metode perankingan dan sintesis indikator majemuk yang paling transparan dan diakui secara global (sering digunakan dalam penyusunan HDI/IPM oleh UNDP). Masing-masing metrik dianggap memiliki bobot kontribusi kerusakan yang sama (Equal Weighting = 25%).
* **Formula**:
  ```python
  Skor_Akumulasi = (Skor_1 + Skor_2 + Skor_3 + Skor_4) / 4
  ```
* **Interpretasi Output**: Menghasilkan skor akhir berskala 0 hingga 10 yang mendasari penentuan "Vonis Eksekutif" di dashboard. Nilai agregat di atas 8.0 menandakan **Status: Daya Tampung Jebol** yang secara saintifik membatalkan klaim aman dari dokumen D3TLH pemerintah.

---
*(Catatan: Model matematis untuk Matriks Daya Dukung Lahan/Kebencanaan, dan Kedaulatan Ruang akan diintegrasikan secara berkesinambungan di bawah blok ini ke depannya).*

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


## 3. Matriks Daya Dukung Lahan & Sosial (Matriks C)

### 3.1. Skor Bencana Ekologis (Banjir & Longsor)
Mengukur efektivitas mitigasi spasial terhadap bencana hidrometeorologi.
* **Metrik Asal**: Frekuensi kejadian Bencana Banjir dan Longsor di Sulteng & Sultra (BNPB).
* **Pendekatan Statistik / Model**: **Disaster Frequency Index**. 
* **Logika Pembuktian**: Jika dokumen AMDAL dan D3TLH berfungsi mengamankan sabuk hijau ekosistem hulu, seharusnya tidak ada lonjakan letusan banjir bandang pasca operasi tambang skala masif.
* **Formula**:
  `python
  Skor_Lahan_1 = min(10.0, (Bencana_Sulteng_Sultra / 500) * 10)
  `
* **Threshold Kritis**: Apabila bencana menembus angka 500 kejadian kumulatif di area sentra nikel, status divonis sebagai **Darurat Bencana**.

### 3.2. Skor Deforestasi Hutan Primer
Mengukur kegagalan perlindungan kawasan penyangga karbon.
* **Metrik Asal**: Luas tutupan pohon / deforestasi yang hilang dalam Ha (Global Forest Watch).
* **Pendekatan Statistik / Model**: **Cumulative Loss Burden**.
* **Logika Pembuktian**: Penilaian Jasa Pengaturan Iklim secara teoretis gagal bila fakta di darat menunjukkan deforestasi primer tidak terkontrol dan dibiarkan atas nama konsesi tambang.
* **Formula**:
  `python
  Skor_Lahan_2 = min(10.0, (Deforestasi_Sentra_Ha / 250_000) * 10)
  `
* **Threshold Kritis**: Kehilangan tutupan pohon lebih dari 250.000 Ha akan mencetak skor kerusakan maksimum 10.0.

### 3.3. Skor Konflik Darat (Sosial & Agraria)
Mengkuantifikasi kekerasan dan letusan perlawanan rakyat mempertahankan ruang hidup.
* **Metrik Asal**: Total kasus perampasan tanah / ruang produktif di luar sektor pesisir (KPA/TanahKita).
* **Pendekatan Statistik / Model**: **Socio-Ecological Escalation Index (Darat)**.
* **Logika Pembuktian**: Mitos bahwa 'tambang menyejahterakan warga lokal' dimentahkan oleh maraknya insiden kriminalisasi warga dan penggusuran kebun pertanian produktif.
* **Formula**:
  `python
  Skor_Sosial_1 = min(10.0, (Konflik_Darat / 300) * 10)
  `
* **Threshold Kritis**: Terkumpulnya 300 kasus konflik tanah memicu skor **Darurat Sosial** 10.0.

### 3.4. Skor Veto Kebijakan (Monopoli Izin)
Mengevaluasi kelumpuhan tata kelola (Regulatory Capture) oleh oligarki ekstraktif.
* **Metrik Asal**: Luas izin konsesi baru (IUP) yang terus diterbitkan.
* **Pendekatan Statistik / Model**: **Policy Recklessness Metric (Pengabaian Alarm Darurat)**.
* **Logika Pembuktian**: Di saat skor udara kritis, penyakit pernapasan meledak, kualitas air ambruk, dan bencana rutin terjadi, pemerintah secara irelevan tetap melelang dan mengobral Izin Baru tanpa mengaktifkan hak Veto Spasial.
* **Formula**:
  `python
  Skor_Veto_1 = min(10.0, (Luas_Izin_Sentra_Ha / 500_000) * 10)
  `
* **Threshold Kritis**: Penguasaan wilayah konsesi IUP baru lebih dari 500.000 Ha memicu vonis kegagalan Tata Kelola.

