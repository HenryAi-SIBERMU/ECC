from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path
import sys

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from src.utils.rev1_logistik_stage import (  # noqa: E402
    DATASET_SCHEMAS,
    SOURCE_PRIORITIES,
    TIER_BUKTI,
    WILAYAH_PRIORITAS,
    build_stage_a_payload,
    get_dataset_columns,
)


RAW_STAGE_DIR = BASE_DIR / "data" / "raw" / "rev1_logistik"
METADATA_DIR = RAW_STAGE_DIR / "metadata"
TEMPLATES_DIR = RAW_STAGE_DIR / "templates"
WORKING_DIR = RAW_STAGE_DIR / "working"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
TODAY = date.today().isoformat()


STAGE_A_CLUSTERS = [
    {
        "cluster_id": "NODE-SULTENG-MOROWALI-IMIP",
        "node_label": "Simpul logistik pesisir IMIP-Bahodopi",
        "anchor_entity": "Indonesia Morowali Industrial Park (IMIP)",
        "anchor_type": "industrial_park",
        "provinsi": "Sulawesi Tengah",
        "kabupaten": "Morowali",
        "wilayah_prioritas": "Morowali",
        "priority_tier": 1,
        "jenis_fasilitas": "tidak_terklasifikasi",
        "fungsi_fasilitas": "logistik_kawasan_industri",
        "nama_kawasan": "IMIP / Bahodopi industrial cluster",
        "komoditas": "nikel",
        "tier_bukti": "tier_2",
        "terkait_kek": "indikatif",
        "permit_patterns": [r"\bKAB\.\s*MOROWALI\b"],
        "permit_exclude_patterns": [r"\bKAB\.\s*MOROWALI\s+UTARA\b"],
        "pltu_patterns": [r"\bMOROWALI\b", r"\bBAHODOPI\b", r"\bLABOTA\b"],
        "search_terms": "IMIP; Bahodopi; Morowali; jetty; terminal khusus; pelabuhan; dermaga industri",
        "source_1": "data/processed/sulawesi_pltu_captive.csv",
        "source_2": "docs/Page1-Assessment-Gaps.md",
        "source_basis": "data/processed/sulawesi_pltu_captive.csv; docs/Page1-Assessment-Gaps.md",
        "catatan": "Node utama untuk mengejar terminal khusus atau jetty kawasan yang menopang klaster smelter Morowali.",
        "next_validation_focus": "Cari nama terminal khusus, jetty, atau dermaga industri yang eksplisit terhubung ke IMIP/Bahodopi.",
    },
    {
        "cluster_id": "NODE-SULTENG-MORUT-PETASIA-GNI",
        "node_label": "Simpul logistik pesisir Petasia-GNI",
        "anchor_entity": "Gunbuster Nickel Industry (GNI)",
        "anchor_type": "smelter_company",
        "provinsi": "Sulawesi Tengah",
        "kabupaten": "Morowali Utara",
        "wilayah_prioritas": "Morowali Utara",
        "priority_tier": 1,
        "jenis_fasilitas": "tidak_terklasifikasi",
        "fungsi_fasilitas": "pengapalan_produk_smelter",
        "nama_kawasan": "Petasia / GNI cluster",
        "komoditas": "nikel",
        "tier_bukti": "tier_2",
        "terkait_kek": "indikatif",
        "permit_patterns": [r"\bKAB\.\s*MOROWALI\s+UTARA\b"],
        "permit_exclude_patterns": [],
        "pltu_patterns": [r"\bPETASIA\b", r"\bGUNBUSTER\b", r"\bDELONG\s+NICKEL\b"],
        "search_terms": "Gunbuster Nickel Industry; GNI; Petasia; terminal khusus; jetty; pelabuhan; Morowali Utara",
        "source_1": "data/processed/sulawesi_pltu_captive.csv",
        "source_2": "tools/scrapling/update_matching_approved.py",
        "source_basis": "data/processed/sulawesi_pltu_captive.csv; tools/scrapling/update_matching_approved.py",
        "catatan": "Node kuat karena ada sinyal PLTU captive berulang di Petasia dan anchor smelter nikel yang jelas.",
        "next_validation_focus": "Cari fasilitas sandar, jetty, atau terminal khusus yang melayani klaster GNI di Morowali Utara.",
    },
    {
        "cluster_id": "NODE-SULTRA-KONAWE-MOROSI-VDNI",
        "node_label": "Simpul logistik Morosi-VDNI",
        "anchor_entity": "Virtue Dragon Nickel Industry (VDNI)",
        "anchor_type": "smelter_company",
        "provinsi": "Sulawesi Tenggara",
        "kabupaten": "Konawe",
        "wilayah_prioritas": "Konawe",
        "priority_tier": 1,
        "jenis_fasilitas": "tidak_terklasifikasi",
        "fungsi_fasilitas": "logistik_kawasan_industri",
        "nama_kawasan": "Morosi / VDNI cluster",
        "komoditas": "nikel",
        "tier_bukti": "tier_2",
        "terkait_kek": "indikatif",
        "permit_patterns": [r"\bKAB\.\s*KONAWE\b"],
        "permit_exclude_patterns": [r"\bKAB\.\s*KONAWE\s+UTARA\b", r"\bKAB\.\s*KONAWE\s+SELATAN\b"],
        "pltu_patterns": [r"\bVDNI\b", r"\bVIRTUE\s+DRAGON\b", r"\bMOROSI\b"],
        "search_terms": "VDNI; Virtue Dragon; Morosi; Konawe; terminal khusus; jetty; pelabuhan; dermaga",
        "source_1": "tools/scrapling/update_matching_approved.py",
        "source_2": "data/processed/sulawesi_limbah_b3.csv",
        "source_basis": "tools/scrapling/update_matching_approved.py; data/processed/sulawesi_limbah_b3.csv",
        "catatan": "Node utama Sultra karena cluster Morosi muncul konsisten pada data dan catatan repo sebagai episentrum smelter.",
        "next_validation_focus": "Cari nama fasilitas logistik yang melayani VDNI atau kawasan Morosi secara eksplisit.",
    },
    {
        "cluster_id": "NODE-SULTRA-KONAWE-OSS",
        "node_label": "Simpul logistik Konawe-OSS",
        "anchor_entity": "Obsidian Stainless Steel (OSS)",
        "anchor_type": "smelter_company",
        "provinsi": "Sulawesi Tenggara",
        "kabupaten": "Konawe",
        "wilayah_prioritas": "Konawe",
        "priority_tier": 1,
        "jenis_fasilitas": "tidak_terklasifikasi",
        "fungsi_fasilitas": "pengapalan_produk_smelter",
        "nama_kawasan": "OSS / Konawe industrial cluster",
        "komoditas": "nikel",
        "tier_bukti": "tier_2",
        "terkait_kek": "indikatif",
        "permit_patterns": [r"\bKAB\.\s*KONAWE\b"],
        "permit_exclude_patterns": [r"\bKAB\.\s*KONAWE\s+UTARA\b", r"\bKAB\.\s*KONAWE\s+SELATAN\b"],
        "pltu_patterns": [r"\bOBSIDIAN\b", r"\bOSS\b"],
        "search_terms": "Obsidian Stainless Steel; OSS; Konawe; terminal khusus; jetty; pelabuhan; smelter nikel",
        "source_1": "data/processed/sulawesi_pltu_captive.csv",
        "source_2": "tools/scrapling/update_matching_approved.py",
        "source_basis": "data/processed/sulawesi_pltu_captive.csv; tools/scrapling/update_matching_approved.py",
        "catatan": "Node tambahan Konawe untuk memisahkan fasilitas yang mungkin melayani OSS dari cluster VDNI.",
        "next_validation_focus": "Cari bukti apakah OSS memakai fasilitas logistik sendiri atau berbagi simpul dengan klaster Morosi.",
    },
    {
        "cluster_id": "NODE-SULTRA-KOLAKA-POMALAA-ANTAM",
        "node_label": "Simpul logistik Pomalaa-ANTAM",
        "anchor_entity": "ANTAM Pomalaa RKEF",
        "anchor_type": "smelter_company",
        "provinsi": "Sulawesi Tenggara",
        "kabupaten": "Kolaka",
        "wilayah_prioritas": "Kolaka",
        "priority_tier": 2,
        "jenis_fasilitas": "tidak_terklasifikasi",
        "fungsi_fasilitas": "pengapalan_produk_smelter",
        "nama_kawasan": "Pomalaa / ANTAM nickel cluster",
        "komoditas": "nikel",
        "tier_bukti": "tier_2",
        "terkait_kek": "indikatif",
        "permit_patterns": [r"\bKAB\.\s*KOLAKA\b"],
        "permit_exclude_patterns": [r"\bKAB\.\s*KOLAKA\s+UTARA\b", r"\bKAB\.\s*KOLAKA\s+TIMUR\b"],
        "pltu_patterns": [r"\bPOMALAA\b", r"\bANEKA\s+TAMBANG\b", r"\bANTAM\b"],
        "search_terms": "ANTAM Pomalaa; Pomalaa; Kolaka; terminal khusus; jetty; pelabuhan; ferronickel",
        "source_1": "docs/CGS_DATA_ASSESSMENT.md",
        "source_2": "data/processed/sulawesi_pltu_captive.csv",
        "source_basis": "docs/CGS_DATA_ASSESSMENT.md; data/processed/sulawesi_pltu_captive.csv",
        "catatan": "Anchor kuat untuk klaster Kolaka/Pomalaa karena repo sudah menyebut eksplisit smelter ANTAM Pomalaa RKEF.",
        "next_validation_focus": "Cari terminal atau dermaga yang eksplisit melayani Pomalaa/ANTAM untuk arus nikel dan ferronickel.",
    },
    {
        "cluster_id": "NODE-SULSEL-LUTIM-SOROWAKO-VALE",
        "node_label": "Simpul logistik Sorowako-Luwu Timur",
        "anchor_entity": "PT Vale Indonesia / Sorowako",
        "anchor_type": "mining_processing_cluster",
        "provinsi": "Sulawesi Selatan",
        "kabupaten": "Luwu Timur",
        "wilayah_prioritas": "Luwu Timur",
        "priority_tier": 2,
        "jenis_fasilitas": "tidak_terklasifikasi",
        "fungsi_fasilitas": "pasokan_bahan_baku",
        "nama_kawasan": "Sorowako / Vale nickel cluster",
        "komoditas": "nikel",
        "tier_bukti": "tier_3",
        "terkait_kek": "tidak",
        "permit_patterns": [r"\bKAB\.\s*LUWU\s+TIMUR\b"],
        "permit_exclude_patterns": [],
        "pltu_patterns": [r"\bVALE\b", r"\bSOROWAKO\b"],
        "search_terms": "Vale Indonesia; Sorowako; Luwu Timur; pelabuhan; terminal; logistik; nikel",
        "source_1": "docs/page8_aktor_oligarki_mapping.md",
        "source_2": "docs/DATASET_SUMMARY_KONFLIK_TAMBANG_SULAWESI.md",
        "source_basis": "docs/page8_aktor_oligarki_mapping.md; docs/DATASET_SUMMARY_KONFLIK_TAMBANG_SULAWESI.md",
        "catatan": "Tetap masuk shortlist karena Luwu Timur adalah sabuk nikel penting, tetapi bukti fasilitas logistiknya masih lebih lemah daripada Morowali/Konawe/Kolaka.",
        "next_validation_focus": "Cari koridor logistik atau fasilitas pelabuhan yang menghubungkan Sorowako/Luwu Timur ke rantai nikel Sulsel.",
    },
]


