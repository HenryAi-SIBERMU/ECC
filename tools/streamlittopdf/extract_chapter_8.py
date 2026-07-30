"""
extract_chapter_8.py
100% faithful extraction of pages/8_Distribusi_Manfaat.py → chapter_8.md
"""
import os, sys, re
import pandas as pd
import scipy.stats as stats
from functools import reduce
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = ROOT / "data" / "processed"
VIS  = HERE / "visuals_bab8"
VIS.mkdir(exist_ok=True)

# ─── DATA LOAD & CROSSTAB 8.3 CALCULATIONS ──────────────────────────────────
df_inv = pd.read_csv(DATA / "sulawesi_investasi_pmdn_2016_2024.csv")
df_inv_agg = df_inv.groupby(['provinsi', 'tahun'])['nilai'].sum().reset_index()
df_inv_agg.rename(columns={'nilai': 'Realisasi_Investasi_Rp'}, inplace=True)

df_pad = pd.read_csv(DATA / "sulawesi_pad_2016_2024.csv")
df_pad.rename(columns={'pad_juta_rupiah': 'PAD_Juta_Rupiah'}, inplace=True)

df_kes = pd.read_csv(DATA / "sulawesi_kesehatan_detail_2014_2024.csv")
df_ispa_agg = df_kes[df_kes['indikator'] == 'Kasus ISPA/Pneumonia'].groupby(['provinsi', 'tahun'])['nilai'].sum().reset_index()
df_ispa_agg.rename(columns={'nilai': 'Kasus_ISPA'}, inplace=True)

df_def = pd.read_csv(DATA / "sulawesi_gfw_master_1_dekade_2014_2023.csv")
df_def.rename(columns={'Provinsi': 'provinsi', 'Tahun': 'tahun', 'Total_Deforestasi_Ha': 'Deforestasi_Ha'}, inplace=True)

dfs = [df_inv_agg, df_pad, df_ispa_agg, df_def[['provinsi', 'tahun', 'Deforestasi_Ha']]]
df_panel = reduce(lambda left, right: pd.merge(left, right, on=['provinsi', 'tahun'], how='outer'), dfs)
df_panel.rename(columns={'provinsi': 'Provinsi', 'tahun': 'Tahun'}, inplace=True)

x_opt = {
    "Realisasi_Investasi_Rp": "Investasi PMDN (Rupiah)",
    "PAD_Juta_Rupiah": "Pendapatan Asli Daerah (Juta Rp)"
}
y_opt = {
    "Kasus_ISPA": "Beban Penyakit (Kasus ISPA)",
    "Deforestasi_Ha": "Beban Pencemaran (Deforestasi Ha)"
}

# Compute Crosstab Default: Realisasi_Investasi_Rp vs Kasus_ISPA
x_col_def = "Realisasi_Investasi_Rp"
y_col_def = "Kasus_ISPA"

med_x = df_panel[x_col_def].median()
med_y = df_panel[y_col_def].median()

lbl_x_h = f"Tinggi (≥{med_x:,.1f})"
lbl_x_l = f"Rendah (<{med_x:,.1f})"
lbl_y_h = f"Tinggi (≥{med_y:,.1f})"
lbl_y_l = f"Rendah (<{med_y:,.1f})"

df_panel["X_Label"] = df_panel[x_col_def].apply(lambda v: lbl_x_h if v >= med_x else lbl_x_l)
df_panel["Y_Label"] = df_panel[y_col_def].apply(lambda v: lbl_y_h if v >= med_y else lbl_y_l)

cats_x = [lbl_x_l, lbl_x_h]
cats_y = [lbl_y_l, lbl_y_h]

crosstab_def = pd.crosstab(df_panel["X_Label"], df_panel["Y_Label"]).reindex(index=cats_x, columns=cats_y, fill_value=0)
try:
    chi2_def, p_def, dof_def, exp_def = stats.chi2_contingency(crosstab_def)
except:
    chi2_def, p_def, dof_def, exp_def = 0, 1, 0, crosstab_def.values

exp_df_def = pd.DataFrame(exp_def, index=cats_x, columns=cats_y)

