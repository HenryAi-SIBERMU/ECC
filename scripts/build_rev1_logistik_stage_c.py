from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_STAGE_DIR = BASE_DIR / "data" / "raw" / "rev1_logistik"
WORKING_DIR = RAW_STAGE_DIR / "working"
MASTER_DIR = RAW_STAGE_DIR / "master"
METADATA_DIR = RAW_STAGE_DIR / "metadata"
TODAY = date.today().isoformat()

CLUSTER_CONTEXT = {
    "NODE-SULTENG-MOROWALI-IMIP": {
        "entitas_kawasan": "IMIP",
        "jenis_relasi": "kawasan_industri_pesisir",
        "status_relasi": "terkonfirmasi",
        "kendaraan_legitimasi": "kawasan_industri_pesisir",
        "status_bukti_kek": "belum_ditemukan_eksplisit",
        "status_bukti_psn_rail": "psn_non_rail_terkonfirmasi",
        "klaim_aman": "Ekspansi nikel Morowali ditopang simpul pesisir industri yang terintegrasi.",
    },
    "NODE-SULTENG-MORUT-PETASIA-GNI": {
        "entitas_kawasan": "GNI / Petasia industrial corridor",
        "jenis_relasi": "koridor_smelter_pesisir",
        "status_relasi": "indikatif_kuat",
        "kendaraan_legitimasi": "koridor_smelter_pesisir",
        "status_bukti_kek": "belum_ditemukan_eksplisit",
        "status_bukti_psn_rail": "belum_ditemukan_eksplisit",
        "klaim_aman": "Morowali Utara memperlihatkan koridor smelter aktif, walau simpul sandar spesifik belum terkunci.",
    },
    "NODE-SULTRA-KONAWE-MOROSI-VDNI": {
        "entitas_kawasan": "Morosi / VDNI industrial cluster",
        "jenis_relasi": "kawasan_industri",
        "status_relasi": "indikatif_kuat",
        "kendaraan_legitimasi": "kawasan_industri + kanal_ekspor_regional",
        "status_bukti_kek": "belum_ditemukan_eksplisit",
        "status_bukti_psn_rail": "program_smelter_kawasan_terkonfirmasi_non_rail",
        "klaim_aman": "Cluster Morosi tersambung ke kanal ekspor regional, tetapi jetty spesifik perusahaan belum aman diklaim.",
    },
    "NODE-SULTRA-KONAWE-OSS": {
        "entitas_kawasan": "Konawe / OSS industrial cluster",
        "jenis_relasi": "kawasan_industri",
        "status_relasi": "indikatif",
        "kendaraan_legitimasi": "kawasan_industri + kanal_ekspor_regional",
        "status_bukti_kek": "belum_ditemukan_eksplisit",
        "status_bukti_psn_rail": "program_smelter_kawasan_terkonfirmasi_non_rail",
        "klaim_aman": "OSS relevan di level cluster Konawe, tetapi masih menyatu dengan dukungan ekspor regional dan belum terpisah rapi dari VDNI.",
    },
    "NODE-SULTRA-KOLAKA-POMALAA-ANTAM": {
        "entitas_kawasan": "Pomalaa / ANTAM hilirisasi node",
        "jenis_relasi": "koridor_hilirisasi",
        "status_relasi": "indikatif_kuat",
        "kendaraan_legitimasi": "koridor_hilirisasi + kanal_ekspor_regional",
        "status_bukti_kek": "belum_ditemukan_eksplisit",
        "status_bukti_psn_rail": "psn_non_rail_terkonfirmasi",
        "klaim_aman": "Pomalaa valid sebagai node hilirisasi dan punya dukungan kanal ekspor regional, meski fasilitas sandarnya belum spesifik.",
    },
    "NODE-SULSEL-LUTIM-SOROWAKO-VALE": {
        "entitas_kawasan": "Sorowako / Luwu Timur nickel belt",
        "jenis_relasi": "sabuk_nikel",
        "status_relasi": "lead_lemah",
        "kendaraan_legitimasi": "sabuk_nikel_legacy",
        "status_bukti_kek": "belum_ditemukan_eksplisit",
        "status_bukti_psn_rail": "belum_ditemukan_eksplisit",
        "klaim_aman": "Sorowako lebih aman dipakai sebagai sabuk nikel historis dan lokasi dampak, bukan simpul logistik pesisir yang sudah terkunci.",
    },
}

DOC_SIGNAL_ROWS = [
    {
        "record_id": "DOC-IMIP-001",
        "cluster_id": "NODE-SULTENG-MOROWALI-IMIP",
        "source_family": "repo_note",
        "signal_theme": "beban_ekologis_industri",
        "impact_channel": "polusi_udara_laut",
        "evidence_tier": "tier_3",
        "reference_year": "",
        "location_label": "Morowali",
        "entity_label": "IMIP / Tsingshan / Bintang Delapan",
        "source_ref": "docs/page8_aktor_oligarki_mapping.md",
        "extract_text": "Catatan repo menempatkan IMIP sebagai pusat mega-industri dengan pencemaran udara dan laut serta PLTU captive >3900 MW.",
        "why_it_matters": "Mengubah node IMIP dari sekadar cluster izin menjadi simpul industri pesisir dengan beban ekologis besar.",
        "match_quality": "cluster_direct",
    },
    {
        "record_id": "DOC-VALE-001",
        "cluster_id": "NODE-SULSEL-LUTIM-SOROWAKO-VALE",
        "source_family": "repo_note",
        "signal_theme": "beban_ekologis_lanskap",
        "impact_channel": "sedimentasi_danau_hutan",
        "evidence_tier": "tier_3",
        "reference_year": "",
        "location_label": "Sorowako / Danau Mahalona-Towuti",
        "entity_label": "PT Vale Indonesia",
        "source_ref": "docs/page8_aktor_oligarki_mapping.md",
        "extract_text": "Catatan repo menyebut sedimentasi di Danau Mahalona dan Towuti serta cumulative ecological loss besar di blok Vale.",
        "why_it_matters": "Menjaga Sorowako tetap relevan di Tahap C sebagai node dampak, meski simpul logistik pesisir belum kuat.",
        "match_quality": "cluster_direct",
    },
]

