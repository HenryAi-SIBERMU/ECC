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
  Skor_2 = min(10.0, max(0.0, (Rasio - 1) * 2.5))
  ```
* **Threshold Kritis**: Jika rasio mencapai 5x lipat lebih masif dari daerah lain, skor menembus nilai absolut 10.0 (Darurat Medis).

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
*(Catatan: Model matematis untuk Matriks Daya Tampung Air, Daya Dukung Lahan/Kebencanaan, dan Kedaulatan Ruang akan diintegrasikan secara berkesinambungan di bawah blok ini ke depannya).*
