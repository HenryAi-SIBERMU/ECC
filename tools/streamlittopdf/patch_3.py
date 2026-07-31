import sys
import re
from pathlib import Path

HERE = Path(r"c:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\tools\streamlittopdf")
target_file = HERE / "extract_chapter_3.py"

with open(target_file, "r", encoding="utf-8") as f:
    content = f.read()

new_md = r'''md = f"""# Beban Kesehatan Masyarakat Terdampak

**CELIOS — Center of Economic and Law Studies**

*Tinjauan empiris beban kesehatan masyarakat akibat paparan emisi dan polutan industri di kawasan penyangga smelter nikel Sulawesi.*

---

## Hilirisasi Nikel dan Dampak Kesehatan: Analisis Data Empiris di Kawasan Penyangga

Data empiris menggambarkan kesenjangan antara klaim pertumbuhan ekonomi dari ekspansi industri nikel dan kondisi kesehatan masyarakat di kawasan penyangga. Selama satu dekade terakhir, emisi partikulat, gas buang PLTU batu bara, dan timbulan limbah dari fasilitas ekstraktif telah memberikan tekanan signifikan terhadap kualitas lingkungan hidup masyarakat. Data empiris merekam bagaimana ekspansi kapasitas industri, yang ditopang oleh PLTU *captive* berkapasitas **{tot_kapasitas_pltu:,.0f} Megawatt**, berjalan sejajar dengan peningkatan kasus penyakit di kawasan-kawasan penyangga.

Sepanjang 2014–2024, data agregat dinas kesehatan mencatat total **kasus ISPA dan Pneumonia sebanyak {tot_ispa:,.0f} kasus**. Sementara itu, **kasus Diare tercatat sebanyak {tot_diare:,.0f} kasus**. Peningkatan insidensi penyakit ini berkorelasi dengan penurunan Indeks Kualitas Air (IKA) secara periodik. Konversi tutupan hutan untuk perluasan konsesi tambang turut berkontribusi pada pergeseran habitat satwa liar, yang berpotensi memicu perpindahan vektor penyakit zoonosis ke permukiman warga. Secara kumulatif, **kasus Malaria tercatat mencapai {tot_malaria:,.0f} kasus**, mengindikasikan tekanan terhadap keseimbangan ekologis di wilayah tambang.

Distribusi infrastruktur kesehatan di wilayah industri menunjukkan kesenjangan yang perlu menjadi perhatian. Ketersediaan fasilitas layanan primer seperti **Puskesmas tercatat sebanyak {tot_puskesmas_2024:,.0f} unit** pada tahun 2024, di kawasan yang bersamaan menanggung beban penyakit di atas rata-rata. Kondisi ini mengindikasikan bahwa pertumbuhan ekonomi dari hilirisasi nikel belum diimbangi dengan distribusi infrastruktur kesehatan yang proporsional bagi masyarakat di wilayah operasi industri (*sacrifice zone*).

---

## 3.1 Kesenjangan Fasilitas Kesehatan di Kawasan Ekstraktif

Data perbandingan distribusi fasilitas kesehatan mengindikasikan bahwa ketersediaan infrastruktur medis di provinsi sentra industri relatif tidak lebih baik dibandingkan wilayah non-sentra, meski beban penyakit di wilayah tersebut lebih tinggi.

Melalui komparasi grafik batang (*Grouped Bar Chart*) di bawah, terlihat bahwa ketersediaan Fasilitas Kesehatan di provinsi dengan konsentrasi industri tinggi justru mengalami defisit relatif. Rata-rata Rumah Sakit di Sentra Industri tercatat **{rs_sentra:.0f} unit** per provinsi, lebih rendah dari wilayah Non-Sentra yang mencapai **{rs_non:.0f} unit**. Kesenjangan distribusi fasilitas medis di area dengan beban penyakit tinggi ini perlu menjadi pertimbangan dalam perencanaan infrastruktur kesehatan ke depan.

![Fasilitas Kesehatan 2024: Sentra Industri vs Non-Sentra](visuals_bab3/chart_3_1_faskes.png)

---

## 3.2 Ketimpangan Beban Penyakit: Sentra Industri vs Non-Sentra

Melalui analisis komparatif spasial, terlihat bahwa beban ekologis tidak terdistribusi secara merata di seluruh wilayah. Provinsi sentra ekspansi nikel—Sulawesi Tengah dan Sulawesi Tenggara—menunjukkan indikator penyakit yang secara konsisten lebih tinggi.

Data menunjukkan bahwa rata-rata penderita **ISPA/Pneumonia** di Sentra Industri tercatat **{ispa_sentra:,.0f} kasus per tahun**, dibandingkan provinsi Non-Sentra di angka **{ispa_non:,.0f} kasus**. Selisih sebesar **{ispa_diff:.1f} kali lipat** ini mengindikasikan beban pernapasan yang lebih berat di kawasan penyangga *smelter*. Temuan ini mendukung hipotesis kerangka riset D3TLH: wilayah dengan konsentrasi industri tinggi cenderung menanggung beban kesehatan yang lebih besar akibat tekanan terhadap daya tampung lingkungan.

![Rata-rata Insidensi Penyakit Tahunan: Sentra vs Non-Sentra](visuals_bab3/chart_3_2_beban_penyakit.png)

---

## 3.3 Lintasan Waktu Ekologis & Dinamika Penyakit di Kawasan Industri Ekstraktif

![Tren 10 Tahun: Insidensi Penyakit Utama di Sentra Nikel Sulawesi](visuals_bab3/chart_3_3_tren_penyakit.png)

#### Uji Statistik: Asosiasi Kualitas Udara (IKU) dengan Insidensi Penyakit

### Detail Uji Statistik (Chi-Square & Odds Ratio)

**Variabel Independen (X):** {x_options[x_col]}

**Variabel Dependen (Y):** {y_options[y_col]}

##### Case Processing Summary

| | Valid N | Valid % | Missing N | Missing % | Total N | Total % |
|---|---|---|---|---|---|---|
| {interaction_label} | {valid_cases} | {valid_cases/total_cases*100:.1f}% | {missing_cases} | {missing_cases/total_cases*100:.1f}% | {total_cases} | 100.0% |

##### {interaction_label} Crosstabulation

{crosstab_md_iku}

##### Chi-Square Tests

**{interaction_label}**

| | Value | df | Asymp. Sig. (2-sided) |
|---|---|---|---|
| Pearson Chi-Square | {chi2:.3f} | {dof} | {p:.3f} |
| Likelihood Ratio | {g:.3f} | {dof} | {p_g:.3f} |
| Linear-by-Linear Association | {lbl_val:.3f} | 1 | {p_corr:.3f} |
| N of Valid Cases | {valid_cases} | | |

### Ringkasan Uji Hipotesis

**Result: {status_text}**

| Parameter | Nilai |
|---|---|
| P-Value | {p:.4f} |
| Chi-Square | {chi2:.3f} |
| df | {dof} |
| **Odds Ratio (Risk Estimate)** | **{odds_ratio:.3f}** |

> **Interpretasi Ekologis:**
>
> {interp_text}

---

### Ringkasan Eksekutif Seluruh Skenario Crosstab

{exec_hdr}
{exec_rows_iku}

> **Pembedahan Realitas Ekologis:**
>
> {exec_narrative}

---

## 3.4 Anomali Zoonosis: Dampak Kritis Ekspansi Industri di Level Tapak (Studi Kasus Sulteng)

Data empiris Dinas Kesehatan mencatat total akumulasi **{total_kasus_tambang:,.0f} kasus** penyakit Zoonosis di wilayah Lingkar Tambang/Smelter Aktif Sulawesi Tengah (Morowali, Morowali Utara, Banggai) sepanjang rentang waktu pengamatan.{peak_narrative}

Peningkatan angka zoonosis ini berkorelasi dengan perubahan ekologis akibat ekspansi penggunaan lahan. Konversi tutupan hutan demi perluasan konsesi dan fasilitas pengolahan *smelter* berdampak pada pergeseran habitat alami satwa liar. Akibatnya, vektor pembawa penyakit terpaksa bermigrasi dan beririsan langsung dengan pemukiman pekerja tambang dan warga lokal. Keberadaan genangan air galian tambang yang tidak direklamasi serta kondisi sanitasi di area industri turut menjadi faktor pendukung perkembangbiakan vektor penyakit.

Pertumbuhan investasi di sektor ekstraktif belum diimbangi dengan alokasi perlindungan sosial dan lingkungan yang memadai bagi masyarakat lokal. Penduduk asli dan pekerja tambang menghadapi risiko kesehatan berlapis: paparan emisi udara dari *captive power plant* sekaligus potensi risiko penyakit menular akibat disrupsi lingkungan hidup.

![Tren Zoonosis 2014-2024: Kasus di Lingkar Tambang vs Non-Tambang Sulteng](visuals_bab3/chart_3_4_tren_zoo_line.png)

![Komparasi Rata-rata Tahunan Penyakit Zoonosis (Sulteng)](visuals_bab3/chart_3_4_tren_zoo_bar.png)

> **Interpretasi Spesifik: {selected_penyakit}**
>
> Perbandingan grafik rata-rata di samping menunjukkan bahwa beban absolut kasus **{selected_penyakit}** di wilayah Lingkar Tambang/Smelter Aktif mencapai **{val_tambang:,.1f} kasus/tahun**.
>
> Meskipun populasi area tambang seringkali lebih terkonsentrasi, angka ini memberikan sinyal kuat bahwa degradasi lingkungan di sekitar smelter menciptakan ceruk ekologis baru (seperti genangan air galian) yang mempercepat siklus penularan {selected_penyakit}.

---

## Analisis Tambahan: Proxy Zoonosis (DBD) dan Tekanan Populasi: Tekanan Populasi dan Beban Kesehatan

#### Lintasan Waktu Kasus Malaria

DBD dipakai sebagai indikator proxy karena penyakit ini sensitif terhadap perubahan lingkungan permukiman, kepadatan, drainase, sanitasi, dan mobilitas penduduk. Analisis ini tidak menyatakan bahwa smelter secara tunggal menyebabkan DBD; yang diuji adalah apakah kabupaten smelter menunjukkan beban kesehatan yang perlu dibaca bersama tekanan demografi dan perubahan ruang. Sejak 2019, total kasus DBD yang tercatat di kabupaten smelter mencapai **{dbd_smelter:,}** kasus, sedangkan kabupaten non-smelter mencapai **{dbd_non_smelter:,}** kasus. Karena jumlah kabupaten dalam dua kelompok tidak sama, grafik memakai rata-rata kasus per kabupaten-tahun. Rata-rata kabupaten smelter tercatat sekitar **{dbd_avg_smelter:.1f}** kasus per observasi, sementara non-smelter sekitar **{dbd_avg_non_smelter:.1f}**. Rasio **{dbd_ratio:.2f} kali** ini harus dibaca hati-hati sebagai sinyal komparatif, bukan bukti kausal final, tetapi tetap penting untuk menilai beban sosial dari industrialisasi.

---

## 3.5 Pemetaan Geospasial: Distribusi Spasial Beban Penyakit

*(Peta Interaktif - Tidak ditampilkan dalam laporan statis)*

---

## 3.6 Krisis Air Bersih: Tinjauan Makro Provinsi dan Bukti Uji Klinis Lingkar Tambang

Menghadapi absennya data **"Akses Air Minum Layak"** di tingkat Kabupaten dari BPS sejak 2019, kami menggunakan **Ground Truth Data** dari pengujian laboratorium independen (AEER & WALHI) sebagai alternatif pengukur pencemaran air secara absolut.

Berdasarkan hasil uji klinis dari **{total_samples}** titik sampel di lingkar kawasan tambang, teridentifikasi bahwa **{exceed_biota} titik ({(exceed_biota/total_samples*100):.0f}%) melampaui batas aman toksisitas biota laut** (0.005 mg/L). Konsentrasi terparah ditemukan di **{max_location}** dengan kadar Kromium Heksavalen mencapai **{max_cr6:.3f} mg/L**, atau **{(max_cr6/0.005):.0f} kali lipat** lebih tinggi dari ambang batas aman.

⚠️ **Peringatan Klinis:** Kromium Heksavalen (Cr6+) adalah logam berat karsinogenik beracun. Paparan berulang pada air yang dikonsumsi atau digunakan mencuci memicu iritasi kulit kronis, kerusakan pernapasan, pencernaan, dan potensi kanker parah di komunitas lingkar tambang. Bukti konkret di level tapak ini mengonfirmasi asimetri dampak ekologis industri ekstraktif yang gagal ditangkap oleh agregasi data makro.

#### Pemetaan Analisis: Kualitas Air dan Kasus Diare

![Korelasi Kualitas Air vs Kasus Diare di Sulawesi (2014-2023)](visuals_bab3/chart_3_6_ika_diare.png)

> **Interpretasi Korelasi Statistik:**
>
> {interp_text_34}

#### Uji Statistik: Asosiasi IKA Rendah dengan Tingginya Kasus Diare

### Detail Uji Statistik (Chi-Square & Odds Ratio)

**Variabel Independen (X):** {x_options_ika[x_col_ika]}

**Variabel Dependen (Y):** {y_options_ika[y_col_ika]}

##### Case Processing Summary

| | Valid N | Valid % | Missing N | Missing % | Total N | Total % |
|---|---|---|---|---|---|---|
| {interaction_label_ika} | {valid_cases_ika} | {valid_cases_ika/total_cases_ika*100:.1f}% | {missing_cases_ika} | {missing_cases_ika/total_cases_ika*100:.1f}% | {total_cases_ika} | 100.0% |

##### {interaction_label_ika} Crosstabulation

{crosstab_md_ika}

##### Chi-Square Tests

**{interaction_label_ika}**

| | Value | df | Asymp. Sig. (2-sided) |
|---|---|---|---|
| Pearson Chi-Square | {chi2_ika:.3f} | {dof_ika} | {p_ika:.3f} |
| Likelihood Ratio | {g_ika:.3f} | {dof_ika} | {p_g_ika:.3f} |
| Linear-by-Linear Association | {lbl_val_ika:.3f} | 1 | {p_corr_ika:.3f} |
| N of Valid Cases | {valid_cases_ika} | | |

### Ringkasan Uji Hipotesis

**Result: {status_text_ika}**

| Parameter | Nilai |
|---|---|
| P-Value | {p_ika:.4f} |
| Chi-Square | {chi2_ika:.3f} |
| df | {dof_ika} |
| **Odds Ratio (Risk Estimate)** | **{odds_ratio_ika:.3f}** |

> **Interpretasi Ekologis:**
>
> {interp_text_ika}

---

### Ringkasan Eksekutif Seluruh Skenario Crosstab

{exec_hdr}
{exec_rows_ika_all}

> **Pembedahan Realitas Ekologis:**
>
> {exec_narrative_ika}

---

## 3.7 Beban Limbah Beracun (B3): Eksternalitas Kesehatan yang Diabaikan

**Skala Ancaman Limbah Beracun**

Data komprehensif dari berbagai sumber (AEER, WALHI, JATAM, BPLH) membuktikan bahwa industri nikel di Sulawesi menghasilkan **lebih dari {total_b3 / 1_000_000:.1f} juta ton limbah B3 per tahun**. Angka ini setara dengan menimbun **{total_b3 / 1000:,.0f} gedung bertingkat** dengan material beracun setiap tahunnya.

Provinsi **{max_prov["Provinsi"]}** menanggung beban terbesar dengan **{max_prov["Estimasi Timbulan (Ton/Tahun)"] / 1_000_000:.1f} juta ton** limbah B3 per tahun, didominasi oleh operasi **IMIP (Indonesia Morowali Industrial Park)** yang menghasilkan slag dan tailing HPAL tanpa izin formal yang memadai.

**Catatan Kritis:** Angka resmi ini kemungkinan besar *underestimate* (meremehkan) karena banyak fasilitas yang tidak melaporkan timbulan limbah secara transparan. Estimasi independen menyebutkan angka sebenarnya bisa 2-3 kali lipat lebih tinggi.

#### Distribusi Limbah B3 per Provinsi

![Distribusi Geografis Estimasi Limbah B3 Tambang & Smelter Nikel di Sulawesi](visuals_bab3/chart_3_7_b3_map.png)

> **Interpretasi Spasial:**
>
> Visualisasi di atas menunjukkan bahwa **Sulawesi Tengah dan Sulawesi Tenggara**—dua provinsi episentrum hilirisasi nikel—menanggung volume limbah B3 yang signifikan. **Sulawesi Tengah** menghasilkan **{sulteng_b3 / 1_000_000:.1f} juta ton B3/tahun**, terutama dari kawasan industri Morowali.
>
> Ini mencerminkan **ketimpangan ekologis**: wilayah penyangga menanggung beban limbah industri yang signifikan dibandingkan manfaat ekonomi langsung yang diterima. Warga lokal beriringan dengan lokasi timbunan slag—**sehingga membutuhkan pengawasan proteksi kesehatan dan transparansi pengolahan**.

#### Komposisi Limbah B3 Berdasarkan Jenis

![Komposisi Jenis Limbah B3 Industri Nikel Sulawesi](visuals_bab3/chart_3_7_b3_composition.png)

> **Interpretasi Komposisi Limbah:**
>
> **Slag dan Tailing** mendominasi timbulan limbah B3 dengan total **{(slag_total + tailing_total) / 1_000_000:.1f} juta ton/tahun**. Material ini mengandung konsentrasi tinggi logam berat seperti **Chromium (Cr), Nikel (Ni), Kadmium (Cd), dan Arsenik (As)** yang bersifat karsinogenik (memicu kanker) dan neurotoksik (merusak sistem saraf).
>
> Klaim industri bahwa slag "aman dimanfaatkan untuk batako" adalah **klaim yang perlu dikaji lebih kritis**. Penelitian mengindikasikan bahwa paparan jangka panjang terhadap debu slag berpotensi memicu **dermatitis dan gangguan pernapasan** pada komunitas sekitar.
>
> **Tailing HPAL** (High-Pressure Acid Leaching) lebih berbahaya lagi karena mengandung **asam sulfat konsentrasi tinggi** yang dapat mencemari sungai dan laut. Proses HPAL yang digunakan PT HNC dan PT QMB di Morowali menghasilkan **12,5 juta ton tailing beracun per tahun**—setara dengan volume banjir bandang yang terjadi setiap hari.

#### Fasilitas Penghasil Limbah B3 Terbesar

![Top 10 Fasilitas Industri Penghasil Limbah B3 Terbesar (Estimasi Ton/Tahun)](visuals_bab3/chart_3_7_b3_top10.png)

#### Kaitan dengan Beban Kesehatan Masyarakat

**Kesimpulan Kritis: Beban Ganda Masyarakat Terdampak**

Data limbah B3 di atas menegaskan bahwa masyarakat di zona penyangga smelter **menanggung beban ganda (double burden)**:
1. **Beban Polusi Aktif:** Paparan harian terhadap emisi SO₂, debu PM2.5, dan pencemaran air (terbukti di sub-bab 3.3 dan 3.5)
2. **Beban Polusi Pasif:** Hidup berdampingan dengan timbunan **{total_b3 / 1_000_000:.1f} juta ton limbah beracun** yang terakumulasi setiap tahun—**tanpa jaminan keamanan jangka panjang**

Kompleks IMIP di Morowali menghasilkan **{imip_b3 / 1_000_000:.1f} juta ton limbah B3/tahun**. Hal ini menunjukkan pentingnya evaluasi independen atas dampak lingkungan dan kesehatan dari ekspansi industri nikel bagi masyarakat sekitar.

**Rekomendasi Kebijakan:** Pemerintah harus segera menghentikan ekspansi smelter baru hingga tersedia kajian risiko kesehatan independen, sistem monitoring limbah B3 yang transparan, dan skema kompensasi yang adil bagi masyarakat terdampak. **Hak atas lingkungan hidup yang sehat adalah hak asasi yang tidak dapat ditawar dengan pertumbuhan ekonomi semata**.
"""'''

pattern = re.compile(r'md\s*=\s*f"""# Beban Kesehatan Masyarakat Terdampak.*?^"""', re.MULTILINE | re.DOTALL)
new_content = pattern.sub(new_md, content)

with open(target_file, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"Patched {target_file}")