BACKLOG_ROWS = [
    {
        "gap_id": "BACKLOG-001",
        "cluster_scope": "NODE-SULTENG-MOROWALI-IMIP",
        "gap_type": "facility_specific_proof",
        "target_bukti": "Nama jetty / terminal khusus / pelabuhan internal IMIP",
        "target_sumber": "Amdalnet / OSS / Kemenhub / annual report kawasan",
        "status_saat_ini": "cluster_siaga_tapi_fasilitas_belum_spesifik",
        "prioritas": "tinggi",
    },
    {
        "gap_id": "BACKLOG-002",
        "cluster_scope": "NODE-SULTENG-MORUT-PETASIA-GNI",
        "gap_type": "facility_specific_proof",
        "target_bukti": "Dokumen sandar atau terminal khusus GNI/Petasia",
        "target_sumber": "Kemenhub / laporan operasional / AMDAL smelter",
        "status_saat_ini": "smelter_aktif_tapi_pelabuhan_belum_terkunci",
        "prioritas": "tinggi",
    },
    {
        "gap_id": "BACKLOG-003",
        "cluster_scope": "NODE-SULTRA-KONAWE-MOROSI-VDNI|NODE-SULTRA-KONAWE-OSS",
        "gap_type": "node_separation",
        "target_bukti": "Pemisahan jetty/fasilitas sandar VDNI vs OSS",
        "target_sumber": "Dokumen terminal khusus / citra kawasan / laporan perusahaan",
        "status_saat_ini": "masih_berbagi_koridor_cluster",
        "prioritas": "tinggi",
    },
    {
        "gap_id": "BACKLOG-004",
        "cluster_scope": "NODE-SULTRA-KOLAKA-POMALAA-ANTAM",
        "gap_type": "facility_specific_proof",
        "target_bukti": "Nama fasilitas pelabuhan/dermaga Pomalaa yang melayani rantai ferronickel",
        "target_sumber": "ANTAM annual report / dokumen Kemenhub / izin kawasan",
        "status_saat_ini": "smelter_valid_tapi_pelabuhan_belum_spesifik",
        "prioritas": "tinggi",
    },
    {
        "gap_id": "BACKLOG-005",
        "cluster_scope": "NODE-SULSEL-LUTIM-SOROWAKO-VALE",
        "gap_type": "coastal_link_gap",
        "target_bukti": "Jalur logistik pesisir Sorowako yang aman diklaim untuk Bab 4.1",
        "target_sumber": "Annual report Vale / dokumen kawasan / peta logistik",
        "status_saat_ini": "masih_sabuk_nikel_belum_node_pesisir",
        "prioritas": "sedang",
    },
    {
        "gap_id": "BACKLOG-006",
        "cluster_scope": "ALL",
        "gap_type": "explicit_kek_gap",
        "target_bukti": "Dokumen yang eksplisit menyebut KEK sebagai kendaraan legitimasi node-node prioritas",
        "target_sumber": "SK KEK / dokumen proyek kawasan / OSS",
        "status_saat_ini": "belum_ada_bukti_lokal_yang_mengunci",
        "prioritas": "tinggi",
    },
    {
        "gap_id": "BACKLOG-007",
        "cluster_scope": "ALL",
        "gap_type": "psn_rail_gap",
        "target_bukti": "Proyek rel/PSN penghubung yang benar-benar relevan ke node nikel Sulawesi",
        "target_sumber": "PSN nasional / RPJMN / berita resmi proyek",
        "status_saat_ini": "tracking_repo_masih_kosong",
        "prioritas": "sedang",
    },
]

