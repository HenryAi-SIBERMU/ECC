# Dokumentasi Model Matematis Skoring ECC (Audit D3TLH)

Dokumen ini menjelaskan formulasi matematis yang digunakan untuk mengubah data empiris (kesehatan, lingkungan, tata ruang) menjadi **Skor Kerusakan Ekologis (0-10)** dalam Dashboard Forensik ECC secara dinamis, rasional, dan terukur.

## 1. Matriks Daya Tampung Udara

### 1.1. Skor Ancaman Udara (Korelasi PLTU & IKU)
Mengukur tingkat ancaman kualitas udara akibat pembakaran batu bara.
* **Metrik Asal**: Kapasitas PLTU Captive beroperasi (MW) & Indeks Kualitas Udara BPS (IKU).
* **Logika Pembuktian**: Kualitas udara divonis memburuk secara asimetris jika kapasitas PLTU meroket sementara nilai IKU anjlok tajam menjauhi standar aman (80).
* **Formula**:
  ```python
  Skor_1 = min(10.0, (Kapasitas_PLTU / 10000) * 5 + max(0, 80 - IKU_Terkini) / 30 * 5)
  ```
* **Threshold Kritis**: Kapasitas 10.000 MW akan memberi kontribusi poin maksimal (5 poin). Penurunan IKU sebesar 30 poin (anjlok dari 80 menjadi 50) akan memberi poin maksimal (5 poin).

### 1.2. Skor Rasio Anomali ISPA (Morbiditas)
Mengukur asimetri distribusi penyakit infeksi saluran pernapasan di ekoregion.
* **Metrik Asal**: Rata-rata Kumulatif Kasus ISPA/Pneumonia per Provinsi.
* **Logika Pembuktian**: Membandingkan intensitas ledakan penyakit antara wilayah Ring-1 Tambang (Sentra Nikel) versus wilayah non-sentra. Jika rasio melampaui 1, itu membuktikan morbiditas dipicu oleh agen polutan dari kawasan sentra, bukan fluktuasi alamiah.
* **Formula**:
  ```python
  Rasio = (Rata_Rata_Kasus_Sentra) / (Rata_Rata_Kasus_Non_Sentra)
  Skor_2 = min(10.0, max(0.0, (Rasio - 1) * 2.5))
  ```
* **Threshold Kritis**: Jika rasio mencapai 5x lipat lebih masif dari daerah lain, skor menembus 10.0 (Darurat Medis).

### 1.3. Skor Over-Capacity Limbah B3
Mengukur tingkat kelampauan daya tampung limbah beracun dan abu terbang (fly ash).
* **Metrik Asal**: Total Estimasi Timbulan Limbah B3 (Juta Ton/Tahun).
* **Logika Pembuktian**: Daya tampung mitigasi ekoregion memiliki batas infrastruktur dan *carrying capacity* alamiah. Di sini diasumsikan *Baseline Toleransi Lingkungan* adalah 1 Juta Ton per tahun.
* **Formula**:
  ```python
  Skor_Overcapacity = Total_Timbulan_B3_Ton / 1_000_000 # Menghasilkan X Lipat
  Skor_3 = min(10.0, (Skor_Overcapacity / 30.0) * 10)
  ```
* **Threshold Kritis**: Apabila akumulasi timbulan limbah melampaui 30 Juta Ton/Tahun (30x lipat dari batas wajar), skor mencapai nilai absolut 10.0 (Kapasitas Jebol).

### 1.4. Skor Defisit Ekosistem Karbon
Mengukur hilangnya "paru-paru udara" akibat eksploitasi perizinan lahan.
* **Metrik Asal**: Total Emisi CO2 Ekivalen Lepas dari Deforestasi Hutan Primer (Megagram / Juta Ton).
* **Logika Pembuktian**: Setiap hektar hutan yang ditebang demi perizinan IUP melepaskan emisi karbon yang sebelumnya tertahan berabad-abad (carbon sink), memaksa udara menerima defisit ganda.
* **Formula**:
  ```python
  Skor_4 = min(10.0, (Total_Emisi_Juta_Ton / 150.0) * 10)
  ```
* **Threshold Kritis**: Pelepasan emisi secara eksponensial hingga menembus 150 Juta Ton CO2 dalam 1 dekade akan mencetak skor mutlak 10.0 (Darurat Karbon).

---
*(Catatan: Model matematis untuk Matriks Daya Tampung Air, Daya Dukung Lahan/Kebencanaan, dan Kedaulatan Ruang akan diintegrasikan secara berkesinambungan di bawah blok ini ke depannya).*
