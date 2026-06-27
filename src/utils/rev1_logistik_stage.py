from __future__ import annotations

from copy import deepcopy


TIER_BUKTI = {
    "tier_1": {
        "label": "Bukti langsung",
        "rule": "Sumber eksplisit menyebut nama fasilitas/proyek, fungsi, lokasi, dan kaitan dengan tambang/smelter/nikel.",
        "allowed_for_main_narrative": True,
        "allowed_language": ["terkait langsung", "digunakan untuk", "berfungsi sebagai"],
    },
    "tier_2": {
        "label": "Bukti tidak langsung kuat",
        "rule": "Hubungan tidak ditulis penuh, tetapi cocok di operator, lokasi, fungsi, dan didukung lebih dari satu sumber.",
        "allowed_for_main_narrative": True,
        "allowed_language": ["terindikasi terkait", "sangat mungkin menopang", "berkorelasi kuat dengan"],
    },
    "tier_3": {
        "label": "Indikasi awal",
        "rule": "Masih berupa lead OSINT atau referensi tunggal yang belum tervalidasi.",
        "allowed_for_main_narrative": False,
        "allowed_language": ["masih perlu verifikasi", "indikasi awal", "belum cukup untuk klaim utama"],
    },
}


SOURCE_PRIORITIES = [
    {"priority": 1, "source": "repo_existing", "label": "Dataset dan dokumen repo yang sudah ada", "purpose": "Baseline entitas smelter, izin, dan kawasan"},
    {"priority": 2, "source": "amdal_and_technical_docs", "label": "AMDAL, lampiran teknis, audit lingkungan, dokumen perusahaan", "purpose": "Bukti langsung fasilitas logistik"},
    {"priority": 3, "source": "esdm_cgs_gem", "label": "ESDM, CGS, GEM, dan sumber smelter yang sudah dipakai repo", "purpose": "Validasi entitas dan relasi industri"},
    {"priority": 4, "source": "bps_port_exports", "label": "BPS ekspor per pelabuhan", "purpose": "Validasi aktivitas logistik dan arus ekspor"},
    {"priority": 5, "source": "official_geospatial", "label": "Geoportal atau peta resmi", "purpose": "Verifikasi lokasi dan bentuk fasilitas"},
    {"priority": 6, "source": "news_and_osint", "label": "Berita, siaran pers, dan OSINT", "purpose": "Lead tambahan, bukan bukti tunggal utama"},
]


WILAYAH_PRIORITAS = [
    {"priority_tier": 1, "wilayah": "Morowali", "provinsi": "Sulawesi Tengah", "alasan": "Konsentrasi smelter dan kawasan industri tertinggi"},
    {"priority_tier": 1, "wilayah": "Morowali Utara", "provinsi": "Sulawesi Tengah", "alasan": "Terkait rantai pasok nikel dan pesisir industri"},
    {"priority_tier": 1, "wilayah": "Konawe", "provinsi": "Sulawesi Tenggara", "alasan": "Relevan untuk smelter, pelabuhan, dan suplai"},
    {"priority_tier": 1, "wilayah": "Konawe Utara", "provinsi": "Sulawesi Tenggara", "alasan": "Potensial kuat untuk simpul logistik pesisir"},
    {"priority_tier": 2, "wilayah": "Kolaka", "provinsi": "Sulawesi Tenggara", "alasan": "Pusat historis nikel dan ekspor"},
    {"priority_tier": 2, "wilayah": "Kolaka Timur", "provinsi": "Sulawesi Tenggara", "alasan": "Perlu cek kaitan ke tambang dan pengapalan"},
    {"priority_tier": 2, "wilayah": "Luwu Timur", "provinsi": "Sulawesi Selatan", "alasan": "Penting untuk pola logistik Sulawesi Selatan"},
]