OFFICIAL_SOURCE_ROWS = [
    {
        "source_id": "SRC-OFFICIAL-001",
        "cluster_scope": "NODE-SULTENG-MOROWALI-IMIP|NODE-SULTRA-KONAWE-MOROSI-VDNI|NODE-SULTRA-KONAWE-OSS",
        "source_family": "kppip_psn_smelter",
        "institution": "KPPIP",
        "evidence_direction": "positive",
        "source_title": "U. Proyek Pembangunan Smelter",
        "source_ref": "https://kppip.go.id/proyek-strategis-nasional/u-proyek-pembangunan-smelter/",
        "access_type": "html",
        "terms_hit": "Morowali; Konawe",
        "key_extract": "Listing proyek smelter KPPIP memasukkan Morowali dan Konawe sebagai lokasi resmi program pembangunan smelter.",
        "stage_c_use": "menaikkan keyakinan bahwa Morowali dan Konawe punya jangkar resmi pada daftar PSN/program smelter nasional",
        "confidence_gain": "psn_program_signal",
        "followup_status": "sudah_diikat",
    },
    {
        "source_id": "SRC-OFFICIAL-002",
        "cluster_scope": "NODE-SULTENG-MOROWALI-IMIP|NODE-SULTRA-KONAWE-MOROSI-VDNI|NODE-SULTRA-KONAWE-OSS",
        "source_family": "kppip_kawasan_industri",
        "institution": "KPPIP",
        "evidence_direction": "positive",
        "source_title": "S. Pembangunan Kawasan Industri Prioritas / Kawasan Ekonomi Khusus",
        "source_ref": "https://kppip.go.id/proyek-strategis-nasional/s-pembangunan-kawasan-industri-prioritas-kawasan-ekonomi-khusus/",
        "access_type": "html",
        "terms_hit": "Kawasan Industri Morowali; Kawasan Industri Konawe",
        "key_extract": "Halaman KPPIP untuk kawasan industri prioritas memasukkan Kawasan Industri Morowali dan Kawasan Industri Konawe.",
        "stage_c_use": "menaikkan keyakinan legitimasi kawasan industri pada node Morowali dan Konawe",
        "confidence_gain": "kawasan_legitimacy_signal",
        "followup_status": "sudah_diikat",
    },
    {
        "source_id": "SRC-OFFICIAL-003",
        "cluster_scope": "ALL",
        "source_family": "kppip_rail_reference",
        "institution": "KPPIP",
        "evidence_direction": "negative",
        "source_title": "Kereta Api Makassar - Parepare",
        "source_ref": "https://kppip.go.id/proyek-prioritas/kereta-api/kereta-api-makassar-parepare/",
        "access_type": "html",
        "terms_hit": "Makassar; Parepare",
        "key_extract": "Halaman proyek kereta KPPIP yang relevan di Sulawesi hanya mengunci Makassar-Parepare, bukan Morowali/Konawe/Pomalaa/Sorowako.",
        "stage_c_use": "negative official evidence untuk membatasi overclaim soal rail penghubung node nikel prioritas",
        "confidence_gain": "rail_negative_signal",
        "followup_status": "sudah_diikat",
    },
    {
        "source_id": "SRC-OFFICIAL-004",
        "cluster_scope": "NODE-SULTRA-KOLAKA-POMALAA-ANTAM",
        "source_family": "company_primary_pdf",
        "institution": "PT Vale Indonesia",
        "evidence_direction": "positive",
        "source_title": "PT Vale Indonesia Officially Begins Pomalaa Block Development",
        "source_ref": "data/raw/rev1_logistik/external_vale_pomalaa.pdf",
        "access_type": "pdf_downloaded",
        "terms_hit": "Pomalaa; Kolaka; National Strategic Project; downstream nickel",
        "key_extract": "PDF resmi Vale menyebut proyek Pomalaa di Kolaka sebagai National Strategic Project dan bagian percepatan downstream nickel production.",
        "stage_c_use": "menaikkan keyakinan node Pomalaa dari sekadar smelter valid menjadi proyek hilirisasi resmi berstatus strategis",
        "confidence_gain": "company_primary_psn_signal",
        "followup_status": "sudah_diunduh",
    },
    {
        "source_id": "SRC-OFFICIAL-005",
        "cluster_scope": "NODE-SULTENG-MOROWALI-IMIP",
        "source_family": "company_primary_pdf",
        "institution": "PT Vale Indonesia",
        "evidence_direction": "positive",
        "source_title": "PT Vale dan PT BNSI Resmikan Pembangunan Proyek Pertambangan dan Pengolahan Nikel Rendah Karbon Terintegrasi di Morowali",
        "source_ref": "data/raw/rev1_logistik/external_vale_morowali.pdf",
        "access_type": "pdf_downloaded",
        "terms_hit": "Morowali; Bahodopi; Bungku Timur; Sambalagi; PSN",
        "key_extract": "PDF resmi Vale menyebut Proyek Morowali dinyatakan sebagai PSN pada 2022 serta mengunci lokasi tambang di Bungku Timur/Bahodopi dan pabrik di Sambalagi.",
        "stage_c_use": "menaikkan keyakinan node Morowali pada level proyek primer resmi dan mengunci geografi proyek",
        "confidence_gain": "company_primary_psn_signal",
        "followup_status": "sudah_diunduh",
    },
    {
        "source_id": "SRC-OFFICIAL-006",
        "cluster_scope": "ALL",
        "source_family": "kemenhub_regulation_signal",
        "institution": "Kementerian Perhubungan",
        "evidence_direction": "methodological",
        "source_title": "Kemenhub Sempurnakan Aturan Penggunaan Terminal Khusus untuk Kepentingan Umum",
        "source_ref": "https://dephub.go.id/post/read/kemenhub-sempurnakan-aturan-penggunaan-terminal-khusus-untuk-kepentingan-umum",
        "access_type": "html",
        "terms_hit": "PM 71 Tahun 2016; terminal khusus; terminal untuk kepentingan sendiri",
        "key_extract": "Artikel Kemenhub mengunci regulasi PM 71 Tahun 2016 sebagai payung untuk terminal khusus dan terminal untuk kepentingan sendiri.",
        "stage_c_use": "memberi jalur resmi untuk dorking dokumen terminal khusus dan konsesi pelabuhan",
        "confidence_gain": "regulatory_anchor",
        "followup_status": "sudah_diikat",
    },
    {
        "source_id": "SRC-OFFICIAL-007",
        "cluster_scope": "NODE-SULTENG-MOROWALI-IMIP",
        "source_family": "dephub_search_negative",
        "institution": "Kementerian Perhubungan",
        "evidence_direction": "negative",
        "source_title": "Hasil pencarian Morowali pada portal Dephub",
        "source_ref": "https://dephub.go.id/search?keyword=Morowali",
        "access_type": "html_search",
        "terms_hit": "Morowali",
        "key_extract": "Pencarian resmi Dephub untuk Morowali yang muncul saat ini didominasi berita banjir/evakuasi, bukan entri terminal khusus atau pelabuhan nikel.",
        "stage_c_use": "menjelaskan kenapa bukti port-specific masih belum naik walau sudah dikejar di portal pemerintah",
        "confidence_gain": "search_negative_signal",
        "followup_status": "sudah_diikat",
    },
]

