from __future__ import annotations

import json
from datetime import date
from pathlib import Path
import sys

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))


RAW_STAGE_DIR = BASE_DIR / "data" / "raw" / "rev1_logistik"
WORKING_DIR = RAW_STAGE_DIR / "working"
METADATA_DIR = RAW_STAGE_DIR / "metadata"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
TODAY = date.today().isoformat()


NODE_EVIDENCE_CONFIG = {
    "NODE-SULTENG-MOROWALI-IMIP-001": {
        "status_validasi": "indikatif_kuat",
        "final_tier": "tier_2",
        "fungsi_tervalidasi": "logistik_kawasan_industri",
        "jenis_fasilitas_final": "tidak_terklasifikasi",
        "operator_fasilitas": "",
        "catatan_final": "Cluster sangat kuat sebagai simpul industri nikel, tetapi repo lokal belum menyebut nama terminal khusus atau jetty final. Tetap valid sebagai node prioritas Tahap C/OSINT.",
        "evidence": [
            {
                "evidence_type": "cluster_signal",
                "source_path": "data/raw/rev1_logistik/working/rev1_tahap_a_region_summary.csv",
                "evidence_strength": "tier_2",
                "summary_template": "{permit_nikel_total} izin nikel dan {pltu_units} unit PLTU captive ({pltu_capacity_mw:.0f} MW) mengunci Morowali sebagai cluster industri nikel terbesar di repo.",
                "supports_function": "ya",
            },
            {
                "evidence_type": "narrative_anchor",
                "source_path": "docs/Page1-Assessment-Gaps.md",
                "evidence_strength": "tier_2",
                "summary": "Repo menandai IMIP sebagai kawasan mega-industri yang perlu direkap sebagai satu cluster, sehingga layak dipakai sebagai jangkar validasi logistik.",
                "supports_function": "ya",
            },
            {
                "evidence_type": "industrial_waste_signal",
                "source_path": "data/processed/sulawesi_limbah_b3.csv",
                "evidence_strength": "tier_2",
                "summary": "Entri limbah B3 untuk IMIP Morowali menunjukkan volume slag dan tailing skala besar, menguatkan fungsi node sebagai simpul operasi industri nikel.",
                "supports_function": "ya",
            },
        ],
    },
    "NODE-SULTENG-MORUT-PETASIA-GNI-001": {
        "status_validasi": "indikatif_kuat",
        "final_tier": "tier_2",
        "fungsi_tervalidasi": "pengapalan_produk_smelter",
        "jenis_fasilitas_final": "tidak_terklasifikasi",
        "operator_fasilitas": "",
        "catatan_final": "Keterkaitan node dengan GNI kuat, tetapi repo belum menyimpan nama jetty atau terminal khusus yang bisa dipakai sebagai klaim final.",
        "evidence": [
            {
                "evidence_type": "cluster_signal",
                "source_path": "data/raw/rev1_logistik/working/rev1_tahap_a_region_summary.csv",
                "evidence_strength": "tier_2",
                "summary_template": "{permit_nikel_total} izin nikel dan {pltu_units} unit PLTU captive ({pltu_capacity_mw:.0f} MW) memperlihatkan Petasia/Morowali Utara sebagai klaster aktif untuk rantai nikel.",
                "supports_function": "ya",
            },
            {
                "evidence_type": "power_anchor",
                "source_path": "data/processed/sulawesi_pltu_captive.csv",
                "evidence_strength": "tier_2",
                "summary": "Dataset PLTU captive berulang kali menyebut PT Gunbuster Nickel Industry di Petasia melalui Delong Nickel Phase III dan IV power station.",
                "supports_function": "ya",
            },
            {
                "evidence_type": "smelter_match",
                "source_path": "tools/scrapling/validate_cgs_matching.py",
                "evidence_strength": "tier_2",
                "summary": "File matching repo mengakui Gunbuster Nickel Industry sebagai entitas smelter nikel yang relevan untuk Morowali Utara.",
                "supports_function": "ya",
            },
        ],
    },
    "NODE-SULTRA-KONAWE-MOROSI-VDNI-001": {
        "status_validasi": "indikatif_kuat",
        "final_tier": "tier_2",
        "fungsi_tervalidasi": "logistik_kawasan_industri",
        "jenis_fasilitas_final": "tidak_terklasifikasi",
        "operator_fasilitas": "",
        "catatan_final": "Node Morosi-VDNI lolos sebagai simpul logistik prioritas. Bukti lokal kuat untuk cluster industrinya, tetapi nama fasilitas sandar final belum muncul eksplisit di repo.",
        "evidence": [
            {
                "evidence_type": "cluster_signal",
                "source_path": "data/raw/rev1_logistik/working/rev1_tahap_a_region_summary.csv",
                "evidence_strength": "tier_2",
                "summary_template": "{permit_nikel_total} izin nikel dan {pltu_units} unit PLTU captive ({pltu_capacity_mw:.0f} MW) menandai Morosi/Konawe sebagai klaster nikel aktif.",
                "supports_function": "ya",
            },
            {
                "evidence_type": "power_anchor",
                "source_path": "data/processed/sulawesi_pltu_captive.csv",
                "evidence_strength": "tier_2",
                "summary": "Dataset PLTU captive menyebut PT Virtue Dragon Nickel Industry sebagai owner Delong Nickel Phase I power station di Sulawesi Tenggara.",
                "supports_function": "ya",
            },
            {
                "evidence_type": "industrial_waste_signal",
                "source_path": "data/processed/sulawesi_limbah_b3.csv",
                "evidence_strength": "tier_2",
                "summary": "Entri limbah B3 untuk VDNI Konawe menyebut pengolahan jutaan ton bijih nikel, menguatkan Morosi sebagai cluster hilirisasi yang butuh simpul logistik.",
                "supports_function": "ya",
            },
        ],
    },
    "NODE-SULTRA-KONAWE-OSS-001": {
        "status_validasi": "indikatif",
        "final_tier": "tier_2",
        "fungsi_tervalidasi": "pengapalan_produk_smelter",
        "jenis_fasilitas_final": "tidak_terklasifikasi",
        "operator_fasilitas": "",
        "catatan_final": "OSS terhubung kuat ke klaster Konawe melalui PLTU captive, tetapi bukti lokal repo masih belum cukup untuk memisahkan simpul logistiknya dari Morosi-VDNI.",
        "evidence": [
            {
                "evidence_type": "cluster_signal",
                "source_path": "data/raw/rev1_logistik/working/rev1_tahap_a_region_summary.csv",
                "evidence_strength": "tier_2",
                "summary_template": "{permit_nikel_total} izin nikel dan {pltu_units} unit PLTU captive ({pltu_capacity_mw:.0f} MW) memperlihatkan Konawe sebagai cluster industri hilirisasi aktif.",
                "supports_function": "ya",
            },
            {
                "evidence_type": "power_anchor",
                "source_path": "data/processed/sulawesi_pltu_captive.csv",
                "evidence_strength": "tier_2",
                "summary": "Dataset PLTU captive menyebut PT Obsidian Stainless Steel sebagai owner Delong Nickel Phase II power station di Sulawesi Tenggara.",
                "supports_function": "ya",
            },
        ],
    },
    "NODE-SULTRA-KOLAKA-POMALAA-ANTAM-001": {
        "status_validasi": "indikatif_kuat",
        "final_tier": "tier_2",
        "fungsi_tervalidasi": "pengapalan_produk_smelter",
        "jenis_fasilitas_final": "tidak_terklasifikasi",
        "operator_fasilitas": "",
        "catatan_final": "Pomalaa-ANTAM adalah cluster valid untuk narasi ekspansi industri. Namun repo lokal belum menyebut nama pelabuhan/jetty final yang bisa dinyatakan sebagai fasilitas logistik terkonfirmasi.",
        "evidence": [
            {
                "evidence_type": "cluster_signal",
                "source_path": "data/raw/rev1_logistik/working/rev1_tahap_a_region_summary.csv",
                "evidence_strength": "tier_2",
                "summary_template": "{permit_nikel_total} izin nikel dan {pltu_units} unit PLTU captive ({pltu_capacity_mw:.0f} MW) menunjukkan Pomalaa/Kolaka tetap relevan sebagai cluster hilirisasi nikel.",
                "supports_function": "ya",
            },
            {
                "evidence_type": "smelter_capacity",
                "source_path": "docs/CGS_DATA_ASSESSMENT.md",
                "evidence_strength": "tier_1",
                "summary": "Dokumen assessment CGS menyebut eksplisit ANTAM Pomalaa RKEF sebagai smelter nikel dengan kapasitas input dan output ferronickel.",
                "supports_function": "ya",
            },
            {
                "evidence_type": "power_anchor",
                "source_path": "data/processed/sulawesi_pltu_captive.csv",
                "evidence_strength": "tier_2",
                "summary": "Dataset PLTU captive menyebut Pomalaa Nickel power station milik PT Aneka Tambang Tbk, memperkuat operasi industri nikel di Pomalaa.",
                "supports_function": "ya",
            },
        ],
    },
    "NODE-SULSEL-LUTIM-SOROWAKO-VALE-001": {
        "status_validasi": "lead_lemah",
        "final_tier": "tier_3",
        "fungsi_tervalidasi": "pasokan_bahan_baku",
        "jenis_fasilitas_final": "tidak_terklasifikasi",
        "operator_fasilitas": "",
        "catatan_final": "Luwu Timur tetap masuk karena sabuk nikel penting, tetapi repo lokal belum memberi bukti cukup untuk menyimpulkan simpul logistik pesisir yang jelas.",
        "evidence": [
            {
                "evidence_type": "permit_signal",
                "source_path": "data/raw/rev1_logistik/working/rev1_tahap_a_region_summary.csv",
                "evidence_strength": "tier_3",
                "summary_template": "{permit_nikel_total} izin nikel pada {unique_permit_companies} entitas mengonfirmasi Luwu Timur sebagai sabuk nikel, meski sinyal logistik khusus belum muncul.",
                "supports_function": "indikatif",
            },
            {
                "evidence_type": "actor_anchor",
                "source_path": "docs/page8_aktor_oligarki_mapping.md",
                "evidence_strength": "tier_3",
                "summary": "Repo menempatkan Vale/Sorowako sebagai aktor penting dalam lanskap nikel Sulawesi Selatan.",
                "supports_function": "indikatif",
            },
            {
                "evidence_type": "conflict_anchor",
                "source_path": "docs/DATASET_SUMMARY_KONFLIK_TAMBANG_SULAWESI.md",
                "evidence_strength": "tier_3",
                "summary": "Ringkasan konflik tambang menegaskan kehadiran panjang PT Vale Indonesia di Luwu Timur, tetapi belum menjawab nama fasilitas logistik yang melayaninya.",
                "supports_function": "indikatif",
            },
        ],
    },
}


