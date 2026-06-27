# 🔍 tools/deduplication — Toolkit Deduplikasi Data (Golden Standard 2026)

Folder ini berisi tiga skrip modular untuk menjalankan pipeline validasi dan pembersihan duplikat dataset di folder `data/processed/`.

---

## Urutan Eksekusi

### 1. `1_semantic_deduplicator_audit.py` — Audit Byte & Subset
```bash
python tools/deduplication/1_semantic_deduplicator_audit.py
```
- **Mode:** DRY-RUN (tidak mengubah apapun)
- **Cek:** SHA-256 hash identik + relasi subset 100% antar file
- **Output:** `data/audit_redundansi.json`

---

### 2. `2_entity_resolver_audit.py` — Audit Fuzzy Entitas
```bash
python tools/deduplication/2_entity_resolver_audit.py
```
- **Mode:** DRY-RUN (tidak mengubah apapun)
- **Cek:** Jaro-Winkler Similarity > 90% pada kolom nama perusahaan/entitas
- **Output:** Tambahan field `entity_resolution_candidates` di `data/audit_redundansi.json`

---

### 3. `3_execute_cleanup.py` — Eksekusi Fisik ⚠️
```bash
python tools/deduplication/3_execute_cleanup.py
```
- **Mode:** LIVE (perubahan permanen)
- **Tindakan:**
  - Merger baris entitas fuzzy di file master
  - Reroute `pd.read_csv()` di `pages/*.py` ke file master
  - Hapus file redundan dari `data/processed/`
- **Prasyarat:** Baca & setujui isi `data/audit_redundansi.json` terlebih dahulu

---

## ⚠️ Peringatan

> Jangan langsung menjalankan `3_execute_cleanup.py` tanpa terlebih dahulu:
> 1. Menjalankan Phase 1 & Phase 2 (audit)
> 2. Meninjau `data/audit_redundansi.json`
> 3. Memastikan Git commit terakhir sudah bersih sebagai backup

---

## Temuan Terakhir (Juni 2026)

| Jenis | File Redundan | Master File | Status |
|---|---|---|---|
| Subset (100%) | `sulawesi_ekspor_2022_2026.csv` | `nasional_ekspor_2022_2026.csv` | **DITOLAK** (Risiko Error UI) |
| Fuzzy Entity | `sulawesi_esdm_nikel.csv` — "STARGATE DUA..." | "STARGATE PASIFIC..." (92.9%) | **DITOLAK** (Valid Anak Perusahaan) |