DORKING_ROWS = [
    {
        "dork_id": "DORK-001",
        "priority": "tinggi",
        "cluster_scope": "NODE-SULTENG-MOROWALI-IMIP",
        "objective": "cari nama terminal khusus / jetty / izin sandar IMIP atau proyek Morowali",
        "query_template": "site:ppid.dephub.go.id OR site:jdih.kemenhub.go.id \"terminal khusus\" Morowali OR Bahodopi OR Sambalagi filetype:pdf",
        "target_domain": "ppid.dephub.go.id; jdih.kemenhub.go.id",
        "expected_artifact": "PDF regulasi/izin terminal khusus atau dokumen lampiran",
    },
    {
        "dork_id": "DORK-002",
        "priority": "tinggi",
        "cluster_scope": "NODE-SULTRA-KOLAKA-POMALAA-ANTAM",
        "objective": "cari fasilitas pelabuhan/dermaga resmi untuk Pomalaa",
        "query_template": "site:antam.com OR site:idx.co.id Pomalaa ferronickel port OR jetty OR terminal filetype:pdf",
        "target_domain": "antam.com; idx.co.id",
        "expected_artifact": "annual report / presentation / operational report",
    },
    {
        "dork_id": "DORK-003",
        "priority": "tinggi",
        "cluster_scope": "NODE-SULTENG-MORUT-PETASIA-GNI",
        "objective": "cari izin atau laporan operasional sandar GNI/Petasia",
        "query_template": "site:jdih.kemenhub.go.id OR site:dephub.go.id \"Gunbuster Nickel Industry\" OR Petasia AND (\"terminal khusus\" OR jetty OR pelabuhan)",
        "target_domain": "jdih.kemenhub.go.id; dephub.go.id",
        "expected_artifact": "berita resmi / keputusan / lampiran terminal khusus",
    },
    {
        "dork_id": "DORK-004",
        "priority": "tinggi",
        "cluster_scope": "NODE-SULTRA-KONAWE-MOROSI-VDNI|NODE-SULTRA-KONAWE-OSS",
        "objective": "pisahkan jetty atau fasilitas sandar VDNI dan OSS",
        "query_template": "site:jdih.kemenhub.go.id OR site:dephub.go.id VDNI OR OSS Konawe \"terminal khusus\" filetype:pdf",
        "target_domain": "jdih.kemenhub.go.id; dephub.go.id",
        "expected_artifact": "izin pelabuhan khusus / konsesi / lampiran koordinat",
    },
    {
        "dork_id": "DORK-005",
        "priority": "sedang",
        "cluster_scope": "NODE-SULSEL-LUTIM-SOROWAKO-VALE",
        "objective": "cari jalur logistik resmi Sorowako yang layak untuk Bab 4.1",
        "query_template": "site:vale.com/indonesia OR site:idx.co.id Sorowako logistics OR port OR shipment filetype:pdf",
        "target_domain": "vale.com; idx.co.id",
        "expected_artifact": "annual report / sustainability / logistics mention",
    },
    {
        "dork_id": "DORK-006",
        "priority": "sedang",
        "cluster_scope": "ALL",
        "objective": "cek apakah ada dokumen KEK eksplisit yang benar-benar memuat node prioritas",
        "query_template": "site:kek.go.id OR site:ekon.go.id Morowali OR Konawe OR Pomalaa OR Sorowako \"Kawasan Ekonomi Khusus\"",
        "target_domain": "kek.go.id; ekon.go.id",
        "expected_artifact": "daftar KEK / SK / rilis resmi",
    },
    {
        "dork_id": "DORK-007",
        "priority": "sedang",
        "cluster_scope": "ALL",
        "objective": "cek apakah ada rail/PSN yang benar-benar terhubung ke node nikel prioritas",
        "query_template": "site:kppip.go.id OR site:ekon.go.id OR site:bappenas.go.id Morowali OR Konawe OR Pomalaa OR Sorowako kereta OR rail OR PSN",
        "target_domain": "kppip.go.id; ekon.go.id; bappenas.go.id",
        "expected_artifact": "halaman proyek / dokumen RPJMN / rilis resmi",
    },
]


def load_master(name: str) -> pd.DataFrame:
    return pd.read_csv(MASTER_DIR / name)


def load_processed(name: str) -> pd.DataFrame:
    return pd.read_csv(BASE_DIR / "data" / "processed" / name)


def write_csv(df: pd.DataFrame, name: str) -> None:
    df.to_csv(WORKING_DIR / name, index=False, encoding="utf-8-sig")


def compact_text(value: object, limit: int = 220) -> str:
    text = " ".join(str(value or "").replace("\n", " ").split())
    return text[: limit - 3] + "..." if len(text) > limit else text


def band_count(value: float, high: float, medium: float) -> str:
    if value >= high:
        return "tinggi"
    if value >= medium:
        return "sedang"
    if value > 0:
        return "rendah"
    return "tidak_ada"


def match_text_series(df: pd.DataFrame, columns: list[str], keywords: list[str]) -> pd.Series:
    mask = pd.Series(False, index=df.index)
    for column in columns:
        if column not in df.columns:
            continue
        text = df[column].fillna("").astype(str)
        for keyword in keywords:
            mask = mask | text.str.contains(keyword, case=False, regex=False)
    return mask