SMELTER_VALIDATION_ROWS = [
    {
        "validation_id": "SMELTER-SULTENG-MOROWALI-BAHODOPI-001",
        "nama_perusahaan": "PT Bahodopi Nickel Smelting Indonesia",
        "nama_fasilitas": "Bahodopi Nickel Smelting Indonesia",
        "provinsi": "Sulawesi Tengah",
        "kabupaten": "Morowali",
        "status_operasional": "unknown",
        "produk_smelter": "nickel processing",
        "klasifikasi_nikel": "ya",
        "dasar_klasifikasi": "Nama fasilitas dan alamat Bahodopi dikenali pada file matching repo untuk cluster Morowali.",
        "sumber_klasifikasi": "tools/scrapling/update_matching_approved.py; tools/scrapling/validate_cgs_matching.py",
        "confidence": "sedang",
        "catatan": "Masuk sebagai smelter nikel, tetapi status operasional final masih butuh verifikasi eksternal.",
        "tanggal_update": TODAY,
    },
    {
        "validation_id": "SMELTER-SULTENG-MORUT-GNI-001",
        "nama_perusahaan": "PT Gunbuster Nickel Industry",
        "nama_fasilitas": "Gunbuster Nickel Industry (GNI)",
        "provinsi": "Sulawesi Tengah",
        "kabupaten": "Morowali Utara",
        "status_operasional": "operating",
        "produk_smelter": "nickel processing / ferronickel chain",
        "klasifikasi_nikel": "ya",
        "dasar_klasifikasi": "Dataset PLTU captive dan file matching repo sama-sama menautkan GNI dengan klaster nikel Petasia.",
        "sumber_klasifikasi": "data/processed/sulawesi_pltu_captive.csv; tools/scrapling/validate_cgs_matching.py",
        "confidence": "tinggi",
        "catatan": "Validasi lokal kuat untuk klasifikasi nikel.",
        "tanggal_update": TODAY,
    },
    {
        "validation_id": "SMELTER-SULTRA-KONAWE-VDNI-001",
        "nama_perusahaan": "PT Virtue Dragon Nickel Industry",
        "nama_fasilitas": "Virtue Dragon Nickel Industry (VDNI)",
        "provinsi": "Sulawesi Tenggara",
        "kabupaten": "Konawe",
        "status_operasional": "operating",
        "produk_smelter": "nickel pig iron / stainless steel chain",
        "klasifikasi_nikel": "ya",
        "dasar_klasifikasi": "Owner PLTU captive dan catatan limbah B3 repo menempatkan VDNI sebagai inti hilirisasi nikel di Konawe.",
        "sumber_klasifikasi": "data/processed/sulawesi_pltu_captive.csv; data/processed/sulawesi_limbah_b3.csv",
        "confidence": "tinggi",
        "catatan": "Validasi lokal kuat untuk klasifikasi nikel.",
        "tanggal_update": TODAY,
    },
    {
        "validation_id": "SMELTER-SULTRA-KONAWE-OSS-001",
        "nama_perusahaan": "PT Obsidian Stainless Steel",
        "nama_fasilitas": "Obsidian Stainless Steel (OSS)",
        "provinsi": "Sulawesi Tenggara",
        "kabupaten": "Konawe",
        "status_operasional": "operating",
        "produk_smelter": "stainless steel / nickel processing",
        "klasifikasi_nikel": "ya",
        "dasar_klasifikasi": "Dataset PLTU captive menyebut owner OSS secara eksplisit pada klaster smelter Konawe.",
        "sumber_klasifikasi": "data/processed/sulawesi_pltu_captive.csv",
        "confidence": "sedang",
        "catatan": "Masih perlu sumber kedua agar pemisahan OSS dari cluster Konawe lain lebih solid.",
        "tanggal_update": TODAY,
    },
    {
        "validation_id": "SMELTER-SULTRA-KOLAKA-ANTAM-001",
        "nama_perusahaan": "PT Aneka Tambang Tbk",
        "nama_fasilitas": "ANTAM Pomalaa RKEF",
        "provinsi": "Sulawesi Tenggara",
        "kabupaten": "Kolaka",
        "status_operasional": "operating",
        "produk_smelter": "ferronickel",
        "klasifikasi_nikel": "ya",
        "dasar_klasifikasi": "Assessment CGS menyebut eksplisit ANTAM Pomalaa RKEF sebagai smelter nikel/ferronickel.",
        "sumber_klasifikasi": "docs/CGS_DATA_ASSESSMENT.md; data/processed/sulawesi_pltu_captive.csv",
        "confidence": "tinggi",
        "catatan": "Anchor terkuat untuk validasi smelter nikel di Pomalaa.",
        "tanggal_update": TODAY,
    },
]


