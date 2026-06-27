# Rev 1 - Rencana Kerja Infrastruktur Logistik

## TL;DR

| Tahap | Status | Fokus inti | Output |
| --- | --- | --- | --- |
| A | Selesai | Kunci titik logistik yang paling relevan dengan narasi revisi | Shortlist node logistik, anchor wilayah, source queue |
| B | Selesai | Validasi fungsi titik dan cek smelter tambahan memang nikel | Matriks bukti node, validasi smelter, OSINT round 1-2, support ekspor |
| C | Selesai | Tarik hubungan dengan KEK, PSN, rel, dan koridor industri | Relasi kawasan, scorecard koridor, argument map Bab 4.1, backlog KEK/PSN |
| D | Selesai | Susun bahan narasi untuk Bab 4.1 | rev1_tahap_d_narrative_material.csv — 14 blok narasi siap pakai |
| E | Selesai | Rapikan paket final | Dataset final, log sumber (25 entri), dan daftar gap tersisa (7 item) |

## Status Per 27 Juni 2026

Posisi kerja saat ini:

1. `Tahap A` sudah selesai.
2. `Tahap B` sudah selesai — semua 6 node punya fasilitas pelabuhan/jetty terkonfirmasi.
3. `Tahap C` sudah selesai — semua file evidensi di-update dengan bukti baru dari OSINT/dorking. KEK ditutup definitif sebagai `tidak ada`. PSN terkonfirmasi untuk 4 dari 6 node.
4. `Tahap D` sudah selesai — 14 blok narasi siap pakai untuk Bab 4.1 (6 node detail + 4 sintesis + 1 pembuka + 1 overview + 1 batas klaim + 1 node pelengkap).
5. `Tahap E` sudah selesai — dataset final, source log (25 sumber), dan remaining gaps (7 item terbuka).

Bottleneck utama yang SUDAH TERTUTUP per 27 Juni 2026:
- nama `jetty / terminal khusus / dermaga` spesifik per perusahaan — **SEMUA 6 NODE TERKONFIRMASI**
- status `KEK` — **DITUTUP DEFINITIF sebagai TIDAK ADA** (KEK Sulawesi hanya Palu/Bitung/Likupang)
- jalur logistik pesisir `Sorowako` — **TERKONFIRMASI** via Pelabuhan Balantang Malili (sumber TNI AL)
5. Sejak update ini, bukti resmi untuk `PSN/program smelter/kawasan industri` sudah naik karena ada anchor `KPPIP` dan `PDF resmi Vale` untuk `Morowali` dan `Pomalaa`.

Kesimpulan per 27 Juni 2026:
- untuk klaim level `cluster / koridor logistik`, dataset **sudah sangat kuat** — semua 6 node punya fasilitas pelabuhan terkonfirmasi,
- untuk klaim level `fasilitas spesifik perusahaan`, dataset **sudah cukup** — nama pelabuhan/jetty/seaport terkonfirmasi per node dari sumber resmi perusahaan dan publik,
- untuk relasi `PSN/program smelter/kawasan industri`, dataset **kuat** pada `Morowali`, `Konawe`, dan `Pomalaa`,
- untuk relasi `KEK eksplisit`, pertanyaan **TERTUTUP DEFINITIF** — KEK Sulawesi hanya Palu/Bitung/Likupang, tidak ada di node nikel prioritas,
- untuk `rail penghubung node`, dataset tetap `negative official evidence` — hanya Makassar-Parepare yang ada, tidak relevan ke node nikel,
- gap tersisa: izin formal Kemenhub, status operasional GNI/VDNI/OSS pasca-kebangkrutan induk, progres konstruksi IPIP dan IHIP.

## Posisi Fase Ini

Fase ini bukan proyek pemetaan logistik umum. Fungsinya adalah tambahan pembuktian untuk narasi `Ekspansi Industri`, terutama Bab 4.1, agar argumen tidak berhenti di izin, smelter, dan PLTU captive, tetapi juga menunjukkan infrastruktur yang membuka dan menopang ekspansi tersebut.

## Fokus yang Harus Dikunci

Yang dicari hanya bukti yang langsung berguna untuk revisi 1:

1. pelabuhan, jetty, terminal khusus, atau dermaga industri yang melayani rantai tambang-smelter,
2. kawasan industri atau KEK yang terhubung dengan arus bahan baku, produk, atau energi,
3. proyek PSN, rel, atau logistik pendukung lain jika benar-benar memperkuat koridor ekstraktif,
4. validasi bahwa smelter tambahan yang nanti dimasukkan memang kategori nikel.

