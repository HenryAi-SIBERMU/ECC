from pathlib import Path

import pandas as pd

P = Path("data/processed")
files = {
    "CP1_tk": "sulawesi_tk_sektor_sdgs.csv",
    "CP1_pdrb_kapita": "sulawesi_pdrb_per_kapita_sdgs.csv",
    "CP1_upah_hunian": "sulawesi_upah_hunian_sdgs.csv",
    "CP1_miskin": "sulawesi_kemiskinan_kab_sdgs.csv",
    "CP2_pdrb_sektoral": "sulawesi_pdrb_sektoral_2016_2024.csv",
    "CP3_populasi": "sulawesi_populasi_kab_simdasi.csv",
    "CP4_demografi": "sulawesi_demografi_master_fase4.csv",
    "CP4_shift": "sulawesi_employment_shift_fase4.csv",
    "CP4_shift_idx": "sulawesi_pdrb_shift_index_2016_2024.csv",
}

print("=== FILE EXISTENCE & BASIC SHAPE ===")
all_ok = True
for k, f in files.items():
    path = P / f
    if not path.exists():
        print(f"[FAIL] {k}: missing {f}")
        all_ok = False
        continue
    df = pd.read_csv(path)
    print(f"[OK] {k}: {f} rows={len(df)} cols={len(df.columns)}")

print("\n=== CP1 AUDIT ===")
for f in [
    "sulawesi_tk_sektor_sdgs.csv",
    "sulawesi_pdrb_per_kapita_sdgs.csv",
    "sulawesi_upah_hunian_sdgs.csv",
]:
    df = pd.read_csv(P / f)
    years = sorted(df["tahun"].dropna().unique())
    dups = df.duplicated(["wilayah", "tahun", "var_id"]).sum()
    print(
        f"{f}: prov={df['wilayah'].nunique()} years={years[:3]}..{years[-3:]} null_nilai={df['nilai'].isnull().sum()} dups={dups}"
    )
mis = pd.read_csv(P / "sulawesi_kemiskinan_kab_sdgs.csv")
print(
    f"kemiskinan: rows={len(mis)} wilayah={mis['wilayah'].nunique()} null={mis['nilai'].isnull().sum()} dups_val_tahun={mis.duplicated(['wilayah_val', 'tahun']).sum()}"
)

print("\n=== CP2 AUDIT ===")
pdrb = pd.read_csv(P / "sulawesi_pdrb_sektoral_2016_2024.csv")
valid = {
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M,N",
    "O",
    "P",
    "Q",
    "R,S,T,U",
}
print(
    "rows",
    len(pdrb),
    "prov",
    pdrb["provinsi"].nunique(),
    "years",
    pdrb["tahun"].min(),
    pdrb["tahun"].max(),
    "sector_valid_all",
    pdrb["sektor_kode"].isin(valid).all(),
    "null_val",
    pdrb["nilai_miliar_rp"].isnull().sum(),
    "dups",
    pdrb.duplicated(["provinsi", "tahun", "sektor_kode"]).sum(),
)
print(
    "pct_sum_bad_count",
    (pdrb.groupby(["provinsi", "tahun"])["pct_dari_total"].sum().round(0) != 100).sum(),
)
print(
    "max_value",
    pdrb["nilai_miliar_rp"].max(),
    "sulteng2014total",
    round(
        pdrb[(pdrb["provinsi"] == "Sulawesi Tengah") & (pdrb["tahun"] == 2014)][
            "nilai_miliar_rp"
        ].sum(),
        1,
    ),
)

print("\n=== CP3 AUDIT ===")
pop = pd.read_csv(P / "sulawesi_populasi_kab_simdasi.csv")
win = pop[(pop["tahun"] >= 2014) & (pop["tahun"] <= 2024)]
print(
    "all rows",
    len(pop),
    "window rows",
    len(win),
    "prov",
    win["provinsi"].nunique(),
    "kab",
    win["kabupaten"].nunique(),
    "dups",
    win.duplicated(["provinsi", "kabupaten", "tahun"]).sum(),
)
print(
    "bad_pop",
    len(win[(win["jumlah_penduduk_rb"] < 5) | (win["jumlah_penduduk_rb"] > 2000)]),
    "bad_yoy_abs_gt50",
    len(win[win["laju_pertumbuhan_yoy_pct"].abs() > 50]),
    "key_null",
    win[
        [
            "provinsi",
            "kabupaten",
            "tahun",
            "jumlah_penduduk_rb",
            "kepadatan_per_km2",
            "is_smelter",
        ]
    ]
    .isnull()
    .sum()
    .sum(),
)
print("smelter_kabs", sorted(win[win["is_smelter"] == True]["kabupaten"].unique()))

print("\n=== CP4 AUDIT ===")
demo = pd.read_csv(P / "sulawesi_demografi_master_fase4.csv")
shift = pd.read_csv(P / "sulawesi_employment_shift_fase4.csv")
print(
    "demo rows",
    len(demo),
    "prov",
    demo["provinsi"].nunique(),
    "kab",
    demo["kabupaten"].nunique(),
    "years",
    demo["tahun"].min(),
    demo["tahun"].max(),
    "dups",
    demo.duplicated(["provinsi", "kabupaten", "tahun"]).sum(),
    "key_null",
    demo[["provinsi", "kabupaten", "tahun", "jumlah_penduduk_rb", "is_smelter"]]
    .isnull()
    .sum()
    .sum(),
)
print(
    "demo pct_miskin_null",
    demo["pct_miskin"].isnull().sum(),
    "dbd_null",
    demo["dbd_kasus"].isnull().sum(),
    "pmdn_null",
    demo["pmdn_nilai_juta_rp"].isnull().sum(),
)
print(
    "shift rows",
    len(shift),
    "prov",
    shift["provinsi"].nunique(),
    "years",
    shift["tahun"].min(),
    shift["tahun"].max(),
    "dups",
    shift.duplicated(["provinsi", "tahun"]).sum(),
    "key_null",
    shift[["provinsi", "tahun", "pct_pdrb_pertanian_A", "pct_industri_tambang_BC"]]
    .isnull()
    .sum()
    .sum(),
)
print("Sulteng shift 2014->2024:")
print(
    shift[
        (shift["provinsi"] == "Sulawesi Tengah") & (shift["tahun"].isin([2014, 2024]))
    ][
        [
            "tahun",
            "pct_pdrb_pertanian_A",
            "pct_industri_tambang_BC",
            "agriculture_to_industry_shift_index",
        ]
    ].to_string(index=False)
)

ready = all_ok
ready = ready and len(demo) == 623
ready = ready and demo.duplicated(["provinsi", "kabupaten", "tahun"]).sum() == 0
ready = ready and shift.duplicated(["provinsi", "tahun"]).sum() == 0
ready = ready and pdrb["sektor_kode"].isin(valid).all()
ready = (
    ready
    and len(win[(win["jumlah_penduduk_rb"] < 5) | (win["jumlah_penduduk_rb"] > 2000)])
    == 0
)
ready = ready and len(win[win["laju_pertumbuhan_yoy_pct"].abs() > 50]) == 0
print("\nVERDICT:", "READY_FOR_CP5" if ready else "NOT_READY")