OSINT_ROUND_1_ROWS = [
    {
        "logistics_id": "NODE-SULTENG-MOROWALI-IMIP-001",
        "cluster_id": "NODE-SULTENG-MOROWALI-IMIP",
        "osint_round": 1,
        "external_signal_status": "hit_jelas",
        "explicit_logistics_name": "",
        "explicit_logistics_type": "seaport",
        "primary_source_label": "WIRED - Workers Are Dying in the EV Industry's 'Tainted' City (2023)",
        "source_ref": "wired.com/story/workers-are-dying-in-the-ev-industrys-tainted-city",
        "external_evidence_summary": "Laporan WIRED menyebut IMIP di Labota/Bahodopi sebagai kompleks industri 3.000 hektare dengan airport dan seaport milik sendiri.",
        "implication": "Node IMIP naik dari sekadar inferensi internal menjadi simpul pesisir yang juga disebut secara eksplisit di sumber publik, meski nama pelabuhannya masih tidak disebut.",
    },
    {
        "logistics_id": "NODE-SULTENG-MOROWALI-IMIP-001",
        "cluster_id": "NODE-SULTENG-MOROWALI-IMIP",
        "osint_round": 1,
        "external_signal_status": "hit_pendukung",
        "explicit_logistics_name": "",
        "explicit_logistics_type": "coastal_industrial_complex",
        "primary_source_label": "arXiv - Causal Attribution of Coastal Water Clarity Degradation to Nickel Processing Expansion at IMIP (2026)",
        "source_ref": "arxiv.org/abs/2603.07331",
        "external_evidence_summary": "Makalah 2026 menyebut IMIP sebagai kompleks pengolahan nikel terintegrasi terbesar di pesisir Sulawesi Tengah.",
        "implication": "Memperkuat bahwa node IMIP memang relevan untuk narasi infrastruktur pesisir dan dampak maritim.",
    },
    {
        "logistics_id": "NODE-SULTENG-MORUT-PETASIA-GNI-001",
        "cluster_id": "NODE-SULTENG-MORUT-PETASIA-GNI",
        "osint_round": 1,
        "external_signal_status": "hit_operasional",
        "explicit_logistics_name": "",
        "explicit_logistics_type": "",
        "primary_source_label": "WIRED - Workers Are Dying in the EV Industry's 'Tainted' City (2023)",
        "source_ref": "wired.com/story/workers-are-dying-in-the-ev-industrys-tainted-city",
        "external_evidence_summary": "WIRED menyebut ledakan di smelter PT Gunbuster Nickel Industry pada 22 Desember 2022 dan menempatkan ekspansi industri ini dalam konteks Morowali Utara.",
        "implication": "Operasi smelter GNI tervalidasi oleh sumber publik, tetapi pencarian cepat belum memunculkan nama pelabuhan, jetty, atau terminal khususnya.",
    },
    {
        "logistics_id": "NODE-SULTRA-KONAWE-MOROSI-VDNI-001",
        "cluster_id": "NODE-SULTRA-KONAWE-MOROSI-VDNI",
        "osint_round": 1,
        "external_signal_status": "belum_ada_hit_logistik",
        "explicit_logistics_name": "",
        "explicit_logistics_type": "",
        "primary_source_label": "",
        "source_ref": "",
        "external_evidence_summary": "Pencarian publik cepat untuk VDNI/Morosi belum memunculkan sumber yang menyebut nama pelabuhan, jetty, atau terminal khusus secara eksplisit.",
        "implication": "Node tetap kuat dari data internal repo, tetapi butuh dokumen AMDAL, izin terminal khusus, atau berita lokal yang lebih spesifik.",
    },
    {
        "logistics_id": "NODE-SULTRA-KOLAKA-POMALAA-ANTAM-001",
        "cluster_id": "NODE-SULTRA-KOLAKA-POMALAA-ANTAM",
        "osint_round": 1,
        "external_signal_status": "belum_ada_hit_logistik",
        "explicit_logistics_name": "",
        "explicit_logistics_type": "",
        "primary_source_label": "",
        "source_ref": "",
        "external_evidence_summary": "Pencarian publik cepat untuk ANTAM Pomalaa belum memunculkan nama pelabuhan/jetty final, walau cluster smelter nikel dan ferronickel sangat kuat.",
        "implication": "Pomalaa valid sebagai node industri nikel, tetapi bukti logistik spesifik masih perlu dokumen eksternal tambahan.",
    },
]


