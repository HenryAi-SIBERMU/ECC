import sys
import re
from pathlib import Path

HERE = Path(r"c:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\tools\streamlittopdf")
target_file = HERE / "extract_chapter_4.py"

with open(target_file, "r", encoding="utf-8") as f:
    content = f.read()

# We'll search from `# Default crosstab table strings` up to `out_path = HERE`
pattern = re.compile(r"# Default crosstab table strings.*?(?=out_path = HERE / \"chapter_4.md\")", re.DOTALL)

new_markdown_logic = """# Default crosstab table strings
total_cases_ct  = len(df_crosstab)
valid_cases_ct  = len(df_crosstab.dropna(subset=['Periode_Ekspansi','Indikasi_Kriminalisasi']))
missing_cases_ct= total_cases_ct - valid_cases_ct
x_lbl_ct = "Periode Ekspansi Industri"
y_lbl_ct = "Tingkat Represi & Kriminalisasi"
interaction_lbl = f"{x_lbl_ct} * {y_lbl_ct}"

cx_def = x_order["Periode_Ekspansi"]
cy_def = y_order["Indikasi_Kriminalisasi"]

# Crosstab rows for markdown table
def fmt_crosstab_md(ct, exp_df, cx, cy):
    header = "| | " + " | ".join(cy) + " | Total |"
    sep    = "|---|" + "|".join(["---"]*len(cy)) + "|---|"
    rows   = [header, sep]
    for x_cat in cx:
        counts = ct.loc[x_cat].tolist()
        exps   = exp_df.loc[x_cat].tolist()
        rows.append(f"| **{x_cat}** Count | " + " | ".join(str(v) for v in counts) + f" | {sum(counts)} |")
        rows.append(f"| **{x_cat}** Expected | " + " | ".join(f"{v:.1f}" for v in exps) + f" | {sum(exps):.1f} |")
    total_c = ct.sum().tolist()
    total_e = exp_df.sum().tolist()
    rows.append("| **Total** Count | " + " | ".join(str(v) for v in total_c) + f" | {sum(total_c)} |")
    rows.append("| **Total** Expected | " + " | ".join(f"{v:.1f}" for v in total_e) + f" | {sum(total_e):.1f} |")
    return "\\n".join(rows)

crosstab_md = fmt_crosstab_md(ct_default, exp_default, cx_def, cy_def)

try:
    g_val, p_g, dof_g, _ = stats.chi2_contingency(ct_default, lambda_="log-likelihood")
except:
    g_val, p_g = 0, 1
x_codes = df_crosstab["Periode_Ekspansi"].replace({cx_def[0]:0, cx_def[1]:1})
y_codes = df_crosstab["Indikasi_Kriminalisasi"].replace({cy_def[0]:0, cy_def[1]:1})
try:
    r_val, p_corr = stats.pearsonr(list(x_codes), list(y_codes))
    lbl_val = (valid_cases_ct - 1) * (r_val**2)
except:
    r_val, p_corr, lbl_val = 0, 1, 0

status_text = "SIGNIFIKAN" if p_default < 0.05 else "TIDAK SIGNIFIKAN"

if p_default < 0.05:
    interp_text = (
        f"Temuan ini sangat krusial: pergeseran status **{x_lbl_ct}** terbukti **berkorelasi kuat dan signifikan** dengan **{y_lbl_ct}** "
        f"(P < 0.05). Angka Odds Ratio (OR: {or_default:.3f}) menjadi konfirmasi empiris bahwa narasi hilirisasi dan investasi bukanlah "
        "agenda nirkekerasan—ekspansi spasial mereka mutlak mengeskalasi pelanggaran hak asasi masyarakat tapak."
    )
else:
    interp_text = (
        f"Secara agregat, hubungan antara **{x_lbl_ct}** dan **{y_lbl_ct}** **tidak menunjukkan perbedaan yang signifikan** secara statistik "
        "(P >= 0.05). Hal ini mengindikasikan bahwa penggunaan instrumen kekerasan sudah mengakar dan sistematis di sepanjang sejarah konflik "
        "agraria tanpa memandang batas waktu rezim atau aktor yang terlihat."
    )

# BUILD ANOMALIES JIWA
jiwa_anomalies_md = ""
import urllib.parse
for i, year in enumerate(top_jiwa.index, 1):
    jiwa_anomalies_md += f"\\n#### ANOMALI JIWA {i}: Lonjakan Korban Jiwa Tahun {year}\\n"
    cases = df_konflik[df_konflik['tahun'] == year].copy()
    cases['jiwa_num'] = pd.to_numeric(cases['dampak_masyarakat_jiwa'].astype(str).replace(',', '', regex=True).replace(' Jiwa', '', regex=True), errors='coerce').fillna(0)
    top_case = cases.sort_values('jiwa_num', ascending=False).iloc[0] if not cases.empty else None
    
    if top_case is not None:
        judul = top_case['judul']
        korban = top_case['jiwa_num']
        pt = top_case['keterlibatan_perusahaan'] if pd.notna(top_case['keterlibatan_perusahaan']) else 'Tidak/Belum Teridentifikasi'
        narasi = str(top_case['narasi'])[:450] + "..." if pd.notna(top_case['narasi']) and str(top_case['narasi']).strip() != 'nan' else (str(top_case['deskripsi'])[:450] + "...")
        sumber_lsm = top_case['sumber'] if 'sumber' in top_case and pd.notna(top_case['sumber']) else 'Kompilasi LSM'
        tk_link = top_case['detail_url'] if 'detail_url' in top_case and pd.notna(top_case['detail_url']) else '#'
        search_query = urllib.parse.quote(f"{judul} {pt}")
        link = f"https://www.google.com/search?q={search_query}"
        
        jiwa_anomalies_md += f"- **Kasus Utama Pendongkrak Statistik:** {judul}\\n"
        jiwa_anomalies_md += f"- **Total Korban (Kasus Ini):** {int(korban):,} Jiwa\\n"
        jiwa_anomalies_md += f"- **Perusahaan Terlibat:** {pt}\\n"
        jiwa_anomalies_md += f"- **Narasi Singkat:** {narasi}\\n"
        jiwa_anomalies_md += f"- **Sumber Referensi:** Laporan {sumber_lsm} ([Telusuri Berita Kasus]({link}) | [Link Asli TanahKita]({tk_link}))\\n"

# BUILD ANOMALIES AREA
ha_anomalies_md = ""
for i, year in enumerate(top_ha.index, 1):
    ha_anomalies_md += f"\\n#### ANOMALI AREA {i}: Monopoli Area Konflik Tahun {year}\\n"
    cases = df_konflik[df_konflik['tahun'] == year].copy()
    cases['ha_num'] = pd.to_numeric(cases['luas_ha'].astype(str).replace(',', '', regex=True).replace(' Ha', '', regex=True), errors='coerce').fillna(0)
    top_case = cases.sort_values('ha_num', ascending=False).iloc[0] if not cases.empty else None
    
    if top_case is not None:
        judul = top_case['judul']
        luas = top_case['ha_num']
        pt = top_case['keterlibatan_perusahaan'] if pd.notna(top_case['keterlibatan_perusahaan']) else 'Tidak/Belum Teridentifikasi'
        narasi = str(top_case['narasi'])[:450] + "..." if pd.notna(top_case['narasi']) and str(top_case['narasi']).strip() != 'nan' else (str(top_case['deskripsi'])[:450] + "...")
        sumber_lsm = top_case['sumber'] if 'sumber' in top_case and pd.notna(top_case['sumber']) else 'Kompilasi LSM'
        tk_link = top_case['detail_url'] if 'detail_url' in top_case and pd.notna(top_case['detail_url']) else '#'
        search_query = urllib.parse.quote(f"{judul} {pt}")
        link = f"https://www.google.com/search?q={search_query}"
        
        ha_anomalies_md += f"- **Kasus Utama Pendongkrak Statistik:** {judul}\\n"
        ha_anomalies_md += f"- **Total Daratan Dirampas (Kasus Ini):** {int(luas):,} Hektar\\n"
        ha_anomalies_md += f"- **Perusahaan Terlibat:** {pt}\\n"
        ha_anomalies_md += f"- **Narasi Singkat:** {narasi}\\n"
        ha_anomalies_md += f"- **Sumber Referensi:** Laporan {sumber_lsm} ([Telusuri Berita Kasus]({link}) | [Link Asli TanahKita]({tk_link}))\\n"

md = f'''# Ruang Hidup yang Terampas

Analisis dinamika konflik sosial dan alokasi ruang agraria dalam konteks pembangunan kawasan.

---

Ekspansi industri ekstraktif dan proyek strategis berimplikasi pada dinamika sosial dan penggunaan lahan masyarakat. Data empiris mencatat akumulasi **{total_konflik} kasus konflik agraria**. Konflik ini berkaitan erat dengan perubahan tata guna lahan dan alokasi ruang di berbagai daerah.

Aktor dan sektor pemicu konflik mencakup sektor **Kehutanan** (Hutan Lindung, Produksi, Konservasi), **Infrastruktur & PSN** (Bendungan, Transmigrasi, Kawasan Industri), hingga proyek **Pariwisata & Pesisir**. Tiga sektor utama (Perkebunan, Kehutanan, dan Pertambangan) menyumbang porsi **{rasio_ekstraktif:.1f}%** dari keseluruhan catatan konflik.

---

### 4.1 Tren Eskalasi Konflik Agraria Seiring Ekspansi Industri

Visualisasi *time-series* di bawah ini memberikan gambaran korelasi antara ekspansi industri dan dinamika konflik agraria di daratan Sulawesi. Secara historis, perbandingan dua periode waktu menunjukkan perbedaan tingkat insidensi konflik. Pada periode pra-2005, sistem pendataan mencatat **{pra_2005} kasus** konflik agraria.

Pada periode pasca-2005 hingga saat ini, data mencatat **{pasca_2005} kasus** konflik lahan, yang mencerminkan peningkatan sebesar **{lonjakan:,.1f}%** dibandingkan periode sebelumnya. Perubahan tren ini beriringan dengan penerbitan Izin Usaha Pertambangan (IUP) serta ekspansi Hak Guna Usaha (HGU) untuk perkebunan.

Penelusuran tren satu dekade terakhir menunjukkan bahwa sengketa agraria mencakup berbagai sektor, termasuk pertambangan nikel, infrastruktur, dan Proyek Strategis Nasional. Akumulasi **{total_ts} insiden historis** ini mengindikasikan perlunya tata kelola alokasi lahan dan perlindungan hak masyarakat lokal yang lebih seimbang di kawasan investasi.

![Peningkatan Signifikan Konflik Agraria di Sulawesi (1990-2025)](visuals_bab4/chart_4_1_konflik_timeseries.png)

> **Interpretasi Ekologis: Puncak Insidensi Konflik 2017**
>
> Grafik memperlihatkan peningkatan insidensi konflik yang memuncak pada **tahun 2017** dengan **75 kasus konflik**. Pembedahan data sektoral menunjukkan konsentrasi pada sektor **Kehutanan (40 kasus)** dan **Perkebunan (21 kasus)**, diikuti oleh **Pertambangan dan Infrastruktur PSN**. Periode ini bertepatan dengan percepatan pelepasan kawasan hutan dan Izin Pinjam Pakai Kawasan Hutan (IPPKH) untuk mendukung proyek strategis dan kawasan industri.

> **Interpretasi Ekologis dan Sosial:**
>
> Peningkatan insidensi konflik beririsan dengan dinamika perizinan kawasan. Pengelolaan alokasi ruang dan perlindungan hak masyarakat di wilayah investasi menjadi faktor penting untuk meminimalkan dampak sosial.

---

### 4.2 Sebaran Sektoral: Dampak Masyarakat dan Penggunaan Lahan

Visualisasi komparatif di bawah ini menggambarkan skala dampak sosial dan penggunaan lahan berdasarkan sektor industri. Data menunjukkan bahwa **Sektor Kehutanan** mencatatkan jumlah warga terdampak sebanyak **{jiwa_kehutanan:,.0f} jiwa**, berkaitan dengan tumpang tindih kawasan hutan produksi, konservasi, dan Hutan Tanaman Industri (HTI) dengan wilayah kelola masyarakat lokal.

Menyusul berikutnya adalah **Sektor Pertambangan** dengan total korban terdampak sebanyak **{jiwa_tambang:,.0f} jiwa**, yang beririsan dengan proyek hilirisasi nikel dan tambang terbuka di kawasan pesisir dan pertanian.

Dari dimensi penggunaan lahan (luasan hektar yang terlibat sengketa), **Sektor Perkebunan** mencatatkan luas sengketa terbesar yaitu **{ha_kebun:,.0f} Hektar**, disusul oleh sektor Kehutanan seluas **{ha_kehutanan:,.0f} Ha** dan Pertambangan seluas **{ha_tambang:,.0f} Ha**. Data ini menunjukkan bahwa dinamika penguasaan lahan di tiga sektor tersebut berkorelasi dengan tingginya insidensi sengketa agraria di tingkat lokal.

![Peningkatan Signifikan Korban Terdampak (Jiwa) per Tahun](visuals_bab4/chart_4_2a_jiwa.png)

![Monopoli Area Konflik (Hektar) per Tahun](visuals_bab4/chart_4_2b_ha.png)

> **Interpretasi Ekologis dan Sosial:**
>
> Dinamika Grafik mencerminkan akumulasi dampak sosial di wilayah industri yang memerlukan perhatian dalam pengelolaan sengketa lahan.

### Bedah Forensik Anomali (Spike) Konflik Agraria

Berdasarkan ekstraksi dataset secara mendalam, berikut adalah bedah anatomis dari lonjakan-lonjakan ekstrem (*spikes*) yang terjadi pada grafik **Peningkatan Signifikan Korban Terdampak (Jiwa)** dan **Monopoli Area Konflik (Hektar)** di wilayah ini.

{jiwa_anomalies_md}

{ha_anomalies_md}

---

### 4.3 Indikasi Represi dan Kriminalisasi dalam Konflik Agraria

Data kuantitatif di wilayah Sulawesi mencatat indikasi terjadinya represi dan tindakan kriminalisasi dalam sebagian sengketa agraria. Dari database yang didokumentasikan, terdapat **{total_kriminalisasi} kasus indikasi kriminalisasi** dan **{total_ditangkap} warga/aktivis lingkungan yang tercatat pernah ditangkap** dalam penanganan sengketa lahan.

Berdasarkan distribusi sektoral, **Sektor {top_sektor}** mencatatkan frekuensi indikasi represi tertinggi dengan **{top_sektor_count} kasus**. Tahun dengan jumlah catatan insiden represi tertinggi adalah **{top_tahun}** dengan **{top_tahun_count} kasus**.

Catatan ini menunjukkan pentingnya pendekatan hukum yang adil, penyelesaian konflik secara ramah HAM, serta jaminan perlindungan bagi pejuang lingkungan dan komunitas lokal sesuai dengan peraturan perundang-undangan.

| Kasus Indikasi Kriminalisasi | Warga/Aktivis Ditangkap | Korban Luka-luka | Korban Tewas |
|---|---|---|---|
| **{total_kriminalisasi} Kasus** | **{total_ditangkap} Orang** | **{total_luka} Orang** | **{total_tewas} Orang** |

![Tren Kasus Kriminalisasi & Represi (Pasca 2000)](visuals_bab4/chart_4_3a_kriminalisasi_trend.png)

![Sektor Industri Paling Represif](visuals_bab4/chart_4_3b_sektor_represif.png)

> **Interpretasi Ekologis & Hak Asasi Manusia:** Keberadaan kasus kriminalisasi di sekitar area konsesi (terutama {top_sektor}) mengindikasikan pentingnya jaminan perlindungan ruang sipil dan penghormatan HAM dalam setiap proses pembangunan.

---

### 4.4 Pembuktian Statistik: Ekspansi vs Eskalasi Konflik

Hipotesis utama dalam evaluasi ini adalah bahwa **industrialisasi dan ekspansi korporasi** berbanding lurus dengan **eskalasi konflik dan represi** terhadap masyarakat. 
Untuk mengujinya secara statistik sesuai pedoman D3TLH, analisis dibagi menjadi dua bagian: (1) Komparasi metrik Before-After, dan (2) Uji signifikansi Crosstab Chi-Square. Unit observasinya adalah catatan kejadian letupan konflik historis.

#### A. Analisis Komparatif Before-After (Pra vs Era Hilirisasi)

Perbandingan absolut eskalasi konflik agraria sebelum dan sesudah rezim hilirisasi masif dimulai (cut-off tahun 2014).

| Periode | Rata-rata Konflik | Total Letupan | Warga Ditangkap | Korban Tewas |
|---|---|---|---|---|
| **Pra-Ekspansi (1990 - 2013)** | **{avg_pra:.1f} Kasus/Tahun** | {len(df_pra)} kejadian | {int(df_pra['jumlah_ditangkap'].sum())} jiwa | {int(df_pra['jumlah_tewas'].sum())} jiwa |
| **Pasca-Ekspansi (2014 - 2024)** | **{avg_pasca:.1f} Kasus/Tahun** | {len(df_pasca)} kejadian | {int(df_pasca['jumlah_ditangkap'].sum())} jiwa | {int(df_pasca['jumlah_tewas'].sum())} jiwa |

#### B. Uji Statistik Crosstab (Chi-Square)

**Variabel Independen (X):** Periode Ekspansi Industri

**Variabel Dependen (Y):** Tingkat Represi & Kriminalisasi

#### Case Processing Summary

| | Valid N | Valid % | Missing N | Missing % | Total N | Total % |
|---|---|---|---|---|---|---|
| {interaction_lbl} | {valid_cases_ct} | {valid_cases_ct/total_cases_ct*100:.1f}% | {missing_cases_ct} | {missing_cases_ct/total_cases_ct*100:.1f}% | {total_cases_ct} | 100.0% |

#### {interaction_lbl} Crosstabulation

{crosstab_md}

#### Chi-Square Tests

**{interaction_lbl}**

| | Value | df | Asymp. Sig. (2-sided) |
|---|---|---|---|
| Pearson Chi-Square | {chi2_default:.3f} | {dof_default} | {p_default:.3f} |
| Likelihood Ratio | {g_val:.3f} | {dof_default} | {p_g:.3f} |
| Linear-by-Linear Association | {lbl_val:.3f} | 1 | {p_corr:.3f} |
| N of Valid Cases | {valid_cases_ct} | | |

### Ringkasan Uji Hipotesis

**Result: {status_text}**

| Parameter | Nilai |
|---|---|
| P-Value | {p_default:.4f} |
| Chi-Square | {chi2_default:.3f} |
| df | {dof_default} |
| **Odds Ratio (Risk Estimate)** | **{or_default:.3f}** |

> **Interpretasi Sosial Kritis:** {interp_text}

---

### Ringkasan Eksekutif Seluruh Skenario Crosstab

Tabel di bawah ini merangkum hasil pengujian statistik (Chi-Square) untuk semua kemungkinan kombinasi antara indikator Ekspansi (X) dan Eskalasi Konflik (Y) pada panel data yang sama.

{exec_table_md}

> **Pembedahan Realitas Kemanusiaan:**
>
> {exec_narrative}

---

### 4.5 Peta Entitas Aktor: Korporasi dan Organisasi Masyarakat

Analisis entitas aktor berbasis pemrosesan teks (*string parsing*) terhadap catatan kronologi dokumentasi TanahKita memetakan keterlibatan berbagai pihak dalam sengketa agraria. Hasil ekstraksi teks mengidentifikasi entitas korporasi, lembaga pemerintah, serta organisasi masyarakat sipil yang tercatat dalam dokumentasi kasus. Grafik frekuensi di bawah menampilkan entitas korporasi dan kelompok masyarakat yang paling sering teridentifikasi dalam catatan sengketa lahan.

#### Top 10 Entitas Korporasi Paling Dominan

![Top 10 Entitas Korporasi Paling Dominan](visuals_bab4/chart_4_5a_korporasi.png)

> **Analisis Data Korporasi:** Ekstraksi teks mencatat frekuensi penyebutan entitas **{top1_corp_name}** dalam **{top1_corp_freq} catatan kasus terpisah**.

#### Top Aktor Proksi & Vigilante Terdeteksi

![Top Aktor Proksi & Vigilante Terdeteksi](visuals_bab4/chart_4_5b_vigilante.png)

> **Analisis Kritis Proksi/Vigilante:** Kemunculan kelompok sipil seperti **{top1_civ_name}** (terdeteksi hingga **{top1_civ_freq} kali**) menangkap besarnya skala orkestrasi horizontal. Korporasi seringkali menggunakan jasa pengamanan swakarsa, kelompok preman, hingga ormas vigilante sebagai "bemper proksi" untuk mengintimidasi warga lokal dan memecah belah solidaritas akar rumput.

*\\* Grafik di atas hanya menampilkan Top 10 entitas. Untuk melihat daftar lengkap dan detail seluruh aktor yang terdeteksi, silakan buka tabel data.*
'''
"""

# USE LAMBDA TO AVOID BACKREFERENCE PARSING IN RE.SUBN
new_content, count = pattern.subn(lambda m: new_markdown_logic, content)

if count > 0:
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Patched {target_file.name} successfully!")
else:
    print("Could not find the target block to patch.")
