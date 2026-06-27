# Daftar Lengkap Portal Web & Sumber Data
## CELIOS D3TLH Research — Data Acquisition Log

**Tanggal:** 14 Juni 2026 (Updated: 14 Juni 2026 — Sesi 4)
**Total Portal:** 73 sumber

---

## Portal Resmi Pemerintah

| # | Portal | URL | Tipe | Metode Akses | Status | Data yang Diperoleh | Keterangan |
|:---:|---|---|:---:|:---:|:---:|---|---|
| 1 | **BPS WebAPI** | `https://webapi.bps.go.id/v1/api` | Pemerintah | API (key: `06fd6...`) | ✅ **BERHASIL** | CSV: Kesehatan (Var 222), Investasi PMDN (Var 793/794), Ekspor (Var 2346/2347), PDRB (eksplorasi) | API key gratis. Rate limit ~1.5s/request. Var ID harus dicari manual. |
| 2 | **BPS Sulsel Ekspor** | `https://sulsel.bps.go.id` (download Excel) | Pemerintah | Manual download | ✅ **BERHASIL** | Excel: `exim_sulsel.bps.go.id_*.xlsx` — Ekspor per komoditas/pelabuhan/negara, 2020-2026 | 518 baris x 215 kolom. Data detail HS code + 5 negara tujuan. |
| 3 | **BPS Query Builder (6 Provinsi)** | `sulut/sulteng/sulsel/sultra/gorontalo/sulbar.bps.go.id` | Pemerintah | Manual download (Cloudflare block scraping) | ⚠️ **SEBAGIAN** | CSV per provinsi: PAD (padsulut, padsulsel, padsulbar, padsultra, padgorontalo) — sulteng tidak tersedia | Cloudflare Turnstile block Playwright/Scrapling. Manual download saja. |
| 4 | **BPS Static Table** | `bps.go.id` static tables | Pemerintah | Scrapling | ❌ **GAGAL** | — | Table hanya sampai 2013 untuk ekspor. Metadata incomplete (30,613 tables, mayoritas not-available). |
| 5 | **ESDM MinerbaOne** | `https://minerbaone.esdm.go.id` | Pemerintah | Scrapling (StealthyFetcher + XHR intercept) | ✅ **BERHASIL** | CSV: `minerbaone_details.csv`, `minerbaone_permits.csv`, `minerbaone_direksi.csv`, `minerbaone_pemegang_saham.csv` | Scraping semua perusahaan mining Sulawesi. |
| 6 | **ESDM MODI** | `https://modi.esdm.go.id` | Pemerintah | Scrapling attempt | ❌ **GAGAL** | — | Auth wall. Butuh login formal / request resmi ke BKPMD. 7,527 perusahaan total. |
| 7 | **ESDM Geoportal** | `https://geoportal.esdm.go.id` | Pemerintah | Explorasi | ⚠️ **SEBAGIAN** | Referensi peta, bukan data tabular | Lebih ke visualisasi GIS, tidak ada bulk download. |
| 8 | **KLHK SIPSN** | `https://sipsn.menlhk.go.id` / `https://sipsn.kemenlh.go.id` | Pemerintah | Explorasi | ❌ **GAGAL** | — | Butuh akun / potentially bayar. Domain baru `kemenlh.go.id` aktif (2024+). |
| 9 | **KLHK PROPER** | `https://proper.menlhk.go.id` | Pemerintah | Explorasi | ❌ **GAGAL** | — | Rating perusahaan, tapi tidak ada bulk data. |
| 10 | **DJPK Kemenkeu** | `https://djpk.kemenkeu.go.id` | Pemerintah | Explorasi / Scrapling attempt | ❌ **GAGAL** | — | Data PAD per Kab/Kota ada di sini tapi Cloudflare block. Sumber data anggaran LH (via SLHI citation). |
| 11 | **Kemendag** | `https://kemendag.go.id` | Pemerintah | Explorasi | ❌ **GAGAL** | — | Data ekspor per provinsi tidak tersedia publik. |
| 12 | **Open Data Sulawesi Utara** | `https://opendata.sulutprov.go.id` | Pemerintah (Regional) | Scrapling (CKAN API) | ✅ **BERHASIL** | 19 CSV: IKA 2020-2024, IKAL 2020-2024, Status Mutu Sungai 2020-2024, IKA/Udara/Lahan/LH per Kab/Kota 2024 | CKAN API: `/api/3/action/package_search`. 23 dataset "kualitas air". |
| 13 | **Open Data Sulawesi Barat** | `https://opendata.sulbarprov.go.id` | Pemerintah (Regional) | Web scraping | ⚠️ **BELUM DICOBA** | Target: IKA, IKU, data lingkungan per kab/kota | ✅ HTTP 200. API merespons tapi JSON parsing gagal. Perlu HTML parsing (BeautifulSoup). |
| 14 | **Satu Data Sulawesi Selatan** | `https://satudata.sulselprov.go.id` | Pemerintah (Regional) | Web scraping | ⚠️ **BELUM DICOBA** | Target: IKA, IKU, data lingkungan per kab/kota | ✅ HTTP 200 (Web) / ❌ 404 (API). Tidak pakai CKAN. Harus scrape via HTML. |
| 15 | **Satu Data Sulawesi Tengah** | `https://satudata.sultengprov.go.id` | Pemerintah (Regional) | Web scraping | ⚠️ **BELUM DICOBA** | Target: IKA, IKU, data lingkungan per kab/kota | ✅ HTTP 200 (Web) / ❌ 404 (API). Mesin berbeda dari Sulsel. Harus scrape HTML. |
| 16 | **SIMDATA Sulawesi Tenggara** | `https://simdata.sultraprov.go.id` | Pemerintah (Regional) | Web scraping | ⚠️ **BELUM DICOBA** | Target: IKA, IKU, data lingkungan per kab/kota | ✅ HTTP 200 (Web) / ❌ 404 (API). SIMDATA custom. Harus scrape HTML. |
| 17 | **Open Data Gorontalo** | `https://data.gorontaloprov.go.id` | Pemerintah (Regional) | Web scraping | ⚠️ **BELUM DICOBA** | Target: IKA, IKU, data lingkungan per kab/kota | Belum diuji. CKAN / Custom. Cek API dulu, fallback ke HTML parsing. |
| 18 | **SLHI (via BPS)** | `https://www.bps.go.id` (publikasi SLHI tahunan) | Pemerintah | Download PDF | ✅ **BERHASIL** | PDF: SLHI 2015-2025 (11 files). Data IKU, IKA, IKL, IKTL, IKAL, Anggaran LH per provinsi. | IKU sudah diekstrak. IKA/IKL/IKTL/IKAL masih di dalam PDF. |
| 19 | **BPS 1372** | `bps.go.id` (tabel 1372) | Pemerintah | Download | ⚠️ **BELUM DICEK** | HTML + Excel: `bps_1372.html`, `bps_1372.xlsx` — Status Kualitas Air Sungai 2007-2016 | Belum diinvestigasi isinya. |
| 20 | **NSWI BKPM** | `https://nswi.bkpm.go.id` | Pemerintah | Explorasi | ❌ **GAGAL** | — | Data investasi per perusahaan, butuh auth. |
| 21 | **KLHK SIMONTANA** | `http://simontana.menlhk.go.id` | Pemerintah | Web scraping + manual | ⚠️ **BELUM DICOBA** | Target: Laju deforestasi per provinsi, tutupan hutan, peta interaktif, download PDF/Excel/Shapefile | Sistem Monitoring Hutan Nasional. Prioritas #1 untuk data deforestasi Sulawesi. |
| 22 | **KLHK Statistik** | `http://statistik.menlhk.go.id` / `http://data.menlhk.go.id` | Pemerintah | Explorasi | ⚠️ **BELUM DICOBA** | Target: Statistik Lingkungan Hidup Kehutanan, deforestasi netto/bruto, perubahan tutupan lahan | Portal data terbuka KLHK. Alternatif jika SIMONTANA tidak bisa diakses. |
| 23 | **KLHK SITALA** | `https://sitala.kemenlh.go.id` | Pemerintah | Web portal | ⚠️ **BELUM DICOBA** | Target: Data IKLH/IRLH (Indeks Kualitas Lingkungan Hidup) per provinsi | Sistem baru pengganti `iklh.menlhk.go.id`. Domain `kemenlh.go.id` (Kementerian LH baru, pemecahan KLHK 2024-2029). ✅ HTTP 200. |
| 24 | **KLHK SIRAJA** | `https://pelayananterpadu.menlhk.go.id` | Pemerintah | Portal (login required) | 🔒 **TERKUNCI** | Target: Data pelaporan Limbah B3 korporasi (smelter/tambang) | Portal pelaporan limbah B3. Enkripsi Festronik, wajib login perusahaan/pemerintah. **Data publik ditutup.** |
| 25 | **KLHK Amdalnet** | (subdomain KLHK) | Pemerintah | Portal (login required) | 🔒 **TERKUNCI** | Target: Dokumen AMDAL/RKL-RPL per perusahaan | Publik hanya bisa lihat status persetujuan. PDF RKL-RPL dikunci (login pemrakarsa/pemerintah). Akses publik butuh sengketa informasi (KIP). |
| 26 | **KemenLH (portal utama)** | `https://kemenlh.go.id` | Pemerintah | Web portal | ⚠️ **BELUM DICOBA** | Target: Publikasi, data, kebijakan Kementerian Lingkungan Hidup (baru) | ✅ HTTP 200. Kementerian baru hasil pemecahan KLHK (2024-2029). |
| 27 | **BPS SIMDASI** | `webapi.bps.go.id` (interoperabilitas/simdasi) | Pemerintah | API | ⚠️ **BELUM DICOBA** | Target: Tabel SIMDASI per wilayah (7 digit MFD code), subjek lingkungan, master table | Endpoint: `/id/22/` (subjects), `/id/23/` (tables by area), `/id/25/` (detail). MFD code: 7100-7600 (Sulawesi). |
| 28 | **BPS SDGs API** | `webapi.bps.go.id` (model=sdgs, domain=0000) | Pemerintah | API | ⚠️ **BELUM DICOBA** | 100+ indikator SDGs: kemiskinan, kesehatan, pendidikan, lingkungan (sanitasi, limbah B3, air) | Var relevan: 1281 (Limbah B3), 1279 (Limbah Industri), 1273 (Sanitasi), 1481 (Obesitas→kesehatan). |
| 29 | **BPS Foreign Trade API** | `webapi.bps.go.id` (dataexim) | Pemerintah | API | ⚠️ **BELUM DICOBA** | Data ekspor/impor: HS Code, nilai (USD), berat (kg), pelabuhan, negara tujuan | Endpoint: `/v1/api/dataexim/`. Param: sumber (1=ekspor,2=impor), kodehs, tahun. |
| 30 | **data.go.id** | `https://data.go.id` | Pemerintah (Nasional) | Portal web + dorking | ⚠️ **BELUM DICOBA** | Target: Portal data terbuka nasional, dataset lingkungan hidup Indonesia | Dorking: `site:data.go.id "lingkungan hidup" filetype:csv`. |
| 31 | **OSS (Online Single Submission)** | `https://oss.go.id` | Pemerintah | Portal (login) | 🔒 **TERKUNCI** | Target: Dokumen AMDAL sebagai syarat perizinan berusaha | Terintegrasi dengan Amdalnet. Data ada tapi tidak publik. |
| 32 | **Kemenperin** | `https://kemenperin.go.id` | Pemerintah | Dorking | ⚠️ **BELUM DICOBA** | Target: Data smelter nikel, investasi industri, kapasitas produksi per perusahaan | Dorking: `site:kemenperin.go.id smelter nikel investasi sulawesi`. Referensi dari DORKING_PLAN_MINING_INVESTMENT. |
| 33 | **BIG (Badan Informasi Geospasial)** | `https://big.go.id` | Pemerintah | Web portal | ⚠️ **BELUM DICOBA** | Target: One Map Policy, peta batas wilayah, peta tematik lingkungan, data geospasial Sulawesi | Geoportal One Map (BIG/KLHK). Referensi dari PRD Fase 1 dan ESDM_DATA_ASSESSMENT. |