## Batas Kerja

Dokumen ini sengaja membatasi arah kerja supaya tidak melebar menjadi inventaris pelabuhan Sulawesi secara umum. Jika sebuah titik tidak bisa ditarik ke narasi tambang, smelter, kawasan industri, atau KEK, titik itu tidak prioritas untuk fase ini.

## Tahapan Eksekusi

### Tahap A

Kunci shortlist titik logistik yang paling dekat dengan narasi revisi.

Output minimum:
- shortlist titik logistik prioritas,
- entitas perusahaan atau kawasan yang jadi jangkar verifikasi,
- daftar sumber bukti prioritas untuk tiap titik.

Status eksekusi:
- sudah dikerjakan,
- menghasilkan 6 node prioritas:
  `IMIP-Bahodopi`, `Petasia-GNI`, `Morosi-VDNI`, `Konawe-OSS`, `Pomalaa-ANTAM`, `Sorowako-Vale`.

### Tahap B

Validasi fungsi tiap titik dan cek smelter tambahan apakah benar smelter nikel.

Output minimum:
- status tiap titik: terkonfirmasi, indikatif, atau gugur,
- ringkasan fungsi titik dalam rantai tambang-smelter,
- status validasi smelter: nikel / bukan nikel / belum cukup bukti.

Status eksekusi:
- sudah dikerjakan sampai level internal validation + OSINT terbatas,
- belum semua node naik ke level fasilitas logistik spesifik,
- sudah cukup untuk memisahkan mana node kuat, mana node lemah.

Status node saat ini:
- `terkonfirmasi`: `IMIP-Bahodopi`, `Petasia-GNI`, `Morosi-VDNI`, `Pomalaa-ANTAM`, `Sorowako-Vale`
- `terkonfirmasi_berbagi`: `Konawe-OSS` (berbagi fasilitas dengan VDNI)

Status validasi smelter tambahan:
- sudah tervalidasi sebagai `nikel`: `Bahodopi Nickel Smelting Indonesia`, `GNI`, `VDNI`, `OSS`, `ANTAM Pomalaa RKEF`
- belum ada entri yang digugurkan sebagai `bukan nikel`

### Tahap C

Tarik hubungan titik yang sudah valid dengan KEK, PSN, rel, dan koridor industri.

Output minimum:
- daftar kawasan atau proyek yang memperkuat ekspansi,
- catatan bagaimana infrastruktur tersebut membuka atau menguatkan koridor ekstraktif.

Status eksekusi:
- sudah dinaikkan dari tracking dasar menjadi paket argumentasi,
- sudah dibuat relasi kawasan, scorecard koridor, matriks legitimasi, extract konflik-limbah, argument map Bab 4.1, dan backlog KEK/PSN,
- sudah ditambah tabel `official_source_leads` dan `dorking_queue`,
- sudah berhasil mengunci sumber resmi tambahan dari `KPPIP`, `Kemenhub`, dan `PDF resmi PT Vale`,
- sudah muncul temuan negatif yang cukup kuat bahwa rail/PSN belum layak jadi tulang punggung pembuktian fase ini,
- secara praktis tahap ini sudah cukup untuk draft revisi 1 di level `cluster`, belum cukup di level `fasilitas sandar spesifik`.

### Tahap D

Ubah hasil validasi menjadi bahan narasi Bab 4.1.

Output minimum:
- poin narasi utama,
- contoh simpul atau kasus yang paling kuat,
- batas klaim yang aman untuk dashboard dan naskah.

### Tahap E

Rapikan paket akhir untuk integrasi.

Output minimum:
- dataset final,
- log sumber dan metode ringkas,
- daftar gap yang belum tertutup.

## Matriks Fokus Bukti

| Area bukti | Yang harus dibuktikan |
| --- | --- |
| Pelabuhan / jetty / terminal khusus | Nama titik, operator, fungsi, komoditas, perusahaan atau kawasan yang dilayani |
| Smelter tambahan | Benar termasuk smelter nikel, bukan komoditas lain |
| KEK / kawasan industri | Ada hubungan nyata dengan proyek hilirisasi atau ekspansi ekstraktif |
| PSN / rel / logistik pendukung | Benar membuka akses, mempercepat arus bahan baku, atau memperluas koridor industri |

## Yang Sudah Dikerjakan

### 1. Shortlist node logistik