try:
    a = crosstab_def.loc[lbl_x_l, lbl_y_l]
    b = crosstab_def.loc[lbl_x_l, lbl_y_h]
    c = crosstab_def.loc[lbl_x_h, lbl_y_l]
    d = crosstab_def.loc[lbl_x_h, lbl_y_h]
    or_def = (a * d) / (b * c) if (b * c) > 0 else 0
except:
    or_def = 0

try:
    g_def, p_g_def, _, _ = stats.chi2_contingency(crosstab_def, lambda_="log-likelihood")
except:
    g_def, p_g_def = 0, 1

valid_cases_def = len(df_panel.dropna(subset=[x_col_def, y_col_def]))
total_cases_def = len(df_panel)
missing_cases_def = total_cases_def - valid_cases_def

x_codes = df_panel["X_Label"].replace({lbl_x_l: 0, lbl_x_h: 1})
y_codes = df_panel["Y_Label"].replace({lbl_y_l: 0, lbl_y_h: 1})
try:
    r_val, p_corr = stats.pearsonr(list(x_codes), list(y_codes))
    lbl_val_def = (valid_cases_def - 1) * (r_val**2)
except:
    r_val, p_corr, lbl_val_def = 0, 1, 0

interaction_lbl = f"{x_opt[x_col_def]} * {y_opt[y_col_def]}"
is_sig_def = p_def < 0.05
status_text_def = "SIGNIFIKAN" if is_sig_def else "TIDAK SIGNIFIKAN"

# Summary of All Combinations
summary_data = []
for k_x, v_x in x_opt.items():
    for k_y, v_y in y_opt.items():
        mx = df_panel[k_x].median()
        my = df_panel[k_y].median()
        lxh = f"Tinggi (≥{mx:,.1f})"; lxl = f"Rendah (<{mx:,.1f})"
        lyh = f"Tinggi (≥{my:,.1f})"; lyl = f"Rendah (<{my:,.1f})"
        sx = df_panel[k_x].apply(lambda v: lxh if v >= mx else lxl)
        sy = df_panel[k_y].apply(lambda v: lyh if v >= my else lyl)
        ct = pd.crosstab(sx, sy).reindex(index=[lxl, lxh], columns=[lyl, lyh], fill_value=0)
        try:
            c2, pv, dofv, _ = stats.chi2_contingency(ct)
        except:
            c2, pv, dofv = 0, 1, 0
        try:
            aa = ct.loc[lxl, lyl]; bb = ct.loc[lxl, lyh]
            cc = ct.loc[lxh, lyl]; dd = ct.loc[lxh, lyh]
            orv = (aa * dd) / (bb * cc) if (bb * cc) > 0 else 0
        except:
            orv = 0
        sig = "🟢 SIGNIFIKAN" if pv < 0.05 else "🔴 TIDAK SIGNIFIKAN"
        summary_data.append({
            "Variabel Independen (X)": v_x,
            "Variabel Dependen (Y)": v_y,
            "Chi-Square": f"{c2:.3f}",
            "P-Value": f"{pv:.3f}",
            "Odds Ratio": f"{orv:.2f}",
            "Kesimpulan": sig
        })

def fmt_ct_md(ct, exp_df, cx, cy):
    header = "| | " + " | ".join(cy) + " | Total |"
    sep    = "|---|" + "|".join(["---"]*len(cy)) + "|---|"
    rows   = [header, sep]
    for x_cat in cx:
        counts = ct.loc[x_cat].tolist()
        exps   = exp_df.loc[x_cat].tolist()
        rows.append(f"| **{x_cat}** Count | " + " | ".join(str(v) for v in counts) + f" | {sum(counts)} |")
        rows.append(f"| **{x_cat}** Expected | " + " | ".join(f"{v:.1f}" for v in exps) + f" | {sum(exps):.1f} |")
    tc = ct.sum().tolist(); te = exp_df.sum().tolist()
    rows.append("| **Total** Count | " + " | ".join(str(v) for v in tc) + f" | {sum(tc)} |")
    rows.append("| **Total** Expected | " + " | ".join(f"{v:.1f}" for v in te) + f" | {sum(te):.1f} |")
    return "\n".join(rows)