---

## Sumber NGO / Lembaga Non-Pemerintah

| # | Portal | URL | Tipe | Metode Akses | Status | Data yang Diperoleh | Keterangan |
|:---:|---|---|:---:|:---:|:---:|---|---|
| 34 | **Tanahkita.id** (KPA/YLBHI) | `https://tanahkita.id` | NGO | Scrapling (XHR intercept, pagination) | ✅ **BERHASIL** | CSV: `tanahkita_konflik.csv` — 568 konflik agraria nasional (judul, lokasi, tahun, status, deskripsi). Filtered: 53 kasus Sulawesi. | 15+ iterasi script. Website async, pagination kompleks. |
| 35 | **WALHI Sulawesi** (semua regional) | `walhi.or.id` + regional | NGO | Download + OSINT | ✅ **BERHASIL** (Sultra) | PDF: WALHI Sultra research. Target: WALHI Sulsel/Sulteng/Sultra/Utara reports 2016-2024 | WALHI Sultra done. Regional lain perlu dorking tambahan. |
| 36 | **JATAM** (Jaringan Advokasi Tambang) | `jatam.org` | NGO | OSINT | ⚠️ **BELUM DICOBA** | Target: Laporan advokasi tambang, dampak deforestasi, kasus lingkungan Sulawesi | Cross-reference dengan data MinerbaOne. |
| 37 | **Auriga Nusantara** | `https://www.auriga.or.id` | NGO | Email collaboration | ⚠️ **BELUM DICOBA** | Target: Peta deforestasi tahunan Indonesia, laporan investigasi Sulawesi, korelasi tambang-deforestasi | NGO forest monitoring terkemuka. Request: auriga@auriga.or.id |
| 38 | **KPA (Konsorsium Pembaruan Agraria)** | `https://kpa.or.id` | NGO | Download PDF | ✅ **BERHASIL** | 9 PDF CATAHU (Catatan Akhir Tahun) 2016-2025. Belum di-parse. | Summary statistik konflik per tahun + breakdown sektor. |
| 39 | **WALHI Sultra** | (via download langsung) | NGO | Download PDF | ✅ **BERHASIL** | PDF: `Riset-Final-WALHI-SULTRA.pdf` — riset dampak industri nikel di Sultra | Data kualitatif + beberapa data kuantitatif limbah. |
| 40 | **ARKL Morowali** | (via download langsung) | NGO/Akademisi | Download PDF | ✅ **BERHASIL** | PDF: `ARKL_Morowali.pdf`, `buku-arkl-morowali-summary.pdf` — Analisis risiko lingkungan Morowali | Data limbah B3, dampak smelter. |
| 41 | **Arinto Sangadji** | (via download langsung) | Akademisi | Download PDF | ✅ **BERHASIL** | PDF: `Arinto-Sangadji-HPAL-dalam-Industri-Nikel-Nov-2024.pdf` — riset HPAL dalam industri nikel | Analisis teknologi dan dampak lingkungan. |

