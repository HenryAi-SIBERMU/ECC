# OSINT: Logistik Pelabuhan Ekspor Nikel Sulawesi

## Overview
Folder ini berisi hasil dorking (Open Source Intelligence) untuk 3 Dataset Cards di **Section 1.5 Dashboard Page 1: Ekspansi Industri**.

Target analisis: **6 node industri nikel utama di Sulawesi** yang memiliki fasilitas pelabuhan ekspor terintegrasi.

---

## Dataset Cards

### Card 1: Fasilitas Pelabuhan Ekspor
**File:** `CARD_1_port_facilities.md`

**Kolom Data:**
- `node_label`: Nama lokasi industri
- `port_facility`: Status konfirmasi fasilitas pelabuhan
- `export_channel`: Jenis komoditas ekspor

**Temuan Utama:**
- **6/6 lokasi** terkonfirmasi memiliki pelabuhan/dermaga ekspor
- Channel utama: Feronikel, NPI, Stainless Steel → China & Asia

---

### Card 2: Status Proyek Strategis Nasional (PSN)
**File:** `CARD_2_psn_status.md`

**Kolom Data:**
- `node_label`: Nama lokasi industri
- `psn_status`: Status PSN (terkonfirmasi/belum_ditemukan)
- `psn_detail`: Referensi dokumen PSN

**Temuan Utama:**
- **4/6 lokasi** berlabel PSN (IMIP, VDNI, OSS, ANTAM)
- **Basis Hukum:** Perpres 58/2017, Perpres 12/2025, KPPIP
- **Implikasi:** Fast-track perizinan & pembebasan lahan

---

### Card 3: Detail Kapasitas Pelabuhan
**File:** `CARD_3_port_capacity.md`

**Kolom Data:**
- `node_label`: Nama lokasi industri
- `port_detail`: Spesifikasi teknis dan kapasitas

**Temuan Utama:**
- **Pelabuhan Terbesar:** GNI Petasia (50.000 ton)
- **Unloading Tercepat:** ANTAM (1.000 ton/jam)
- **Infrastruktur:** Jalan eksklusif, belt conveyor, airport
- **Model Kolaborasi:** OSS berbagi fasilitas dengan VDNI

---

## 6 Nodes Target

| No | Node Label | Lokasi | Provinsi | Status Pelabuhan | PSN |
|----|------------|--------|----------|------------------|-----|
| 1 | IMIP | Bahodopi Morowali | Sulawesi Tengah | ✅ Terkonfirmasi | ✅ |
| 2 | GNI | Petasia Morowali Utara | Sulawesi Tengah | ✅ Terkonfirmasi (TERBESAR) | ❌ |
| 3 | VDNI | Morosi Konawe | Sulawesi Tenggara | ✅ Terkonfirmasi | ✅ |
| 4 | OSS | Morosi Konawe | Sulawesi Tenggara | ✅ Terkonfirmasi (Shared) | ✅ |
| 5 | ANTAM | Pomalaa Kolaka | Sulawesi Tenggara | ✅ Terkonfirmasi | ✅ |
| 6 | Vale | Sorowako Luwu Timur | Sulawesi Selatan | ✅ Terkonfirmasi (Multi-stage) | ❌ |

---

## Metodologi OSINT

### Sumber Data Primer
1. **Website Resmi Perusahaan**
   - gunbusternickelindustry.com (GNI)
   - imip.co.id (IMIP)
   - vale.com (Vale)
   - antam.com (ANTAM)
   - vdni.co.id (VDNI)

2. **Dokumen Pemerintah**
   - Perpres 58/2017 (Proyek Strategis Nasional)
   - Perpres 12/2025 (Percepatan Industri Nikel)
   - KPPIP (Komite Percepatan Infrastruktur Prioritas)
   - BAPPENAS project documentation

3. **Media & Investigasi**
   - Katadata.co.id
   - Kompas.com
   - Tempo.co
   - Mongabay Indonesia
   - JATAM (Jaringan Advokasi Tambang)

4. **Dokumen Lingkungan**
   - AMDAL perusahaan
   - UKL-UPL
   - RKL-RPL

5. **Tools Geospasial**
   - Google Earth Pro
   - Sentinel Hub
   - Marine Traffic (vessel tracking)
   - Vessel Tracker

### Teknik Dorking
```
site:domain.com keyword1 OR keyword2
filetype:pdf "perpres" "58" "2017"
"perusahaan" "pelabuhan" "kapasitas"
intext:"PSN" "nikel" "sulawesi"
```

### Validasi Silang
- ✅ Cross-check minimal 3 sumber independen
- ✅ Verifikasi dengan citra satelit
- ✅ Konfirmasi dengan dokumen resmi pemerintah
- ✅ Tracking vessel movement untuk validasi operasional

---

## Output Processing

### File Processed
Hasil akhir dikompilasi dalam:
```
data/processed/sulawesi_logistik_simpul_nikel.csv
```

