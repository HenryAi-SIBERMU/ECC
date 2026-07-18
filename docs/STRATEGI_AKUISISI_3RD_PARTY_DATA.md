# Strategi Akuisisi Dataset Ekologis 3rd Party (NGO & Internasional)

**Konteks:**
Mengingat limitasi pada portal resmi pemerintah (kuota API Google CSE yang habis, data pelaporan SIRAJA yang terkunci untuk publik, dan data SIMONTANA yang sulit diekstrak massal), kita perlu mengeksekusi "Misi Sapu Bersih" untuk menarik *dataset* alternatif dari portal Internasional dan NGO (3rd Party). 

Strategi ini krusial untuk melengkapi **Fase 1 (Data Acquisition)** dari PRD, di mana kita bukan hanya mengumpulkan data realitas fisik (seperti luas area rusak), tetapi juga menyiapkan **Faktor Konversi** (Multiplier) yang akan sangat krusial di Fase 2 (Analisis Jejak Ekologis & Karbon).

---

## 🧺 Keranjang 1: Dataset Primer (Realita Fisik di Lapangan)

Keranjang ini berfokus pada pengumpulan metrik fisik secara spasial (Hektar, Ton) yang merepresentasikan dampak langsung operasi nikel.

### 1. Global Forest Watch (GFW - WRI)
* **Target Indikator:** Deforestasi (Tree Cover Loss).
* **Fungsi:** Menggantikan/melengkapi data SIMONTANA KLHK. GFW mengukur kehilangan tutupan pohon secara historis (2001-2023) dengan resolusi 30 meter.
* **Metode:** Menggunakan pustaka Python `gfwpy` atau langsung menembak API (`data-api.globalforestwatch.org`) untuk menarik area agregat (Ha) yang hilang per Kabupaten di wilayah Sulawesi (Morowali, Konawe, Haltim, dll).
* **Output:** `sulawesi_deforestasi_gfw_2001_2023.csv`

### 2. Global Tailings Portal (GRID-Arendal / PBB)
* **Target Indikator:** Limbah B3 (Volume & Lokasi Bendungan Tailing).
* **Fungsi:** Melengkapi *dataset* limbah B3 yang sebelumnya kita ambil dari AMDAL/NGO.
* **Metode:** Mengunduh *database* bendungan tailing dari portal GRID-Arendal, lalu mem-filter khusus untuk nikel di Indonesia (Sulawesi).
* **Output:** `sulawesi_bendungan_tailing_pbb.csv`

### 3. NASA FIRMS (Fire Information for Resource Management System)
* **Target Indikator:** Pembukaan Lahan / Kebakaran (*Land Clearing Proxy*).
* **Fungsi:** Titik api (hotspots) historis sering berkorelasi kuat dengan indikasi deforestasi paksa di dalam konsesi tambang.
* **Metode:** Mengakses NASA FIRMS API untuk menarik koordinat titik api (VIIRS/MODIS) di sekitar poligon IUP nikel Sulawesi.
* **Output:** `sulawesi_fire_hotspots_nasa.csv`

---

## 🧺 Keranjang 2: Dataset Konverter (Alat Hitung Dampak)

Keranjang ini berfokus pada "Faktor Pengali" (Multipliers). Memiliki data ini dari awal akan mempercepat kerja ekonom CELIOS saat melakukan perhitungan emisi karbon dan jejak ekologis.

### 4. Global Footprint Network (GFN)
* **Target Indikator:** Jejak Ekologis (Ecological Footprint).
* **Fungsi:** Mengubah luas lahan rusak (Hektar) menjadi standar *Global Hectares* (gha).
* **Metode:** Menarik *Equivalence Factors* (EQF) untuk berbagai tipe tutupan lahan (contoh: Hutan = 1,26) dan *Yield Factors* (YF) spesifik untuk kapasitas ekologis negara Indonesia.
* **Output:** `konverter_gfn_indonesia.csv`

### 5. IPCC EFDB (Emission Factor Database)
* **Target Indikator:** Jejak Karbon / Gas Rumah Kaca (CO2-eq).
* **Fungsi:** Mengubah volume fisik tambang (Ton Limbah, Ha Lahan Rusak) menjadi besaran emisi karbon yang dilepaskan ke udara.
* **Metode:** Mengekstrak standar *Emission Factor* IPCC khusus untuk sektor pertambangan (*Mining Waste*) dan Alih Fungsi Lahan (*Land Use Change*).
* **Output:** `konverter_ipcc_mining_emissions.csv`

---

## 🚀 Rencana Eksekusi (Roadmap)

Untuk memastikan pengumpulan data berjalan efisien, kita akan mengeksekusi dengan urutan dari yang paling statis hingga yang paling dinamis:

1. **Fase Konverter (Cepat):** Mengekstrak data GFN dan IPCC terlebih dahulu menjadi tabel rujukan (CSV). Karena ini adalah konstanta (faktor statis), pemrosesan akan sangat cepat.
2. **Fase Spasial Skala Menengah (Sedang):** Mengekstrak data Global Tailings Portal (PBB) khusus untuk Sulawesi.
3. **Fase Big Data (Berat):** Membangun *script* API untuk GFW dan NASA FIRMS guna menyedot data deforestasi dan *hotspots* yang volumenya besar, diagregasikan per kabupaten basis nikel.