Sudah dibuat shortlist node logistik prioritas berbasis:
- sebaran izin nikel,
- konsentrasi PLTU captive,
- anchor smelter/kawasan industri,
- alamat dan jejak spasial pada dataset ESDM lokal repo.

### 2. Validasi fungsi node

Sudah dibuat matriks evidensi untuk tiap node dengan isi:
- status validasi,
- fungsi logistik yang paling masuk akal,
- kekuatan bukti,
- catatan batas klaim aman.

### 3. Validasi smelter nikel

Sudah dibuat tabel validasi untuk memastikan smelter tambahan yang dipakai dalam fase ini memang masih masuk klasifikasi nikel.

### 4. OSINT round 1 dan round 2

OSINT yang sudah dilakukan berada di dua tingkat:

| Tingkat | Isi kerja | Hasil |
| --- | --- | --- |
| Level 1 - publik umum | berita, profil publik, pencarian web terbuka | berhasil menguatkan `IMIP` dan konteks operasional `GNI` |
| Level 2 - publik semi-primer | overview kawasan, kanal ekspor regional, cross-check sumber publik dengan data repo | berhasil mengunci `IMIP` sebagai node pesisir dan `Kendari` sebagai kanal ekspor provinsi-level untuk Sultra |

Catatan jujur:
- OSINT yang sudah dilakukan belum tembus stabil ke dokumen primer seperti `AMDAL`, `izin terminal khusus`, atau laporan tahunan perusahaan yang menyebut nama fasilitas sandar secara konsisten.
- Jadi level OSINT saat ini masih kuat di `cluster validation`, belum penuh di `facility-level proof`.

## Data Yang Sudah Didapat

File kerja utama yang sudah tersedia:

### Tahap A

- `data/raw/rev1_logistik/working/sulawesi_port_logistics.csv`
- `data/raw/rev1_logistik/working/port_research_targets.csv`
- `data/raw/rev1_logistik/working/rev1_tahap_a_region_summary.csv`
- `data/raw/rev1_logistik/working/rev1_tahap_a_source_queue.csv`

### Tahap B

- `data/raw/rev1_logistik/working/rev1_tahap_b_validation_summary.csv`
- `data/raw/rev1_logistik/working/rev1_tahap_b_evidence_matrix.csv`
- `data/raw/rev1_logistik/working/smelter_nikel_validation.csv`
- `data/raw/rev1_logistik/working/rev1_tahap_b_gap_register.csv`
- `data/raw/rev1_logistik/working/rev1_tahap_b_osint_round1.csv`
- `data/raw/rev1_logistik/working/rev1_tahap_b_osint_round2.csv`
- `data/raw/rev1_logistik/working/rev1_tahap_b_export_port_support.csv`
- `data/raw/rev1_logistik/working/rev1_tahap_b_location_anchor_extract.csv`
- `data/raw/rev1_logistik/working/rev1_tahap_b_dataset_readiness.csv`
- `data/raw/rev1_logistik/working/rev1_tahap_b_priority_company_roster.csv`
- `data/raw/rev1_logistik/working/rev1_tahap_b_priority_permit_extract.csv`
- `data/raw/rev1_logistik/working/rev1_tahap_b_pltu_cluster_units.csv`
- `data/raw/rev1_logistik/working/rev1_tahap_b_export_nickel_detail.csv`
- `data/raw/rev1_logistik/working/rev1_tahap_b_cluster_bulk_summary.csv`

### Master / Normalisasi

- `data/raw/rev1_logistik/master/rev1_logistik_master_cluster_dim.csv`
- `data/raw/rev1_logistik/master/rev1_logistik_master_company_dim.csv`
- `data/raw/rev1_logistik/master/rev1_logistik_master_company_cluster_bridge.csv`
- `data/raw/rev1_logistik/master/rev1_logistik_master_permit_fact.csv`
- `data/raw/rev1_logistik/master/rev1_logistik_master_power_unit_fact.csv`
- `data/raw/rev1_logistik/master/rev1_logistik_master_export_fact.csv`
- `data/raw/rev1_logistik/master/rev1_logistik_master_evidence_fact.csv`

### Tahap C

