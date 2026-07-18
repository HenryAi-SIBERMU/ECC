"""
CP3 — Fetch Populasi Kabupaten via BPS SIMDASI
===============================================
Jalankan: .venv/Scripts/python.exe scripts/fetch_simdasi_populasi_kab.py

Sumber: SIMDASI id=25
Tabel target: "Jumlah Penduduk, Laju Pertumbuhan, Kepadatan Menurut Kabupaten/Kota"
Output: data/processed/sulawesi_populasi_kab_simdasi.csv
"""

import re
import time
from pathlib import Path

import pandas as pd
import requests

API_KEY = "06fd644648629502353deaed29fc6383"
BASE_URL = "https://webapi.bps.go.id/v1/api"

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw" / "bps_simdasi"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
RAW_DIR.mkdir(parents=True, exist_ok=True)

SULAWESI_PROVS = {
    "7100000": "Sulawesi Utara",
    "7200000": "Sulawesi Tengah",
    "7300000": "Sulawesi Selatan",
    "7400000": "Sulawesi Tenggara",
    "7500000": "Gorontalo",
    "7600000": "Sulawesi Barat",
}


def clean(s):
    return re.sub(r"<[^>]*>", "", str(s)).strip()


def parse_num(s):
    if not s or str(s).strip() in ["...", "–", "-", "NA", "", "~0"]:
        return None
    try:
        return float(str(s).replace(".", "").replace(",", "."))
    except:
        return None


def parse_population_rb(s):
    """
    Normalisasi jumlah penduduk ke satuan ribu jiwa.

    SIMDASI tidak konsisten:
    - '120,1'      = 120.1 ribu jiwa
    - '167.024,0'  = 167,024 jiwa = 167.024 ribu jiwa
    Heuristic: jika hasil parse > 2.000, anggap satuan jiwa dan bagi 1000.
    """
    val = parse_num(s)
    if val is None:
        return None
    if val > 2000:
        return round(val / 1000, 3)
    return val


def find_pop_table(mfd):
    """Cari table_id 'Jumlah Penduduk...Menurut Kabupaten/Kota'."""
    for mms_id in [519, 531, 520]:
        url = f"{BASE_URL}/interoperabilitas/datasource/simdasi/id/23/wilayah/{mfd}/mms_id/{mms_id}/key/{API_KEY}/"
        try:
            resp = requests.get(url, timeout=30).json()
            tables = (
                resp.get("data", [{}, {}])[1].get("data", [])
                if len(resp.get("data", [])) > 1
                else []
            )
            for t in tables:
                j = t.get("judul", "").lower()
                if (
                    "penduduk" in j
                    and ("kabupaten" in j or "kota" in j)
                    and ("kepadatan" in j or "pertumbuhan" in j)
                    and "pdrb" not in j
                    and "produk" not in j
                ):
                    return t.get("id_tabel"), t.get("ketersediaan_tahun", [])
        except:
            pass
        time.sleep(1)
    return None, []