def build_kawasan_relations(cluster_df: pd.DataFrame, evidence_df: pd.DataFrame) -> pd.DataFrame:
    evidence_counts = evidence_df.groupby("cluster_id").size().to_dict()
    rows = []
    for _, row in cluster_df.iterrows():
        context = CLUSTER_CONTEXT[row["cluster_id"]]
        rows.append(
            {
                "cluster_key": row["cluster_key"],
                "cluster_id": row["cluster_id"],
                "entitas_kawasan": context["entitas_kawasan"],
                "jenis_relasi": context["jenis_relasi"],
                "status_relasi": context["status_relasi"],
                "kendaraan_legitimasi": context["kendaraan_legitimasi"],
                "status_bukti_kek_eksplisit": context["status_bukti_kek"],
                "status_bukti_psn_rail": context["status_bukti_psn_rail"],
                "indikasi_terkait_kek_field": row["terkait_KEK"],
                "nama_kawasan_field": row["nama_KEK_atau_kawasan"],
                "evidence_rows": evidence_counts.get(row["cluster_id"], 0),
                "kesimpulan": row["kesimpulan"],
            }
        )
    return pd.DataFrame(rows)


def build_transport_project_tracking() -> pd.DataFrame:
    rows = [
        {
            "project_id": "TRANSPORT-001",
            "project_name": "Seaport IMIP / Bahodopi",
            "project_type": "seaport",
            "cluster_id": "NODE-SULTENG-MOROWALI-IMIP",
            "status_relevansi": "terkonfirmasi_publik",
            "evidence_level": "public_osint",
            "catatan": "Sumber publik yang sudah dikunci di Tahap B menyebut IMIP memiliki seaport sendiri; nama fasilitas spesifik belum diperoleh.",
        },
        {
            "project_id": "TRANSPORT-002",
            "project_name": "Kendari New Port",
            "project_type": "regional_export_port",
            "cluster_id": "NODE-SULTRA-KONAWE-MOROSI-VDNI",
            "status_relevansi": "dukungan_provinsi",
            "evidence_level": "public_osint + export_data",
            "catatan": "Dipakai sebagai kanal ekspor provinsi-level untuk cluster Konawe/Pomalaa, belum otomatis sama dengan jetty perusahaan.",
        },
        {
            "project_id": "TRANSPORT-003",
            "project_name": "Kendari New Port",
            "project_type": "regional_export_port",
            "cluster_id": "NODE-SULTRA-KONAWE-OSS",
            "status_relevansi": "dukungan_provinsi",
            "evidence_level": "public_osint + export_data",
            "catatan": "Dukungan regional untuk OSS, belum memisahkan fasilitas sandar spesifik.",
        },
        {
            "project_id": "TRANSPORT-004",
            "project_name": "Kendari New Port",
            "project_type": "regional_export_port",
            "cluster_id": "NODE-SULTRA-KOLAKA-POMALAA-ANTAM",
            "status_relevansi": "dukungan_provinsi",
            "evidence_level": "export_data",
            "catatan": "Kanal ekspor ferronickel/alloy nickel Sultra pada data repo.",
        },
        {
            "project_id": "TRANSPORT-005",
            "project_name": "Rail / PSN connector for priority nodes",
            "project_type": "rail_or_psn_connector",
            "cluster_id": "",
            "status_relevansi": "belum_terbukti_kuat",
            "evidence_level": "negative_finding",
            "catatan": "File tracking rel/PSN lokal masih kosong, jadi rail/PSN belum layak dijadikan tulang punggung narasi Fase 3.",
        },
    ]
    return pd.DataFrame(rows)


def build_negative_findings() -> pd.DataFrame:
    rows = [
        {
            "finding_id": "NEG-001",
            "finding_type": "facility_specific_gap",
            "cluster_scope": "NODE-SULTRA-KONAWE-MOROSI-VDNI|NODE-SULTRA-KONAWE-OSS|NODE-SULTRA-KOLAKA-POMALAA-ANTAM",
            "statement": "Nama jetty / terminal khusus spesifik belum bisa dikunci hanya dari data repo lokal dan OSINT cepat.",
            "implication": "Narasi aman tetap di level cluster dan kanal ekspor regional, jangan memaksa nama fasilitas perusahaan tanpa dokumen primer.",
        },
        {
            "finding_id": "NEG-002",
            "finding_type": "rail_psn_gap",
            "cluster_scope": "ALL",
            "statement": "Bukti rel/PSN penghubung yang benar-benar relevan dengan node prioritas belum cukup kuat.",
            "implication": "Rail/PSN harus ditempatkan sebagai backlog pembuktian, bukan fondasi utama Bab 4.1.",
        },
        {
            "finding_id": "NEG-003",
            "finding_type": "explicit_kek_gap",
            "cluster_scope": "ALL",
            "statement": "Belum ada dokumen lokal yang mengunci status KEK eksplisit untuk node prioritas Fase 3.",
            "implication": "Gunakan istilah kawasan industri, koridor hilirisasi, atau simpul pesisir bila itu yang benar-benar didukung data.",
        },
        {
            "finding_id": "NEG-004",
            "finding_type": "node_separation_gap",
            "cluster_scope": "NODE-SULTRA-KONAWE-MOROSI-VDNI|NODE-SULTRA-KONAWE-OSS",
            "statement": "Cluster Konawe masih berbagi dukungan ekspor regional dan belum terpisah rapi di level fasilitas sandar.",
            "implication": "VDNI dan OSS aman dipisah di level entitas smelter, tetapi belum aman dipisah keras di level jetty.",
        },
        {
            "finding_id": "NEG-005",
            "finding_type": "coastal_link_gap",
            "cluster_scope": "NODE-SULSEL-LUTIM-SOROWAKO-VALE",
            "statement": "Sorowako kuat sebagai sabuk nikel dan node dampak, tetapi jalur logistik pesisirnya belum terkunci.",
            "implication": "Pakai Sorowako sebagai pembanding batas klaim dan bukti dampak, bukan contoh utama infrastruktur pelabuhan.",
        },
    ]
    return pd.DataFrame(rows)