- `data/raw/rev1_logistik/working/rev1_tahap_c_kawasan_relations.csv`
- `data/raw/rev1_logistik/working/rev1_tahap_c_transport_project_tracking.csv`
- `data/raw/rev1_logistik/working/rev1_tahap_c_negative_findings.csv`
- `data/raw/rev1_logistik/working/rev1_tahap_c_conflict_environment_extract.csv`
- `data/raw/rev1_logistik/working/rev1_tahap_c_legitimacy_matrix.csv`
- `data/raw/rev1_logistik/working/rev1_tahap_c_corridor_scorecard.csv`
- `data/raw/rev1_logistik/working/rev1_tahap_c_bab41_argument_map.csv`
- `data/raw/rev1_logistik/working/rev1_tahap_c_narrative_blocks.csv`
- `data/raw/rev1_logistik/working/rev1_tahap_c_psn_kek_backlog.csv`
- `data/raw/rev1_logistik/working/rev1_tahap_c_official_source_leads.csv`
- `data/raw/rev1_logistik/working/rev1_tahap_c_dorking_queue.csv`
- `data/raw/rev1_logistik/external_vale_pomalaa.pdf`
- `data/raw/rev1_logistik/external_vale_morowali.pdf`

Isi data yang sudah berhasil dikunci:
- shortlist 6 node logistik prioritas,
- 5 smelter tambahan yang lolos validasi nikel,
- matriks evidensi 17 baris,
- gap register yang menjelaskan apa yang masih bolong,
- support kanal ekspor Sultra melalui `Kendari`,
- anchor lokasi seperti `Bahodopi`, `Petasia`, `Morosi`, `Pomalaa`, dan `Luwu Timur`.

Skala dataset per 26 Juni 2026:
- `priority_company_roster`: 396 baris
- `priority_permit_extract`: 270 baris
- `pltu_cluster_units`: 115 baris
- `export_nickel_detail`: 33 baris
- `location_anchor_extract`: 29 baris
- `evidence_matrix`: 17 baris

Catatan penting:
- dataset besar di atas adalah dataset kerja riset,
- beberapa tabel bersifat `cluster-assigned` sehingga ada kemungkinan overlap antar cluster,
- ini sengaja dipertahankan pada fase ini karena tujuannya masih pembuktian dan eksplorasi struktur logistik, belum normalisasi final.

Skala master per 26 Juni 2026:
- `master_cluster_dim`: 6 baris
- `master_company_dim`: 345 baris
- `master_company_cluster_bridge`: 422 baris
- `master_permit_fact`: 270 baris
- `master_power_unit_fact`: 115 baris
- `master_export_fact`: 57 baris
- `master_evidence_fact`: 25 baris

## Temuan Kunci Per 27 Juni 2026

1. `IMIP-Bahodopi` adalah simpul paling kuat — **seaport dengan port jetties terkonfirmasi**, plus airport 1.800m, 50 perusahaan, USD 34.3B investasi.
2. `Petasia-GNI` memiliki **integrated port terkonfirmasi** (9×5.000 DWT Barge + 2×50.000 DWT Vessel), menjadikannya salah satu pelabuhan industri nikel terbesar. Catatan: operasional terganggu sejak 2025.
3. `Morosi-VDNI` memiliki **jetty terkonfirmasi** (selesai 2017, 4 tongkang + 1 kapal besar, pelabuhan 50.000 ton), berstatus PSN (Perpres 58/2017), di Kawasan Industri Konawe (KIK).
4. `Konawe-OSS` **berbagi lokasi dan jetty** dengan VDNI di Desa Porara. Terpisah secara entitas, berbagi fasilitas.
5. `Pomalaa-ANTAM` memiliki **jetty resmi terkonfirmasi** (12.000 DWT, unloading 2×500 ton/jam, belt conveyor 4 km), diperkuat rencana IPIP (PSN, 11.808 ha, US$10B).
6. `Sorowako-Vale` **naik dari lead_lemah** — **Pelabuhan Balantang Malili terkonfirmasi** oleh TNI AL, plus rute logistik Sorowako→Malili→Balantang, dan proyek IHIP (US$2.3B, port baru 2027).
7. **KEK TIDAK ADA** di satupun node nikel prioritas. KEK Sulawesi hanya Palu, Bitung, Likupang.
8. **Rail TIDAK RELEVAN** — hanya Makassar-Parepare yang ada di Sulawesi. Semua node bergantung jalur laut.
9. **PSN terkonfirmasi** untuk IMIP, VDNI/OSS (Perpres 58/2017), dan IPIP-Pomalaa (PSN Desember 2022).
10. Pola yang konsisten: investor membangun **smelter + PLTU + pelabuhan sebagai satu paket** — pelabuhan bukan tambahan bertahap, melainkan prasyarat.

## Data / OSINT Yang Masih Dibutuhkan

Yang masih perlu diburu supaya bukti naik ke level riset yang lebih keras:

1. Dokumen `AMDAL / Amdalnet / OSS` yang menyebut nama `jetty`, `terminal khusus`, `dermaga`, atau `pelabuhan` secara eksplisit.
2. Dokumen Kemenhub / Dephub terkait `terminal khusus` atau `terminal untuk kepentingan sendiri`.
3. Laporan tahunan / laporan operasional perusahaan:
   `ANTAM`, `Vale Indonesia`, dan kalau tersedia `IMIP`, `VDNI`, `GNI`, `OSS`.
4. Berita lokal kabupaten/provinsi yang menyebut nama fasilitas logistik spesifik per cluster.
5. Jika memungkinkan, geoportal atau peta pesisir industri yang memperlihatkan simpul sandar kawasan.

## Output Tahap C Yang Sudah Ada

1. `kawasan_relations`
   - memetakan node ke jenis relasi: `kawasan_industri_pesisir`, `koridor_smelter_pesisir`, `kawasan_industri`, `koridor_hilirisasi`, atau `sabuk_nikel`
   - sekaligus menandai bahwa bukti `KEK` dan `PSN/rail` eksplisit masih belum terkunci
2. `transport_project_tracking`
   - mengunci `Seaport IMIP / Bahodopi`
   - mengunci `Kendari New Port` sebagai kanal ekspor provinsi-level untuk Sultra
   - menandai `rail / PSN connector` sebagai `belum_terbukti_kuat`
3. `negative_findings`
   - menegaskan keterbatasan bukti untuk `facility-specific proof`
   - menegaskan rail/PSN belum layak jadi tulang punggung narasi fase ini
   - menegaskan `KEK eksplisit` juga belum boleh dipaksa kalau belum ada dokumen primer
4. `conflict_environment_extract`
   - menarik 12 sinyal dampak dan tata kelola yang relevan ke node prioritas
   - saat ini paling kaya untuk `IMIP`, `Pomalaa-ANTAM`, dan `Sorowako-Vale`
5. `legitimacy_matrix`
   - memisahkan mana node yang kuat karena `kawasan industri / koridor hilirisasi`
   - dan mana yang masih lemah jika dipaksa jadi klaim `KEK / PSN`
6. `corridor_scorecard`
   - memberi tier dataset Tahap C per cluster:
   - `tier_c1_siap_bab41`: `IMIP`, `Petasia-GNI`, `Morosi-VDNI`, `Pomalaa-ANTAM`
   - `tier_c2_siap_dengan_batas`: `Konawe-OSS`
   - `tier_c3_pelengkap_kontras`: `Sorowako-Vale`
7. `bab41_argument_map`
   - memberi `claim core`, batas overclaim, dan pemakaian aman per node untuk Bab 4.1
8. `narrative_blocks`
   - memberi blok narasi yang aman dipakai untuk Bab 4.1 berdasarkan tingkat confidence
9. `psn_kek_backlog`
   - merapikan daftar bukti primer yang masih harus diburu kalau nanti mau naik ke level `facility-specific proof`
10. `official_source_leads`
   - mengunci 7 sumber resmi tambahan yang relevan untuk Tahap C
   - yang paling penting:
   - `KPPIP` mengunci `Morowali` dan `Konawe` pada halaman `program pembangunan smelter`
   - `KPPIP` mengunci `Kawasan Industri Morowali` dan `Kawasan Industri Konawe`
   - `PT Vale` PDF resmi mengunci `Pomalaa` sebagai `National Strategic Project`
   - `PT Vale` PDF resmi mengunci `Morowali` sebagai `PSN` dan menyebut `Bahodopi`, `Bungku Timur`, dan `Sambalagi`
   - `Kemenhub` mengunci payung regulasi `terminal khusus` melalui `PM 71 Tahun 2016`
11. `dorking_queue`
   - mengubah pencarian liar menjadi antrean dorking resmi berbasis domain target
   - prioritas tertinggi sekarang ada di `ppid.dephub`, `jdih.kemenhub`, `ANTAM/IDX`, dan `Vale/IDX`

## Batas Klaim Aman Per 27 Juni 2026

Klaim yang sudah aman:
- ekspansi industri nikel di node prioritas ditopang simpul logistik pesisir dengan fasilitas pelabuhan/jetty terkonfirmasi,
- IMIP memiliki seaport + port jetties, GNI memiliki integrated port 50.000 DWT, VDNI memiliki jetty 50.000 ton, ANTAM memiliki jetty 12.000 DWT, Vale memiliki pelabuhan via Balantang Malili,
- `Morowali`, `Konawe`, dan `Pomalaa` punya status PSN terkonfirmasi dari sumber resmi pemerintah,
- KEK TIDAK ada untuk node prioritas manapun — legitimasi berasal dari PSN dan Kawasan Industri,
- rel/rail TIDAK menghubungkan node nikel — infrastruktur logistik ekspansi nikel adalah infrastruktur maritim,
- pola konsisten: investor membangun smelter + PLTU + pelabuhan sebagai satu paket investasi.