---

## Sumber Akademis / Internasional / 3rd Party

| # | Portal | URL | Tipe | Metode Akses | Status | Data yang Diperoleh | Keterangan |
|:---:|---|---|:---:|:---:|:---:|---|---|
| 42 | **CGS (Center for Global Sustainability)** | (University of Maryland) | Akademis | Download dataset | ✅ **BERHASIL** | Excel: `CGS_Nickel_Smelter_Dataset_V1.xlsx` — 31 smelter nikel Indonesia (21 di Sulawesi). Company, lokasi, kapasitas, status, koordinat. | Dataset paling lengkap untuk smelter nikel. |
| 43 | **UMD Nickel Indonesia Brief** | (University of Maryland) | Akademis | Download PDF | ✅ **BERHASIL** | PDF: `UMD_NickelIndonesia_Brief2025.pdf` — research brief komprehensif industri nikel Indonesia | Analisis dampak, produksi, ekspor, policy. |
| 44 | **GEM (Global Energy Monitor)** | `https://globalenergymonitor.org` | NGO Internasional | Download Excel | ✅ **BERHASIL** | 30+ Excel files: Coal Mine Tracker, Coal Plant Tracker, GMET (metal mining), LNG, dll. | Scope global. Sebagian dipakai untuk cross-reference Sulawesi. |
| 45 | **OpenAQ** | `https://openaq.org` / `https://api.openaq.org` | NGO (API) | API client (v3) | ❌ **DATA CORRUPT** | CSV: `sulawesi_locations.csv` — **DATA TIDAK VALID**: lokasi "Makassar" padahal country = Ghana | API key: `e60fb...`. **Indonesia TIDAK ADA** di coverage OpenAQ. Batalkan. |
| 46 | **NASA FIRMS** | `https://firms.modaps.eosdis.nasa.gov` | Pemerintah (AS) | API (registrasi gratis) | ⚠️ **BELUM DICOBA** | Fire hotspots VIIRS/MODIS 2000-sekarang. Proxy deforestasi: korelasi hotspot ↔ izin tambang | API: `firms.modaps.eosdis.nasa.gov/api/`. Overlay dengan MinerbaOne. |
| 47 | **Bhumi ATR/BPN** | `https://bhumi.atrbpn.go.id` | Pemerintah | Explorasi | ❌ **GAGAL** | — | Peta tanah, tidak ada bulk download konflik. |
| 48 | **Copernicus/ESA Land Cover** | `https://land.copernicus.eu/global/products/lc` | Internasional (EU) | Download / Google Earth Engine | ⚠️ **BELUM DICOBA** | Land cover 100m resolusi global, deteksi perubahan tahunan, klasifikasi hutan/lahan/urban | Cross-validasi GFW. |
| 49 | **GRID-Arendal (Global Tailings Portal)** | `https://tailing.grida.no/` | PBB/Internasional | Portal web | ⚠️ **BELUM DICOBA** | Database tailing bendungan seluruh dunia. Filter: Indonesia → nikel → Sulawesi | Sumber PBB. |
| 50 | **UN Statistics Division** | `https://unstats.un.org/unsd/environment/` | PBB/Internasional | Download PDF | ✅ **BERHASIL** | **Mirror resmi SLHI 2015-2021** (7 PDF) | Sumber paling reliable untuk SLHI historical. |
| 51 | **Neliti** | `https://www.neliti.com` | Akademis | Download PDF | ✅ **BERHASIL** | Host SLHI 2016 PDF | Digital library Indonesia. |
| 52 | **CIFOR** | `https://www.cifor.org/knowledge/data/` | Akademis/NGO | Download + email | ⚠️ **BELUM DICOBA** | Target: Forest cover change datasets, deforestation drivers | Contact: dataservices@cifor.org |
| 53 | **IPCC EFDB** | `https://www.ipcc-nggip.iges.or.jp/EFDB/` | Internasional | Portal web | ⚠️ **BELUM DICOBA** | Target: Emission Factor Database — faktor emisi CO2 dari sampah, limbah, perubahan lahan | Referensi dari KLHK_DATA_SOURCES. |
| 54 | **GFN (Global Footprint Network)** | `http://data.footprintnetwork.org/` | Internasional (NGO) | Portal web | ⚠️ **BELUM DICOBA** | Target: Data biokapasitas, EQF, YF per negara | EQF forest=1.26, cropland=2.51; YF Indonesia forest=0.87, cropland=0.82. |
| 55 | **Google Earth Engine** | `https://earthengine.google.com` | Internasional (Google) | Python API | ⚠️ **BELUM DICOBA** | Target: Land cover change, NDVI, forest loss via satellite | Python API: `ee.Initialize()`. Cross-validasi GFW. |