def ensure_dirs() -> None:
    for path in (RAW_STAGE_DIR, METADATA_DIR, TEMPLATES_DIR, WORKING_DIR):
        path.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_csv(path: Path, columns: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)


def write_dataframe(path: Path, df: pd.DataFrame) -> None:
    df.to_csv(path, index=False, encoding="utf-8-sig")


def load_esdm() -> pd.DataFrame:
    return pd.read_csv(PROCESSED_DIR / "sulawesi_esdm_nikel.csv")


def load_pltu() -> pd.DataFrame:
    return pd.read_csv(PROCESSED_DIR / "sulawesi_pltu_captive.csv")


def compile_mask(series: pd.Series, patterns: list[str], exclude_patterns: list[str] | None = None) -> pd.Series:
    values = series.fillna("").astype(str).str.upper()
    mask = pd.Series(False, index=series.index)
    for pattern in patterns:
        mask = mask | values.str.contains(pattern, regex=True)
    for pattern in exclude_patterns or []:
        mask = mask & ~values.str.contains(pattern, regex=True)
    return mask


def format_top(values: pd.Series, limit: int = 5) -> str:
    cleaned = [value for value in values.dropna().astype(str).tolist() if value.strip()]
    return " | ".join(cleaned[:limit])


def build_region_signal(esdm_df: pd.DataFrame, pltu_df: pd.DataFrame, cluster: dict) -> dict:
    permit_mask = compile_mask(
        esdm_df["lokasi_izin"],
        cluster["permit_patterns"],
        cluster.get("permit_exclude_patterns", []),
    )
    permit_df = esdm_df.loc[permit_mask].copy()
    permit_df["jumlah_izin_nikel_num"] = pd.to_numeric(permit_df["jumlah_izin_nikel"], errors="coerce").fillna(0).astype(int)

    pltu_mask = pd.Series(False, index=pltu_df.index)
    for column in ["Plant name", "Owner", "Parent", "Local area (taluk, county)", "Subnational unit (province, state)"]:
        pltu_mask = pltu_mask | compile_mask(pltu_df[column], cluster["pltu_patterns"])
    pltu_df_cluster = pltu_df.loc[pltu_mask].copy()
    pltu_df_cluster["capacity_num"] = pd.to_numeric(pltu_df_cluster["Capacity (MW)"], errors="coerce").fillna(0.0)

    return {
        "permit_rows": int(len(permit_df)),
        "permit_nikel_total": int(permit_df["jumlah_izin_nikel_num"].sum()),
        "unique_permit_companies": int(permit_df["nama_perusahaan"].nunique()),
        "top_permit_companies": format_top(permit_df["nama_perusahaan"]),
        "pltu_units": int(len(pltu_df_cluster)),
        "pltu_capacity_mw": float(pltu_df_cluster["capacity_num"].sum()),
        "top_pltu_owners": format_top(pltu_df_cluster["Owner"]),
        "top_pltu_plants": format_top(pltu_df_cluster["Plant name"]),
    }


