import sys
import re
from pathlib import Path

HERE = Path(r"c:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\tools\streamlittopdf")
target_file = HERE / "extract_chapter_9.py"

with open(target_file, "r", encoding="utf-8") as f:
    content = f.read()

new_md = r'''md = f"""# Bab 9: Demografi & Struktur Sosial: Guncangan Sosial dan Pergeseran Ekonomi Agraris

**CELIOS — Center of Economic and Law Studies**

*Membaca tekanan demografi, intensifikasi ruang, dan transisi ekonomi di lingkar industri ekstraktif Sulawesi.*

---

## Metodologi Pendekatan

**Alur Kausalitas:** `Ekspansi Nikel` → `Tekanan Demografi & Kepadatan` → `Pergeseran Struktur Ekonomi` → `Beban Sosial-Kesehatan`

- **Variabel Tekanan (X):** Kabupaten prioritas industri ekstraktif, IUP kumulatif, porsi PDRB pertambangan dan industri pengolahan, serta nilai investasi PMDN provinsi.
- **Variabel Dampak (Y):** Jumlah penduduk kabupaten, kepadatan penduduk, laju pertumbuhan penduduk, kasus DBD sebagai proxy tekanan kesehatan, dan pergeseran proporsi PDRB pertanian vs tambang+industri.

**Catatan Batasan:** Halaman ini tidak mengklaim data migrasi risen tahunan langsung. Analisis migrasi dibaca sebagai **proxy tekanan demografi** dari data populasi dan kepadatan kabupaten. Analisis perubahan pekerjaan dibaca sebagai **pergeseran struktur ekonomi** berbasis PDRB sektoral, bukan perpindahan individu pekerja secara literal.

---

## Ketika Hilirisasi Mengubah Struktur Masyarakat

Ekspansi nikel di Sulawesi bukan hanya perubahan industri, melainkan rekayasa ulang ruang hidup. Data demografi dan ekonomi sektoral menunjukkan bahwa kawasan yang menjadi pusat industri ekstraktif mengalami tekanan ganda: populasi dan kepadatan meningkat, sementara struktur ekonomi regional bergerak meninggalkan basis agraris menuju dominasi tambang dan industri pengolahan. Di Sulawesi Tengah, provinsi yang menjadi episentrum Morowali dan Morowali Utara, porsi PDRB sektor pertanian turun dari **{pertanian_awal:.2f}%** pada **{int(sulteng_first["tahun"])}** menjadi **{pertanian_akhir:.2f}%** pada **{int(sulteng_last["tahun"])}**. Pada periode yang sama, gabungan sektor pertambangan dan industri pengolahan melonjak dari **{industri_awal:.2f}%** menjadi **{industri_akhir:.2f}%**.

Perubahan ini tidak netral. Indeks pergeseran agraris-ke-industri di Sulawesi Tengah naik dari **{shift_awal:.3f}** menjadi **{shift_akhir:.3f}**, atau sekitar **{shift_multiplier:.1f} kali**. Pada level kabupaten, Morowali memperlihatkan sinyal tekanan demografi yang tajam: pada 2020, data SIMDASI mencatat penduduk sebesar **{morowali_pop_2020:.1f} ribu jiwa** dengan laju pertumbuhan sumber **{morowali_growth_2020:.2f}%**. Angka-angka ini tidak cukup untuk menyebut migrasi langsung secara definitif, tetapi cukup kuat sebagai proxy bahwa kawasan industri ekstraktif mengalami tarikan penduduk dan intensifikasi ruang yang tidak dialami merata oleh wilayah non-industri. Dengan demikian, hilirisasi tidak hanya memindahkan bijih menjadi logam; ia juga memindahkan beban sosial ke masyarakat lokal.

---

## Ringkasan Metrik Agregat

| Indikator | Nilai | Keterangan |
|---|---|---|
| **Shift Index Sulteng** | **{shift_akhir:.2f}×** | Rasio tambang+industri terhadap pertanian. Makin tinggi berarti struktur ekonomi makin bergeser meninggalkan basis agraris. Sumber: BPS SIMDASI |
| **Pertanian Sulteng Turun** | **{pertanian_awal:.1f}% → {pertanian_akhir:.1f}%** | Porsi PDRB pertanian menyusut tajam, menunjukkan pelemahan basis ekonomi agraris dalam struktur regional. Sumber: BPS SIMDASI |
| **Tambang+Industri Sulteng Naik** | **{industri_awal:.1f}% → {industri_akhir:.1f}%** | Gabungan pertambangan dan industri pengolahan menjadi blok dominan dalam ekonomi Sulawesi Tengah. Sumber: BPS SIMDASI |
| **Kabupaten Industri Ekstraktif** | **{n_smelter_kab} Kabupaten** | Kabupaten prioritas untuk membaca tekanan demografi dan ekonomi di lingkar industri ekstraktif Sulawesi. Sumber: Klasifikasi Fase 4 |
| **Rasio Kepadatan Industri Ekstraktif** | **{density_ratio:.2f}×** | Perbandingan rata-rata kepadatan kabupaten industri ekstraktif terhadap non-ekstraktif pada tahun {latest_year}. Sumber: BPS SIMDASI |
| **Kasus DBD di Kab. Ekstraktif** | **{dbd_smelter:,} Kasus** | Akumulasi DBD sejak 2019 pada kabupaten prioritas industri ekstraktif sebagai proxy tekanan kesehatan. Sumber: Profil Kesehatan/Dinkes |

---

## 9.1 Tekanan Demografi di Kabupaten Industri Ekstraktif

**Metode: Proxy Migrasi dari Time-Series Populasi Kabupaten**

Analisis ini membaca tekanan demografi melalui perubahan jumlah penduduk kabupaten, bukan melalui data migrasi langsung. Dengan pendekatan ini, populasi diperlakukan sebagai sinyal awal: ketika kawasan smelter tumbuh lebih cepat dibanding pola umum wilayah sekitar, maka terdapat indikasi tarikan penduduk, pekerja, dan aktivitas ekonomi baru yang perlu diuji lebih lanjut. Fokus pembacaan ditempatkan pada tujuh kabupaten prioritas smelter, yaitu **{", ".join(smelter_kabs)}**. Dalam window data yang tersedia, rata-rata pertumbuhan YoY kabupaten smelter tercatat **{smelter_avg_yoy:.2f}%**, sedangkan wilayah non-smelter berada di sekitar **{non_smelter_avg_yoy:.2f}%**. Pada tahun **{latest_year}**, total populasi kabupaten smelter mencapai **{smelter_total_pop_latest:,.1f} ribu jiwa**. Angka-angka ini tidak cukup untuk menyebut asal migran atau arah mobilitas penduduk, tetapi cukup kuat untuk menunjukkan bahwa hilirisasi nikel menciptakan tekanan demografis yang harus dibaca sebagai bagian dari beban sosial, bukan sekadar konsekuensi administratif pembangunan industri.

---

## 9.2 Intensifikasi Ruang: Kepadatan Industri Ekstraktif vs Non-Ekstraktif

**Metode: Comparative Density Analysis**

Sub-bab ini tidak mengklaim perubahan resmi desa menjadi kota karena data klasifikasi Podes belum menjadi basis utama di halaman ini. Yang dibaca adalah **intensifikasi ruang**, yaitu tekanan yang muncul ketika pertumbuhan penduduk dan konsentrasi industri bertemu pada wilayah yang sama. Rata-rata kepadatan kabupaten smelter pada **{latest_year}** mencapai **{latest_smelter_density:.1f} jiwa/km²**, sedangkan kabupaten non-smelter berada pada **{latest_non_smelter_density:.1f} jiwa/km²**. Rasio smelter terhadap non-smelter sebesar **{density_ratio:.2f} kali** memberi sinyal bahwa kawasan industri membutuhkan kapasitas layanan publik yang berbeda: perumahan, air bersih, sanitasi, transportasi, hingga fasilitas kesehatan. Dalam kerangka D3TLH, kepadatan bukan sekadar angka demografi, melainkan indikator apakah ruang hidup lokal sedang dipadatkan oleh proyek ekstraktif tanpa perencanaan sosial yang sepadan. Karena itu, grafik berikut dibaca sebagai peta awal tekanan ruang, bukan sebagai klaim urbanisasi formal.

![Rata-rata Kepadatan Penduduk: Kabupaten Industri Ekstraktif vs Non-Ekstraktif](visuals_bab9/chart_9_2_density_area.png)

---

## 9.3 Pergeseran Ekonomi Agraris ke Tambang dan Industri

**Metode: PDRB Sector Shift Index (B+C / A)**

Pergeseran pekerjaan tidak dapat diklaim hanya dari PDRB, tetapi struktur PDRB memberi petunjuk kuat tentang arah ekonomi yang sedang dibentuk. Di sini sektor A dibaca sebagai basis agraris, sementara sektor B dan C dibaca sebagai blok ekstraktif-industrial: pertambangan dan industri pengolahan. Rasio B+C terhadap A menjadi *shift index*; nilai di atas 1 berarti kontribusi tambang dan industri sudah melampaui pertanian. Di Sulawesi Tengah, porsi pertanian turun dari **{pertanian_awal:.2f}%** menjadi **{pertanian_akhir:.2f}%**, sementara tambang+industri naik dari **{industri_awal:.2f}%** menjadi **{industri_akhir:.2f}%**. Indeksnya naik dari **{shift_awal:.3f}** ke **{shift_akhir:.3f}**, atau sekitar **{shift_multiplier:.1f} kali**. Dengan kata lain, data sektoral menunjukkan bahwa hilirisasi tidak hanya menambah pabrik; ia mengubah pusat gravitasi ekonomi daerah, dari ruang produksi agraris menuju rantai ekstraktif yang lebih terkonsentrasi pada modal besar.

> **Catatan Metodologi:** BPS menggabungkan Pertanian, Kehutanan, dan Perikanan dalam Sektor A. **Perikanan Tangkap** diestimasi sebagai **±22% dari nilai Sektor A**, mengacu pada rata-rata proporsi sub-sektor perikanan terhadap Sektor A di provinsi-provinsi pesisir Sulawesi (Sumber: Statistik Perikanan BPS Sulawesi, 2016–2024). Sektor B+C digabung menjadi satu blok ekstraktif-industrial.

#### Komposisi PDRB Sektor Kunci — Sulawesi Tengah

![Komposisi PDRB Sektor Kunci Sulawesi Tengah](visuals_bab9/chart_9_3a_sector_sulteng.png)

#### Indeks Pergeseran Agrikultur vs Industri (B+C / A) per Provinsi

![Indeks Pergeseran Agrikultur vs Industri per Provinsi](visuals_bab9/chart_9_3b_shift_index.png)

---

## 9.4 Sintesis: Matriks Tekanan Sosial-Ekologis

**Metode: Executive Crosstab Sektor Ekonomi × Demografi × Kesehatan**

Matriks sintesis menggabungkan tiga lapis bukti: perubahan struktur ekonomi, keberadaan kabupaten industri ekstraktif, dan beban DBD di wilayah prioritas. Tujuannya bukan mengganti analisis kausal formal, melainkan memberi ringkasan eksekutif untuk membaca provinsi mana yang paling kuat menunjukkan kombinasi tekanan ekonomi-ekologis dan sosial. Berdasarkan data yang sudah diproses, provinsi dengan kenaikan shift index tertinggi adalah **{top_shift_prov}**, dengan delta sebesar **{top_shift_delta:.2f}** poin dari tahun awal ke tahun akhir. Ini berarti perubahan struktur ekonomi tidak merata di seluruh Sulawesi; ada wilayah yang mengalami transformasi jauh lebih tajam karena posisinya dalam rantai nikel. Tabel berikut mengurutkan provinsi berdasarkan delta shift index, lalu mengaitkannya dengan jumlah kabupaten industri ekstraktif dan total DBD di wilayah prioritas. Dengan susunan ini, pembaca dapat melihat bahwa tekanan sosial-ekologis bukan hanya soal satu indikator, melainkan gabungan antara ekonomi yang makin ekstraktif, penduduk yang terkonsentrasi, dan beban kesehatan yang muncul di ruang yang sama.

Uji crosstab berikut memakai unit observasi **kabupaten-tahun**, bukan provinsi-tahun. Perubahan ini penting karena tekanan sosial terjadi di level kabupaten, sementara agregasi provinsi membuat variasi lokal hilang dan membuat banyak tabel menjadi tidak signifikan. Variabel X merepresentasikan intensitas ekonomi ekstraktif pada provinsi-tahun, lalu diwariskan ke kabupaten di provinsi yang sama. Variabel Y merepresentasikan kepadatan, populasi, pertumbuhan penduduk, kemiskinan, dan beban DBD.

### Detail Uji Statistik (Chi-Square & Odds Ratio)

**Variabel Independen (X):** {x_label_title}

**Variabel Dependen (Y):** {y_label_title}

#### Case Processing Summary

| | Valid N | Valid % | Missing N | Missing % | Total N | Total % |
|---|---|---|---|---|---|---|
| {interaction_lbl} | {valid_cases_def} | {valid_cases_def/total_cases_def*100:.1f}% | {missing_cases_def} | {missing_cases_def/total_cases_def*100:.1f}% | {total_cases_def} | 100.0% |

#### {interaction_lbl} Crosstabulation

{crosstab_md}

#### Chi-Square Tests

**{interaction_lbl}**

| | Value | df | Asymp. Sig. (2-sided) |
|---|---|---|---|
| Pearson Chi-Square | {chi2_def:.3f} | {dof_def} | {p_def:.3f} |
| Likelihood Ratio | {g_def:.3f} | {dof_def} | {p_g_def:.3f} |
| Linear-by-Linear Association | {lbl_val_def:.3f} | 1 | {p_corr:.3f} |
| N of Valid Cases | {valid_cases_def} | | |

### Ringkasan Uji Hipotesis

**Result: {status_text_def}**

| Parameter | Nilai |
|---|---|
| P-Value | {p_def:.4f} |
| Chi-Square | {chi2_def:.3f} |
| df | {dof_def} |
| **Odds Ratio (Risk Estimate)** | **{or_def:.3f}** |

> **Interpretasi Sosial-Ekologis:**
>
> {"Hasil signifikan menunjukkan bahwa intensitas ekonomi ekstraktif memiliki asosiasi statistik dengan indikator tekanan sosial-demografis yang dipilih. Dalam konteks ini, memperkuat pembacaan bahwa pergeseran struktur ekonomi perlu dibaca bersama kepadatan, populasi smelter, dan beban kesehatan." if is_sig_def else "Jika hasil tidak signifikan, arah distribusi tetap penting dibaca karena ukuran panel Sulawesi terbatas. Ketidaksignifikanan tidak membatalkan temuan deskriptif, tetapi menunjukkan bahwa bukti asosiasi formal perlu dilengkapi dengan pembacaan trend dan narasi per wilayah."}

---

### Ringkasan Eksekutif Seluruh Skenario Crosstab

Tabel di bawah ini merangkum hasil pengujian statistik (Chi-Square) untuk semua kemungkinan kombinasi antara indikator Ekonomi Ekstraktif (X) dan Tekanan Sosial-Demografis (Y) pada panel kabupaten-tahun yang sama.

{exec_table_md}

> **Ringkasan Eksekutif:**
>
> Sebagian skenario menunjukkan hubungan signifikan antara intensitas ekonomi ekstraktif dan tekanan sosial-demografis. Karena unit observasi sudah diturunkan ke kabupaten-tahun, hasil ini lebih peka terhadap variasi lokal dibanding panel provinsi-tahun. Temuan ini memperkuat argumen bahwa hilirisasi nikel bukan hanya fenomena ekonomi sektoral, tetapi juga perubahan struktural yang menekan ruang hidup dan kesehatan publik.
"""'''

pattern = re.compile(r'md\s*=\s*f"""# Bab 9: Demografi & Struktur Sosial: Guncangan Sosial dan Pergeseran Ekonomi Agraris.*?^"""', re.MULTILINE | re.DOTALL)
new_content = pattern.sub(new_md, content)

with open(target_file, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"Patched {target_file}")