---

## OSINT / Search / Media / Investasi

| # | Portal | URL | Tipe | Metode Akses | Status | Data yang Diperoleh | Keterangan |
|:---:|---|---|:---:|:---:|:---:|---|---|
| 56 | **Google CSE (Custom Search Engine)** | `cse.google.com` | OSINT | API (dorking) | ✅ **BERHASIL** | 320+ URLs ditemukan untuk IKU historical | 35+ targeted queries. |
| 57 | **DuckDuckGo / Google Dorks** | Various | OSINT | Manual + scripted | ✅ **BERHASIL** | AMDAL PDFs (42 files), CATAHU KPA, NGO reports, SLHI historical | `filetype:pdf + company name + AMDAL/konflik/lingkungan` |
| 58 | **Mongabay / Media Lingkungan** | `https://mongabay.co.id` | Media | OSINT | ⚠️ **SEBAGIAN** | Referensi kasus, bukan data tabular | Untuk konteks dan validasi temuan. |
| 59 | **Pasal.id** | `https://pasal.id` | Hukum | Explorasi | ❌ **GAGAL** | — | Database putusan, tidak ada bulk access. |
| 60 | **Putusan MA** | `https://putusan3.mahkamahagung.go.id` | Hukum | Explorasi | ❌ **GAGAL** | — | Putusan pengadilan, sulit filter per kasus lingkungan. |
| 61 | **S&P Global Market Intelligence** | (berbayar) | Komersial | Dorking | ⚠️ **OPSIONAL** | Target: Mine Economics, estimasi biaya pengelolaan limbah tailing | Opsi tingkat lanjut. |
| 62 | **Benchmark Mineral Intelligence** | (berbayar) | Komersial | Dorking | ⚠️ **OPSIONAL** | Target: ESG nickel tailings, jejak karbon rantai pasok EV | Dork: `"Benchmark Mineral Intelligence" ESG nickel tailings Indonesia` |
| 63 | **satu-data.go.id** | `https://satu-data.go.id` | Pemerintah (Nasional) | Portal web + dorking | ⚠️ **BELUM DICOBA** | Target: Portal Satu Data Indonesia, dataset IKLH, kualitas udara | Dorking: `site:satu-data.go.id "IKLH" 2014..2016`. |
| 64 | **Wayback Machine (Web Archive)** | `https://web.archive.org` | Internasional | OSINT / Archive | ⚠️ **BELUM DICOBA** | Target: Arsip halaman KLHK/BPS lama yang sudah dihapus/migrasi | Dorking: `site:web.archive.org "bps.go.id" "SLHI 2014"`. |
| 65 | **PPID BPS** | `https://ppid.bps.go.id` | Pemerintah | Permintaan informasi | ⚠️ **BELUM DICOBA** | Target: Data SLHI arsip, dokumen publik BPS | Portal Keterbukaan Informasi Publik BPS. |
| 66 | **PPID KLHK** | `https://ppid.menlhk.go.id` | Pemerintah | Permintaan informasi | ⚠️ **BELUM DICOBA** | Target: Dokumen lingkungan hidup, SLHI lama, data limbah B3 | Portal PPID Kementerian LHK. |
| 67 | **IDX (Bursa Efek Indonesia)** | `https://www.idx.co.id` | Keuangan | Dorking | ⚠️ **BELUM DICOBA** | Target: Laporan keuangan perusahaan tambang terdaftar (ANTAM, MBMA, INCO) — capex, investasi nikel | URL: `idx.co.id/perusahaan-tercatat/laporan-keuangan-dan-tahunan/`. Referensi dari INVESTMENT_DATA_DORKING_PLAN. |
| 68 | **OJK (Otoritas Jasa Keuangan)** | `https://ojk.go.id` | Pemerintah | Dorking | ⚠️ **BELUM DICOBA** | Target: Data regulasi keuangan perusahaan tambang, laporan tahunan | Dorking: `site:ojk.go.id [NAMA_PERUSAHAAN] investasi tambang`. |
| 69 | **ANTAM Investor Relations** | `https://www.antam.com/id/investor-relations` | Perusahaan | Dorking / PDF | ⚠️ **BELUM DICOBA** | Target: Laporan tahunan ANTAM, capex nikel Pomalaa/Kolaka, kapasitas produksi | Perusahaan tambang nikel terdaftar di IDX. |
| 70 | **Vale Indonesia Investor** | `https://www.vale.com/indonesia/en/investors` | Perusahaan | Dorking / PDF | ⚠️ **BELUM DICOBA** | Target: Annual report, production capacity, investment Sorowako | Perusahaan tambang nikel terbesar di Sulsel. |

