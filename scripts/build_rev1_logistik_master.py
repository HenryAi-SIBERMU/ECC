from __future__ import annotations

import json
from datetime import date
from pathlib import Path
import re

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_STAGE_DIR = BASE_DIR / "data" / "raw" / "rev1_logistik"
WORKING_DIR = RAW_STAGE_DIR / "working"
MASTER_DIR = RAW_STAGE_DIR / "master"
METADATA_DIR = RAW_STAGE_DIR / "metadata"
TODAY = date.today().isoformat()


def ensure_dirs() -> None:
    for path in (MASTER_DIR, METADATA_DIR):
        path.mkdir(parents=True, exist_ok=True)


def normalize_name(value: str) -> str:
    text = "" if pd.isna(value) else str(value).upper()
    text = re.sub(r"[^A-Z0-9]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(WORKING_DIR / name)


def write_csv(df: pd.DataFrame, name: str) -> None:
    df.to_csv(MASTER_DIR / name, index=False, encoding="utf-8-sig")


def build_cluster_dim(
    cluster_summary_df: pd.DataFrame,
    logistics_df: pd.DataFrame,
    validation_df: pd.DataFrame,
) -> pd.DataFrame:
    logistics_working = logistics_df.copy()
    logistics_working["cluster_id"] = logistics_working["logistics_id"].astype(str).str.replace(r"-001$", "", regex=True)
    validation_working = validation_df.copy()
    merged = (
        cluster_summary_df.merge(
            logistics_working[
                [
                    "cluster_id",
                    "logistics_id",
                    "nama_fasilitas_logistik",
                    "jenis_fasilitas",
                    "fungsi_fasilitas",
                    "terkait_KEK",
                    "nama_KEK_atau_kawasan",
                    "tier_bukti",
                ]
            ],
            on="cluster_id",
            how="left",
        )
        .merge(
            validation_working[["cluster_id", "logistics_id", "status_validasi", "tier_final", "kesimpulan"]],
            on=["cluster_id", "logistics_id"],
            how="left",
        )
    )
    merged.insert(0, "cluster_key", [f"CLUSTER-{i+1:03d}" for i in range(len(merged))])
    return merged


def build_company_dim_and_bridge(
    company_roster_df: pd.DataFrame,
    smelter_df: pd.DataFrame,
    pltu_df: pd.DataFrame,
    cluster_dim_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    records: list[dict] = []

    for _, row in company_roster_df.iterrows():
        records.append(
            {
                "cluster_id": row["cluster_id"],
                "company_name": row["nama_perusahaan"],
                "company_role": "iup_holder",
                "source_table": "priority_company_roster",
            }
        )
    for _, row in smelter_df.iterrows():
        records.append(
            {
                "cluster_id": "",
                "company_name": row["nama_perusahaan"],
                "company_role": "smelter_validated",
                "source_table": "smelter_nikel_validation",
            }
        )
    for _, row in pltu_df.iterrows():
        records.append(
            {
                "cluster_id": row["cluster_id"],
                "company_name": row["owner"],
                "company_role": "pltu_owner",
                "source_table": "pltu_cluster_units",
            }
        )
    company_source_df = pd.DataFrame(records)
    company_source_df["company_norm"] = company_source_df["company_name"].apply(normalize_name)
    company_dim = (
        company_source_df[["company_norm", "company_name"]]
        .drop_duplicates(subset=["company_norm"])
        .reset_index(drop=True)
    )
    company_dim.insert(0, "company_key", [f"COMP-{i+1:04d}" for i in range(len(company_dim))])

    bridge = company_source_df.merge(company_dim, on=["company_norm", "company_name"], how="left")
    cluster_key_lookup = cluster_dim_df[["cluster_id", "cluster_key"]].drop_duplicates()
    bridge = bridge.merge(cluster_key_lookup, on="cluster_id", how="left")
    bridge = bridge[
        ["cluster_key", "cluster_id", "company_key", "company_name", "company_role", "source_table"]
    ].drop_duplicates()
    return company_dim, bridge.reset_index(drop=True)


def build_permit_fact(permit_df: pd.DataFrame, cluster_dim_df: pd.DataFrame) -> pd.DataFrame:
    out = permit_df.copy()
    out.insert(0, "permit_key", [f"PERMIT-{i+1:04d}" for i in range(len(out))])
    out = out.merge(cluster_dim_df[["cluster_id", "cluster_key"]], on="cluster_id", how="left")
    return out


def build_power_fact(pltu_df: pd.DataFrame, cluster_dim_df: pd.DataFrame) -> pd.DataFrame:
    out = pltu_df.copy()
    out.insert(0, "power_unit_key", [f"PLTU-{i+1:04d}" for i in range(len(out))])
    out = out.merge(cluster_dim_df[["cluster_id", "cluster_key"]], on="cluster_id", how="left")
    return out


def build_export_fact(export_df: pd.DataFrame, cluster_dim_df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict] = []
    cluster_lookup = cluster_dim_df[["cluster_id", "cluster_key"]].drop_duplicates()
    for _, row in export_df.iterrows():
        cluster_ids = [item for item in str(row["cluster_support"]).split("|") if item and item != "AGREGAT_SULAWESI"]
        if not cluster_ids:
            rows.append(
                {
                    "cluster_id": "",
                    **row.to_dict(),
                }
            )
            continue
        for cluster_id in cluster_ids:
            payload = row.to_dict()
            payload["cluster_id"] = cluster_id
            rows.append(payload)
    out = pd.DataFrame(rows)
    out["export_key"] = [f"EXPORT-{i+1:04d}" for i in range(len(out))]
    out = out.merge(cluster_lookup, on="cluster_id", how="left")
    front_cols = ["export_key", "cluster_key", "cluster_id"]
    other_cols = [col for col in out.columns if col not in front_cols]
    return out[front_cols + other_cols]


def build_evidence_fact(cluster_dim_df: pd.DataFrame) -> pd.DataFrame:
    evidence_df = load_csv("rev1_tahap_b_evidence_matrix.csv")
    osint_round1_df = load_csv("rev1_tahap_b_osint_round1.csv")
    osint_round2_df = load_csv("rev1_tahap_b_osint_round2.csv")

    evidence_rows = evidence_df.rename(
        columns={
            "evidence_type": "evidence_type_detail",
            "evidence_strength": "evidence_level",
            "evidence_summary": "evidence_text",
            "source_path": "source_ref",
        }
    )
    evidence_rows["evidence_family"] = "internal_validation"
    evidence_rows["stage_origin"] = "tahap_b"
    evidence_rows = evidence_rows[
        ["cluster_id", "logistics_id", "evidence_family", "evidence_type_detail", "evidence_level", "source_ref", "evidence_text", "stage_origin"]
    ]

    osint_frames = []
    for frame, label in [(osint_round1_df, "osint_round1"), (osint_round2_df, "osint_round2")]:
        temp = frame.copy()
        temp["logistics_id"] = temp["logistics_id"]
        temp["evidence_family"] = label
        temp["evidence_type_detail"] = temp["external_signal_status"]
        temp["evidence_level"] = "public_osint"
        temp["source_ref"] = temp["source_ref"].fillna("")
        temp["evidence_text"] = temp["external_evidence_summary"]
        temp["stage_origin"] = "tahap_b"
        osint_frames.append(
            temp[
                ["cluster_id", "logistics_id", "evidence_family", "evidence_type_detail", "evidence_level", "source_ref", "evidence_text", "stage_origin"]
            ]
        )

    out = pd.concat([evidence_rows, *osint_frames], ignore_index=True)
    out.insert(0, "evidence_key", [f"EVID-{i+1:04d}" for i in range(len(out))])
    out = out.merge(cluster_dim_df[["cluster_id", "cluster_key"]], on="cluster_id", how="left")
    return out


def build_manifest(outputs: dict[str, int]) -> dict:
    return {
        "stage": "rev1_logistik_master",
        "generated_at": TODAY,
        "master_dir": str(MASTER_DIR.relative_to(BASE_DIR)).replace("\\", "/"),
        "outputs": outputs,
    }


def main() -> None:
    ensure_dirs()

    cluster_summary_df = load_csv("rev1_tahap_b_cluster_bulk_summary.csv")
    logistics_df = load_csv("sulawesi_port_logistics.csv")
    validation_df = load_csv("rev1_tahap_b_validation_summary.csv")
    company_roster_df = load_csv("rev1_tahap_b_priority_company_roster.csv")
    permit_df = load_csv("rev1_tahap_b_priority_permit_extract.csv")
    pltu_df = load_csv("rev1_tahap_b_pltu_cluster_units.csv")
    export_df = load_csv("rev1_tahap_b_export_nickel_detail.csv")
    smelter_df = load_csv("smelter_nikel_validation.csv")

    cluster_dim_df = build_cluster_dim(cluster_summary_df, logistics_df, validation_df)
    company_dim_df, company_cluster_bridge_df = build_company_dim_and_bridge(company_roster_df, smelter_df, pltu_df, cluster_dim_df)
    permit_fact_df = build_permit_fact(permit_df, cluster_dim_df)
    power_fact_df = build_power_fact(pltu_df, cluster_dim_df)
    export_fact_df = build_export_fact(export_df, cluster_dim_df)
    evidence_fact_df = build_evidence_fact(cluster_dim_df)

    write_csv(cluster_dim_df, "rev1_logistik_master_cluster_dim.csv")
    write_csv(company_dim_df, "rev1_logistik_master_company_dim.csv")
    write_csv(company_cluster_bridge_df, "rev1_logistik_master_company_cluster_bridge.csv")
    write_csv(permit_fact_df, "rev1_logistik_master_permit_fact.csv")
    write_csv(power_fact_df, "rev1_logistik_master_power_unit_fact.csv")
    write_csv(export_fact_df, "rev1_logistik_master_export_fact.csv")
    write_csv(evidence_fact_df, "rev1_logistik_master_evidence_fact.csv")

    outputs = {
        "cluster_dim_rows": len(cluster_dim_df),
        "company_dim_rows": len(company_dim_df),
        "company_cluster_bridge_rows": len(company_cluster_bridge_df),
        "permit_fact_rows": len(permit_fact_df),
        "power_unit_fact_rows": len(power_fact_df),
        "export_fact_rows": len(export_fact_df),
        "evidence_fact_rows": len(evidence_fact_df),
    }
    (METADATA_DIR / "rev1_logistik_master_manifest.json").write_text(
        json.dumps(build_manifest(outputs), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("rev1_logistik master build completed.")
    for key, value in outputs.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