crosstab_md = fmt_ct_md(crosstab_def, exp_df_def, cats_x, cats_y)

exec_header = "| Variabel Independen (X) | Variabel Dependen (Y) | Chi-Square | P-Value | Odds Ratio | Kesimpulan |"
exec_sep    = "|---|---|---|---|---|---|"
exec_rows   = [exec_header, exec_sep]
for row in summary_data:
    exec_rows.append(f"| {row['Variabel Independen (X)']} | {row['Variabel Dependen (Y)']} | {row['Chi-Square']} | {row['P-Value']} | {row['Odds Ratio']} | {row['Kesimpulan']} |")
exec_table_md = "\n".join(exec_rows)

# ─── BUILD MARKDOWN ──────────────────────────────────────────────────────────
print("Writing 100% faithful chapter_8.md ...")

md = f"""# Bab 8: Distribusi Manfaat vs Beban Ekologis

**CELIOS — Center of Economic and Law Studies**

*Analisis Ketimpangan: Distribusi Manfaat Ekonomi dan Dampak Lingkungan Sektor Ekstraktif*

---

## Metodologi
**Alur Analisis (Ekonomi Politik Ekologi):** `Investasi Ekstraktif` → `Konsentrasi Manfaat Ekonomi` → `Dampaknya Terhadap Beban Lingkungan & Sosial`

Bagian ini menguji distribusi manfaat dan dampak dengan pendekatan analisis *Crosstabulation* (tabulasi silang) antara indikator akumulasi kekayaan/investasi dengan sebaran dampak sosial-ekologis di wilayah ekstraktif Sulawesi.

---

## Hilirisasi & Distribusi Manfaat

Pengembangan kawasan industri nikel di Sulawesi ditujukan untuk meningkatkan nilai tambah ekonomi dan pendapatan daerah. Namun, analisis data memperlihatkan adanya dinamika ketimpangan dalam distribusi manfaat dan dampak ekologis.

Bagian ini menguji sejauh mana eksternalitas ekonomi dan lingkungan terdistribusi. Analisis menyandingkan indikator arus investasi dan profitabilitas korporasi dengan indikator beban lingkungan (seperti insidensi ISPA, sengketa lahan, dan kualitas sumber daya air) yang dirasakan oleh komunitas lokal di Sulawesi.

---

## 8.1 Sisi Manfaat: Gurita Bisnis & Monopoli Keuntungan Ekstraktif

**Metode: Wealth Database Analysis (CELIOS Inequality Report 2026)**

### Metodologi: Pemetaan Konsentrasi Kekayaan Ekstraktif

**Metode Analisis:** Sub-bab ini menggunakan pemrofilan entitas bisnis berjenjang (*Hierarchical Entity Profiling*) untuk melacak aliran penguasaan sumber daya menuju kelompok elit (*Top 50 Wealthy Individuals*).

1. **Model Pengungkapan Afiliasi Oligarki:**
    * **Mega-Crosstab Pemetaan Aktor:** Menghubungkan secara langsung data akumulasi kekayaan agregat (Net Worth) dari laporan ketimpangan dengan instrumen kerusakan aktual di lapangan (Luas Konsesi, Kapasitas PLTU, Deforestasi, dan Dampak Sosial).
    * **Kuantifikasi Daya Rusak Privat:** Mengukur skala kerugian publik (eksternalitas negatif) yang dihasilkan oleh konsorsium atau grup bisnis afiliasi milik segelintir triliuner.
2. **Kalkulasi/Formula Pengolahan:**
    * `Total_Kekayaan_Ekstraktif = SUM(Harta_Triliuner) WHERE Sektor = 'Ekstraktif'`
    * `Beban_Ekologis_Grup_X = SUM(Rugi_Ekologis) GROUP BY Afiliasi_Pemilik`
3. **Variabel & Fitur Data:**
    * **Kategori Entitas (X):** `Grup_Taipan`, `Afiliasi_Blok_Sulawesi`
    * **Indikator Monopoli/Dampak (Y):** `Luas_Konsesi_Ha`, `Emisi_PLTU_MW`, `Estimasi_Rugi_Ekologis`
4. **Dataset & File:**
    * CELIOS Inequality Report 2026
    * `sulawesi_kawasan_nikel_luas.csv`
    * `sulawesi_pltu_captive.csv`
    * `sulawesi_konflik_agraria_tanahkita.csv`

---

Analisis terhadap distribusi manfaat ekonomi sektor nikel dan PLTU di Sulawesi menunjukkan konsentrasi nilai tambah pada kelompok usaha skala besar. Data dari Laporan Ketimpangan CELIOS mencatat bahwa akumulasi kekayaan 50 individu/kelompok usaha terbesar di Indonesia mencapai **Rp4.651 Triliun**, di mana sekitar **58% bersumber dari sektor berbasis sumber daya alam** (pertambangan nikel, batu bara, kelapa sawit, dan pemurnian logam). Hal ini mengindikasikan perlunya kebijakan redistribusi manfaat dan pengelolaan dampak lingkungan yang lebih seimbang.

### Ringkasan Indikator Kekayaan Taipan

| Indikator | Nilai | Keterangan |
|---|---|---|
| **Proporsi Kekayaan Ekstraktif** | **58,0%** | Persentase total harta 50 triliuner Indonesia yang dicetak murni dari pengerukan sumber daya alam (Nikel, Batu Bara, Sawit). Sumber: CELIOS Inequality Report 2026 |
| **Total Harta 50 Triliuner** | **Rp4.651 Triliun** | Nilai fantastis yang melampaui postur APBN nasional. Kekayaan ini naik nyaris 2x lipat sejak 2019 (Periode booming komoditas). Sumber: CELIOS Inequality Report 2026 |
| **Laju Kekayaan (Harian)** | **Rp13 Miliar** | Kenaikan harta harian elit oligarki, sangat kontras dengan rata-rata kenaikan upah buruh nasional yang hanya tumbuh sekitar Rp2 ribu per hari. Sumber: CELIOS Inequality Report 2026 |

---

### Top 10 Penguasa Tahta Ekstraktif vs Kerugian Publik

Berikut adalah irisan langsung (*Mega-Crosstab*) antara Grup Oligarki dengan data konsesi tambang, kapasitas PLTU, deforestasi, kerugian ekologis, dan jejak konflik di Sulawesi. Tabel ini **diurutkan (Top 10)** berdasarkan skala daya rusak (Kombinasi Luas Konsesi terbesar dan Emisi PLTU raksasa):

| Rank & Grup Taipan / Konsorsium | Total Harta (CELIOS) | Afiliasi Blok (Sulawesi) | Luas Konsesi (Aktual) | Status Deforestasi Lindung | Emisi PLTU Captive | Estimasi Rugi Ekologis | Dampak Sosial & Konflik |
|---|---|---|---|---|---|---|---|
| **#1 PT Vale Indonesia** *(MIND ID & Konsorsium)* | **Rp 259,2 T** *(▲ Aset MIND ID 2023)* | Blok Sorowako, Bahodopi, Pomalaa | **118.017 Ha** | Monopoli & deforestasi kronis Pegunungan Verbeek | 0 MW *(Suplai PLTA Sorowako, emisi metana bendungan)* | > Rp 40,0 Triliun *(Kumulatif kerusakan danau)* | 460+ Jiwa Terdampak *(Perampasan wilayah adat To Karunsi'e)* |
| **#2 Salim Group** *(Anthony Salim)* | **Rp 160,0 T** *(▲ Terkaya #5)* | Citra Palu Minerals, Gorontalo Min. | **110.175 Ha** | Tumpang tindih dengan Taman Hutan Raya (Tahura) | Tambang Emas (Non-Smelter) *(Daya rusak deforestasi)* | > Rp 8,0 Triliun *(Ancaman cemaran air tanah)* | Konflik PETI Poboya *(Penertiban paksa penambang)* |
| **#3 Jiangsu Delong Nickel** *(Tony Zhou Yuan)* | **Rp 45,0 T** *(▲ Investasi VDNI/OSS)* | PT VDNI, OSS (Konawe), GNI (Morut) | **2.253 Ha** | Perusakan DAS Laronai & bentang alam Morosi | **5.175 MW** *(≈ 36,2 Juta Ton CO2/thn)* | > Rp 20,0 Triliun *(Pemicu banjir bandang)* | 2 Pekerja Tewas *(Bentrokan maut GNI 2023)* |
| **#4 Tsingshan Holding** *(Xiang Guangda)* | **Rp 163,0 T** *(▲ Raja Nikel Dunia)* | Bintangdelapan, Eternal (IMIP) | **20.765 Ha** | Deforestasi masif hutan pesisir & reklamasi | **4.030 MW** *(≈ 28,2 Juta Ton CO2/thn)* | > Rp 40,0 Triliun *(Pencemaran udara & laut)* | Puluhan Pekerja Tewas *(Tragedi Peningkatan Signifikan Tungku ITSS)* |
| **#5 Boy Thohir & Edwin S.** *(Adaro / Saratoga)* | **Rp 64,1 T** *(▲ Terkaya #17)* | PT Sulawesi Cahaya Mineral (SCM) | **21.100 Ha** | Sinyal hilangnya hutan primer tinggi (GFW) | Disuplai Listrik PLN *(Data MW Undisclosed)* | > Rp 15,0 Triliun *(Fungsi serapan karbon hilang)* | Konflik Tenurial Laten *(Deforestasi blok Routa)* |
| **#6 J Resources** *(Jimmy Budiarto)* | **Rp 7,5 T** *(▲ Market Cap PSAB)* | J Resources Bolaang Mongondow | **38.150 Ha** | Eksploitasi lanskap Pegunungan Bolmong | Tambang Emas (Non-Smelter) *(Risiko tailing beracun)* | > Rp 5,0 Triliun *(Ancaman tailing emas)* | Potensi Pencemaran *(Masyarakat lingkar tambang)* |
| **#7 Rajawali Group** *(Peter Sondakh)* | **Rp 32,5 T** *(▲ Terkaya #22)* | Tambang Tondano Nusajaya (Archi) | **30.848 Ha** | Berkurangnya resapan air di Minahasa | Tambang Emas (Non-Smelter) *(Kerusakan hidrologi)* | > Rp 4,5 Triliun *(Beban hidrologis)* | Banjir & Longsor *(Aktivitas tambang Sulut)* |
| **#8 Kalla Group** *(Keluarga Jusuf Kalla)* | **Rp 900,8 M** *(▲ LHKPN 2018)* | PT Kalla Arebamma, Bumi Mineral | **20.173 Ha** | Reklamasi pesisir merusak ekosistem mangrove | 0 MW *(Suplai PLTA Poso, emisi metana bendungan)* | > Rp 2,5 Triliun *(Ancaman pesisir Luwu)* | Konflik Lahan Luwu *(Gusur paksa nelayan Bua)* |
| **#9 Harita Group** *(Lim Hariyanto W.S.)* | **Rp 108,0 T** *(▲ Terkaya #9)* | PT Gema Kreasi Perdana (Wawonii) | **~ 1.000 Ha** | Menabrak larangan tambang pulau kecil | Ekspor Bijih Mentah *(PLTU >1.100 MW di P. Obi)* | > Rp 1,5 Triliun *(Hancurnya tangkapan air)* | 37.000 Jiwa Terdampak *(Kriminalisasi warga penolak)* |
| **#10 Zhenshi Holding** *(Zhang Yuqiang)* | **Rp 40,0 T** *(▲ Estimasi Forbes)* | Zhenshi Holding Group Co Ltd | **4.000 Ha** | Mengubah kawasan hijau pesisir menjadi beton | **450 MW** *(≈ 3,1 Juta Ton CO2/thn)* | > Rp 5,0 Triliun *(Limbah slag nikel padat)* | Krisis Ruang Hidup *(Desa lingkar tambang Morowali)* |

**Sumber Dataset Internal:**
- Luas Lahan (Ha): `data/processed/sulawesi_kawasan_nikel_luas.csv` (Di-aggregate berdasarkan nama perusahaan normatif).
- Kapasitas PLTU (MW): `data/processed/sulawesi_pltu_captive.csv` (Di-aggregate berdasarkan 'Parent' & 'Capacity (MW)').
- Konflik (Jiwa): `data/processed/sulawesi_konflik_agraria_tanahkita.csv` (Spesifik: PT Gema Kreasi Perdana berdampak 37.000 jiwa).
- Total Harta & Pertumbuhan: **Laporan 50 Taipan Terkaya CELIOS** (Hasil riset kekayaan taipan ekstraktif).

> **Penjelasan Metodologi: Perhitungan Estimasi Rugi Ekologis**
>
> Kolom **Estimasi Rugi Ekologis** (yang mencapai rentang triliunan Rupiah) dihitung menggunakan pendekatan valuasi ekonomi lingkungan dengan mengadaptasi formula dari **Peraturan Menteri LHK No. 7 Tahun 2014**.
>
> Nilai raksasa tersebut merepresentasikan akumulasi nyata dari dua komponen utama yang selama ini ditanggung (disubsidi) oleh rakyat dan tidak pernah masuk dalam neraca rugi korporasi:
> 1. **Kerugian Ekonomi Publik:** Meliputi anjloknya hasil tangkapan nelayan akibat laut yang tercemar sedimen, matinya tanaman lada/kakao warga karena debu pabrik, hingga membengkaknya biaya pengobatan *(out-of-pocket)* masyarakat akibat wabah ISPA.
> 2. **Biaya Pemulihan Alam:** Mengkuantifikasi harga mutlak yang harus dibayar untuk merehabilitasi fungsi ekologis yang hancur, seperti biaya teknis reboisasi hutan, netralisasi air sungai dari limbah *slag* beracun, serta biaya sosial dari puluhan juta ton emisi karbon PLTU *captive*.
>
> **Matriks & Skala Formula Perhitungan:**
> `Total Kerugian Ekologis = (Luas Konsesi × Valuasi Hutan/Pesisir per Ha) + (Kapasitas PLTU MW × Biaya Sosial Emisi Karbon)`
> - **Variabel Konsesi (Ha):** Semakin besar luasan konsesi (HGU/IUP) yang beroperasi menembus Cagar Alam, Taman Nasional, atau merangsek permukiman warga, maka nilai *multiplier* kerugian ekonomi dan pemulihan per hektarnya akan semakin dikalikan lipat secara eksponensial.
> - **Variabel Emisi PLTU (MW):** Operasional PLTU *captive* berbahan bakar fosil oleh *smelter* dikonversi ke taksiran jejak karbon (Jutaan ton CO2 ekuivalen per tahun). Jejak karbon ini kemudian dikalikan dengan parameter *Social Cost of Carbon (SCC)* atau Nilai Ekonomi Karbon (NEK).

> **Catatan Analisis:** Fakta dataset di atas menelanjangi ilusi pembangunan. Ratusan ribu hektar hutan dan pulau kecil telah dikapling, dan lebih dari **9.000 MW PLTU Batu Bara** dibakar secara tertutup oleh Delong dan Tsingshan.
>
> *\*Terkait Emisi PLN:* Untuk entitas tambang yang menyedot listrik jaringan PLN, besaran daya aktual (MW) dan Emisi Karbon tidak dapat dikuantifikasi karena **data spesifik tersebut dirahasiakan (Undisclosed)** oleh korporasi dalam publikasi publiknya.

---

## 8.2 Sisi Beban: Indikator Kesehatan dan Sengketa Lahan

**Metode: Analisis Dataset ISPA & Tanahkita (CATAHU)**

### Metodologi: Kalkulasi Tren Eksternalitas Negatif

**Metode Analisis:** Sub-bab ini menggunakan agregasi deret waktu deskriptif (*Descriptive Time-Series Aggregation*) untuk mengukur beban penyakit dan sengketa sosial seiring masifnya industrialisasi ekstraktif.

1. **Model Pelacakan Krisis Kesehatan & Agraria:**
    * **Trend Mapping:** Melacak kurva penderita Infeksi Saluran Pernapasan Akut (ISPA) dari rentang tahun 2014 hingga 2024 di Sulawesi Tengah dan Tenggara.
    * **Agregasi Kasus Kritis:** Mengumpulkan metrik kuantitatif insiden sengketa lahan dan nilai estimasi dampak lingkungan hidup.
2. **Kalkulasi/Formula Pengolahan:**
    * `Tren_Kasus_ISPA_Sentra = SUM(Penderita_ISPA) GROUP BY Tahun WHERE Provinsi IN (Sulteng, Sultra)`
    * `Valuasi_Kerusakan_LHK = F(Luas_Deforestasi, Hilang_Fungsi_Air, Cemaran_Laut)`
3. **Variabel & Fitur Data:**
    * **Rentang Waktu (X):** `Tahun` (2014-2024)
    * **Metrik Beban Publik (Y):** `Jumlah_Kasus_ISPA`, `Jumlah_Konflik_Agraria`, `Estimasi_Rupiah_Kerusakan`
4. **Dataset & File:**
    * `data/processed/sulawesi_kesehatan_detail_2014_2024.csv`
    * `Tanahkita.id` / `KPA`

---

Aktivitas ekstraktif skala besar berpotensi menimbulkan **eksternalitas negatif** yang dirasakan oleh komunitas sekitar. Hal ini tercermin pada indikator sengketa tata guna lahan serta fluktuasi prevalensi penyakit saluran pernapasan di sekitar kawasan industri.

Berikut adalah ringkasan indikator dampak lingkungan dan sosial yang memerlukan pemantauan serta mitigasi berkesinambungan:

| Indikator Beban Publik | Nilai | Keterangan |
|---|---|---|
| **Krisis Kesehatan (ISPA)** | **117.775 Kasus** | Akumulasi kasus infeksi saluran pernapasan di sentra nikel Sulteng & Sultra (2014-2024), berkorelasi dengan polusi debu dan sulfur PLTU Captive. Sumber: Data Panel Kesehatan (Dinkes/BPS) |
| **Konflik Agraria & FPIC** | **12 Kasus Kritis** | Terdokumentasi meletus di Sulawesi. Mengorbankan puluhan ribu jiwa, melibatkan perampasan kebun, pelanggaran hak adat, dan penembakan warga. Sumber: Tanahkita.id (KPA / YLBHI) |
| **Estimasi Kerugian Ekologis** | **> Rp 100 Triliun** | Valuasi kumulatif kasar dari hilangnya fungsi hutan primer, rusaknya ekosistem terumbu karang laut, dan lenyapnya sumber air bersih akibat sedimentasi limbah. Sumber: Proksi Kalkulasi Valuasi Lingkungan LHK |

---

## 8.3 Pembuktian Statistik: Hubungan Indikator Ekonomi Makro dan Indikator Dampak

**Metode: Crosstabulation & Pearson Chi-Square Test**

### Metodologi: Uji Korelasi Investasi vs Ledakan Penyakit

**Metode Analisis:** Sub-bab ini menggunakan pengujian statistik inferensial (*Crosstabulation & Chi-Square Test*) untuk menguji apakah arus investasi yang masuk berasosiasi dengan dinamika indikator kesehatan pernapasan dan deforestasi.

1. **Uji Signifikansi Statistik (Chi-Square):**
    * **Binning (Kategorisasi Data):** Data numerik investasi dan jumlah kasus penyakit dikategorikan menjadi 2 level (Tinggi & Rendah) menggunakan ambang batas Median historis. `Nilai > Median = Tinggi`, `Nilai <= Median = Rendah`.
    * `H0 (Null Hypothesis): Tidak ada korelasi yang signifikan secara statistik antara nilai investasi PMDN/PAD dengan jumlah penderita ISPA/Deforestasi di provinsi Sulawesi pada suatu tahun tertentu.`
    * `Decision Rule: Tolak H0 jika nilai Asymptotic Significance (P-Value) pada uji Pearson Chi-Square < 0.05 (Alpha 5%).`
2. **Kalkulasi/Formula Pengolahan:**
    * `Chi-Square (χ²) = Σ [ (O_i - E_i)² / E_i ]`
    * `Odds Ratio = (Peluang Penyakit Tinggi pada Investasi Tinggi) / (Peluang Penyakit Tinggi pada Investasi Rendah)`
3. **Variabel & Fitur Data:**
    * **Variabel Independen/Manfaat (X):** `Realisasi_Investasi_Rp` atau `PAD_Juta_Rupiah`
    * **Variabel Dependen/Beban (Y):** `Kasus_ISPA` atau `Deforestasi_Ha`
4. **Dataset & File:**
    * Integrasi Panel: `sulawesi_investasi_pmdn_2016_2024.csv`, `sulawesi_pad_2016_2024.csv`, `sulawesi_kesehatan_detail_2014_2024.csv`, `sulawesi_gfw_master...csv`

---

Untuk menguji hubungan antara **Manfaat Ekonomi** dan **Indikator Dampak**, dilakukan analisis tabulasi silang (*crosstabulation*). Uji statistik ini bertujuan mengevaluasi sejauh mana peningkatan arus investasi berasosiasi dengan indikator kesehatan dan lingkungan di tingkat daerah.

### Detail Uji Statistik (Chi-Square & Odds Ratio)

**Variabel Independen (X):** {x_opt[x_col_def]}

**Variabel Dependen (Y):** {y_opt[y_col_def]}

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

> **Interpretasi Ekologis:**
>
> {"Terdapat korelasi kuat dan SIGNIFIKAN secara statistik (P < 0.05). Provinsi dengan aliran manfaat ekonomi tertinggi mutlak mencatatkan ledakan penderitaan ekologis terparah. Ini membuktikan bahwa keuntungan finansial terkonsentrasi di atas, sementara beban penyakit & pencemaran disebar (disosialisasikan) langsung ke masyarakat." if is_sig_def else "Meskipun tidak mencapai ambang signifikansi ketat (P ≥ 0.05) akibat agregasi provinsi, kecenderungan data empiris sangat jelas: provinsi yang menjadi lumbung investasi/PAD juga menjadi episentrum krisis. Distribusi kekayaan tidak pernah menetes (trickle down), tapi dampaknya merata dirasakan rakyat."}

---

### Ringkasan Eksekutif Seluruh Skenario Crosstab

Tabel di bawah ini merangkum hasil pengujian statistik (Chi-Square) untuk semua kemungkinan kombinasi antara indikator Manfaat Ekonomi (X) dan Beban Ekologis (Y) pada panel data yang sama.

{exec_table_md}

> **Pembedahan Realitas Ekologis:**
>
> {"**KESIMPULAN METODOLOGIS: Korelasi Indikator Investasi dan Dampak Lingkungan**<br><br>Hasil pengujian statistik menunjukkan korelasi signifikan antara peningkatan arus investasi dan indikator dampak lingkungan di Sulawesi. Wilayah dengan pertumbuhan investasi tinggi mencatatkan tren insidensi penyakit saluran pernapasan dan deforestasi yang lebih tinggi.<br><br>Nilai *Odds Ratio* mengindikasikan bahwa peningkatan aktivitas industri berasosiasi dengan kenaikan risiko eksternalitas lingkungan. Temuan ini menekankan pentingnya pengalokasian anggaran yang lebih memadai untuk perlindungan kesehatan publik, rehabilitasi ekologis, dan penguatan layanan dasar masyarakat di kawasan sekitar industri ekstraktif." if (p_def < 0.05) else "**KESIMPULAN METODOLOGIS: Evaluasi Penyebaran Dampak dan Perlunya Presisi Data**<br><br>Meskipun pengujian pada skala agregat provinsi menunjukkan hasil tidak signifikan secara statistik (P ≥ 0.05), hal ini dipengaruhi oleh *aggregation effect* pada skala data provinsi.<br><br>Analisis tingkat mikro mengindikasikan bahwa dampak lingkungan dan sosial terkonsentrasi di wilayah sekitar kawasan industri. Oleh karena itu, pengumpulan data pada tingkat kabupaten/kecamatan sangat diperlukan untuk memetakan dampak secara lebih presisi dan merumuskan intervensi kebijakan yang tepat sasaran."}
"""

out_path = HERE / "chapter_8.md"
out_path.write_text(md, encoding="utf-8")
print(f"Done! 100% faithful chapter_8.md saved to {out_path}")
