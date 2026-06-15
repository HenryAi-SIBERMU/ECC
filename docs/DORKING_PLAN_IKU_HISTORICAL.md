# Rencana Google Dorking - Data IKU Historis (2014-2018)

## 🎯 Target
Mencari publikasi KLHK/BPS yang berisi data **Indeks Kualitas Udara (IKU)** untuk provinsi Sulawesi tahun **2014-2018**.

## 📋 Informasi Target

**Data yang dicari:**
- Indeks Kualitas Udara (IKU) atau PM2.5/PM10
- Wilayah: 6 provinsi Sulawesi (Utara, Tengah, Selatan, Tenggara, Barat, Gorontalo)
- Periode: 2014-2018 (5 tahun)
- Format: PDF (SLHI), Excel/CSV (publikasi BPS), atau HTML (portal lama)

**Sumber potensial:**
1. SLHI (Status Lingkungan Hidup Indonesia) tahun 2014, 2015, 2016
2. Publikasi BPS Provinsi Sulawesi tentang lingkungan hidup
3. Portal lama KLHK/KemenLH (archive.org)
4. Publikasi akademis/penelitian tentang kualitas udara Sulawesi

---

## 🔍 Query Google Dorking

### 1. SLHI Tahun Lama (2014-2016)

```
"Status Lingkungan Hidup Indonesia" 2014 filetype:pdf
"Status Lingkungan Hidup Indonesia" 2015 filetype:pdf
"Status Lingkungan Hidup Indonesia" 2016 filetype:pdf
"SLHI" 2014 "indeks kualitas udara" filetype:pdf
"SLHI" 2015 "indeks kualitas udara" filetype:pdf
"SLHI" 2016 "indeks kualitas udara" filetype:pdf
```

**Target domains:**
- `site:bps.go.id`
- `site:menlhk.go.id`
- `site:kemenlh.go.id`
- `site:archive.bps.go.id`

### 2. Publikasi BPS Provinsi Sulawesi

```
site:sulutprov.bps.go.id "indeks kualitas udara" 2014..2018
site:sultengprov.bps.go.id "kualitas udara" 2014..2018
site:sulsel.bps.go.id "IKU" 2014..2018 filetype:pdf
site:sultraprov.bps.go.id "lingkungan hidup" 2014..2018
site:sulbarprov.bps.go.id "udara" 2014..2018
site:gorontaloprov.bps.go.id "IKLH" 2014..2018
```

### 3. Portal Lama via Archive.org

```
site:web.archive.org "iklh.menlhk.go.id" "sulawesi" "kualitas udara"
site:web.archive.org "sipsn.menlhk.go.id" 2014..2018
site:web.archive.org inurl:bps.go.id "indeks kualitas udara" "sulawesi"
```

### 4. Data Terbuka Nasional

```
site:data.go.id "kualitas udara" "sulawesi" 2014..2018
site:data.go.id "IKU" filetype:csv
site:satu-data.go.id "indeks kualitas udara" 2014..2018
```

### 5. Publikasi Akademis

```
"air quality index" "sulawesi" 2014..2018 filetype:pdf
"PM2.5" "sulawesi" "indonesia" 2014..2018 site:researchgate.net
"particulate matter" "sulawesi" 2014..2018 site:.ac.id
"indeks kualitas udara" "sulawesi" 2014..2018 site:.ac.id
```

### 6. IKLH Provinsi (Portal Lama)

```
intitle:"indeks kualitas lingkungan hidup" "sulawesi utara" 2014..2018
"IKLH" "sulawesi selatan" 2014..2018 site:.go.id
"indeks kualitas udara" inurl:sulut 2014..2018
```

---

## 📊 Strategi Pencarian Bertahap

### Fase 1: SLHI Official (Priority: HIGH)
1. Cari SLHI 2014, 2015, 2016 di domain BPS/KLHK
2. Check archive.bps.go.id untuk publikasi lama
3. Gunakan Archive.org untuk akses portal lama

### Fase 2: BPS Provinsi (Priority: MEDIUM)
1. Scan setiap website BPS provinsi Sulawesi
2. Fokus pada publikasi "Statistik Lingkungan Hidup Daerah"
3. Cek publikasi "Sulawesi Dalam Angka" tahun 2015-2019 (berisi data retrospektif)

### Fase 3: Portal Data Terbuka (Priority: MEDIUM)
1. data.go.id (One Data Indonesia)
2. satu-data.go.id
3. Portal Open Data Kementerian

### Fase 4: Akademis & Penelitian (Priority: LOW)
1. ResearchGate, Google Scholar
2. Repository universitas (.ac.id)
3. Jurnal lingkungan Indonesia

---

## 🎯 Target Output

**Jika ditemukan:**
- Download PDF/Excel ke `data/raw/slhi_historical/`
- Extract data IKU untuk 6 provinsi Sulawesi
- Format ke CSV sesuai skema existing: `Tahun, Provinsi, IKU, Sumber`
- Merge dengan data 2019-2024 yang sudah ada

**Jika tidak ditemukan:**
- Dokumentasikan semua query yang sudah dicoba
- Lakukan interpolasi backfill dari 2019
- Atau gunakan data nasional sebagai proxy dengan adjustment

---

## 📝 Checklist Eksekusi

- [ ] Query 1-6 untuk SLHI 2014
- [ ] Query 1-6 untuk SLHI 2015
- [ ] Query 1-6 untuk SLHI 2016
- [ ] Scan 6 website BPS Provinsi
- [ ] Check Archive.org untuk portal lama
- [ ] Search data.go.id dan satu-data.go.id
- [ ] Fallback: Publikasi akademis
- [ ] Dokumentasi hasil pencarian
- [ ] Extract data jika ditemukan
- [ ] Update dataset final

---

## 🚀 Ready to Execute

Script dorking automated akan dijalankan untuk query batch.
Hasil akan disimpan ke `docs/DORKING_RESULTS_IKU_HISTORICAL.md`.
