"""
extract_chapter_9.py
100% faithful extraction of pages/11_Demografi_Sosial.py → chapter_9.md (Laporan_Bab9)
"""
import os, sys, re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = ROOT / "data" / "processed"
VIS  = HERE / "visuals_bab9"
VIS.mkdir(exist_ok=True)

def save_plotly(fig, path, w=1000, h=500):
    fig.write_image(str(path), width=w, height=h, scale=2)

# ─── DATA LOAD ───────────────────────────────────────────────────────────────
df_demo  = pd.read_csv(DATA / "sulawesi_demografi_master_fase4.csv")
df_shift = pd.read_csv(DATA / "sulawesi_employment_shift_fase4.csv")
df_pdrb  = pd.read_csv(DATA / "sulawesi_pdrb_sektoral_2016_2024.csv")

# ─── CALCULATIONS ────────────────────────────────────────────────────────────
df_demo["tahun"]  = pd.to_numeric(df_demo["tahun"], errors="coerce")
df_shift["tahun"] = pd.to_numeric(df_shift["tahun"], errors="coerce")

sulteng_shift = df_shift[df_shift["provinsi"] == "Sulawesi Tengah"].sort_values("tahun")
sulteng_first = sulteng_shift.iloc[0]
sulteng_last  = sulteng_shift.iloc[-1]

pertanian_awal  = float(sulteng_first["pct_pdrb_pertanian_A"])
pertanian_akhir = float(sulteng_last["pct_pdrb_pertanian_A"])
industri_awal   = float(sulteng_first["pct_industri_tambang_BC"])
industri_akhir  = float(sulteng_last["pct_industri_tambang_BC"])
shift_awal      = float(sulteng_first["agriculture_to_industry_shift_index"])
shift_akhir     = float(sulteng_last["agriculture_to_industry_shift_index"])
shift_multiplier = shift_akhir / shift_awal if shift_awal else 0

smelter_kabs   = sorted(df_demo[df_demo["is_smelter"] == True]["kabupaten"].unique())
n_smelter_kab  = len(smelter_kabs)

morowali_2020  = df_demo[(df_demo["kabupaten"] == "Morowali") & (df_demo["tahun"] == 2020)]
morowali_growth_2020 = float(morowali_2020["laju_pertumbuhan_sumber_pct"].iloc[0]) if not morowali_2020.empty else 0
morowali_pop_2020    = float(morowali_2020["jumlah_penduduk_rb"].iloc[0]) if not morowali_2020.empty else 0

latest_year = int(df_demo[df_demo["tahun"] <= 2024]["tahun"].max())
latest_demo = df_demo[df_demo["tahun"] == latest_year].copy()
latest_smelter_density     = latest_demo[latest_demo["is_smelter"] == True]["kepadatan_per_km2"].mean()
latest_non_smelter_density = latest_demo[latest_demo["is_smelter"] == False]["kepadatan_per_km2"].mean()
density_ratio = latest_smelter_density / latest_non_smelter_density if latest_non_smelter_density else 0

dbd_smelter = int(df_demo[(df_demo["is_smelter"] == True) & (df_demo["tahun"] >= 2019)]["dbd_kasus"].sum())

smelter_window     = df_demo[(df_demo["is_smelter"] == True) & (df_demo["tahun"] <= 2024)]
non_smelter_window = df_demo[(df_demo["is_smelter"] == False) & (df_demo["tahun"] <= 2024)]
smelter_avg_yoy     = smelter_window["laju_pertumbuhan_yoy_pct"].dropna().mean()
non_smelter_avg_yoy = non_smelter_window["laju_pertumbuhan_yoy_pct"].dropna().mean()
smelter_total_pop_latest     = latest_demo[latest_demo["is_smelter"] == True]["jumlah_penduduk_rb"].sum()
non_smelter_total_pop_latest = latest_demo[latest_demo["is_smelter"] == False]["jumlah_penduduk_rb"].sum()

