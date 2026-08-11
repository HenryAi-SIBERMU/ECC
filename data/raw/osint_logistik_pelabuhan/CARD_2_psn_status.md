# CARD 2: Status Proyek Strategis Nasional (PSN)

## Data Struktur
Kolom: `node_label`, `psn_status`, `psn_detail`

---

## HASIL DORKING

### 1. IMIP — Bahodopi Morowali
- **psn_status:** terkonfirmasi
- **psn_detail:** PSN terkonfirmasi (Vale PDF; PSN 2022); KPPIP program smelter
- **Sumber:**
  - Vale PDF document
  - KPPIP PSN 2022 list
  - data/processed/sulawesi_logistik_simpul_nikel.csv

### 2. GNI — Petasia Morowali Utara
- **psn_status:** belum_ditemukan
- **psn_detail:** tidak ditemukan eksplisit untuk GNI
- **Sumber:**
  - data/processed/sulawesi_logistik_simpul_nikel.csv
  - Tidak tercantum di Perpres 58/2017 atau Perpres 12/2025

### 3. VDNI — Morosi Konawe  
- **psn_status:** terkonfirmasi
- **psn_detail:** PSN Perpres 58/2017; Kawasan Industri Konawe (IKN); KPPIP program smelter
- **Sumber:**
  - Perpres 58/2017
  - KPPIP
  - data/processed/sulawesi_logistik_simpul_nikel.csv

### 4. OSS — Morosi Konawe
- **psn_status:** terkonfirmasi
- **psn_detail:** PSN Perpres 58/2017; Kawasan Industri Konawe (IKN)
- **Sumber:**
  - Perpres 58/2017
  - data/processed/sulawesi_logistik_simpul_nikel.csv

### 5. ANTAM — Pomalaa Kolaka  
- **psn_status:** terkonfirmasi
- **psn_detail:** PSN (Vale PDF; NSP Pomalaa); IHIP PSN Desember 2022 (Huusyi, 11.808 ha, US$108)
- **Sumber:**
  - Vale PDF document
  - PSN Desember 2022 list
  - data/processed/sulawesi_logistik_simpul_nikel.csv

### 6. Vale — Sorowako Luwu Timur
- **psn_status:** belum_ditemukan
- **psn_detail:** Tidak ditemukan PSN eksplisit untuk Vale GP; tapi proyek Vale (GP) berstatus "ongoing"
- **Sumber:**
  - data/processed/sulawesi_logistik_simpul_nikel.csv
  - Status proyek ongoing namun tidak tercatat sebagai PSN resmi

---

## SUMMARY STATUS PSN

| Node | PSN Status | Perpres | KPPIP |
|------|-----------|---------|-------|
| IMIP | ✅ Terkonfirmasi | - | ✅ |
| GNI | ❌ Belum Ditemukan | - | - |
| VDNI | ✅ Terkonfirmasi | ✅ 58/2017 | ✅ |
| OSS | ✅ Terkonfirmasi | ✅ 58/2017 | - |
| ANTAM | ✅ Terkonfirmasi | - | ✅ |
| Vale | ❌ Belum Ditemukan | - | - |

**Total PSN:** 4/6 lokasi terkonfirmasi sebagai Proyek Strategis Nasional

---

## REFERENSI DOKUMEN

### Perpres 58/2017
- **Judul:** Peraturan Presiden tentang Proyek Strategis Nasional
- **Relevansi:** Mencantumkan Kawasan Industri Konawe (VDNI, OSS)
- **Status:** Aktif
- **URL:** https://peraturan.go.id

### Perpres 12/2025  
- **Judul:** Peraturan Presiden tentang Percepatan Pembangunan Industri Nikel
- **Relevansi:** Update terbaru PSN industri nikel
- **Status:** Terbaru
- **URL:** https://jdih.setneg.go.id

### KPPIP (Komite Percepatan Penyediaan Infrastruktur Prioritas)
- **Website:** https://kppip.go.id
- **Data:** Program smelter PSN 2022
- **Mencakup:** IMIP, VDNI, ANTAM

### Vale PDF Documents
- **Sumber:** Internal Vale sustainability reports
- **Menyebutkan:** Status PSN untuk IMIP dan ANTAM Pomalaa

---

## CATATAN VALIDASI
- **Metode:** Cross-checking Perpres, KPPIP, dan dokumen perusahaan
- **Status Label PSN:** Mempercepat perizinan & memudahkan pembebasan lahan
- **Implikasi:** PSN memberikan jalur fast-track untuk infrastruktur