def fetch_pop_year(table_id, mfd, provinsi, year):
    url = (
        f"{BASE_URL}/interoperabilitas/datasource/simdasi/id/25"
        f"/id_tabel/{table_id}/wilayah/{mfd}/tahun/{year}/key/{API_KEY}/"
    )
    try:
        resp = requests.get(url, timeout=30).json()
        if resp.get("data-availability") != "available":
            return []
        content = resp["data"][1] if len(resp.get("data", [])) > 1 else {}
        cols = content.get("kolom", {})
        rows = content.get("data", [])
        if not rows or not cols:
            return []

        # Map kolom: cari key untuk penduduk, laju, kepadatan
        col_pop = col_laju = col_kpd = None
        for k, v in cols.items():
            nm = v.get("nama_variabel", "").lower()
            if "jumlah penduduk" in nm:
                col_pop = k
            elif "laju pertumbuhan" in nm:
                col_laju = k
            elif "kepadatan" in nm:
                col_kpd = k

        # Set label agregat yang harus dibuang (exact match)
        skip_labels = {
            "jumlah",
            "total",
            "sulawesi",
            provinsi.lower(),
            "provinsi " + provinsi.lower(),
        }

        results = []
        for r in rows:
            label = clean(r.get("label_raw", r.get("label", "")))
            if not label:
                continue
            # Skip HANYA jika label persis sama dengan nama provinsi atau kata agregat
            if label.lower() in skip_labels:
                continue
            vrs = r.get("variables", {})
            pop = (
                parse_population_rb(vrs.get(col_pop, {}).get("value_raw"))
                if col_pop
                else None
            )
            # Catatan: kolom "laju" dari SIMDASI tidak selalu YoY. Pada beberapa provinsi
            # nilainya adalah laju antarsensus/baseline, jadi hanya disimpan sebagai sumber.
            laju = (
                parse_num(vrs.get(col_laju, {}).get("value_raw")) if col_laju else None
            )
            kpd = parse_num(vrs.get(col_kpd, {}).get("value_raw")) if col_kpd else None
            if pop is None and laju is None:
                continue
            results.append(
                {
                    "provinsi": provinsi,
                    "kabupaten": label,
                    "tahun": year,
                    "jumlah_penduduk_rb": pop,  # ribu jiwa
                    "laju_pertumbuhan_sumber_pct": laju,
                    "kepadatan_per_km2": kpd,
                }
            )
        return results
    except Exception as e:
        print(f"    [!] {year}: {e}")
        return []