def extract_conflict_environment_signals() -> pd.DataFrame:
    records: list[dict[str, object]] = []

    agraria_df = load_processed("sulawesi_konflik_agraria_tanahkita.csv")
    agraria_map = [
        (
            "NODE-SULTRA-KOLAKA-POMALAA-ANTAM",
            ["Hakatotubu", "Tambea", "Pomalaa"],
        ),
        (
            "NODE-SULSEL-LUTIM-SOROWAKO-VALE",
            ["Karunsi", "Sorowako", "Luwu Timur", "Towuti", "Mahalona"],
        ),
    ]
    record_no = 1
    for cluster_id, keywords in agraria_map:
        mask = match_text_series(agraria_df, ["judul", "deskripsi", "narasi"], keywords)
        for _, row in agraria_df[mask].head(4).iterrows():
            records.append(
                {
                    "record_id": f"AGR-{record_no:03d}",
                    "cluster_id": cluster_id,
                    "source_family": "konflik_agraria",
                    "signal_theme": "konflik_dan_ruang_hidup",
                    "impact_channel": "pesisir_livelihood" if cluster_id.endswith("POMALAA-ANTAM") else "adat_dan_permukiman",
                    "evidence_tier": "tier_2",
                    "reference_year": row.get("tahun", ""),
                    "location_label": compact_text(row.get("lokasi", "")),
                    "entity_label": compact_text(row.get("judul", "")),
                    "source_ref": "data/processed/sulawesi_konflik_agraria_tanahkita.csv",
                    "extract_text": compact_text(row.get("narasi") or row.get("deskripsi", "")),
                    "why_it_matters": "Menambah bukti bahwa node tidak hanya punya izin/PLTU, tetapi juga jejak tekanan sosial-ekologis di sekitarnya.",
                    "match_quality": "cluster_direct",
                }
            )
            record_no += 1

    fpic_df = load_processed("sulawesi_konflik_tambang_fpic.csv")
    fpic_mask = match_text_series(
        fpic_df,
        ["judul", "deskripsi", "nama_perusahaan"],
        ["Karunsi", "Sorowako", "Luwu Timur"],
    )
    for _, row in fpic_df[fpic_mask].head(3).iterrows():
        records.append(
            {
                "record_id": f"FPIC-{record_no:03d}",
                "cluster_id": "NODE-SULSEL-LUTIM-SOROWAKO-VALE",
                "source_family": "konflik_fpic",
                "signal_theme": "fpic_dan_kriminalisasi",
                "impact_channel": "adat_dan_hak_tanah",
                "evidence_tier": "tier_2",
                "reference_year": row.get("tahun", ""),
                "location_label": compact_text(row.get("provinsi", "")),
                "entity_label": compact_text(row.get("judul", "")),
                "source_ref": "data/processed/sulawesi_konflik_tambang_fpic.csv",
                "extract_text": compact_text(row.get("deskripsi") or row.get("judul", "")),
                "why_it_matters": "Memberi dasar bahwa Sorowako/ Vale tetap penting di Tahap C sebagai node dampak dan konflik tata kelola.",
                "match_quality": "cluster_direct",
            }
        )
        record_no += 1

    waste_df = load_processed("sulawesi_limbah_b3.csv")
    waste_map = [
        ("NODE-SULTENG-MOROWALI-IMIP", ["IMIP", "Morowali", "Huayue", "QMB"]),
        ("NODE-SULTRA-KONAWE-MOROSI-VDNI", ["VDNI", "Konawe"]),
    ]
    for cluster_id, keywords in waste_map:
        mask = match_text_series(waste_df, ["Kawasan/Perusahaan"], keywords)
        for _, row in waste_df[mask].head(4).iterrows():
            records.append(
                {
                    "record_id": f"WASTE-{record_no:03d}",
                    "cluster_id": cluster_id,
                    "source_family": "limbah_b3",
                    "signal_theme": "beban_limbah_industri",
                    "impact_channel": "slag_tailing_limbah",
                    "evidence_tier": "tier_2",
                    "reference_year": "",
                    "location_label": compact_text(row.get("Provinsi", "")),
                    "entity_label": compact_text(row.get("Kawasan/Perusahaan", "")),
                    "source_ref": "data/processed/sulawesi_limbah_b3.csv",
                    "extract_text": compact_text(row.get("Catatan", "")),
                    "why_it_matters": "Menguatkan bahwa node industri pesisir memerlukan arus logistik besar sekaligus menghasilkan beban limbah besar.",
                    "match_quality": "cluster_direct" if "VDNI" in str(row.get("Kawasan/Perusahaan", "")) or "IMIP" in str(row.get("Kawasan/Perusahaan", "")) else "cluster_area",
                }
            )
            record_no += 1

    permit_issue_df = load_processed("kpa_masalah_izin_perusahaan.csv")
    issue_mask = match_text_series(permit_issue_df, ["nama_perusahaan", "excerpt"], ["IMIP", "Morowali Industrial Park"])
    for _, row in permit_issue_df[issue_mask].iterrows():
        records.append(
            {
                "record_id": f"ISSUE-{record_no:03d}",
                "cluster_id": "NODE-SULTENG-MOROWALI-IMIP",
                "source_family": "masalah_izin",
                "signal_theme": "tumpang_tindih_izin",
                "impact_channel": "governance_bottleneck",
                "evidence_tier": "tier_2",
                "reference_year": row.get("tahun_laporan", ""),
                "location_label": compact_text(row.get("lokasi", "")),
                "entity_label": compact_text(row.get("nama_perusahaan", "")),
                "source_ref": "data/processed/kpa_masalah_izin_perusahaan.csv",
                "extract_text": compact_text(row.get("excerpt", "")),
                "why_it_matters": "Menambah jalur argumen bahwa ekspansi infrastruktur juga terkait bottleneck tata kelola dan tumpang tindih izin.",
                "match_quality": "cluster_direct",
            }
        )
        record_no += 1

    records.extend(DOC_SIGNAL_ROWS)
    return pd.DataFrame(records)