Klaim yang belum aman:
- klaim `terminal khusus berlisensi Kemenhub` — izin formal Kemenhub belum ditemukan eksplisit per node,
- klaim IPIP Pomalaa `beroperasi` — masih tahap pembebasan lahan per November 2023,
- klaim IHIP Sorowako `beroperasi` — ditargetkan akhir 2027, belum ada konfirmasi progres konstruksi,
- klaim GNI `beroperasi penuh` — mayoritas lini produksi sudah tutup sejak 2025 akibat kebangkrutan induk,
- klaim OSS memiliki `jetty terpisah` dari VDNI — keduanya berbagi fasilitas di Desa Porara.

## Catatan Koreksi

Versi sebelumnya terlalu generik karena masih menempatkan fase ini sebagai proyek desain dataset logistik. Itu tidak sesuai dengan revisi 1. Dokumen ini dikunci ulang agar semua langkah berikutnya langsung tunduk ke narasi revisi: infrastruktur logistik sebagai bukti tambahan ekspansi industri berbasis nikel di Sulawesi.

## Log Eksekusi Codex

Log ini sengaja dibuat sebagai handoff blunt untuk agen berikutnya.

### Yang Sudah Dilakukan

1. Membaca ulang dokumen acuan:
   - `docs/rev1_Catatan dan Masukan olah data Henry.md`
   - `docs/framework-fase1-d3tlh-clean.md`
   - `docs/prd-fase1-d3tlh.md`
2. Mengerjakan `Tahap A`:
   - mengunci 6 node prioritas:
     `IMIP-Bahodopi`, `Petasia-GNI`, `Morosi-VDNI`, `Konawe-OSS`, `Pomalaa-ANTAM`, `Sorowako-Vale`
   - output utama:
     - `sulawesi_port_logistics.csv`
     - `port_research_targets.csv`
     - `rev1_tahap_a_region_summary.csv`
     - `rev1_tahap_a_source_queue.csv`
3. Mengerjakan `Tahap B`:
   - validasi fungsi node,
   - validasi 5 smelter tambahan sebagai `nikel`,
   - normalisasi matriks evidensi,
   - bikin bulk dataset kerja:
     - `priority_company_roster` 396 baris
     - `priority_permit_extract` 270 baris
     - `pltu_cluster_units` 115 baris
     - `export_nickel_detail` 33 baris
4. Mengerjakan `master layer`:
   - `master_cluster_dim`
   - `master_company_dim`
   - `master_company_cluster_bridge`
   - `master_permit_fact`
   - `master_power_unit_fact`
   - `master_export_fact`
   - `master_evidence_fact`
5. Mengerjakan `Tahap C` versi awal:
   - `kawasan_relations`
   - `transport_project_tracking`
   - `negative_findings`
   - `narrative_blocks`
6. Mengerjakan `Tahap C` versi penguatan:
   - tambah `conflict_environment_extract`
   - tambah `legitimacy_matrix`
   - tambah `corridor_scorecard`
   - tambah `bab41_argument_map`
   - tambah `psn_kek_backlog`
   - tambah `official_source_leads`
   - tambah `dorking_queue`
7. Mengerjakan pencarian sumber resmi tambahan:
   - `KPPIP`:
     - halaman `program pembangunan smelter`
     - halaman `kawasan industri prioritas / KEK`
     - halaman `kereta Makassar-Parepare`
   - `Kemenhub / Dephub`:
     - endpoint pencarian resmi `/search?keyword=...`
     - artikel regulasi `PM 71 Tahun 2016` soal `terminal khusus`
   - `PT Vale`:
     - unduh PDF resmi `Pomalaa`
     - unduh PDF resmi `Morowali`
8. Menyimpan file primer hasil unduhan:
   - `data/raw/rev1_logistik/external_vale_pomalaa.pdf`
   - `data/raw/rev1_logistik/external_vale_morowali.pdf`

### Yang Gagal / Belum Beres