---

## Portal Data Kesehatan

| # | Portal | URL | Tipe | Metode Akses | Status | Data yang Diperoleh | Keterangan |
|:---:|---|---|:---:|:---:|:---:|---|---|
| 71 | **Kemenkes Pusdatin** | `https://pusdatin.kemkes.go.id` (Profil Kesehatan Indonesia PDF) | Pemerintah | Download PDF + Camelot parsing | ✅ **BERHASIL** | 13 PDF Profil Kesehatan (2014-2024). Diekstrak: ISPA/Pneumonia, Diare, Malaria, Kusta, Puskesmas, RS per provinsi. | 110+ CSV raw files. |
| 72 | **BPS Var 222** | `webapi.bps.go.id` (Var 222) | Pemerintah | API | ✅ **BERHASIL** | CSV: Keluhan Kesehatan Umum (%) per provinsi 2014-2024 | Data makro, 10 tahun lengkap. |
| 73 | **BPS Var 42** | `webapi.bps.go.id` (Var 42) | Pemerintah | API | ⚠️ **SEBAGIAN** | CSV: Kasus Penyakit (2014-2015 saja). ISPA & Penyakit Kulit tidak ada sebagai variabel terpisah. | Data 2016+ tidak tersedia di BPS API. |

---

## Data Deforestasi & Kehutanan (Prioritas)