def build_legitimacy_matrix(
    cluster_df: pd.DataFrame,
    conflict_env_df: pd.DataFrame,
    source_leads_df: pd.DataFrame,
) -> pd.DataFrame:
    impact_counts = conflict_env_df.groupby("cluster_id").size().to_dict()
    official_counts = (
        source_leads_df.assign(cluster_scope_split=source_leads_df["cluster_scope"].str.split("|", regex=False))
        .explode("cluster_scope_split")
        .groupby("cluster_scope_split")
        .size()
        .to_dict()
    )
    rows = []
    for _, row in cluster_df.iterrows():
        context = CLUSTER_CONTEXT[row["cluster_id"]]
        impact_count = impact_counts.get(row["cluster_id"], 0)
        official_count = official_counts.get(row["cluster_id"], 0)
        if row["cluster_id"] == "NODE-SULTENG-MOROWALI-IMIP":
            assessment = "cukup_kuat_untuk_bukti_infrastruktur_pesisir"
            risk = "sedang"
        elif row["status_validasi"] == "indikatif_kuat":
            assessment = "cukup_kuat_untuk_bukti_koridor_industri"
            risk = "sedang"
        elif row["status_validasi"] == "indikatif":
            assessment = "cukup_dengan_batas_klaster"
            risk = "tinggi"
        else:
            assessment = "pelengkap_dan_kontras"
            risk = "tinggi"
        rows.append(
            {
                "cluster_key": row["cluster_key"],
                "cluster_id": row["cluster_id"],
                "node_label": row["node_label"],
                "kendaraan_legitimasi": context["kendaraan_legitimasi"],
                "status_bukti_kek_eksplisit": context["status_bukti_kek"],
                "status_bukti_psn_rail": context["status_bukti_psn_rail"],
                "indikasi_kawasan_field": row["nama_KEK_atau_kawasan"],
                "core_nickel_permit_rows": row["core_nickel_permit_rows"],
                "pltu_capacity_mw": row["pltu_capacity_mw"],
                "export_rows": row["export_rows"],
                "impact_signal_rows": impact_count,
                "official_source_rows": official_count,
                "legitimacy_assessment": assessment,
                "overclaim_risk": risk,
                "recommended_safe_sentence": context["klaim_aman"],
            }
        )
    return pd.DataFrame(rows)


def build_corridor_scorecard(
    cluster_df: pd.DataFrame,
    evidence_df: pd.DataFrame,
    conflict_env_df: pd.DataFrame,
    source_leads_df: pd.DataFrame,
) -> pd.DataFrame:
    evidence_counts = evidence_df.groupby("cluster_id").size().to_dict()
    impact_counts = conflict_env_df.groupby("cluster_id").size().to_dict()
    official_counts = (
        source_leads_df.assign(cluster_scope_split=source_leads_df["cluster_scope"].str.split("|", regex=False))
        .explode("cluster_scope_split")
        .groupby("cluster_scope_split")
        .size()
        .to_dict()
    )
    rows = []
    for _, row in cluster_df.iterrows():
        evidence_count = evidence_counts.get(row["cluster_id"], 0)
        impact_count = impact_counts.get(row["cluster_id"], 0)
        official_count = official_counts.get(row["cluster_id"], 0)
        permit_score = band_count(float(row["core_nickel_permit_rows"]), 25, 10)
        power_score = band_count(float(row["pltu_capacity_mw"]), 3000, 500)
        export_score = band_count(float(row["export_rows"]), 10, 1)
        impact_score = band_count(float(impact_count), 4, 2)
        context = CLUSTER_CONTEXT[row["cluster_id"]]
        if row["cluster_id"] == "NODE-SULTENG-MOROWALI-IMIP":
            readiness = "tier_c1_siap_bab41"
        elif row["status_validasi"] == "indikatif_kuat":
            readiness = "tier_c1_siap_bab41"
        elif row["status_validasi"] == "indikatif":
            readiness = "tier_c2_siap_dengan_batas"
        else:
            readiness = "tier_c3_pelengkap_kontras"
        rows.append(
            {
                "cluster_key": row["cluster_key"],
                "cluster_id": row["cluster_id"],
                "node_label": row["node_label"],
                "permit_intensity_score": permit_score,
                "power_support_score": power_score,
                "export_channel_score": export_score,
                "evidence_rows": evidence_count,
                "official_source_rows": official_count,
                "impact_signal_rows": impact_count,
                "impact_signal_score": impact_score,
                "psn_rail_signal": context["status_bukti_psn_rail"],
                "dataset_tier_stage_c": readiness,
                "reason": row["kesimpulan"],
            }
        )
    return pd.DataFrame(rows)