# ── Main ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 65)
    print("  CP3 — POPULASI KABUPATEN SULAWESI (SIMDASI)")
    print("=" * 65)

    all_rows = []

    for mfd, provinsi in SULAWESI_PROVS.items():
        print(f"\n[{provinsi}]")
        tid, avail_years = find_pop_table(mfd)
        if not tid:
            print("  [!!] Tabel tidak ditemukan")
            continue
        print(f"  Table ID: {tid[:20]}...")
        print(f"  Tahun tersedia: {avail_years}")

        prov_count = 0
        for yr in avail_years:
            rows = fetch_pop_year(tid, mfd, provinsi, yr)
            if rows:
                all_rows.extend(rows)
                prov_count += len(rows)
                print(f"  [+] {yr}: {len(rows)} kabupaten")
            else:
                print(f"  [-] {yr}: tidak ada data")
            time.sleep(1.2)
        print(f"  Total: {prov_count} baris")

    if not all_rows:
        print("\n[FAIL] Tidak ada data.")
    else:
        df = pd.DataFrame(all_rows)
        df["tahun"] = df["tahun"].astype(int)
        df = df.sort_values(["provinsi", "kabupaten", "tahun"]).reset_index(drop=True)

        # ── Derived YoY Growth ─────────────────────────────────────────
        # Gunakan pertumbuhan YoY hasil hitung dari jumlah_penduduk_rb,
        # bukan kolom laju sumber yang tidak konsisten antar provinsi/tahun.
        # Manual correction: SIMDASI Sulsel 2018 untuk Kota Parepare berisi typo
        # '1.508.154,0' (1,508 juta jiwa), padahal tren 2017=142.1 dan 2019=145.2.
        # Koreksi dengan interpolasi linear agar tidak menciptakan spike palsu.
        parepare_mask = (
            (df["provinsi"] == "Sulawesi Selatan")
            & (df["kabupaten"] == "Kota Parepare")
            & (df["tahun"] == 2018)
            & (df["jumlah_penduduk_rb"] > 1000)
        )
        if parepare_mask.any():
            base = (df["provinsi"] == "Sulawesi Selatan") & (
                df["kabupaten"] == "Kota Parepare"
            )
            v17 = df.loc[base & (df["tahun"] == 2017), "jumlah_penduduk_rb"].iloc[0]
            v19 = df.loc[base & (df["tahun"] == 2019), "jumlah_penduduk_rb"].iloc[0]
            df.loc[parepare_mask, "jumlah_penduduk_rb"] = round((v17 + v19) / 2, 3)

        df = df.sort_values(["provinsi", "kabupaten", "tahun"]).reset_index(drop=True)
        df["laju_pertumbuhan_yoy_pct"] = (
            df.groupby(["provinsi", "kabupaten"])["jumlah_penduduk_rb"].pct_change()
            * 100
        ).round(2)

        # ── Enrich: is_smelter flag ────────────────────────────────────
        # Jangan derive dari semua lokasi IUP nikel karena itu terlalu luas.
        # Flag ini hanya untuk kabupaten prioritas smelter/industri nikel.
        SMELTER_KABS = {
            "Morowali",
            "Morowali Utara",
            "Banggai",
            "Konawe",
            "Konawe Utara",
            "Kolaka",
            "Luwu Timur",
        }
        df["is_smelter"] = df["kabupaten"].isin(SMELTER_KABS)

        # ── Enrich: iup_kumulatif ───────────────────────────────────────
        izin = pd.read_csv(PROCESSED_DIR / "sulawesi_izin_baru_per_tahun.csv")
        izin_cum = (
            izin.sort_values("Tahun")
            .groupby("Provinsi")["Jumlah_Izin_Baru"]
            .cumsum()
            .rename("iup_kumulatif")
        )
        izin_with_cum = izin.join(izin_cum)
        izin_map = izin_with_cum.rename(
            columns={"Provinsi": "provinsi", "Tahun": "tahun"}
        )[["provinsi", "tahun", "iup_kumulatif"]]
        df = df.merge(izin_map, on=["provinsi", "tahun"], how="left")

        # Save
        out = PROCESSED_DIR / "sulawesi_populasi_kab_simdasi.csv"
        df.to_csv(out, index=False)
        print(f"\n[SAVED] {out.name} — {len(df)} baris")

        # ── Summary ────────────────────────────────────────────────────
        print("\n=== COVERAGE PER PROVINSI ===")
        for prov in sorted(df["provinsi"].unique()):
            sub = df[df["provinsi"] == prov]
            yrs = sorted(sub["tahun"].unique())
            kabs = sub["kabupaten"].nunique()
            print(f"  {prov}: {kabs} kab | tahun: {yrs}")

        print("\n=== KABUPATEN SMELTER KUNCI ===")
        smelter_df = df[df["is_smelter"] == True][
            [
                "kabupaten",
                "tahun",
                "jumlah_penduduk_rb",
                "laju_pertumbuhan_sumber_pct",
                "laju_pertumbuhan_yoy_pct",
            ]
        ]
        for kab in [
            "Morowali",
            "Morowali Utara",
            "Banggai",
            "Konawe",
            "Konawe Utara",
            "Kolaka",
            "Luwu Timur",
        ]:
            sub = smelter_df[smelter_df["kabupaten"] == kab]
            if not sub.empty:
                latest = sub.sort_values("tahun").iloc[-1]
                print(
                    f"  {kab}: pop={latest['jumlah_penduduk_rb']} rb | "
                    f"laju_sumber={latest['laju_pertumbuhan_sumber_pct']}% | "
                    f"yoy={latest['laju_pertumbuhan_yoy_pct']}% ({int(latest['tahun'])})"
                )

        # Gate condition
        print("\n=== GATE CONDITION ===")
        g1 = df["provinsi"].nunique() >= 5
        g2 = df["kabupaten"].nunique() >= 50
        g3 = len(df["tahun"].unique()) >= 3
        g4 = df["jumlah_penduduk_rb"].notnull().mean() > 0.8
        for ok, label in [
            (g1, f"≥5 provinsi ({df['provinsi'].nunique()})"),
            (g2, f"≥50 kabupaten unik ({df['kabupaten'].nunique()})"),
            (g3, f"≥3 titik waktu ({sorted(df['tahun'].unique())})"),
            (
                g4,
                f"≥80% non-null penduduk ({df['jumlah_penduduk_rb'].notnull().mean() * 100:.0f}%)",
            ),
        ]:
            print(f"  [{'PASS' if ok else 'FAIL'}] {label}")

        print("\n  CP3 SELESAI." if all([g1, g2, g3, g4]) else "\n  CP3 PARTIAL.")