DATASET_SCHEMAS = {
    "sulawesi_port_logistics": {
        "filename": "sulawesi_port_logistics.csv",
        "description": "Fasilitas logistik yang relevan dengan tambang, smelter, KEK, atau kawasan industri nikel di Sulawesi.",
        "required_minimum_fields": [
            "nama_fasilitas_logistik",
            "jenis_fasilitas",
            "kabupaten",
            "provinsi",
            "tier_bukti",
            "sumber_1",
        ],
        "enums": {
            "jenis_fasilitas": [
                "pelabuhan_umum",
                "terminal_khusus",
                "terminal_kepentingan_sendiri",
                "jetty",
                "dermaga_industri",
                "stockpile_port",
                "tidak_terklasifikasi",
            ],
            "fungsi_fasilitas": [
                "pengapalan_ore",
                "pengapalan_produk_smelter",
                "pasokan_bahan_baku",
                "logistik_kawasan_industri",
                "multi_fungsi",
                "tidak_jelas",
            ],
            "status_operasional": ["operating", "construction", "planned", "suspended", "unknown"],
            "terkait_KEK": ["ya", "tidak", "indikatif"],
            "indikasi_risiko_pasokan": ["tidak_ada", "indikatif", "butuh_verifikasi", "bukti_langsung"],
            "tier_bukti": list(TIER_BUKTI.keys()),
        },
        "columns": [
            {"name": "logistics_id", "type": "string", "required": True, "description": "ID unik internal, mis. PORT-SULTENG-MOROWALI-001"},
            {"name": "nama_fasilitas_logistik", "type": "string", "required": True, "description": "Nama pelabuhan, jetty, terminal, atau dermaga"},
            {"name": "nama_asli_sumber", "type": "string", "required": False, "description": "Nama mentah sesuai penulisan di sumber"},
            {"name": "jenis_fasilitas", "type": "string", "required": True, "description": "Klasifikasi jenis fasilitas logistik"},
            {"name": "fungsi_fasilitas", "type": "string", "required": True, "description": "Fungsi utama fasilitas"},
            {"name": "operator_fasilitas", "type": "string", "required": False, "description": "Pengelola/operator terminal atau pelabuhan"},
            {"name": "perusahaan_terkait", "type": "string", "required": False, "description": "Perusahaan tambang/smelter/kawasan terkait"},
            {"name": "smelter_terkait", "type": "string", "required": False, "description": "Nama smelter jika hubungan eksplisit atau kuat"},
            {"name": "tambang_terkait", "type": "string", "required": False, "description": "Nama entitas tambang jika ada"},
            {"name": "komoditas_terkait", "type": "string", "required": True, "description": "nikel, multi-komoditas, tidak_jelas, dll"},
            {"name": "kabupaten", "type": "string", "required": True, "description": "Kabupaten/kota lokasi"},
            {"name": "provinsi", "type": "string", "required": True, "description": "Provinsi lokasi"},
            {"name": "koordinat_lat", "type": "float", "required": False, "description": "Latitude jika tersedia"},
            {"name": "koordinat_lon", "type": "float", "required": False, "description": "Longitude jika tersedia"},
            {"name": "status_operasional", "type": "string", "required": True, "description": "Status operasional fasilitas"},
            {"name": "terkait_KEK", "type": "string", "required": True, "description": "ya, tidak, atau indikatif"},
            {"name": "nama_KEK_atau_kawasan", "type": "string", "required": False, "description": "Nama KEK/kawasan industri bila ada"},
            {"name": "indikasi_risiko_pasokan", "type": "string", "required": True, "description": "Status indikasi risiko pasokan"},
            {"name": "tier_bukti", "type": "string", "required": True, "description": "tier_1, tier_2, atau tier_3"},
            {"name": "sumber_1", "type": "string", "required": True, "description": "Sumber utama"},
            {"name": "sumber_2", "type": "string", "required": False, "description": "Sumber sekunder"},
            {"name": "catatan_verifikasi", "type": "string", "required": False, "description": "Catatan singkat verifikasi/manual judgement"},
            {"name": "tanggal_update", "type": "date", "required": True, "description": "Tanggal entri diperbarui"},
        ],
    },
    "sulawesi_rail_psn_tracking": {
        "filename": "sulawesi_rail_psn_tracking.csv",
        "description": "Pelacakan proyek rel, koridor transportasi, atau PSN yang relevan dengan smelter, tambang, KEK, atau kawasan industri nikel.",
        "required_minimum_fields": [
            "nama_proyek",
            "jenis_proyek",
            "provinsi",
            "status_proyek",
            "tier_bukti",
            "sumber_utama",
        ],
        "enums": {
            "jenis_proyek": ["rail", "road_corridor", "port_expansion", "psn_multi", "other"],
            "status_proyek": ["operating", "construction", "planned", "cancelled", "unknown"],
            "terkait_KEK_atau_kawasan_industri": ["ya", "tidak", "indikatif"],
            "relevansi_ke_nikel": ["tinggi", "sedang", "rendah", "tidak_relevan"],
            "tier_bukti": list(TIER_BUKTI.keys()),
        },
        "columns": [
            {"name": "project_id", "type": "string", "required": True, "description": "ID unik internal"},
            {"name": "nama_proyek", "type": "string", "required": True, "description": "Nama proyek transportasi/PSN"},
            {"name": "jenis_proyek", "type": "string", "required": True, "description": "Jenis proyek"},
            {"name": "lokasi_ringkas", "type": "string", "required": True, "description": "Ringkasan lokasi"},
            {"name": "kabupaten_terkait", "type": "string", "required": False, "description": "Kabupaten terkait"},
            {"name": "provinsi", "type": "string", "required": True, "description": "Provinsi utama"},
            {"name": "status_proyek", "type": "string", "required": True, "description": "Status proyek"},
            {"name": "tahun_mulai", "type": "string", "required": False, "description": "Tahun awal yang teridentifikasi"},
            {"name": "tahun_update_terakhir", "type": "string", "required": False, "description": "Tahun update terakhir dari sumber"},
            {"name": "terkait_KEK_atau_kawasan_industri", "type": "string", "required": True, "description": "ya, tidak, atau indikatif"},
            {"name": "entitas_terkait", "type": "string", "required": False, "description": "KEK, smelter, perusahaan, atau kawasan"},
            {"name": "relevansi_ke_nikel", "type": "string", "required": True, "description": "tinggi, sedang, rendah, atau tidak_relevan"},
            {"name": "tier_bukti", "type": "string", "required": True, "description": "tier_1, tier_2, atau tier_3"},
            {"name": "sumber_utama", "type": "string", "required": True, "description": "Sumber utama"},
            {"name": "sumber_pendukung", "type": "string", "required": False, "description": "Sumber tambahan"},
            {"name": "catatan", "type": "string", "required": False, "description": "Catatan evaluasi relevansi"},
            {"name": "tanggal_update", "type": "date", "required": True, "description": "Tanggal entri diperbarui"},
        ],
    },
    "smelter_nikel_validation": {
        "filename": "smelter_nikel_validation.csv",
        "description": "Validasi fasilitas yang dipakai dalam narasi Fase 3 agar benar-benar termasuk smelter atau fasilitas pengolahan nikel.",
        "required_minimum_fields": [
            "nama_perusahaan",
            "nama_fasilitas",
            "produk_smelter",
            "klasifikasi_nikel",
            "confidence",
            "sumber_klasifikasi",
        ],
        "enums": {
            "status_operasional": ["operating", "construction", "planned", "unknown"],
            "klasifikasi_nikel": ["ya", "tidak", "campuran", "belum_pasti"],
            "confidence": ["tinggi", "sedang", "rendah"],
        },
        "columns": [
            {"name": "validation_id", "type": "string", "required": True, "description": "ID unik internal"},
            {"name": "nama_perusahaan", "type": "string", "required": True, "description": "Nama entitas usaha"},
            {"name": "nama_fasilitas", "type": "string", "required": True, "description": "Nama pabrik/smelter"},
            {"name": "provinsi", "type": "string", "required": True, "description": "Provinsi"},
            {"name": "kabupaten", "type": "string", "required": False, "description": "Kabupaten/kota"},
            {"name": "status_operasional", "type": "string", "required": True, "description": "Status operasional"},
            {"name": "produk_smelter", "type": "string", "required": True, "description": "Produk utama"},
            {"name": "klasifikasi_nikel", "type": "string", "required": True, "description": "ya, tidak, campuran, atau belum_pasti"},
            {"name": "dasar_klasifikasi", "type": "string", "required": True, "description": "Dasar singkat kenapa diklasifikasi demikian"},
            {"name": "sumber_klasifikasi", "type": "string", "required": True, "description": "Sumber utama"},
            {"name": "confidence", "type": "string", "required": True, "description": "tinggi, sedang, atau rendah"},
            {"name": "catatan", "type": "string", "required": False, "description": "Catatan manual"},
            {"name": "tanggal_update", "type": "date", "required": True, "description": "Tanggal entri diperbarui"},
        ],
    },
}


def build_stage_a_payload() -> dict:
    return {
        "stage": "rev1_logistik_tahap_a",
        "datasets": deepcopy(DATASET_SCHEMAS),
        "tier_bukti": deepcopy(TIER_BUKTI),
        "source_priorities": deepcopy(SOURCE_PRIORITIES),
        "priority_regions": deepcopy(WILAYAH_PRIORITAS),
    }


def get_dataset_columns(dataset_key: str) -> list[str]:
    return [column["name"] for column in DATASET_SCHEMAS[dataset_key]["columns"]]
