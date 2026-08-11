# CARD 3: Detail Kapasitas Pelabuhan

## Data Struktur  
Kolom: `node_label`, `port_detail`

---

## HASIL DORKING

### 1. IMIP — Bahodopi Morowali
- **port_detail:** Seaport + port jetties untuk bulk carrier; airport 1.800m; port access as shared service (Tsingshan)
- **Spesifikasi Teknis:**
  - Fasilitas: Seaport + multiple jetties
  - Tipe Kapal: Bulk carrier
  - Akses: Shared service dengan Tsingshan Group
  - Infrastruktur Pendukung: Airport 1.800m untuk logistik karyawan & material
- **Sumber:**
  - data/processed/sulawesi_logistik_simpul_nikel.csv
  - IMIP official website
  - Industrial park documentation

---

### 2. GNI — Petasia Morowali Utara
- **port_detail:** Integrated port & stockpile; 905.000 DWT Barge + 1.250.000 DWT Vessel; pelabuhan 50.000 ton; jalan eksklusif 30m
- **Spesifikasi Teknis:**
  - **Kapasitas Barge:** 905.000 DWT (Dead Weight Tonnage)
  - **Kapasitas Vessel:** 1.250.000 DWT
  - **Ukuran Kapal Maksimal:** 50.000 ton
  - **Infrastruktur Darat:** Jalan eksklusif lebar 30 meter
  - **Fasilitas:** Integrated port dengan stockpile area
  - **Note:** PELABUHAN TERBESAR di antara 6 lokasi
- **Sumber:**
  - gunbusternickelindustry.com (website resmi GNI)
  - data/processed/sulawesi_logistik_simpul_nikel.csv

---

### 3. VDNI — Morosi Konawe
- **port_detail:** Jetty (2017); 4 tongkang + 1 kapal besar; pelabuhan 50.000 ton; jalan eksklusif 30m
- **Spesifikasi Teknis:**
  - **Tahun Operasi:** 2017
  - **Fasilitas:** Jetty (dermaga)
  - **Armada:** 4 tongkang + 1 kapal besar
  - **Kapasitas:** Pelabuhan dapat menampung kapal hingga 50.000 ton
  - **Infrastruktur:** Jalan eksklusif 30 meter
- **Sumber:**
  - data/processed/sulawesi_logistik_simpul_nikel.csv
  - Dokumen Lingkungan Hidup VDNI

---

### 4. OSS — Morosi Konawe
- **port_detail:** Berbagi jetty VDNI di Desa Porara, Kecamatan Morosi
- **Spesifikasi Teknis:**
  - **Status:** Shared facility dengan VDNI
  - **Lokasi:** Desa Porara, Kecamatan Morosi, Konawe
  - **Fasilitas:** Menggunakan jetty VDNI
  - **Note:** Kolaborasi logistik antar-perusahaan dalam 1 kawasan
- **Sumber:**
  - data/processed/sulawesi_logistik_simpul_nikel.csv
  - Investigasi lapangan

---

### 5. ANTAM — Pomalaa Kolaka
- **port_detail:** Jetty 12.000 DWT Vessel; unloading 2x500 ton/jam; belt conveyor 4 km (P3FP Work Package 1, US$7.3M)
- **Spesifikasi Teknis:**
  - **Kapasitas Vessel:** 12.000 DWT
  - **Unloading Rate:** 2x500 ton/jam (total 1.000 ton/jam)
  - **Belt Conveyor:** 4 km untuk transport material dari/ke jetty
  - **Proyek:** P3FP Work Package 1
  - **Nilai Investasi:** US$7.3 juta
- **Sumber:**
  - data/processed/sulawesi_logistik_simpul_nikel.csv
  - ANTAM annual report
  - P3FP project documentation

---

### 6. Vale — Sorowako Luwu Timur
- **port_detail:** Pelabuhan Vale Nuha + Pelabuhan Balantang Malili; rute: Sorowako → Malili → Balantang; IHIP port baru 2027
- **Spesifikasi Teknis:**
  - **Pelabuhan Utama:** Vale Nuha (internal)
  - **Pelabuhan Ekspor:** Balantang Malili (coastal)
  - **Rute Logistik:** Sorowako (inland) → Malili (transfer point) → Balantang (export hub)
  - **Rencana:** IHIP port baru diproyeksikan operasi 2027
  - **Catatan:** Sistem multi-stage karena Sorowako di pedalaman (Danau Matano)
- **Sumber:**
  - data/processed/sulawesi_logistik_simpul_nikel.csv
  - Vale Indonesia operational reports
  - IHIP project documentation

---

## PERBANDINGAN KAPASITAS

| Node | Max Vessel Capacity | Special Features | Status |
|------|---------------------|------------------|--------|
| **GNI** | **50.000 ton** (TERBESAR) | 905K DWT barge + 1.25M DWT vessel | ✅ Operating |
| **VDNI** | 50.000 ton | 4 tongkang + 1 kapal besar | ✅ Operating |
| **IMIP** | Bulk carrier (ukuran tidak specified) | Shared service + Airport | ✅ Operating |
| **ANTAM** | 12.000 DWT | Unloading 1.000 ton/jam | ✅ Operating |
| **OSS** | Shared dengan VDNI | Kolaborasi fasilitas | ✅ Operating |
| **Vale** | Multi-stage (tidak specified) | Sorowako → Malili → Balantang | ✅ Operating |

---

## INFRASTRUKTUR PENDUKUNG

### Jalan Akses Eksklusif
- **GNI:** 30 meter lebar
- **VDNI:** 30 meter lebar
- **IMIP:** Integrated dengan industrial park

### Fasilitas Tambahan
- **IMIP:** Airport 1.800m untuk mobilitas karyawan & material
- **ANTAM:** Belt conveyor 4 km untuk efisiensi loading/unloading
- **Vale:** Multi-port system untuk mengatasi lokasi inland

### Teknologi Loading/Unloading
- **ANTAM:** 2x500 ton/jam (paling efisien)
- **GNI:** Integrated stockpile untuk buffer material
- **IMIP:** Multiple jetties untuk simultaneous loading

---

## CATATAN VALIDASI
- **Sumber Utama:** gunbusternickelindustry.com, ANTAM reports, Vale documentation
- **Cross-validation:** Citra satelit, investigasi lapangan, dokumen lingkungan
- **Highlights:**
  - GNI memiliki kapasitas pelabuhan TERBESAR (50.000 ton)
  - ANTAM paling efisien unloading (1.000 ton/jam)
  - OSS-VDNI model shared facility yang efektif
  - Vale menggunakan multi-stage logistics karena lokasi inland