> **PRIORITAS #1** untuk deforestasi. Cross-reference: KLHK SIMONTANA (#21), CIFOR (#52), Auriga Nusantara (#37), Copernicus/ESA (#48).

| # | Portal | URL | Tipe | Metode Akses | Status | Keterangan |
|:---:|---|---|:---:|:---:|:---:|---|
| — | **Global Forest Watch (GFW)** ⭐ | `https://www.globalforestwatch.org` / API: `data.globalforestwatch.org` + `production-api.globalforestwatch.org` | Internasional (NGO) | API (gratis) | ⚠️ **BELUM DICOBA** | Tree cover loss 2001-2023, 30m, GLAD/RADD alerts. Hansen et al. (2013, Science). SDK: `pip install gfwpy`. API v1: `production-api.globalforestwatch.org`, v2: `data-api.globalforestwatch.org`. |

> GFW tidak diberi nomor karena merupakan cross-reference prioritas dari section Akademis/Internasional.

---

## Ringkasan

### Statistik

| Status | Jumlah |
|---|:---:|
| ✅ Berhasil | **21** |
| ⚠️ Sebagian / Terbatas / Belum Dicoba | **38** |
| ❌ Gagal / Data Corrupt | **9** |
| 🔒 Terkunci (Login Required) | **3** |
| ❓ Opsi (berbayar) | **2** |
| **Total** | **73** |