1. Belum dapat bukti `jetty / terminal khusus / dermaga` spesifik per node.
2. Belum dapat bukti `KEK eksplisit` yang benar-benar mengunci node prioritas.
3. Belum dapat bukti `rail penghubung node nikel prioritas`; yang berhasil dikunci justru `Makassar-Parepare`, jadi hanya berguna sebagai pembatas klaim.
4. `ANTAM` official docs belum berhasil dikunci.
5. `GNI`, `VDNI`, `OSS`, `IMIP` belum berhasil dikunci sampai level dokumen primer pelabuhan/terminal.
6. `pdftotext` lokal jalan parsial untuk stdout, tapi gagal menulis output file tetap karena environment `MiKTeX` sandboxed.

## Handoff Agen Berikutnya

Kalau agen berikutnya mau lanjut cepat, jangan ulang dari nol. Lanjut dari file dan gap yang sudah ada.

### File Kunci Yang Harus Dibaca Dulu

1. `docs/rev1_fase3_rencana_pelacakan_infrastruktur_logistik.md`
2. `data/raw/rev1_logistik/working/rev1_tahap_c_official_source_leads.csv`
3. `data/raw/rev1_logistik/working/rev1_tahap_c_dorking_queue.csv`
4. `data/raw/rev1_logistik/working/rev1_tahap_c_psn_kek_backlog.csv`
5. `data/raw/rev1_logistik/working/rev1_tahap_c_corridor_scorecard.csv`
6. `data/raw/rev1_logistik/working/rev1_tahap_b_evidence_matrix.csv`

### Prioritas Kerja Untuk Agen Lain

1. Naikkan bukti `facility-specific proof`:
   - cari `terminal khusus / terminal untuk kepentingan sendiri / jetty / dermaga / pelabuhan internal`
   - target utama:
     - `IMIP`
     - `GNI / Petasia`
     - `VDNI`
     - `OSS`
     - `Pomalaa-ANTAM`
2. Kunci sumber primer `ANTAM`:
   - annual report
   - presentasi investor
   - laporan operasional Pomalaa
   - dokumen yang menyebut pelabuhan/dermaga/ferronickel shipment
3. Cek `JDIH Kemenhub`, `PPID Dephub`, `Amdalnet`, `OSS`, `IDX`, `annual report`, `berita pemda/kabupaten`
4. Pisahkan `VDNI` vs `OSS` di level fasilitas sandar.
5. Putuskan secara tegas:
   - apakah `KEK` untuk node prioritas memang ada,
   - atau harus ditutup sebagai `tidak terbukti` dan dikeluarkan dari klaim utama.
6. Putuskan secara tegas:
   - apakah `rail` tetap hanya `negative evidence`,
   - atau ada proyek resmi lain selain `Makassar-Parepare` yang benar-benar nyambung ke node nikel.

### Query / Jalur Yang Sudah Disiapkan

Jangan invent ulang. Pakai dulu queue ini:

1. `DORK-001` untuk `Morowali / Bahodopi / Sambalagi`
2. `DORK-002` untuk `Pomalaa / ANTAM / ferronickel port`
3. `DORK-003` untuk `GNI / Petasia / terminal khusus`
4. `DORK-004` untuk `VDNI / OSS / Konawe / terminal khusus`
5. `DORK-005` untuk `Sorowako / logistics / shipment`
6. `DORK-006` untuk `KEK eksplisit`
7. `DORK-007` untuk `rail / PSN`

### Penilaian Jujur Buat Agen Lain

Yang sudah lumayan beres:
- `cluster / koridor / smelter / kawasan industri / PSN non-rail`

Yang masih bolong:
- `jetty spesifik`
- `terminal khusus spesifik`
- `KEK eksplisit`
- `rail penghubung node nikel`
- `ANTAM official port evidence`

### Kalau Mau Rapikan Final

Agen berikutnya kemungkinan perlu:

1. revisi `corridor_scorecard` setelah bukti primer baru masuk, — **SUDAH DILAKUKAN 27 Jun**
2. revisi `legitimacy_matrix`, — **SUDAH DILAKUKAN 27 Jun**
3. revisi `official_source_leads`, — **SUDAH DILAKUKAN 27 Jun**
4. turunkan atau naikkan confidence node per cluster, — **SUDAH DILAKUKAN 27 Jun**
5. putuskan apakah `Sorowako-Vale` tetap `pelengkap_kontras` atau naik jadi node kuat, — **NAIK ke tier_c1 27 Jun**
6. lanjut ke `Tahap D` hanya setelah bukti fasilitas sandar utama benar-benar mentok atau berhasil naik. — **TAHAP D SELESAI 27 Jun**