OSINT_ROUND_2_ROWS = [
    {
        "logistics_id": "NODE-SULTENG-MOROWALI-IMIP-001",
        "cluster_id": "NODE-SULTENG-MOROWALI-IMIP",
        "osint_round": 2,
        "external_signal_status": "hit_jelas",
        "explicit_logistics_name": "",
        "explicit_logistics_type": "seaport",
        "primary_source_label": "Morowali Industrial Park overview (public source)",
        "source_ref": "wikipedia.org/wiki/Morowali_Industrial_Park",
        "external_evidence_summary": "Deskripsi publik IMIP menyebut kawasan Bahodopi dilayani oleh seaport, airport, dan PLTU batubara skala besar.",
        "implication": "Ini cukup untuk mengunci IMIP sebagai node pesisir/logistik nyata, walau nama pelabuhan spesifiknya masih belum diperoleh.",
    },
    {
        "logistics_id": "NODE-SULTRA-KONAWE-MOROSI-VDNI-001",
        "cluster_id": "NODE-SULTRA-KONAWE-MOROSI-VDNI",
        "osint_round": 2,
        "external_signal_status": "hit_provincial_channel",
        "explicit_logistics_name": "Kendari New Port",
        "explicit_logistics_type": "international_container_port",
        "primary_source_label": "Kendari city economy/transport overview (public source)",
        "source_ref": "wikipedia.org/wiki/Kendari",
        "external_evidence_summary": "Deskripsi publik Kendari menyebut kawasan industri Konawe memproduksi baterai/nikel dan arus pengapalan datang melalui Kendari New Port yang berfungsi sebagai pelabuhan internasional ekspor-impor regional.",
        "implication": "Belum membuktikan jetty VDNI secara langsung, tetapi cukup untuk mengunci kanal ekspor provinsi-level bagi cluster Morosi/Konawe.",
    },
    {
        "logistics_id": "NODE-SULTRA-KONAWE-OSS-001",
        "cluster_id": "NODE-SULTRA-KONAWE-OSS",
        "osint_round": 2,
        "external_signal_status": "hit_provincial_channel",
        "explicit_logistics_name": "Kendari New Port",
        "explicit_logistics_type": "international_container_port",
        "primary_source_label": "Kendari city economy/transport overview (public source)",
        "source_ref": "wikipedia.org/wiki/Kendari",
        "external_evidence_summary": "Sumber publik yang sama menempatkan kawasan industri Konawe dan Kendari New Port dalam satu arsitektur logistik ekspor regional.",
        "implication": "Ini cukup sebagai dukungan kanal ekspor provinsi-level untuk OSS, meski belum memisahkan fasilitas sandar OSS dari cluster Konawe lain.",
    },
]


EXPORT_CHANNEL_CONFIG = [
    {
        "cluster_id": "NODE-SULTENG-MOROWALI-IMIP",
        "logistics_id": "NODE-SULTENG-MOROWALI-IMIP-001",
        "province": "Sulawesi Tengah",
        "expected_port": "PANTOLOAN",
        "signal_mode": "negative_support",
        "target_products": ["nikel", "nickel", "ferro", "stainless"],
        "interpretation": "Dataset ekspor repo tidak menunjukkan PantoLoan sebagai kanal utama ekspor nikel/ferronikel. Ini konsisten dengan kebutuhan mencari simpul pesisir khusus di IMIP sendiri, bukan bergantung pada pelabuhan umum provinsi.",
    },
    {
        "cluster_id": "NODE-SULTRA-KONAWE-MOROSI-VDNI",
        "logistics_id": "NODE-SULTRA-KONAWE-MOROSI-VDNI-001",
        "province": "Sulawesi Tenggara",
        "expected_port": "KENDARI",
        "signal_mode": "positive_support",
        "target_products": ["nikel", "nickel", "ferro", "stainless"],
        "interpretation": "Dataset ekspor repo menunjukkan Pelabuhan Kendari sebagai kanal ekspor penting untuk ferronickel, ferro alloy nickel, dan produk semi-finished stainless steel dari Sulawesi Tenggara.",
    },
    {
        "cluster_id": "NODE-SULTRA-KONAWE-OSS",
        "logistics_id": "NODE-SULTRA-KONAWE-OSS-001",
        "province": "Sulawesi Tenggara",
        "expected_port": "KENDARI",
        "signal_mode": "positive_support",
        "target_products": ["nikel", "nickel", "ferro", "stainless"],
        "interpretation": "Kanal ekspor nikel/ferronikel Sultra pada dataset repo berkonsentrasi di Pelabuhan Kendari, sehingga ini layak dipakai sebagai dukungan provinsi-level untuk cluster Konawe.",
    },
    {
        "cluster_id": "NODE-SULTRA-KOLAKA-POMALAA-ANTAM",
        "logistics_id": "NODE-SULTRA-KOLAKA-POMALAA-ANTAM-001",
        "province": "Sulawesi Tenggara",
        "expected_port": "KENDARI",
        "signal_mode": "positive_support",
        "target_products": ["nikel", "nickel", "ferro", "stainless"],
        "interpretation": "Pelabuhan Kendari muncul sebagai kanal ekspor ferronickel dan alloy nickel pada data repo, sehingga dapat dipakai sebagai dukungan ekspor tingkat provinsi untuk Pomalaa/ANTAM.",
    },
]


BULK_CLUSTER_CONFIGS = [
    {
        "cluster_id": "NODE-SULTENG-MOROWALI-IMIP",
        "node_label": "Simpul logistik pesisir IMIP-Bahodopi",
        "permit_tokens": ["KAB. MOROWALI"],
        "permit_exclude_tokens": ["KAB. MOROWALI UTARA"],
        "address_tokens": ["GEDUNG IMIP", "BAHODOPI", "LABOTA", "DAMPALA"],
        "pltu_tokens": ["MOROWALI", "LABOTA", "BAHODOPI", "SULAWESI MINING"],
    },
    {
        "cluster_id": "NODE-SULTENG-MORUT-PETASIA-GNI",
        "node_label": "Simpul logistik pesisir Petasia-GNI",
        "permit_tokens": ["KAB. MOROWALI UTARA"],
        "permit_exclude_tokens": [],
        "address_tokens": ["PETASIA", "KOLONODALE", "TOMPIRA", "KOROLAKI"],
        "pltu_tokens": ["PETASIA", "GUNBUSTER", "DELONG NICKEL"],
    },
    {
        "cluster_id": "NODE-SULTRA-KONAWE-MOROSI-VDNI",
        "node_label": "Simpul logistik Morosi-VDNI",
        "permit_tokens": ["KAB. KONAWE", "KAB. KONAWE SELATAN"],
        "permit_exclude_tokens": ["KAB. KONAWE UTARA"],
        "address_tokens": ["MOROSI", "VIRTU DRAGON", "VIRTUE DRAGON", "VDNI"],
        "pltu_tokens": ["VDNI", "VIRTUE DRAGON", "MOROSI", "DELONG NICKEL PHASE I"],
    },
    {
        "cluster_id": "NODE-SULTRA-KONAWE-OSS",
        "node_label": "Simpul logistik Konawe-OSS",
        "permit_tokens": ["KAB. KONAWE"],
        "permit_exclude_tokens": ["KAB. KONAWE UTARA"],
        "address_tokens": ["KONAWE"],
        "pltu_tokens": ["OBSIDIAN", "OSS", "DELONG NICKEL PHASE II"],
    },
    {
        "cluster_id": "NODE-SULTRA-KOLAKA-POMALAA-ANTAM",
        "node_label": "Simpul logistik Pomalaa-ANTAM",
        "permit_tokens": ["KAB. KOLAKA"],
        "permit_exclude_tokens": ["KAB. KOLAKA UTARA", "KAB. KOLAKA TIMUR"],
        "address_tokens": ["POMALAA", "KOLAKA-POMALAA", "DAWI-DAWI", "TONGGONI", "BAULA"],
        "pltu_tokens": ["POMALAA", "ANTAM", "ANEKA TAMBANG"],
    },
    {
        "cluster_id": "NODE-SULSEL-LUTIM-SOROWAKO-VALE",
        "node_label": "Simpul logistik Sorowako-Luwu Timur",
        "permit_tokens": ["KAB. LUWU TIMUR"],
        "permit_exclude_tokens": [],
        "address_tokens": ["SOROWAKO", "MALILI", "LUWU TIMUR", "PONGKERU"],
        "pltu_tokens": ["VALE", "SOROWAKO", "MALILI"],
    },
]


