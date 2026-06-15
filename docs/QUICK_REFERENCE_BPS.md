# 📄 QUICK REFERENCE CARD - BPS Download

> **Print this page and keep beside you while downloading**

---

## 🎯 PAD FORM TEMPLATE (Copy untuk setiap provinsi)

### URLs
```
Sulut:    https://sulut.bps.go.id/id/query-builder
Sulteng:  https://sulteng.bps.go.id/id/query-builder
Sulsel:   https://sulsel.bps.go.id/id/query-builder
Sultra:   https://sultra.bps.go.id/id/query-builder
Gorontalo: https://gorontalo.bps.go.id/id/query-builder
Sulbar:   https://sulbar.bps.go.id/id/query-builder
```

### Form Values (Same for all provinces)
```
┌──────────────────────┬─────────────────────────────┐
│ Field                │ Value                       │
├──────────────────────┼─────────────────────────────┤
│ Kategori Subjek      │ Keuangan Daerah             │
│ Subjek               │ Keuangan Pemerintah Daerah  │
│ Tabel                │ [Search: "realisasi"]       │
│                      │ Pick: Realisasi Pendapatan..│
│ Tahun                │ ☑ ALL 2016-2024            │
│ Turunan Tahun        │ Tahunan / (blank)           │
│ Karakteristik        │ Kabupaten/Kota              │
│ Judul Baris          │ Jenis Pendapatan            │
└──────────────────────┴─────────────────────────────┘
```

### Output Naming
```
pad_7100_sulawesi_utara_2016-2024.csv
pad_7200_sulawesi_tengah_2016-2024.csv
pad_7300_sulawesi_selatan_2016-2024.csv
pad_7400_sulawesi_tenggara_2016-2024.csv
pad_7500_gorontalo_2016-2024.csv
pad_7600_sulawesi_barat_2016-2024.csv
```

---

## 📊 EKSPOR FORM TEMPLATES

### URL (All downloads)
```
https://www.bps.go.id/id/exim
```

**⚠️ BATCH STRATEGY:** Karena batas maksimal field, download dibagi jadi batch

---

### Download A1: HS Priority 2016-2020 ⭐⭐⭐ MANDATORY
```
┌──────────────┬────────────────────────┐
│ Field        │ Value                  │
├──────────────┼────────────────────────┤
│ Pilih Data   │ ○ Ekspor               │
│ Agregasi     │ Menurut Kode HS        │
│ Tahun        │ ☑ 2016-2020 (5 years) │
│ Bulan        │ (blank)                │
│ Jenis HS     │ HS 2 Digit             │
│ Kode HS      │ 03,08,09,15,16,        │
│              │ 24,44,72,85,87 (10)    │
└──────────────┴────────────────────────┘

Output: ekspor_hs_prioritas_2016-2020.csv
```

### Download A2: HS Priority 2021-2024 ⭐⭐⭐ MANDATORY
```
┌──────────────┬────────────────────────┐
│ Field        │ Value                  │
├──────────────┼────────────────────────┤
│ Pilih Data   │ ○ Ekspor               │
│ Agregasi     │ Menurut Kode HS        │
│ Tahun        │ ☑ 2021-2024 (4 years) │
│ Bulan        │ (blank)                │
│ Jenis HS     │ HS 2 Digit             │
│ Kode HS      │ SAME 10 codes          │
└──────────────┴────────────────────────┘

Output: ekspor_hs_prioritas_2021-2024.csv
```

---

### Download B1: Pelabuhan 2016-2020 ⭐⭐
```
┌──────────────┬────────────────────────┐
│ Field        │ Value                  │
├──────────────┼────────────────────────┤
│ Pilih Data   │ ○ Ekspor               │
│ Agregasi     │ Menurut Pelabuhan      │
│ Tahun        │ ☑ 2016-2020 (5 years) │
│ Bulan        │ (blank)                │
│ Pelabuhan    │ ☑ Makassar            │
│              │ ☑ Bitung              │
│              │ ☑ Pantoloan           │
│              │ ☑ Kendari             │
│              │ ☑ Gorontalo           │
│              │ ☑ Mamuju (6 total)    │
└──────────────┴────────────────────────┘

Output: ekspor_pelabuhan_sulawesi_2016-2020.csv
```

### Download B2: Pelabuhan 2021-2024 ⭐⭐
```
Same fields, change Tahun to 2021-2024
Output: ekspor_pelabuhan_sulawesi_2021-2024.csv
```

---

### Download C1: Negara Asia 2016-2020 ⭐⭐
```
┌──────────────┬────────────────────────┐
│ Field        │ Value                  │
├──────────────┼────────────────────────┤
│ Pilih Data   │ ○ Ekspor               │
│ Agregasi     │ Menurut Negara         │
│ Tahun        │ ☑ 2016-2020 (5 years) │
│ Bulan        │ (blank)                │
│ Negara       │ China, Japan,          │
│              │ Singapore, India,      │
│              │ Malaysia, Thailand,    │
│              │ S.Korea, Taiwan,       │
│              │ Vietnam, Philippines   │
│              │ (10 total)             │
└──────────────┴────────────────────────┘

Output: ekspor_negara_asia_2016-2020.csv
```

### Download C2: Negara Asia 2021-2024 ⭐⭐
```
Same fields, change Tahun to 2021-2024
Output: ekspor_negara_asia_2021-2024.csv
```

---

### OPTIONAL: A3 & A4 (HS Secondary) ⭐
```
Repeat A1 & A2 format
Change Kode HS to: 01,02,04,07,10,21,27,39,40,64
Output: ekspor_hs_sekunder_2016-2020.csv
        ekspor_hs_sekunder_2021-2024.csv
```

---

## ⚡ TROUBLESHOOTING QUICK FIXES

| Problem | Solution |
|---------|----------|
| Form tidak muncul | Refresh (F5) + Clear cache |
| Tabel tidak muncul | Wait 1 min / Reduce years (max 5) |
| Browser hang | Reduce fields (max 10 HS codes) |
| Download corrupt | Re-download / Try Excel format |
| File 0 KB | Connection issue, retry |
| "Max field exceeded" | Too many selections, use batch |
| Kode HS can't be blank | MUST select specific codes (10 max) |

---

## 📁 FILE LOCATIONS

```
PAD files → tools\scrapling\bps_eksporpad\downloads\
Ekspor files → tools\bpsapi\output\ekspor\
```

---

## ✅ QUICK CHECKLIST

```
PAD (6 files):
☐ Sulut (7100)
☐ Sulteng (7200)
☐ Sulsel (7300)
☐ Sultra (7400)
☐ Gorontalo (7500)
☐ Sulbar (7600)

Ekspor MINIMUM (6 files):
☐ A1: HS Priority 2016-2020 ⭐⭐⭐
☐ A2: HS Priority 2021-2024 ⭐⭐⭐
☐ B1: Pelabuhan 2016-2020 ⭐⭐
☐ B2: Pelabuhan 2021-2024 ⭐⭐
☐ C1: Negara 2016-2020 ⭐⭐
☐ C2: Negara 2021-2024 ⭐⭐

Ekspor OPTIONAL (2 files):
☐ A3: HS Secondary 2016-2020 ⭐
☐ A4: HS Secondary 2021-2024 ⭐

Total Minimum: 12 files
Total Full: 14 files
```

---

## ⏱️ TIME TRACKING

```
Start: _____
PAD done: _____
Ekspor done: _____
End: _____

Total: _____ hours
```

---

*Keep this card visible while downloading*  
*Created: 9 Juni 2026*