def build_bab41_argument_map(
    cluster_df: pd.DataFrame,
    scorecard_df: pd.DataFrame,
    legitimacy_df: pd.DataFrame,
) -> pd.DataFrame:
    score_map = scorecard_df.set_index("cluster_id").to_dict("index")
    legit_map = legitimacy_df.set_index("cluster_id").to_dict("index")
    rows = []
    for _, row in cluster_df.iterrows():
        cluster_id = row["cluster_id"]
        score_row = score_map[cluster_id]
        legit_row = legit_map[cluster_id]
        if score_row["dataset_tier_stage_c"] == "tier_c1_siap_bab41":
            safe_usage = "narasi_utama_bab_4_1"
        elif score_row["dataset_tier_stage_c"] == "tier_c2_siap_dengan_batas":
            safe_usage = "narasi_pelengkap_bab_4_1"
        else:
            safe_usage = "catatan_batas_klaim"
        rows.append(
            {
                "cluster_key": row["cluster_key"],
                "cluster_id": cluster_id,
                "node_label": row["node_label"],
                "claim_core": legit_row["recommended_safe_sentence"],
                "claim_support_minimum": "izin nikel + PLTU captive + bukti kawasan/ekspor + sinyal dampak bila ada",
                "forbidden_overclaim": "jangan sebut nama jetty/terminal khusus spesifik tanpa dokumen primer",
                "safe_usage": safe_usage,
                "dataset_tier_stage_c": score_row["dataset_tier_stage_c"],
            }
        )
    return pd.DataFrame(rows)


def build_narrative_blocks(argument_map_df: pd.DataFrame) -> pd.DataFrame:
    confidence_map = {
        "tier_c1_siap_bab41": "tinggi",
        "tier_c2_siap_dengan_batas": "sedang",
        "tier_c3_pelengkap_kontras": "rendah",
    }
    return argument_map_df.assign(
        confidence=argument_map_df["dataset_tier_stage_c"].map(confidence_map),
        narrative_claim=argument_map_df["claim_core"],
    )[
        ["cluster_key", "cluster_id", "confidence", "narrative_claim", "safe_usage"]
    ]


def build_manifest(outputs: dict[str, int]) -> dict:
    return {
        "stage": "rev1_logistik_tahap_c",
        "generated_at": TODAY,
        "working_dir": str(WORKING_DIR.relative_to(BASE_DIR)).replace("\\", "/"),
        "outputs": outputs,
    }


def main() -> None:
    cluster_df = load_master("rev1_logistik_master_cluster_dim.csv")
    evidence_df = load_master("rev1_logistik_master_evidence_fact.csv")

    kawasan_rel_df = build_kawasan_relations(cluster_df, evidence_df)
    transport_df = build_transport_project_tracking()
    negative_df = build_negative_findings()
    conflict_env_df = extract_conflict_environment_signals()
    source_leads_df = pd.DataFrame(OFFICIAL_SOURCE_ROWS)
    dorking_df = pd.DataFrame(DORKING_ROWS)
    legitimacy_df = build_legitimacy_matrix(cluster_df, conflict_env_df, source_leads_df)
    scorecard_df = build_corridor_scorecard(cluster_df, evidence_df, conflict_env_df, source_leads_df)
    argument_map_df = build_bab41_argument_map(cluster_df, scorecard_df, legitimacy_df)
    narrative_df = build_narrative_blocks(argument_map_df)
    backlog_df = pd.DataFrame(BACKLOG_ROWS)

    write_csv(kawasan_rel_df, "rev1_tahap_c_kawasan_relations.csv")
    write_csv(transport_df, "rev1_tahap_c_transport_project_tracking.csv")
    write_csv(negative_df, "rev1_tahap_c_negative_findings.csv")
    write_csv(conflict_env_df, "rev1_tahap_c_conflict_environment_extract.csv")
    write_csv(legitimacy_df, "rev1_tahap_c_legitimacy_matrix.csv")
    write_csv(scorecard_df, "rev1_tahap_c_corridor_scorecard.csv")
    write_csv(argument_map_df, "rev1_tahap_c_bab41_argument_map.csv")
    write_csv(narrative_df, "rev1_tahap_c_narrative_blocks.csv")
    write_csv(backlog_df, "rev1_tahap_c_psn_kek_backlog.csv")
    write_csv(source_leads_df, "rev1_tahap_c_official_source_leads.csv")
    write_csv(dorking_df, "rev1_tahap_c_dorking_queue.csv")

    outputs = {
        "kawasan_relations_rows": len(kawasan_rel_df),
        "transport_project_tracking_rows": len(transport_df),
        "negative_findings_rows": len(negative_df),
        "conflict_environment_extract_rows": len(conflict_env_df),
        "legitimacy_matrix_rows": len(legitimacy_df),
        "corridor_scorecard_rows": len(scorecard_df),
        "bab41_argument_map_rows": len(argument_map_df),
        "narrative_blocks_rows": len(narrative_df),
        "psn_kek_backlog_rows": len(backlog_df),
        "official_source_leads_rows": len(source_leads_df),
        "dorking_queue_rows": len(dorking_df),
    }
    (METADATA_DIR / "rev1_logistik_stage_c_manifest.json").write_text(
        json.dumps(build_manifest(outputs), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("rev1_logistik Tahap C initialized.")
    for key, value in outputs.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