def ensure_stage_a_outputs() -> None:
    required_paths = [
        WORKING_DIR / "sulawesi_port_logistics.csv",
        WORKING_DIR / "rev1_tahap_a_region_summary.csv",
    ]
    missing = [str(path) for path in required_paths if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Tahap A belum lengkap. File hilang: {missing}")


def write_dataframe(df: pd.DataFrame, path: Path) -> None:
    df.to_csv(path, index=False, encoding="utf-8-sig")


def load_stage_a_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    shortlist_df = pd.read_csv(WORKING_DIR / "sulawesi_port_logistics.csv")
    region_df = pd.read_csv(WORKING_DIR / "rev1_tahap_a_region_summary.csv")
    return shortlist_df, region_df


def load_export_data() -> pd.DataFrame:
    return pd.read_csv(PROCESSED_DIR / "sulawesi_ekspor_detail_2020_2026.csv")


def load_esdm_data() -> pd.DataFrame:
    return pd.read_csv(PROCESSED_DIR / "sulawesi_esdm_nikel.csv")


def _mask_from_tokens(series: pd.Series, include_tokens: list[str], exclude_tokens: list[str] | None = None) -> pd.Series:
    values = series.fillna("").astype(str).str.upper()
    mask = values.apply(lambda value: any(token in value for token in include_tokens))
    for token in exclude_tokens or []:
        mask = mask & ~values.str.contains(token, regex=False)
    return mask


def build_evidence_matrix(region_df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict] = []
    region_lookup = region_df.set_index("cluster_id").to_dict(orient="index")

    for logistics_id, config in NODE_EVIDENCE_CONFIG.items():
        cluster_id = logistics_id.replace("-001", "")
        region = region_lookup[cluster_id]
        for idx, evidence in enumerate(config["evidence"], start=1):
            summary = evidence.get("summary")
            if not summary:
                summary = evidence["summary_template"].format(**region)

            rows.append(
                {
                    "logistics_id": logistics_id,
                    "cluster_id": cluster_id,
                    "anchor_entity": region["anchor_entity"],
                    "kabupaten": region["kabupaten"],
                    "provinsi": region["provinsi"],
                    "status_validasi": config["status_validasi"],
                    "evidence_rank": idx,
                    "evidence_type": evidence["evidence_type"],
                    "source_path": evidence["source_path"],
                    "evidence_strength": evidence["evidence_strength"],
                    "supports_function": evidence["supports_function"],
                    "inferred_logistics_function": config["fungsi_tervalidasi"],
                    "evidence_summary": summary,
                    "verdict_note": config["catatan_final"],
                }
            )

    return pd.DataFrame(rows)


def build_validation_summary(region_df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict] = []
    region_lookup = region_df.set_index("cluster_id").to_dict(orient="index")

    for logistics_id, config in NODE_EVIDENCE_CONFIG.items():
        cluster_id = logistics_id.replace("-001", "")
        region = region_lookup[cluster_id]
        rows.append(
            {
                "logistics_id": logistics_id,
                "cluster_id": cluster_id,
                "anchor_entity": region["anchor_entity"],
                "kabupaten": region["kabupaten"],
                "provinsi": region["provinsi"],
                "status_validasi": config["status_validasi"],
                "tier_final": config["final_tier"],
                "fungsi_tervalidasi": config["fungsi_tervalidasi"],
                "permit_nikel_total": region["permit_nikel_total"],
                "pltu_units": region["pltu_units"],
                "pltu_capacity_mw": region["pltu_capacity_mw"],
                "top_permit_companies": region["top_permit_companies"],
                "top_pltu_owners": region["top_pltu_owners"],
                "kesimpulan": config["catatan_final"],
            }
        )
    return pd.DataFrame(rows)


def apply_stage_b_to_shortlist(shortlist_df: pd.DataFrame) -> pd.DataFrame:
    updated = shortlist_df.copy()
    for column in [
        "tier_bukti",
        "fungsi_fasilitas",
        "jenis_fasilitas",
        "operator_fasilitas",
        "catatan_verifikasi",
    ]:
        updated[column] = updated[column].fillna("").astype(str)
    for logistics_id, config in NODE_EVIDENCE_CONFIG.items():
        mask = updated["logistics_id"] == logistics_id
        updated.loc[mask, "tier_bukti"] = config["final_tier"]
        updated.loc[mask, "fungsi_fasilitas"] = config["fungsi_tervalidasi"]
        updated.loc[mask, "jenis_fasilitas"] = config["jenis_fasilitas_final"]
        updated.loc[mask, "operator_fasilitas"] = config["operator_fasilitas"]
        updated.loc[mask, "catatan_verifikasi"] = (
            "Tahap B: "
            + config["status_validasi"]
            + ". "
            + config["catatan_final"]
        )
    return updated


def build_gap_register() -> pd.DataFrame:
    rows = []
    for logistics_id, config in NODE_EVIDENCE_CONFIG.items():
        rows.append(
            {
                "logistics_id": logistics_id,
                "status_validasi": config["status_validasi"],
                "gap_type": "nama_fasilitas_logistik_final",
                "gap_detail": "Repo lokal belum menyimpan nama terminal khusus / jetty / dermaga final yang bisa langsung dipakai sebagai klaim utama.",
                "priority_next_step": "Cari sumber AMDAL, izin terminal khusus, atau geoportal yang menyebut nama fasilitas secara eksplisit.",
            }
        )
    return pd.DataFrame(rows)


def build_osint_round_1() -> pd.DataFrame:
    return pd.DataFrame(OSINT_ROUND_1_ROWS)


def build_osint_round_2() -> pd.DataFrame:
    return pd.DataFrame(OSINT_ROUND_2_ROWS)


def build_export_support(export_df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict] = []
    export_df = export_df.copy()
    export_df["deskripsi_norm"] = export_df["deskripsi"].fillna("").astype(str).str.lower()
    export_df["pelabuhan_norm"] = export_df["pelabuhan"].fillna("").astype(str).str.upper()
    export_df["nilai_usd_num"] = pd.to_numeric(export_df["nilai_usd"], errors="coerce").fillna(0.0)

    for config in EXPORT_CHANNEL_CONFIG:
        mask_products = export_df["deskripsi_norm"].apply(
            lambda value: any(token in value for token in config["target_products"])
        )
        product_df = export_df.loc[mask_products].copy()
        port_df = product_df.loc[product_df["pelabuhan_norm"] == config["expected_port"]].copy()

        rows.append(
            {
                "cluster_id": config["cluster_id"],
                "logistics_id": config["logistics_id"],
                "expected_port": config["expected_port"],
                "signal_mode": config["signal_mode"],
                "matched_rows": int(len(port_df)),
                "matched_value_usd": float(port_df["nilai_usd_num"].sum()),
                "top_products": " | ".join(
                    port_df.groupby("deskripsi")["nilai_usd_num"]
                    .sum()
                    .sort_values(ascending=False)
                    .head(5)
                    .index.astype(str)
                    .tolist()
                ),
                "interpretation": config["interpretation"],
                "source_dataset": "data/processed/sulawesi_ekspor_detail_2020_2026.csv",
            }
        )

    return pd.DataFrame(rows)


def build_dataset_readiness() -> pd.DataFrame:
    rows = [
        {
            "scope": "cluster_level_narrative",
            "status": "cukup",
            "reason": "IMIP sudah punya bukti seaport eksplisit; Sultra sudah punya kanal ekspor Kendari + data ekspor ferronickel/stainless dari repo; GNI tervalidasi sebagai cluster smelter aktif.",
            "safe_claim": "Ekspansi industri nikel di node prioritas ditopang simpul pesisir dan kanal ekspor regional yang nyata.",
        },
        {
            "scope": "facility_specific_claim",
            "status": "belum_cukup",
            "reason": "Nama jetty/terminal khusus/perusahaan spesifik belum berhasil didapat untuk semua node dari pencarian publik cepat.",
            "safe_claim": "Jangan klaim fasilitas sandar perusahaan tertentu kecuali untuk penyebutan umum seperti seaport IMIP atau kanal ekspor provinsi-level.",
        },
    ]
    return pd.DataFrame(rows)


def build_location_anchor_extract(esdm_df: pd.DataFrame) -> pd.DataFrame:
    configs = [
        {
            "cluster_id": "NODE-SULTENG-MOROWALI-IMIP",
            "tokens": ["LABOTA", "BAHODOPI", "GEDUNG IMIP"],
        },
        {
            "cluster_id": "NODE-SULTENG-MORUT-PETASIA-GNI",
            "tokens": ["PETASIA", "KOLONODALE"],
        },
        {
            "cluster_id": "NODE-SULTRA-KONAWE-MOROSI-VDNI",
            "tokens": ["MOROSI", "VIRTU DRAGON", "VIRTUE DRAGON"],
        },
        {
            "cluster_id": "NODE-SULTRA-KOLAKA-POMALAA-ANTAM",
            "tokens": ["POMALAA", "TONGGONI", "KOLAKA-POMALAA", "BAULA"],
        },
        {
            "cluster_id": "NODE-SULSEL-LUTIM-SOROWAKO-VALE",
            "tokens": ["MALILI", "SOROWAKO", "LUWU TIMUR"],
        },
    ]

    working = esdm_df.copy()
    working["alamat_norm"] = working["alamat"].fillna("").astype(str).str.upper()
    working["lokasi_norm"] = working["lokasi_izin"].fillna("").astype(str).str.upper()

    rows: list[dict] = []
    for config in configs:
        mask = working["alamat_norm"].apply(lambda value: any(token in value for token in config["tokens"]))
        mask = mask | working["lokasi_norm"].apply(lambda value: any(token in value for token in config["tokens"]))
        subset = working.loc[mask, ["nama_perusahaan", "provinsi", "alamat", "lokasi_izin", "komoditas"]].head(12)
        for _, record in subset.iterrows():
            rows.append(
                {
                    "cluster_id": config["cluster_id"],
                    "nama_perusahaan": record["nama_perusahaan"],
                    "provinsi": record["provinsi"],
                    "alamat": record["alamat"],
                    "lokasi_izin": record["lokasi_izin"],
                    "komoditas": record["komoditas"],
                }
            )
    return pd.DataFrame(rows)


def build_priority_company_roster(esdm_df: pd.DataFrame) -> pd.DataFrame:
    working = esdm_df.copy()
    working["alamat_norm"] = working["alamat"].fillna("").astype(str).str.upper()
    working["lokasi_norm"] = working["lokasi_izin"].fillna("").astype(str).str.upper()
    working["jumlah_izin_nikel_num"] = pd.to_numeric(working["jumlah_izin_nikel"], errors="coerce").fillna(0).astype(int)

    rows: list[dict] = []
    for config in BULK_CLUSTER_CONFIGS:
        permit_mask = _mask_from_tokens(
            working["lokasi_izin"],
            config["permit_tokens"],
            config["permit_exclude_tokens"],
        )
        address_mask = _mask_from_tokens(working["alamat"], config["address_tokens"])
        subset = working.loc[permit_mask | address_mask].copy()
        subset["is_core_nickel"] = subset["komoditas"].fillna("").astype(str).str.contains("Nikel", case=False, regex=False)

        for _, record in subset.iterrows():
            rows.append(
                {
                    "cluster_id": config["cluster_id"],
                    "node_label": config["node_label"],
                    "nama_perusahaan": record["nama_perusahaan"],
                    "provinsi": record["provinsi"],
                    "lokasi_izin": record["lokasi_izin"],
                    "alamat": record["alamat"],
                    "jumlah_izin": record["jumlah_izin"],
                    "jumlah_izin_nikel": record["jumlah_izin_nikel_num"],
                    "status_iup": record["status_iup"],
                    "komoditas": record["komoditas"],
                    "is_core_nickel": "ya" if bool(record["is_core_nickel"]) else "tidak",
                    "source_dataset": "data/processed/sulawesi_esdm_nikel.csv",
                }
            )

    df = pd.DataFrame(rows)
    return df.drop_duplicates(subset=["cluster_id", "nama_perusahaan", "lokasi_izin", "alamat"]).reset_index(drop=True)


def build_priority_permit_extract(izin_df: pd.DataFrame) -> pd.DataFrame:
    working = izin_df.copy()
    working["is_core_nickel"] = working["komoditas"].fillna("").astype(str).str.contains("Nikel", case=False, regex=False)

    rows: list[dict] = []
    for config in BULK_CLUSTER_CONFIGS:
        permit_mask = _mask_from_tokens(
            working["lokasi_perizinan"],
            config["permit_tokens"],
            config["permit_exclude_tokens"],
        )
        subset = working.loc[permit_mask].copy()
        for _, record in subset.iterrows():
            rows.append(
                {
                    "cluster_id": config["cluster_id"],
                    "node_label": config["node_label"],
                    "nama_badan_usaha": record["nama_badan_usaha"],
                    "nomor_izin": record["nomor_izin"],
                    "jenis_badan_usaha": record["jenis_badan_usaha"],
                    "komoditas": record["komoditas"],
                    "is_core_nickel": "ya" if bool(record["is_core_nickel"]) else "tidak",
                    "tahap_kegiatan": record["tahap_kegiatan"],
                    "provinsi": record["Provinsi"],
                    "lokasi_perizinan": record["lokasi_perizinan"],
                    "tahun": record["Tahun"],
                    "luas_ha": record["luas_ha"],
                    "source_dataset": "data/processed/sulawesi_izin_raw_details.csv",
                }
            )

    df = pd.DataFrame(rows)
    return df.drop_duplicates(subset=["cluster_id", "nama_badan_usaha", "nomor_izin"]).reset_index(drop=True)


def build_pltu_cluster_units(pltu_df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict] = []
    for config in BULK_CLUSTER_CONFIGS:
        mask = pd.Series(False, index=pltu_df.index)
        for column in ["Plant name", "Owner", "Parent", "Local area (taluk, county)", "Subnational unit (province, state)"]:
            mask = mask | _mask_from_tokens(pltu_df[column], config["pltu_tokens"])
        subset = pltu_df.loc[mask].copy()
        subset["capacity_num"] = pd.to_numeric(subset["Capacity (MW)"], errors="coerce").fillna(0.0)
        for _, record in subset.iterrows():
            rows.append(
                {
                    "cluster_id": config["cluster_id"],
                    "node_label": config["node_label"],
                    "plant_name": record["Plant name"],
                    "unit_name": record["Unit name"],
                    "owner": record["Owner"],
                    "parent": record["Parent"],
                    "capacity_mw": record["capacity_num"],
                    "status": record["Status"],
                    "start_year": record["Start year"],
                    "province": record["Subnational unit (province, state)"],
                    "local_area": record["Local area (taluk, county)"],
                    "captive_industry_use": record["Captive industry use"],
                    "source_dataset": "data/processed/sulawesi_pltu_captive.csv",
                }
            )

    df = pd.DataFrame(rows)
    return df.drop_duplicates(subset=["cluster_id", "plant_name", "unit_name", "owner"]).reset_index(drop=True)


def build_export_nickel_detail(export_df: pd.DataFrame) -> pd.DataFrame:
    working = export_df.copy()
    working["deskripsi_norm"] = working["deskripsi"].fillna("").astype(str).str.lower()
    mask = working["deskripsi_norm"].str.contains("nickel|nikel|ferro|stainless", case=False, regex=True)
    subset = working.loc[mask, ["deskripsi", "tahun", "negara_tujuan", "pelabuhan", "nilai_usd", "Sumber"]].copy()
    subset["cluster_support"] = subset["pelabuhan"].fillna("").astype(str).str.upper().map(
        {
            "KENDARI": "NODE-SULTRA-KONAWE-MOROSI-VDNI|NODE-SULTRA-KONAWE-OSS|NODE-SULTRA-KOLAKA-POMALAA-ANTAM",
            "MAKASSAR": "NODE-SULSEL-LUTIM-SOROWAKO-VALE",
            "PANTOLOAN": "NODE-SULTENG-MOROWALI-IMIP|NODE-SULTENG-MORUT-PETASIA-GNI",
            "SEMUA": "AGREGAT_SULAWESI",
        }
    ).fillna("")
    subset["source_dataset"] = "data/processed/sulawesi_ekspor_detail_2020_2026.csv"
    return subset.reset_index(drop=True)


def build_cluster_bulk_summary(
    company_df: pd.DataFrame,
    permit_df: pd.DataFrame,
    pltu_df: pd.DataFrame,
    export_df: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    for config in BULK_CLUSTER_CONFIGS:
        cluster_id = config["cluster_id"]
        company_subset = company_df[company_df["cluster_id"] == cluster_id]
        permit_subset = permit_df[permit_df["cluster_id"] == cluster_id]
        pltu_subset = pltu_df[pltu_df["cluster_id"] == cluster_id]
        export_subset = export_df[export_df["cluster_support"].fillna("").str.contains(cluster_id, regex=False)]
        rows.append(
            {
                "cluster_id": cluster_id,
                "node_label": config["node_label"],
                "company_rows": int(len(company_subset)),
                "core_nickel_company_rows": int((company_subset["is_core_nickel"] == "ya").sum()),
                "permit_rows": int(len(permit_subset)),
                "core_nickel_permit_rows": int((permit_subset["is_core_nickel"] == "ya").sum()),
                "pltu_unit_rows": int(len(pltu_subset)),
                "pltu_capacity_mw": float(pd.to_numeric(pltu_subset["capacity_mw"], errors="coerce").fillna(0.0).sum()),
                "export_rows": int(len(export_subset)),
                "export_value_usd": float(pd.to_numeric(export_subset["nilai_usd"], errors="coerce").fillna(0.0).sum()),
            }
        )
    return pd.DataFrame(rows)


def build_manifest(
    shortlist_count: int,
    validation_count: int,
    evidence_count: int,
    summary_count: int,
    gap_count: int,
    osint_count: int,
    osint_round_2_count: int,
    export_support_count: int,
    readiness_count: int,
    location_anchor_count: int,
    company_roster_count: int,
    permit_extract_count: int,
    pltu_extract_count: int,
    export_detail_count: int,
    bulk_summary_count: int,
) -> dict:
    return {
        "stage": "rev1_logistik_tahap_b",
        "generated_at": TODAY,
        "working_dir": str(WORKING_DIR.relative_to(BASE_DIR)).replace("\\", "/"),
        "summary": {
            "validated_logistics_nodes": shortlist_count,
            "validated_smelter_rows": validation_count,
            "evidence_rows": evidence_count,
            "validation_summary_rows": summary_count,
            "gap_rows": gap_count,
            "osint_round_1_rows": osint_count,
            "osint_round_2_rows": osint_round_2_count,
            "export_support_rows": export_support_count,
            "dataset_readiness_rows": readiness_count,
            "location_anchor_rows": location_anchor_count,
            "priority_company_roster_rows": company_roster_count,
            "priority_permit_rows": permit_extract_count,
            "pltu_cluster_unit_rows": pltu_extract_count,
            "export_nickel_detail_rows": export_detail_count,
            "cluster_bulk_summary_rows": bulk_summary_count,
        },
        "outputs": {
            "shortlist_logistics": "data/raw/rev1_logistik/working/sulawesi_port_logistics.csv",
            "smelter_validation": "data/raw/rev1_logistik/working/smelter_nikel_validation.csv",
            "evidence_matrix": "data/raw/rev1_logistik/working/rev1_tahap_b_evidence_matrix.csv",
            "validation_summary": "data/raw/rev1_logistik/working/rev1_tahap_b_validation_summary.csv",
            "gap_register": "data/raw/rev1_logistik/working/rev1_tahap_b_gap_register.csv",
            "osint_round_1": "data/raw/rev1_logistik/working/rev1_tahap_b_osint_round1.csv",
            "osint_round_2": "data/raw/rev1_logistik/working/rev1_tahap_b_osint_round2.csv",
            "export_support": "data/raw/rev1_logistik/working/rev1_tahap_b_export_port_support.csv",
            "dataset_readiness": "data/raw/rev1_logistik/working/rev1_tahap_b_dataset_readiness.csv",
            "location_anchor_extract": "data/raw/rev1_logistik/working/rev1_tahap_b_location_anchor_extract.csv",
            "priority_company_roster": "data/raw/rev1_logistik/working/rev1_tahap_b_priority_company_roster.csv",
            "priority_permit_extract": "data/raw/rev1_logistik/working/rev1_tahap_b_priority_permit_extract.csv",
            "pltu_cluster_units": "data/raw/rev1_logistik/working/rev1_tahap_b_pltu_cluster_units.csv",
            "export_nickel_detail": "data/raw/rev1_logistik/working/rev1_tahap_b_export_nickel_detail.csv",
            "cluster_bulk_summary": "data/raw/rev1_logistik/working/rev1_tahap_b_cluster_bulk_summary.csv",
        },
    }


def main() -> None:
    ensure_stage_a_outputs()
    shortlist_df, region_df = load_stage_a_data()
    export_df = load_export_data()
    esdm_df = load_esdm_data()
    izin_df = pd.read_csv(PROCESSED_DIR / "sulawesi_izin_raw_details.csv")
    pltu_source_df = pd.read_csv(PROCESSED_DIR / "sulawesi_pltu_captive.csv")

    updated_shortlist_df = apply_stage_b_to_shortlist(shortlist_df)
    smelter_df = pd.DataFrame(SMELTER_VALIDATION_ROWS)
    evidence_df = build_evidence_matrix(region_df)
    summary_df = build_validation_summary(region_df)
    gap_df = build_gap_register()
    osint_df = build_osint_round_1()
    osint_round_2_df = build_osint_round_2()
    export_support_df = build_export_support(export_df)
    readiness_df = build_dataset_readiness()
    location_anchor_df = build_location_anchor_extract(esdm_df)
    company_roster_df = build_priority_company_roster(esdm_df)
    permit_extract_df = build_priority_permit_extract(izin_df)
    pltu_cluster_df = build_pltu_cluster_units(pltu_source_df)
    export_detail_df = build_export_nickel_detail(export_df)
    bulk_summary_df = build_cluster_bulk_summary(
        company_roster_df,
        permit_extract_df,
        pltu_cluster_df,
        export_detail_df,
    )

    write_dataframe(updated_shortlist_df, WORKING_DIR / "sulawesi_port_logistics.csv")
    write_dataframe(smelter_df, WORKING_DIR / "smelter_nikel_validation.csv")
    write_dataframe(evidence_df, WORKING_DIR / "rev1_tahap_b_evidence_matrix.csv")
    write_dataframe(summary_df, WORKING_DIR / "rev1_tahap_b_validation_summary.csv")
    write_dataframe(gap_df, WORKING_DIR / "rev1_tahap_b_gap_register.csv")
    write_dataframe(osint_df, WORKING_DIR / "rev1_tahap_b_osint_round1.csv")
    write_dataframe(osint_round_2_df, WORKING_DIR / "rev1_tahap_b_osint_round2.csv")
    write_dataframe(export_support_df, WORKING_DIR / "rev1_tahap_b_export_port_support.csv")
    write_dataframe(readiness_df, WORKING_DIR / "rev1_tahap_b_dataset_readiness.csv")
    write_dataframe(location_anchor_df, WORKING_DIR / "rev1_tahap_b_location_anchor_extract.csv")
    write_dataframe(company_roster_df, WORKING_DIR / "rev1_tahap_b_priority_company_roster.csv")
    write_dataframe(permit_extract_df, WORKING_DIR / "rev1_tahap_b_priority_permit_extract.csv")
    write_dataframe(pltu_cluster_df, WORKING_DIR / "rev1_tahap_b_pltu_cluster_units.csv")
    write_dataframe(export_detail_df, WORKING_DIR / "rev1_tahap_b_export_nickel_detail.csv")
    write_dataframe(bulk_summary_df, WORKING_DIR / "rev1_tahap_b_cluster_bulk_summary.csv")

    manifest = build_manifest(
        len(updated_shortlist_df),
        len(smelter_df),
        len(evidence_df),
        len(summary_df),
        len(gap_df),
        len(osint_df),
        len(osint_round_2_df),
        len(export_support_df),
        len(readiness_df),
        len(location_anchor_df),
        len(company_roster_df),
        len(permit_extract_df),
        len(pltu_cluster_df),
        len(export_detail_df),
        len(bulk_summary_df),
    )
    (METADATA_DIR / "rev1_logistik_stage_b_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("rev1_logistik Tahap B completed.")
    print(f"Validated logistics nodes: {len(updated_shortlist_df)}")
    print(f"Validated smelter rows: {len(smelter_df)}")
    print(f"Evidence rows: {len(evidence_df)}")
    print(f"Gap rows: {len(gap_df)}")
    print(f"OSINT rows: {len(osint_df)}")
    print(f"OSINT round 2 rows: {len(osint_round_2_df)}")
    print(f"Export support rows: {len(export_support_df)}")
    print(f"Readiness rows: {len(readiness_df)}")
    print(f"Location anchor rows: {len(location_anchor_df)}")
    print(f"Priority company roster rows: {len(company_roster_df)}")
    print(f"Priority permit rows: {len(permit_extract_df)}")
    print(f"PLTU cluster unit rows: {len(pltu_cluster_df)}")
    print(f"Export nickel detail rows: {len(export_detail_df)}")
    print(f"Cluster bulk summary rows: {len(bulk_summary_df)}")


if __name__ == "__main__":
    main()