### Data yang Berhasil Diambil per Jenis

| Jenis Data | Format | Jumlah |
|---|---|---|
| Data tabular (CSV/Excel) | CSV, XLSX | ~20 datasets |
| Laporan PDF | PDF | ~70 files (SLHI 2015-2025, CATAHU, AMDAL, NGO, Kemenkes) |
| Metadata/Scraping | CSV | 4 files (minerbaone) |
| Hasil ekstraksi PDF | CSV intermediate | ~150 files |
| **SLHI Historical (via UN Stats)** | PDF | 7 files (2015-2021, mirror resmi BPS) |

### BPS WebAPI — Endpoint yang Sudah Dikenali

| Endpoint | Model | Fungsi | Status |
|---|---|---|---|
| `/v1/api/domain` | domain | Master wilayah (provinsi/kabupaten) | ✅ Digunakan |
| `/v1/api/list` | subject | Daftar subjek statistik | ✅ Digunakan |
| `/v1/api/list` | data | Data dinamis per variabel | ✅ Digunakan (Var 222, 42, 793, 794, 2346, 2347) |
| `/v1/api/list` | subcat | Kategori subjek | ✅ Digunakan |
| `/v1/api/list` | turvar | Derived variable | 📋 Terdokumentasi |
| `/v1/api/list` | th | Period data (tahun) | ✅ Digunakan |
| `/v1/api/list` | var | Variable listing | ✅ Digunakan |
| `/v1/api/list` | vervar | Vertical variable | 📋 Terdokumentasi |
| `/v1/api/list` | unit | Unit data | 📋 Terdokumentasi |
| `/v1/api/list` | statictable | Static table listing | ❌ Gagal (data sampai 2013 saja) |
| `/v1/api/view` | statictable | Detail static table | 📋 Terdokumentasi |
| `/v1/api/view` | pressrelease | Detail press release | 📋 Terdokumentasi |
| `/v1/api/list` | pressrelease | List all press releases | 📋 Terdokumentasi |
| `/v1/api/view` | publication | Detail publication (PDF, ISSN) | 📋 Terdokumentasi |
| `/v1/api/list` | publication | List all publications | 📋 Terdokumentasi |
| `/v1/api/list` | indicators | Strategic indicators | 📋 Terdokumentasi |
| `/v1/api/list` | infographic | List infographics (481 items) | 📋 Terdokumentasi |
| `/v1/api/list` | glosarium | Glosarium (5078 items, bilingual) | 📋 Terdokumentasi |
| `/v1/api/view` | glosarium | Detail statistical concept | 📋 Terdokumentasi |
| `/v1/api/dataexim/` | — | Foreign trade (HS code, USD, kg) | 📋 Terdokumentasi |
| `/v1/api/list` | sdgs | SDGs (100+ indikator, domain=0000) | 📋 Terdokumentasi |
| `/v1/api/list` | sdds | SDDS (48+ macro indicators) | 📋 Terdokumentasi |
| `/v1/api/list` | subcatcsa | CSA Subject Categories | 📋 Terdokumentasi |
| `/v1/api/list` | subjectcsa | CSA Subject | 📋 Terdokumentasi |
| `/v1/api/list` | newscategory | News categories | 📋 Terdokumentasi |
| `/v1/api/list` | news | BPS News | 📋 Terdokumentasi |
| `/v1/api/list` | kbli2020/kbki2015 | Statistical Classifications | 📋 Terdokumentasi |
| `/v1/api/interoperabilitas/sensus/` | — | Census Data (events, topics, areas) | 📋 Terdokumentasi |
| `/v1/api/interoperabilitas/simdasi/` | — | SIMDASI (subjects, tables, MFD codes) | 📋 Terdokumentasi |
| `/v1/api/list/` | — | Searching (keyword, domain) | 📋 Terdokumentasi |