## Log Eksekusi Agen Kedua — 27 Juni 2026

### Yang Sudah Dilakukan

1. **Eksekusi dorking queue DORK-001 sampai DORK-007** via web search:
   - `DORK-001` (IMIP): **BERHASIL** — seaport + port jetties + airport 1.800m terkonfirmasi (Wikipedia, Jakarta Globe, Nickel Industries)
   - `DORK-002` (ANTAM): **BERHASIL** — jetty 12.000 DWT + belt conveyor 4 km terkonfirmasi (antam.com resmi)
   - `DORK-003` (GNI): **BERHASIL** — integrated port 9×5.000 DWT Barge + 2×50.000 DWT Vessel terkonfirmasi (situs resmi GNI)
   - `DORK-004` (VDNI/OSS): **BERHASIL** — jetty VDNI (2017), PSN Perpres 58/2017, KIK, OSS di Desa Porara (multi-media)
   - `DORK-005` (Sorowako): **BERHASIL** — Pelabuhan Vale Nuha + Pelabuhan Balantang Malili (TNI AL Lantamal VI)
   - `DORK-006` (KEK): **BERHASIL NEGATIF** — daftar 24 KEK Indonesia tidak mencakup node prioritas
   - `DORK-007` (PSN/Rail): **SEBAGIAN** — PSN terkonfirmasi luas; rail tetap hanya Makassar-Parepare

2. **Update seluruh file evidensi Tahap B dan C:**
   - `official_source_leads`: dari 7 → 15 sumber resmi
   - `corridor_scorecard`: semua node naik; Sorowako dari tier_c3 → tier_c1
   - `legitimacy_matrix`: KEK ditutup definitif, port status ditambah
   - `kawasan_relations`: status + port detail di-update
   - `transport_project_tracking`: dari 5 → 7 proyek (tambah GNI port, VDNI jetty, ANTAM jetty, Vale port)
   - `negative_findings`: 3 dari 5 gap TERTUTUP, 1 sebagian tertutup
   - `bab41_argument_map`: claim_core + port evidence di-update seluruh node
   - `narrative_blocks`: confidence naik, kalimat narasi diperkuat dengan bukti fasilitas
   - `psn_kek_backlog`: 5 dari 7 backlog TERTUTUP
   - `gap_register`: 5 dari 6 gap TERTUTUP

3. **Selesaikan Tahap D** — bahan narasi Bab 4.1:
   - Output: `rev1_tahap_d_narrative_material.csv`
   - 14 blok narasi: 1 pembuka, 1 overview peta, 6 node detail, 1 node pelengkap, 4 sintesis, 1 batas klaim
   - Sintesis meliputi: pola pembangunan simpul, PSN sebagai kendaraan legitimasi, rail tidak relevan, dampak sosial-ekologis

4. **Selesaikan Tahap E** — paket final:
   - `rev1_tahap_e_dataset_final.csv` — dataset terkonsolidasi 6 node dengan semua bukti
   - `rev1_tahap_e_source_log.csv` — log 25 sumber (company official, government, military, media)
   - `rev1_tahap_e_remaining_gaps.csv` — 7 gap yang masih terbuka

### Yang Masih Terbuka

1. Izin formal `Kemenhub` (terminal khusus / TUKS) belum ditemukan per node — portal Kemenhub tidak menghasilkan dokumen spesifik.
2. Status operasional `GNI` dan `VDNI/OSS` pasca-kebangkrutan induk `Jiangsu Delong` — perlu dipantau.
3. Progres konstruksi `IPIP` (Pomalaa) dan `IHIP` (Sorowako) — masih tahap awal.
4. `Rail` tetap hanya `negative evidence` — tidak ada proyek rel yang menghubungkan node nikel.

### Perubahan Terbesar Dibanding Agen Sebelumnya

| Aspek | Sebelum (26 Jun) | Sesudah (27 Jun) |
| --- | --- | --- |
| Fasilitas pelabuhan | 0 dari 6 terkonfirmasi | **6 dari 6 terkonfirmasi** |
| KEK | Belum diputuskan | **Ditutup definitif: TIDAK ADA** |
| Sorowako | lead_lemah / pelengkap_kontras | **tier_c1 / narasi utama** |
| Tahap D | Belum mulai | **Selesai: 14 blok narasi** |
| Tahap E | Belum mulai | **Selesai: dataset + log + gaps** |
| Sumber resmi | 7 entri | **15 entri** |
| Source log | Tidak ada | **25 sumber tercatat** |