def build_logistics_shortlist(esdm_df: pd.DataFrame, pltu_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    shortlist_rows: list[dict] = []
    region_rows: list[dict] = []

    for cluster in STAGE_A_CLUSTERS:
        signal = build_region_signal(esdm_df, pltu_df, cluster)
        repo_summary = (
            f"{signal['permit_nikel_total']} izin nikel pada {signal['unique_permit_companies']} entitas; "
            f"{signal['pltu_units']} unit PLTU captive / {signal['pltu_capacity_mw']:.0f} MW sebagai sinyal klaster industri."
        )
        catatan = (
            f"Tahap A hanya mengunci node kandidat, belum mengklaim nama terminal final. "
            f"Sinyal repo: {repo_summary} Validasi berikutnya: {cluster['next_validation_focus']}"
        )

        shortlist_rows.append(
            {
                "logistics_id": f"{cluster['cluster_id']}-001",
                "nama_fasilitas_logistik": cluster["node_label"],
                "nama_asli_sumber": "",
                "jenis_fasilitas": cluster["jenis_fasilitas"],
                "fungsi_fasilitas": cluster["fungsi_fasilitas"],
                "operator_fasilitas": "",
                "perusahaan_terkait": cluster["anchor_entity"],
                "smelter_terkait": cluster["anchor_entity"] if cluster["anchor_type"] != "industrial_park" else "",
                "tambang_terkait": f"Cluster izin nikel {cluster['kabupaten']}",
                "komoditas_terkait": cluster["komoditas"],
                "kabupaten": cluster["kabupaten"],
                "provinsi": cluster["provinsi"],
                "koordinat_lat": "",
                "koordinat_lon": "",
                "status_operasional": "unknown",
                "terkait_KEK": cluster["terkait_kek"],
                "nama_KEK_atau_kawasan": cluster["nama_kawasan"],
                "indikasi_risiko_pasokan": "butuh_verifikasi",
                "tier_bukti": cluster["tier_bukti"],
                "sumber_1": cluster["source_1"],
                "sumber_2": cluster["source_2"],
                "catatan_verifikasi": catatan,
                "tanggal_update": TODAY,
            }
        )

        region_rows.append(
            {
                "cluster_id": cluster["cluster_id"],
                "node_label": cluster["node_label"],
                "anchor_entity": cluster["anchor_entity"],
                "anchor_type": cluster["anchor_type"],
                "wilayah_prioritas": cluster["wilayah_prioritas"],
                "kabupaten": cluster["kabupaten"],
                "provinsi": cluster["provinsi"],
                "priority_tier": cluster["priority_tier"],
                "permit_rows": signal["permit_rows"],
                "permit_nikel_total": signal["permit_nikel_total"],
                "unique_permit_companies": signal["unique_permit_companies"],
                "pltu_units": signal["pltu_units"],
                "pltu_capacity_mw": round(signal["pltu_capacity_mw"], 2),
                "top_permit_companies": signal["top_permit_companies"],
                "top_pltu_owners": signal["top_pltu_owners"],
                "top_pltu_plants": signal["top_pltu_plants"],
                "source_basis": cluster["source_basis"],
                "next_validation_focus": cluster["next_validation_focus"],
            }
        )

    shortlist_df = pd.DataFrame(shortlist_rows)
    region_df = pd.DataFrame(region_rows)
    return shortlist_df, region_df


def build_research_targets(region_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for cluster in STAGE_A_CLUSTERS:
        signal_row = region_df.loc[region_df["cluster_id"] == cluster["cluster_id"]].iloc[0]
        rows.append(
            {
                "target_id": cluster["cluster_id"],
                "anchor_entity": cluster["anchor_entity"],
                "anchor_type": cluster["anchor_type"],
                "wilayah_prioritas": cluster["wilayah_prioritas"],
                "provinsi": cluster["provinsi"],
                "kabupaten": cluster["kabupaten"],
                "priority_tier": cluster["priority_tier"],
                "search_terms": cluster["search_terms"],
                "source_basis": cluster["source_basis"],
                "catatan": (
                    f"{cluster['catatan']} "
                    f"Sinyal repo saat ini: {signal_row['permit_nikel_total']} izin nikel dan "
                    f"{signal_row['pltu_units']} unit PLTU captive."
                ),
            }
        )
    return pd.DataFrame(rows)


def build_source_queue() -> pd.DataFrame:
    rows = []
    source_map = {item["source"]: item for item in SOURCE_PRIORITIES}
    sequence = [
        ("repo_existing", "Kunci anchor perusahaan, wilayah, dan cluster smelter dari data repo yang sudah ada."),
        ("amdal_and_technical_docs", "Cari nama terminal khusus, jetty, dermaga industri, atau pelabuhan yang disebut eksplisit."),
        ("official_geospatial", "Verifikasi posisi pesisir, bentuk fasilitas, dan kedekatan dengan kawasan industri."),
        ("news_and_osint", "Cari lead tambahan untuk nama simpul logistik, ekspansi terminal, atau dugaan suplai ilegal."),
    ]

    for cluster in STAGE_A_CLUSTERS:
        for source_code, extraction_goal in sequence:
            source_item = source_map[source_code]
            rows.append(
                {
                    "cluster_id": cluster["cluster_id"],
                    "node_label": cluster["node_label"],
                    "priority_order": source_item["priority"],
                    "source_code": source_code,
                    "source_label": source_item["label"],
                    "target_output": "Tahap A shortlist logistik",
                    "extraction_goal": extraction_goal,
                }
            )

    return pd.DataFrame(rows)


def build_manifest(shortlist_df: pd.DataFrame, targets_df: pd.DataFrame, region_df: pd.DataFrame, source_queue_df: pd.DataFrame) -> dict:
    return {
        "stage": "rev1_logistik_tahap_a",
        "generated_at": TODAY,
        "metadata_dir": str(METADATA_DIR.relative_to(BASE_DIR)).replace("\\", "/"),
        "templates_dir": str(TEMPLATES_DIR.relative_to(BASE_DIR)).replace("\\", "/"),
        "working_dir": str(WORKING_DIR.relative_to(BASE_DIR)).replace("\\", "/"),
        "summary": {
            "shortlist_nodes": int(len(shortlist_df)),
            "anchor_targets": int(len(targets_df)),
            "region_summaries": int(len(region_df)),
            "source_queue_rows": int(len(source_queue_df)),
        },
        "outputs": {
            "shortlist_logistics": "data/raw/rev1_logistik/working/sulawesi_port_logistics.csv",
            "research_targets": "data/raw/rev1_logistik/working/port_research_targets.csv",
            "region_summary": "data/raw/rev1_logistik/working/rev1_tahap_a_region_summary.csv",
            "source_queue": "data/raw/rev1_logistik/working/rev1_tahap_a_source_queue.csv",
        },
    }


def reset_non_stage_a_working_files() -> None:
    write_csv(WORKING_DIR / "sulawesi_rail_psn_tracking.csv", get_dataset_columns("sulawesi_rail_psn_tracking"))
    write_csv(WORKING_DIR / "smelter_nikel_validation.csv", get_dataset_columns("smelter_nikel_validation"))


def main() -> None:
    ensure_dirs()

    payload = build_stage_a_payload()
    write_json(METADATA_DIR / "rev1_logistik_stage_a_schema.json", payload)
    write_json(METADATA_DIR / "rev1_logistik_stage_a_tier_bukti.json", TIER_BUKTI)
    write_json(METADATA_DIR / "rev1_logistik_stage_a_source_priorities.json", SOURCE_PRIORITIES)
    write_json(METADATA_DIR / "rev1_logistik_stage_a_priority_regions.json", WILAYAH_PRIORITAS)

    for dataset_key, dataset_schema in DATASET_SCHEMAS.items():
        filename = dataset_schema["filename"]
        write_csv(TEMPLATES_DIR / filename, get_dataset_columns(dataset_key))

    esdm_df = load_esdm()
    pltu_df = load_pltu()
    shortlist_df, region_df = build_logistics_shortlist(esdm_df, pltu_df)
    targets_df = build_research_targets(region_df)
    source_queue_df = build_source_queue()

    write_dataframe(WORKING_DIR / "sulawesi_port_logistics.csv", shortlist_df)
    write_dataframe(WORKING_DIR / "port_research_targets.csv", targets_df)
    write_dataframe(WORKING_DIR / "rev1_tahap_a_region_summary.csv", region_df)
    write_dataframe(WORKING_DIR / "rev1_tahap_a_source_queue.csv", source_queue_df)
    write_dataframe(WORKING_DIR / "nikel_priority_region_extract.csv", region_df)

    reset_non_stage_a_working_files()

    manifest = build_manifest(shortlist_df, targets_df, region_df, source_queue_df)
    write_json(METADATA_DIR / "rev1_logistik_stage_a_manifest.json", manifest)

    print("rev1_logistik Tahap A completed.")
    print(f"Shortlist nodes: {len(shortlist_df)}")
    print(f"Anchor targets: {len(targets_df)}")
    print(f"Region summaries: {len(region_df)}")
    print(f"Source queue rows: {len(source_queue_df)}")


if __name__ == "__main__":
    main()