### Struktur CSV
```csv
node_label,port_facility,export_channel,psn_status,psn_detail,port_detail
IMIP,terkonfirmasi,bulk carrier ke China,terkonfirmasi,"PSN 2022; KPPIP","Seaport + jetties; airport 1.800m"
GNI,terkonfirmasi,NPI ke China dan Asia,belum_ditemukan,"tidak ditemukan eksplisit","905K DWT barge; 50.000 ton vessel"
...
```

---

## Temuan Kritis

### 1. Integrasi Vertikal Lengkap
Semua 6 lokasi memiliki **integrasi penuh tambang → smelter → pelabuhan**, menunjukkan kontrol supply chain end-to-end oleh perusahaan.

### 2. Dominasi Label PSN
4 dari 6 lokasi berlabel PSN, memberikan **privilese hukum**:
- Fast-track perizinan lingkungan
- Kemudahan pembebasan lahan
- Dukungan infrastruktur pemerintah
- Proteksi dari gugatan warga

### 3. Kapasitas Ekspor Masif
- **GNI:** 50.000 ton/kapal (terbesar)
- **ANTAM:** 1.000 ton/jam unloading (tercepat)
- **Estimasi Total:** Jutaan ton nikel per tahun ke China

### 4. Infrastruktur Eksklusif
- Jalan khusus lebar 30m (GNI, VDNI)
- Airport 1.800m (IMIP)
- Belt conveyor 4 km (ANTAM)
- Multi-stage port system (Vale)

### 5. Model Kolaborasi
OSS berbagi jetty dengan VDNI menunjukkan **konsolidasi logistik** untuk efisiensi biaya.

---

## Implikasi Advokasi

### Eksternalitas Lingkungan
1. **Reklamasi Pantai:** Pembangunan pelabuhan merusak ekosistem pesisir
2. **Polusi Air Laut:** Limbah loading/unloading + ballast water kapal
3. **Kerusakan Terumbu Karang:** Alur pelayaran kapal besar
4. **Sedimentasi:** Material tailing dari proses smelter

### Ketimpangan Sosial-Ekonomi
1. **Penggusuran Nelayan:** Pelabuhan menggusur wilayah tangkap tradisional
2. **Pembebasan Lahan Paksa:** Label PSN mempercepat land grab
3. **Akses Terbatas:** Jalan eksklusif membatasi mobilitas warga lokal
4. **Benefit Tidak Merata:** Profit ekspor tidak kembali ke komunitas lokal

### Kedaulatan Ekonomi
1. **Dependensi China:** 90%+ ekspor ke China
2. **Harga Ditentukan China:** Perusahaan China mendominasi ownership
3. **Kontrol Supply Chain:** Integrasi vertikal oleh korporasi asing
4. **Nilai Tambah Rendah:** Ekspor masih berupa intermediate products

---

## Rekomendasi Penelitian Lanjutan

### 1. Vessel Tracking
Gunakan Marine Traffic API untuk tracking kapal ekspor real-time:
- Identifikasi destination ports (mayoritas China)
- Frekuensi ekspor per bulan
- Volume cargo aktual
- Pola seasonal shipping

### 2. Financial Flow Analysis
Investigasi aliran keuangan ekspor:
- Transfer pricing schemes
- Tax avoidance strategies
- Royalty & dividend repatriation
- Kontribusi aktual ke APBN vs profit perusahaan

### 3. Environmental Impact Assessment
Monitoring dampak pelabuhan:
- Water quality testing (TSS, heavy metals)
- Coral reef damage assessment
- Mangrove deforestation
- Fish population decline

### 4. Community Impact Study
Etnografi dampak sosial:
- Wawancara nelayan terdampak
- Survei pembebasan lahan
- Analisis konflik agraria
- Assessment akses ekonomi lokal

---

## Citation

Jika menggunakan data ini untuk publikasi, gunakan sitasi:

```
DuniaHub Research Team (2025). "OSINT: Logistik Pelabuhan Ekspor Nikel Sulawesi - 
Analisis Integrasi Vertikal Industri Pemurnian Nikel." Dataset version 1.0.
Source: data/raw/osint_logistik_pelabuhan/
```

---

## Kontak

Untuk pertanyaan atau verifikasi data, hubungi:
- **Research Team:** research@duniahub.org
- **Data Issues:** GitHub Issues
- **Collaboration:** partnerships@duniahub.org

---

## Changelog

### Version 1.0 (2025-08-03)
- Initial dorking dan kompilasi 3 dataset cards
- Dokumentasi 6 nodes industri nikel
- Cross-validation dengan 25+ sumber
- Export ke processed CSV

---

## License

Data ini tersedia untuk **penelitian, advokasi, dan jurnalisme publik**. 

**Attribution Required:** Wajib menyebutkan sumber DuniaHub Research Team.

**Commercial Use:** Hubungi tim untuk lisensi komersial.

---

**Last Updated:** 2025-08-03  
**Status:** Validated & Ready for Analysis
