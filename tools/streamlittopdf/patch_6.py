import sys
import re
from pathlib import Path

HERE = Path(r"c:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\tools\streamlittopdf")
target_file = HERE / "extract_chapter_6.py"

with open(target_file, "r", encoding="utf-8") as f:
    content = f.read()

# Define the new markdown block
new_md = r'''md = f"""# Bab 6: Audit Forensik Metodologi D3TLH

**CELIOS — Center of Economic and Law Studies**

*Fase 1: Evaluasi Kebijakan Ekstraktif - Pembuktian Terbalik*

---

> **Kesimpulan Eksekutif**
>
> Evaluasi empiris mengindikasikan perlunya perbaikan substansial dalam integrasi dokumen D3TLH dan AMDAL. Instrumen pengelolaan lingkungan perlu diperkuat agar mampu memetakan dampak akumulatif dan berfungsi sebagai pertimbangan yang lebih efektif dalam pengendalian perizinan investasi.

---

## Ringkasan Audit Kritis D3TLH

| Dimensi Audit | Skor Kerusakan | Status Vonis | Indikator Utama |
|---|---|---|---|
| **DAYA TAMPUNG UDARA** | **{skor_akumulasi_udara:.1f} / 10** | STATUS: EVALUASI KUALITAS UDARA - Analisis data menunjukkan korelasi antara aktivitas industri dan tren penyakit saluran pernapasan. | NOTE: Perlu pengawasan lebih ketat terhadap emisi industri \| Kapasitas PLTU: {kapasitas_terkini:,.0f} MW / NO2 NASA: {no2_terkini:.2e} / Rasio ISPA: {rasio_anomali:.1f}x |
| **DAYA TAMPUNG AIR** | **{skor_akumulasi_air:.1f} / 10** | STATUS: EVALUASI KUALITAS AIR - Pemantauan Indeks Kualitas Air dan prevalensi penyakit berbasis air sebagai indikator lingkungan. | NOTE: Pentingnya penguatan standar pemantauan limbah \| IKA Sulteng: {ika_sulteng:.1f} / Kasus Diare: {kasus_diare_sentra:,.0f} / Konflik Air: {jumlah_konflik_air} |
| **DAYA DUKUNG LAHAN** | **{skor_akumulasi_lahan:.1f} / 10** | STATUS: EVALUASI TATA GUNA LAHAN - Pemetaan dampak tutupan lahan terhadap risiko bencana hidrometeorologi. | NOTE: Perlu peninjauan tata ruang berbasis mitigasi bencana \| Bencana: {bencana_sulteng_sultra:,.0f} Kejadian / Deforestasi: {deforestasi_sentra:,.0f} Ha |
| **DAYA DUKUNG SOSIAL** | **{skor_akumulasi_sosial:.1f} / 10** | STATUS: EVALUASI SOSIAL AGRARIA - Pemantauan sengketa lahan dan dampaknya terhadap kesejahteraan masyarakat lokal. | NOTE: Pentingnya pendekatan dialogis dalam kebijakan agraria \| Konflik Lahan: {konflik_darat} Kasus TanahKita |
| **VETO KEBIJAKAN** | **{skor_akumulasi_veto:.1f} / 10** | STATUS: EVALUASI PERIZINAN - Peninjauan pemberian izin operasional industri dibandingkan dengan kapasitas ekologi. | NOTE: Penyelarasan izin dengan daya dukung lingkungan \| {izin_baru:,.0f} Izin Baru & {kapasitas_pltu/1000:,.1f} GW PLTU Captive Diloloskan |

---

## 1. Kerangka Analisis Evaluasi D3TLH

AMDAL dan D3TLH dirancang bersifat prediktif untuk menilai batasan daya dukung lingkungan sebelum izin diterbitkan. Evaluasi empiris diperlukan untuk menilai efektivitas instrumen ini dalam meredam dampak lingkungan dan sosial di lapangan.

**Standpoint Riset ECC:** 
Pendekatan riset menggunakan **Evaluasi Berbasis Bukti Empiris**. Analisis menyandingkan indikator daya dukung spasial dengan indikator empiris seperti tren kesehatan masyarakat, kejadian bencana hidrometeorologi, dan dinamika sengketa lahan guna mengukur sejauh mana daya dukung ekologis dan sosial telah tertekan.

Halaman ini merangkum indikator-indikator tersebut untuk memberikan rekomendasi perbaikan tata kelola lingkungan dan sistem perizinan.

---

## 2. Fakta: Metodologi Resmi D3TLH Pemerintah (Jasa Ekosistem)

Berdasarkan dokumen pedoman teknis D3TLH (seperti Permen LH 17/2009 dan panduan KLHK), pemerintah saat ini menyusun D3TLH dengan pendekatan murni spasial/bio-fisik yang disebut **Jasa Ekosistem (Ecosystem Services)**.

Indikator resmi yang digunakan dibagi menjadi 4 kategori:
*   **Jasa Penyediaan (Provisioning):** Kapasitas lahan menyediakan pangan, air bersih, dll.
*   **Jasa Pengaturan (Regulating):** Kapasitas tata air, mitigasi iklim, mitigasi banjir, pemurnian udara.
*   **Jasa Pendukung (Supporting):** Siklus hara, pembentukan tanah.
*   **Jasa Budaya (Cultural):** Estetika alam, rekreasi.

### Letak Cacat Metodologi (Blind Spots):

Rumus utama yang dipakai pemerintah untuk menghitung indeks di atas hanyalah: **Peta Ekoregion + Peta Tutupan Lahan (Land Cover)**.

*   **Abaikan Nyawa & Morbiditas:** Menghitung kapasitas udara dari peta vegetasi, namun **TIDAK PERNAH** menghitung rekam medis warga (ISPA) yang paru-parunya rusak akibat debu smelter.
*   **Abaikan Kedaulatan Ruang:** Mengukur kapasitas pertanian, tapi abai terhadap perampasan lahan yang memicu konflik sosial berdarah.
*   **Bukan Veto Kebijakan:** Saat D3TLH menyatakan daya dukung turun, instrumen ini tidak dipakai untuk "menyetop" penerbitan IUP (Izin Usaha Pertambangan) baru.

---

## 3. Matriks Pembuktian Terbalik: D3TLH vs Fakta Lapangan

Di sinilah seluruh temuan riset kita diintegrasikan untuk "menelanjangi" cacat bawaan D3TLH. Di bawah ini adalah benturan langsung antara **Mitos (Klaim Dokumen Resmi)** versus **Realitas Lapangan (Bukti Forensik)**.

---

### A. Audit D3TLH: Daya Tampung Udara

> **Klaim Mitos:** *"Daya tampung udara (berdasarkan peta tutupan lahan) dianalisis sebagai indikator kapasitas pemulihan emisi."*
>
> **Fakta Empiris:** Data menunjukkan tren penyakit saluran pernapasan di sekitar kawasan industri.
> **Akumulasi Skor Kerusakan:** **{skor_akumulasi_udara:.1f} / 10** — *STATUS: PERLU PENGAWASAN \| ANALISIS: Pemantauan Morbiditas Akumulatif*

#### 1. Korelasi PLTU & Kualitas Udara
Pemerintah sebelumnya mengklaim IKU 'Masih Aman'. Namun pantauan independen Satelit TROPOMI NASA mengungkap realitas lain: konsentrasi gas beracun NO2 meledak meroket sejajar dengan ekspansi PLTU captive. **Threshold Kritis NASA: NO2 > 6.0e-6 mol/m²**.

![PLTU vs NO2 NASA](visuals_bab6/chart_6_1a_pltu_no2.png)

#### 2. Dampak Kasus ISPA/Pneumonia
Dokumen daya dukung mengabaikan lonjakan tajam pasien ISPA di RSUD Morowali dan Kendari. Grafik membuktikan bahwa tren ISPA di provinsi non-tambang relatif stabil, namun meroket secara paralel dengan asap di provinsi sentra nikel.

![Insiden ISPA per 10.000 Penduduk](visuals_bab6/chart_6_1b_ispa_trend.png)

#### 3. Fakta Beban Limbah & Emisi
Data perizinan D3TLH fokus pada syarat emisi cerobong di atas kertas, tetapi mengabaikan gunung-gunung debu slag (fly ash) di darat yang bebas tertiup angin memapari puluhan desa setiap harinya. **Threshold Kritis: 30 Juta Ton/Tahun** = 7% dari total neraca B3 nasional 427 juta ton dari 1 provinsi (anomali 2,4x proporsional). Sumber: *KLHK LKj 2022, IKK Pengelolaan Limbah B3, Hal. 47*.

![Beban Timbulan B3 per Provinsi](visuals_bab6/chart_6_1c_b3_beban.png)

#### 4. Hilangnya Paru-Paru Udara (Emisi CO2)
Audit resmi pemerintah hanya menghitung 'emisi yang keluar dari corong pabrik', tetapi dengan sengaja mengaburkan 'emisi dari jutaan pohon yang mati' akibat ekspansi lahan tambang itu sendiri. **Threshold Kritis: 150 Juta Ton CO2e** = melampaui target NDC FOLU Net Sink 2030 (-140 juta ton CO2e). Sumber: *SK MenLHK No.SK.168/MENLHK/PKTL/PLA.1/2/2022, Bag. III, Hal. 5*.

![Emisi CO2 Akibat Deforestasi](visuals_bab6/chart_6_1d_co2_emisi.png)

---

### B. Audit D3TLH: Daya Tampung Air

> **Klaim Mitos:** *"Daya tampung air diukur berdasarkan rasio pengenceran alami dan neraca kualitas air."*
>
> **Fakta Empiris:** Indeks Kualitas Air dan prevalensi penyakit saluran pencernaan menunjukkan perlunya pengawasan kualitas air.
> **Akumulasi Skor Kerusakan:** **{skor_akumulasi_air:.1f} / 10** — *STATUS: PERLU PENGAWASAN \| ANALISIS: Pemantauan Toksisitas dan Sanitasi*

#### 1. Kualitas Air (IKA)
Klaim sungai/laut mampu mengencerkan limbah berbanding terbalik dengan hancurnya Indeks Kualitas Air BPS hingga menyentuh batas cemar kotor.

![Indeks Kualitas Air](visuals_bab6/chart_6_2a_ika_line.png)

#### 2. Morbiditas Diare
AMDAL gagal menghitung dampak kontaminasi logam berat ke air tanah yang dikonsumsi warga, dibuktikan dengan ledakan pasien Diare di lingkar tambang. **Threshold Kritis: Incidence Rate Ratio (IRR) > 2.0** (Risiko 2x lipat dari populasi rata-rata). Sumber: *Kemenkes Profil Kesehatan 2023, Hal. 112*.

![Kasus Diare](visuals_bab6/chart_6_2b_diare_area.png)

#### 3. Konflik Nelayan & Pesisir
Ekosistem tangkap nelayan dihancurkan oleh limbah tailing dan privatisasi pesisir untuk Smelter, memicu lonjakan konflik agraria laut.

![Konflik Nelayan & Pesisir](visuals_bab6/chart_6_2c_konflik_nelayan.png)

#### 4. Beban Tailing (Treemap B3)
Resiko kebocoran Tailings Dam (Bendungan Tailing) atau Deep Sea Tailing Placement (DSTP) yang ditutupi oleh klaim 'mitigasi teknologi'. **Threshold Kritis: 25 Juta Ton/Tahun** (Batas Kapasitas AMDAL Gabungan Kawasan IMIP & OSS). Sumber: *Dokumen AMDAL KLHK, PPID*.

![Proporsi Beban Limbah Tailing & B3](visuals_bab6/chart_6_2d_tailing_treemap.png)

---

### C. Audit D3TLH: Daya Dukung Lahan

> **Klaim Mitos:** *"Daya dukung lahan dianalisis berdasarkan kecukupan tutupan hutan dan batas fungsi kawasan."*
>
> **Fakta Empiris:** Perubahan tutupan lahan berpotensi memengaruhi laju bencana hidrometeorologi di kawasan industri.
> **Skor Kerusakan Lahan:** **{skor_akumulasi_lahan:.1f} / 10** — *STATUS: PERLU PENGAWASAN \| ANALISIS: Evaluasi Pengelolaan Lanskap*

#### 1. Bencana Banjir & Longsor (BNPB)
Data BNPB membuktikan bahwa klaim 'mitigasi bencana' dalam AMDAL sama sekali tidak terbukti di lapangan.

![Bencana Hidrometeorologi](visuals_bab6/chart_6_3a_bencana_bnpb.png)

#### 2. Deforestasi Primer (GFW)
Hutan primer yang berfungsi sebagai jasa penyediaan air dan penyerap karbon ditebang habis atas nama IUP.

![Laju Deforestasi Pertambangan & Sawit](visuals_bab6/chart_6_3b_deforestasi_gfw.png)

#### 3. Pelanggaran Kawasan Lindung
Temuan **paling mematikan**: Data GFW membuktikan bahwa **100% dari setiap Ha deforestasi** yang terjadi di Sulteng dan Sultra selama 10 tahun (2014–2023) terjadi di dalam **Kawasan Lindung / Protected Areas (IUCN)**. Tidak ada satu pun hektar yang dibabat di luar batas kawasan yang seharusnya tidak boleh disentuh.

![Deforestasi Kawasan Lindung](visuals_bab6/chart_6_3c_kawasan_lindung.png)

#### 4. Aktor Deforestasi
Data atribusi GFW mematahkan alibi 'ladang berpindah'. Pertambangan dan Sawit adalah aktor dominan penghancur hutan. ⚠️ *Catatan: Data GFW untuk Sulteng absen/kosong, angka setengah juta hektar ini MURNI dari Sulawesi Tenggara saja.*

![Drivers of Deforestation](visuals_bab6/chart_6_3d_drivers_pie.png)

---

### D. Audit D3TLH: Daya Dukung Sosial

> **Klaim Mitos:** *"Status kawasan dialokasikan untuk peruntukan industri dengan pelaksanaan konsultasi publik."*
>
> **Fakta Empiris:** Pentingnya transparansi dan pelibatan masyarakat lokal dalam penataan ruang dan perizinan.
> **Skor Kerusakan Sosial:** **{skor_akumulasi_sosial:.1f} / 10** — *STATUS: PERLU PENGAWASAN \| ANALISIS: Pelibatan Masyarakat Lokal*

#### 1. Manipulasi Persetujuan FPIC
'Persetujuan Warga' hanyalah stempel karet. Data investigasi Konsorsium Pembaruan Agraria membuktikan perusahaan memanipulasi persetujuan (FPIC) sejak fase sosialisasi AMDAL.

![Timeline Konflik Tambang vs Masalah Izin](visuals_bab6/chart_6_4a_fpic_timeline.png)

#### 2. Perampasan Ruang Hidup
Setelah izin keluar lewat manipulasi, perampasan paksa terjadi. Ruang hidup warga menyusut drastis, memicu letusan konflik yang berdampak pada ratusan ribu korban jiwa.

![Frekuensi Letusan Konflik Perampasan Lahan](visuals_bab6/chart_6_4b_perampasan_lahan.png)

#### 3. Kriminalisasi Warga
Di fase akhir, ketika warga melakukan penolakan yang sah atas perampasan, negara tidak hadir melindungi, melainkan mengirim aparat untuk memenjarakan mereka.

![Insiden Kriminalisasi & Kekerasan](visuals_bab6/chart_6_4c_kriminalisasi.png)

#### 4. Defisit Layanan Dasar (Faskes)
Di tengah ekspor nikel sentra Sulawesi yang meledak ratusan kali lipat, kualitas layanan dasar hancur. Mayoritas Puskesmas gagal memenuhi standar minimal **Sarana, Prasarana, dan Alat Kesehatan (SPA)**. Klaim AMDAL tentang 'peningkatan kesejahteraan' adalah fiksi belaka.

![Tren Jumlah Fisik Faskes](visuals_bab6/chart_6_4d_faskes_line.png)

---

### E. Audit D3TLH: Veto Kebijakan

> **Klaim Mitos:** *"Penyusunan D3TLH dirancang sebagai pertimbangan dalam membatasi izin eksploitasi."*
>
> **Fakta Empiris:** Evaluasi menunjukkan pentingnya penguatan kepatuhan hukum dan efektivitas instrumen pengendalian perizinan.
> **Skor Kegagalan Tata Kelola:** **{skor_akumulasi_veto:.1f} / 10** — *STATUS: PERLU REFORMASI \| ANALISIS: Penguatan Pengawasan Kebijakan*

#### 1. Obral Konsesi Legal
Di tengah memuncaknya status krisis daya dukung lingkungan, pemerintah secara paradoks justru menerbitkan ratusan izin eksploitasi tambang (IUP) baru. Dokumen veto tidak berfungsi.

![Lonjakan Penerbitan IUP Baru](visuals_bab6/chart_6_5a_iup_baru.png)

#### 2. Pembiaran Pelanggaran Korporat
Bukti mutlak 'Regulatory Capture'—bahkan ketika perusahaan beroperasi ilegal, menabrak izin, tumpang tindih, atau HGU kedaluwarsa, negara tidak berani melakukan penegakan hukum dan membiarkannya.

![Distribusi Modus Pelanggaran Izin Korporat](visuals_bab6/chart_6_5b_modus_pelanggaran.png)

#### 3. Karpet Merah Energi Kotor (PLTU Captive)
Inkonsistensi paling telanjang terhadap komitmen iklim. Di wilayah ekoregion krisis, pemerintah memberikan karpet merah pembangunan infrastruktur penyumbang emisi terbesar (PLTU Batubara Captive) khusus untuk menyuplai kawasan smelter nikel.

![Proporsi Status PLTU Captive](visuals_bab6/chart_6_5c_pltu_status_pie.png)
"""'''

# Use regex to replace everything from `md = f"""# Bab 6: Audit Forensik Metodologi D3TLH` up to the end of the string
pattern = re.compile(r'md\s*=\s*f"""# Bab 6: Audit Forensik Metodologi D3TLH.*?^"""', re.MULTILINE | re.DOTALL)
new_content = pattern.sub(new_md, content)

with open(target_file, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"Patched {target_file}")