### Tools yang Digunakan

| Tool | Penggunaan |
|---|---|
| `requests` + BPS API | Data BPS (kesehatan, PMDN, ekspor) |
| **Scrapling** (StealthyFetcher) | MinerbaOne ESDM, Tanahkita, BPS Query Builder |
| **Camelot / Tabula-py** | PDF parsing Kemenkes, KPA, NGO reports |
| **Google CSE API** | OSINT dorking (320+ URLs) |
| **Pandas** | Semua data processing & cleaning |
| **PageIndex** (VectifyAI) | RAG tanpa chunking untuk PDF parsing (rencana Phase 12) |
| **GHunt** (mxrch) | Google OSINT framework untuk penelusuran peneliti |

---

## Catatan Pembaruan

### Update Sesi 4 — Final v2 (14 Juni 2026):
- ✅ Tambah **5 portal Open Data Regional**: Sulbar, Sulsel, Sulteng, Sultra, Gorontalo
- ✅ Tambah **4 portal KLHK baru**: SITALA, SIRAJA, Amdalnet, KemenLH (domain baru)
- ✅ Tambah portal nasional: **data.go.id**, **satu-data.go.id**, **OSS**
- ✅ Tambah portal PPID: **PPID BPS**, **PPID KLHK**
- ✅ Tambah referensi internasional: **IPCC EFDB**, **GFN**, **Google Earth Engine**
- ✅ Tambah **Wayback Machine** untuk arsip halaman lama
- ✅ Tambah portal investasi: **IDX**, **OJK**, **Kemenperin**, **BIG**, **ANTAM IR**, **Vale IR** (dari DORKING_PLAN_MINING_INVESTMENT & INVESTMENT_DATA_DORKING_PLAN)
- ✅ Upgrade OpenAQ: API v3, status tetap ❌ DATA CORRUPT
- ✅ Upgrade GFW: tambah API v1 (`production-api`) & v2 (`data-api`) URLs
- ✅ Section Deforestasi: hapus duplikat, hanya GFW sebagai entri prioritas
- ✅ Rename section OSINT → "OSINT / Search / Media / Investasi"
- ✅ Statistik final: 21 berhasil, 38 belum/sebagian, 9 gagal, 3 terkunci, 2 opsional = **73 portal total**