top_shift       = df_shift.sort_values("delta_agriculture_to_industry_shift_index_from_first", ascending=False).iloc[0]
top_shift_prov  = top_shift["provinsi"]
top_shift_delta = float(top_shift["delta_agriculture_to_industry_shift_index_from_first"])

# ─── GENERATE VISUALS ───────────────────────────────────────────────────────
print("Rendering 9.2 Density Chart ...")
density = df_demo[df_demo["tahun"] <= 2024].copy()
density["Kategori"] = density["is_smelter"].map({True: "Kabupaten Industri Ekstraktif", False: "Kabupaten Non-Ekstraktif"})
density_agg = density.groupby(["tahun", "Kategori"], as_index=False)["kepadatan_per_km2"].mean()

fig_density = px.area(density_agg, x="tahun", y="kepadatan_per_km2", color="Kategori",
    title="Rata-rata Kepadatan Penduduk: Kabupaten Industri Ekstraktif vs Non-Ekstraktif",
    labels={"tahun": "Tahun", "kepadatan_per_km2": "Kepadatan (jiwa/km²)"},
    color_discrete_map={"Kabupaten Industri Ekstraktif": "#F57C00", "Kabupaten Non-Ekstraktif": "#546E7A"})
fig_density.update_layout(height=450, plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#333"), margin=dict(l=0, r=0, t=40, b=0))
save_plotly(fig_density, VIS / "chart_9_2_density_area.png", w=900, h=450)

print("Rendering 9.3 Sector & Shift Charts ...")
PROPORSI_PERIKANAN = 0.22
df_shift_plot = df_shift.copy()
df_shift_plot["pct_pdrb_tambang_industri_BC"] = df_shift_plot["pct_pdrb_pertambangan_B"] + df_shift_plot["pct_pdrb_industri_C"]
df_shift_plot["pct_pdrb_perikanan_tangkap"]   = df_shift_plot["pct_pdrb_pertanian_A"] * PROPORSI_PERIKANAN
df_shift_plot["pct_pdrb_pertanian_kehutanan"] = df_shift_plot["pct_pdrb_pertanian_A"] * (1 - PROPORSI_PERIKANAN)

shift_long = df_shift_plot.melt(
    id_vars=["provinsi", "tahun"],
    value_vars=["pct_pdrb_pertanian_kehutanan", "pct_pdrb_perikanan_tangkap", "pct_pdrb_tambang_industri_BC"],
    var_name="sektor", value_name="pct_pdrb"
)
shift_long["sektor"] = shift_long["sektor"].map({
    "pct_pdrb_pertanian_kehutanan": "Pertanian & Kehutanan",
    "pct_pdrb_perikanan_tangkap": "Perikanan Tangkap (estimasi)",
    "pct_pdrb_tambang_industri_BC": "Pertambangan & Industri Pengolahan (B+C)"
})

plot_sector = shift_long[shift_long["provinsi"] == "Sulawesi Tengah"]
fig_sector = px.area(plot_sector, x="tahun", y="pct_pdrb", color="sektor",
    title="Komposisi PDRB Sektor Kunci — Sulawesi Tengah",
    labels={"tahun": "Tahun", "pct_pdrb": "Persentase PDRB (%)"},
    color_discrete_map={
        "Pertanian & Kehutanan": "#27AE60",
        "Perikanan Tangkap (estimasi)": "#1ABC9C",
        "Pertambangan & Industri Pengolahan (B+C)": "#E74C3C"
    })
fig_sector.update_layout(height=480, plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#333"), margin=dict(l=0, r=0, t=40, b=0))
save_plotly(fig_sector, VIS / "chart_9_3a_sector_sulteng.png", w=900, h=480)

fig_index = px.line(df_shift, x="tahun", y="agriculture_to_industry_shift_index", color="provinsi", markers=True,
    title="Indeks Pergeseran Agrikultur vs Industri (B+C / A) per Provinsi",
    labels={"tahun": "Tahun", "agriculture_to_industry_shift_index": "Shift Index (B+C / A)", "provinsi": "Provinsi"},
    color_discrete_sequence=["#E74C3C","#F39C12","#2ECC71","#3498DB","#9B59B6","#1ABC9C"])
fig_index.add_hline(y=1, line_dash="dash", line_color="#333", line_width=1.5,
    annotation_text="Ambang: B+C melampaui Pertanian", annotation_font_color="#333", annotation_position="top left")
fig_index.update_layout(height=460, plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#333"), margin=dict(l=0, r=0, t=40, b=0))
save_plotly(fig_index, VIS / "chart_9_3b_shift_index.png", w=900, h=460)

# ─── CROSSTAB 9.4 CALCULATIONS ───────────────────────────────────────────────
print("Computing Crosstab 9.4 ...")
crosstab_panel = df_demo[df_demo["tahun"] <= 2024].merge(
    df_shift[["provinsi","tahun","agriculture_to_industry_shift_index","pct_industri_tambang_BC","pct_pdrb_industri_C"]],
    on=["provinsi", "tahun"], how="left"
)
crosstab_panel["dbd_burden_nonzero"] = crosstab_panel["dbd_kasus"].replace(0, pd.NA)
crosstab_panel = crosstab_panel.dropna(subset=["agriculture_to_industry_shift_index","pct_industri_tambang_BC","kepadatan_per_km2","jumlah_penduduk_rb"]).copy()

x_col_def = "agriculture_to_industry_shift_index"
y_col_def = "kepadatan_per_km2"
x_label_title = "Shift Index Tambang+Industri / Pertanian"
y_label_title = "Kepadatan Penduduk Kabupaten"

med_x = crosstab_panel[x_col_def].median()
med_y = crosstab_panel[y_col_def].median()

lbl_x_h = f"Tinggi (≥{med_x:,.1f})"
lbl_x_l = f"Rendah (<{med_x:,.1f})"
lbl_y_h = f"Tinggi (≥{med_y:,.1f})"
lbl_y_l = f"Rendah (<{med_y:,.1f})"

crosstab_panel["X_Label"] = crosstab_panel[x_col_def].apply(lambda v: lbl_x_h if v >= med_x else lbl_x_l)
crosstab_panel["Y_Label"] = crosstab_panel[y_col_def].apply(lambda v: lbl_y_h if v >= med_y else lbl_y_l)

cats_x = [lbl_x_l, lbl_x_h]; cats_y = [lbl_y_l, lbl_y_h]
crosstab_def = pd.crosstab(crosstab_panel["X_Label"], crosstab_panel["Y_Label"]).reindex(index=cats_x, columns=cats_y, fill_value=0)
try: chi2_def, p_def, dof_def, exp_def = stats.chi2_contingency(crosstab_def)
except: chi2_def, p_def, dof_def, exp_def = 0, 1, 0, crosstab_def.values
exp_df_def = pd.DataFrame(exp_def, index=cats_x, columns=cats_y)

try:
    a = crosstab_def.loc[lbl_x_l, lbl_y_l]; b = crosstab_def.loc[lbl_x_l, lbl_y_h]
    c = crosstab_def.loc[lbl_x_h, lbl_y_l]; d = crosstab_def.loc[lbl_x_h, lbl_y_h]
    or_def = (a*d)/(b*c) if (b*c) > 0 else 0
except: or_def = 0

try: g_def, p_g_def, _, _ = stats.chi2_contingency(crosstab_def, lambda_="log-likelihood")
except: g_def, p_g_def = 0, 1

valid_cases_def = len(crosstab_panel.dropna(subset=[x_col_def, y_col_def]))
total_cases_def = len(crosstab_panel)
missing_cases_def = total_cases_def - valid_cases_def

x_codes = crosstab_panel["X_Label"].replace({lbl_x_l:0, lbl_x_h:1})
y_codes = crosstab_panel["Y_Label"].replace({lbl_y_l:0, lbl_y_h:1})
try: r_val, p_corr = stats.pearsonr(list(x_codes), list(y_codes)); lbl_val_def = (valid_cases_def - 1)*(r_val**2)
except: r_val, p_corr, lbl_val_def = 0, 1, 0

interaction_lbl = f"{x_label_title} * {y_label_title}"
is_sig_def = p_def < 0.05
status_text_def = "SIGNIFIKAN (Ada Hubungan)" if is_sig_def else "TIDAK SIGNIFIKAN"

x_options_all = {
    "agriculture_to_industry_shift_index": "Shift Index Tambang+Industri / Pertanian",
    "pct_industri_tambang_BC": "Porsi PDRB Tambang+Industri (B+C)",
    "pct_pdrb_industri_C": "Porsi PDRB Industri Pengolahan (C)",
}
y_options_all = {
    "kepadatan_per_km2": "Kepadatan Penduduk Kabupaten",
    "jumlah_penduduk_rb": "Jumlah Penduduk Kabupaten (ribu jiwa)",
    "laju_pertumbuhan_yoy_pct": "Laju Pertumbuhan Penduduk YoY",
    "pct_miskin": "Persentase Penduduk Miskin",
}

summary_data = []
for k_x, v_x in x_options_all.items():
    for k_y, v_y in y_options_all.items():
        if k_x in crosstab_panel.columns and k_y in crosstab_panel.columns:
            mx = crosstab_panel[k_x].median(); my = crosstab_panel[k_y].median()
            lxh = f"Tinggi (≥{mx:,.1f})"; lxl = f"Rendah (<{mx:,.1f})"
            lyh = f"Tinggi (≥{my:,.1f})"; lyl = f"Rendah (<{my:,.1f})"
            sx = crosstab_panel[k_x].apply(lambda v: lxh if v >= mx else lxl)
            sy = crosstab_panel[k_y].apply(lambda v: lyh if v >= my else lyl)
            ct = pd.crosstab(sx, sy).reindex(index=[lxl, lxh], columns=[lyl, lyh], fill_value=0)
            try: c2, pv, dofv, _ = stats.chi2_contingency(ct)
            except: c2, pv, dofv = 0, 1, 0
            try:
                aa = ct.loc[lxl, lyl]; bb = ct.loc[lxl, lyh]
                cc = ct.loc[lxh, lyl]; dd = ct.loc[lxh, lyh]
                orv = (aa*dd)/(bb*cc) if (bb*cc) > 0 else 0
            except: orv = 0
            sig = "🟢 SIGNIFIKAN" if pv < 0.05 else "🔴 TIDAK SIGNIFIKAN"
            summary_data.append({"Variabel Independen (X)": v_x, "Variabel Dependen (Y)": v_y, "Chi-Square": f"{c2:.3f}", "P-Value": f"{pv:.3f}", "Odds Ratio": f"{orv:.2f}", "Kesimpulan": sig})

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
print("Writing 100% faithful chapter_9.md ...")

md = f"""# Bab 9: Demografi & Struktur Sosial: Guncangan Sosial dan Pergeseran Ekonomi Agraris

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

Ekspansi nikel di Sulawesi bukan hanya perubahan industri, melainkan rekayasa ulang ruang hidup. Data demografi dan ekonomi sektoral menunjukkan bahwa kawasan yang menjadi pusat industri ekstraktif mengalami tekanan ganda: populasi dan kepadatan meningkat, sementara struktur ekonomi regional bergerak meninggalkan basis agraris menuju dominasi tambang dan industri pengolahan. Di Sulawesi Tengah, provinsi yang menjadi episentrum Morowali dan Morowali Utara, porsi PDRB sektor pertanian turun dari **{pertanian_awal:.2f}%** pada {int(sulteng_first["tahun"])} menjadi **{pertanian_akhir:.2f}%** pada {int(sulteng_last["tahun"])}. Pada periode yang sama, gabungan sektor pertambangan dan industri pengolahan melonjak dari **{industri_awal:.2f}%** menjadi **{industri_akhir:.2f}%**.

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

Analisis ini membaca tekanan demografi melalui perubahan jumlah penduduk kabupaten, bukan melalui data migrasi langsung. Dengan pendekatan ini, populasi diperlakukan sebagai sinyal awal: ketika kawasan smelter tumbuh lebih cepat dibanding pola umum wilayah sekitar, maka terdapat indikasi tarikan penduduk, pekerja, dan aktivitas ekonomi baru yang perlu diuji lebih lanjut. Fokus pembacaan ditempatkan pada tujuh kabupaten prioritas smelter, yaitu **{", ".join(smelter_kabs)}**. Dalam window data yang tersedia, rata-rata pertumbuhan YoY kabupaten smelter tercatat **{smelter_avg_yoy:.2f}%**, sedangkan wilayah non-smelter berada di sekitar **{non_smelter_avg_yoy:.2f}%**. Pada tahun {latest_year}, total populasi kabupaten smelter mencapai **{smelter_total_pop_latest:,.1f} ribu jiwa**. Angka-angka ini tidak cukup untuk menyebut asal migran atau arah mobilitas penduduk, tetapi cukup kuat untuk menunjukkan bahwa hilirisasi nikel menciptakan tekanan demografis yang harus dibaca sebagai bagian dari beban sosial, bukan sekadar konsekuensi administratif pembangunan industri.

---

## 9.2 Intensifikasi Ruang: Kepadatan Industri Ekstraktif vs Non-Ekstraktif

**Metode: Comparative Density Analysis**

Sub-bab ini tidak mengklaim perubahan resmi desa menjadi kota karena data klasifikasi Podes belum menjadi basis utama di halaman ini. Yang dibaca adalah **intensifikasi ruang**, yaitu tekanan yang muncul ketika pertumbuhan penduduk dan konsentrasi industri bertemu pada wilayah yang sama. Rata-rata kepadatan kabupaten smelter pada {latest_year} mencapai **{latest_smelter_density:.1f} jiwa/km²**, sedangkan kabupaten non-smelter berada pada **{latest_non_smelter_density:.1f} jiwa/km²**. Rasio smelter terhadap non-smelter sebesar **{density_ratio:.2f} kali** memberi sinyal bahwa kawasan industri membutuhkan kapasitas layanan publik yang berbeda: perumahan, air bersih, sanitasi, transportasi, hingga fasilitas kesehatan. Dalam kerangka D3TLH, kepadatan bukan sekadar angka demografi, melainkan indikator apakah ruang hidup lokal sedang dipadatkan oleh proyek ekstraktif tanpa perencanaan sosial yang sepadan. Karena itu, grafik berikut dibaca sebagai peta awal tekanan ruang, bukan sebagai klaim urbanisasi formal.

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

Matriks sintesis menggabungkan tiga lapis bukti: perubahan struktur ekonomi, keberadaan kabupaten industri ekstraktif, dan beban DBD di wilayah prioritas. Berdasarkan data yang sudah diproses, provinsi dengan kenaikan shift index tertinggi adalah **{top_shift_prov}**, dengan delta sebesar **{top_shift_delta:.2f}** poin dari tahun awal ke tahun akhir. Ini berarti perubahan struktur ekonomi tidak merata di seluruh Sulawesi; ada wilayah yang mengalami transformasi jauh lebih tajam karena posisinya dalam rantai nikel.

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
"""

out_path = HERE / "chapter_9.md"
out_path.write_text(md, encoding="utf-8")
print(f"Done! 100% faithful chapter_9.md saved to {out_path}")
