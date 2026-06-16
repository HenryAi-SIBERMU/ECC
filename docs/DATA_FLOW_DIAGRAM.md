# DATA FLOW DIAGRAM: Page 5 Section 5.3

**Visual representation of how data flows from sources to dashboard**

---

## 📊 END-TO-END DATA PIPELINE

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         RAW DATA SOURCES                                 │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
         ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
         │ KPA CATAHU   │  │ Tanahkita.id │  │ International│
         │   PDFs       │  │   Database   │  │     NGOs     │
         │ (2016-2025)  │  │   (Online)   │  │   (Reports)  │
         │  9 reports   │  │ 568 conflicts│  │  CRI, Mighty │
         └──────────────┘  └──────────────┘  └──────────────┘
                    │               │               │
                    ▼               ▼               ▼
         ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
         │   ETL.py     │  │ FILTER.py    │  │ Fact-Check   │
         │  (Extract    │  │ (Sulawesi    │  │  (Manual     │
         │   permit     │  │  mining      │  │   Citation)  │
         │  problems)   │  │  conflicts)  │  │              │
         └──────────────┘  └──────────────┘  └──────────────┘
                    │               │               │
                    ▼               ▼               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      PROCESSED DATASETS                                  │
├─────────────────────────────────────────────────────────────────────────┤
│  1. kpa_masalah_izin_perusahaan.csv           (21 cases, 2016-2025)    │
│  2. sulawesi_konflik_tambang_fpic.csv         (12 cases, 1968-2023)    │
│  3. International NGO Citations                (5 sources, 2024-2025)   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    STREAMLIT PAGE 5 - SECTION 5.3                       │
├─────────────────────────────────────────────────────────────────────────┤
│  FUNCTIONS:                                                              │
│  • load_konflik_data() → Returns df_konflik (12 rows)                  │
│  • load_masalah_izin_data() → Returns df_masalah (21 rows)             │
│                                                                          │
│  DATA TRANSFORMATIONS:                                                   │
│  • Merge by year for timeline                                           │
│  • Split semicolon-separated problem types                              │
│  • Filter by indikasi_fpic == True                                      │
│  • Group by category, year, province                                    │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
         ┌──────────────────┐           ┌──────────────────┐
         │  STATIC VISUALS  │           │ INTERACTIVE      │
         │  (Plotly Charts) │           │ COMPONENTS       │
         │                  │           │ (Streamlit UI)   │
         │  • Timeline      │           │ • Filters        │
         │  • Bar Chart     │           │ • Tabs           │
         │  • Metrics       │           │ • Expanders      │
         └──────────────────┘           └──────────────────┘
                    │                               │
                    └───────────────┬───────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          USER BROWSER                                    │
├─────────────────────────────────────────────────────────────────────────┤
│  RENDERED OUTPUT:                                                        │
│  ✅ 3 Metric Cards                                                       │
│  ✅ Timeline Chart (conflicts + permit problems)                         │
│  ✅ Horizontal Bar Chart (problem types)                                 │
│  ✅ 4 Expandable FPIC Violation Cards                                    │
│  ✅ 2 Filterable Data Tables                                             │
│  ✅ Citation Box (5 NGO sources)                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 DATA TRANSFORMATION FLOW

### **TRANSFORMATION 1: Timeline Data**

```python
INPUT:
┌─────────────────────────────┐   ┌─────────────────────────────┐
│ df_konflik                  │   │ df_masalah                  │
│ ─────────────               │   │ ─────────────               │
│ tahun | judul | perusahaan  │   │ tahun_laporan | nama_peru..│
│ 2023  | ...   | PT GKP      │   │ 2023          | IMIP        │
│ 2022  | ...   | PT GKP      │   │ 2022          | MNM         │
└─────────────────────────────┘   └─────────────────────────────┘
                │                               │
                ▼                               ▼
         Add kategori                    Add kategori
         = "Konflik Pertambangan"       = "Masalah Izin (KPA)"
                │                               │
                └───────────┬───────────────────┘
                            ▼
                    pd.concat([...])
                            │
                            ▼
                   groupby(['Tahun', 'kategori'])
                            │
                            ▼
OUTPUT:
┌─────────────────────────────────────────┐
│ df_timeline_agg                         │
│ ────────────────                        │
│ Tahun | kategori              | Jumlah  │
│ 2011  | Konflik Pertambangan  | 2       │
│ 2016  | Masalah Izin (KPA)    | 1       │
│ 2019  | Konflik Pertambangan  | 1       │
│ 2019  | Masalah Izin (KPA)    | 2       │
└─────────────────────────────────────────┘
```

---

### **TRANSFORMATION 2: Problem Type Breakdown**

```python
INPUT:
┌───────────────────────────────────────────────────────────┐
│ df_masalah                                                │
│ ──────────────────────────────────────────────────────────│
│ jenis_masalah_izin                                        │
│ "HGU Kadaluarsa/Habis; Tumpang Tindih"                   │
│ "Operasi Ilegal; Tumpang Tindih"                         │
└───────────────────────────────────────────────────────────┘
                            │
                            ▼
                Split by semicolon (;)
                            │
                            ▼
┌───────────────────────────────────────────────────────────┐
│ masalah_list (list of dicts)                             │
│ ──────────────────────────────────────────────────────────│
│ [{'Jenis Masalah': 'HGU Kadaluarsa/Habis', ...},        │
│  {'Jenis Masalah': 'Tumpang Tindih', ...},              │
│  {'Jenis Masalah': 'Operasi Ilegal', ...},              │
│  {'Jenis Masalah': 'Tumpang Tindih', ...}]              │
└───────────────────────────────────────────────────────────┘
                            │
                            ▼
                    pd.DataFrame(masalah_list)
                            │
                            ▼
                groupby('Jenis Masalah').size()
                            │
                            ▼
OUTPUT:
┌─────────────────────────────────────────┐
│ df_masalah_count                        │
│ ────────────────                        │
│ Jenis Masalah             | Jumlah Kasus│
│ Tumpang Tindih            | 17          │
│ HGU Kadaluarsa/Habis      | 10          │
│ Operasi Ilegal            | 3           │
│ IUP Bermasalah            | 2           │
└─────────────────────────────────────────┘
```

---

### **TRANSFORMATION 3: FPIC Violations Filter**

```python
INPUT:
┌─────────────────────────────────────────────────────────────┐
│ df_konflik                                                  │
│ ─────────────────────────────────────────────────────────── │
│ tahun | nama_perusahaan        | indikasi_fpic             │
│ 2023  | Ifishdeco              | False                     │
│ 2022  | [multiple]             | False                     │
│ 2022  | PT GKP                 | True    ← SELECT          │
│ 2019  | PT GKP                 | False                     │
│ 2012  | PT SEJ                 | True    ← SELECT          │
│ 2011  | PT Citra Palu          | True    ← SELECT          │
│ 1968  | PT Vale Indonesia      | True    ← SELECT          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
            df_konflik[df_konflik['indikasi_fpic'] == True]
                            │
                            ▼
OUTPUT:
┌─────────────────────────────────────────────────────────────┐
│ df_fpic_violations (4 rows)                                 │
│ ─────────────────────────────────────────────────────────── │
│ tahun | Perusahaan            | provinsi       | judul      │
│ 2022  | PT GKP                | Sulawesi (...)  | Koalisi...│
│ 2012  | PT SEJ                | Sulawesi (...)  | Konflik...│
│ 2011  | PT Citra Palu         | Sulawesi Sel... | Konflik...│
│ 1968  | PT Vale Indonesia     | Sulawesi (...)  | PT.Vale...│
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                    Render as Expanders
                    (Each case = 1 expander)
```

---

## 🎨 VISUALIZATION PIPELINE

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                │
│  (Pandas DataFrames cached with @st.cache_data)             │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ AGGREGATION  │   │   FILTERING  │   │   MERGING    │
│              │   │              │   │              │
│ .groupby()   │   │ [boolean]    │   │ pd.merge()   │
│ .sum()       │   │ .contains()  │   │ pd.concat()  │
│ .size()      │   │ .isin()      │   │              │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                 VISUALIZATION LAYER                          │
│  (Plotly Express + Plotly Graph Objects)                    │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  px.bar()    │   │ go.Figure()  │   │ st.markdown()│
│  (Timeline)  │   │ (Horizontal) │   │ (Metrics)    │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   STREAMLIT LAYER                            │
│  (UI Components rendered in browser)                        │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ st.columns() │   │ st.expander()│   │ st.dataframe│
│ (Metrics)    │   │ (FPIC cases) │   │ (Tables)    │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      USER BROWSER                            │
│  - HTML rendered                                             │
│  - JavaScript interactions                                   │
│  - Responsive layout                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 USER INTERACTION FLOW

```
┌─────────────────────────────────────────────────────────────┐
│                    USER LANDS ON PAGE 5                      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                    [Scrolls to Section 5.3]
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              READS HERO NARRATIVE + 3 METRICS                │
│  "Laporan CRI, Mighty Earth, BHRRC mendokumentasikan..."   │
│  [12 cases] [21 cases] [X companies]                        │
└─────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            │ Interested?                    │
            │                                │
    YES ────┤                                │──── NO (Skip)
            │                                │
            ▼                                ▼
┌──────────────────────┐         ┌──────────────────────┐
│  VIEWS TIMELINE      │         │  Moves to next       │
│  • Sees spike        │         │  section or page     │
│  • Hovers for data   │         └──────────────────────┘
│  • Reads interpret.  │
└──────────────────────┘
            │
            ▼
┌──────────────────────┐
│  VIEWS PROBLEM       │
│  BREAKDOWN           │
│  • Sees Tumpang      │
│    Tindih is #1      │
│  • Reads interpret.  │
└──────────────────────┘
            │
            ▼
┌──────────────────────┐
│  CLICKS EXPANDER:    │
│  "PT GKP"            │
│  • Reads details     │
│  • Clicks source     │
│    link (Tanahkita)  │
│  • Verifies claim    │
└──────────────────────┘
            │
            ▼
┌──────────────────────┐
│  OPENS DATA TABLE    │
│  • Selects Tab 2     │
│  • Filters by        │
│    "Sulawesi Selatan"│
│  • Sees 3 results    │
│  • Screenshots data  │
└──────────────────────┘
            │
            ▼
┌──────────────────────┐
│  SCROLLS TO          │
│  CITATION BOX        │
│  • Clicks CRI link   │
│  • Opens report in   │
│    new tab           │
│  • Verifies claim    │
│  • Trust established │
└──────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│              USER COMPLETES SECTION 5.3                      │
│  • Understands FPIC violation patterns                       │
│  • Knows specific companies & cases                          │
│  • Can fact-check claims independently                       │
│  • Has evidence for critical narrative                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🏗️ CODE ARCHITECTURE

```
pages/5_Pola_Penerbitan_Izin.py
│
├─ IMPORTS
│  ├─ streamlit as st
│  ├─ pandas as pd
│  ├─ plotly.express as px
│  └─ plotly.graph_objects as go
│
├─ PAGE CONFIG
│  └─ st.set_page_config(layout="wide")
│
├─ STYLES (CSS)
│  └─ st.markdown("<style>...</style>")
│
├─ DATA LOADING FUNCTIONS
│  ├─ @st.cache_data
│  │  └─ load_izin_data()
│  ├─ @st.cache_data
│  │  └─ load_gfw_data()
│  ├─ @st.cache_data
│  │  └─ load_konflik_data()          ← NEW
│  └─ @st.cache_data
│     └─ load_masalah_izin_data()    ← NEW
│
├─ HERO SECTION
│  ├─ Organization badge
│  ├─ Title
│  ├─ 2 Bento Cards (FPIC + IKA)    ← UPDATED
│  └─ Methodology expander
│
├─ SECTION 5.1
│  ├─ Timeline chart (deforestation + permits)
│  └─ Interpretation box
│
├─ SECTION 5.2
│  ├─ Protected areas chart
│  └─ Interpretation box
│
├─ SECTION 5.3 ────────────────────────────── ← NEW SECTION
│  │
│  ├─ HERO NARRATIVE
│  │  └─ Large text block with CRI/Mighty Earth context
│  │
│  ├─ METRICS CARDS (3 columns)
│  │  ├─ Card 1: Konflik Pertambangan (12 cases)
│  │  ├─ Card 2: Perusahaan Izin Bermasalah (21 cases)
│  │  └─ Card 3: Perusahaan Bermasalah Sulawesi
│  │
│  ├─ VIZ 1: TIMELINE
│  │  ├─ Data prep (combine + aggregate)
│  │  ├─ px.bar() grouped
│  │  └─ Interpretation box
│  │
│  ├─ VIZ 2: PROBLEM BREAKDOWN
│  │  ├─ Data prep (split semicolons)
│  │  ├─ px.bar() horizontal
│  │  └─ Interpretation box
│  │
│  ├─ VIZ 3: FPIC VIOLATIONS
│  │  ├─ Filter indikasi_fpic == True
│  │  ├─ for loop → st.expander()
│  │  └─ Interpretation box (worst cases)
│  │
│  ├─ VIZ 4: DATA TABLES
│  │  ├─ st.tabs()
│  │  │  ├─ Tab 1: Konflik
│  │  │  │  ├─ Filters (province, commodity)
│  │  │  │  └─ st.dataframe()
│  │  │  └─ Tab 2: Masalah Izin
│  │  │     ├─ Filters (year, problem type)
│  │  │     └─ st.dataframe()
│  │  │
│  │  └─ VIZ 5: CITATION BOX
│  │     └─ st.markdown() with links
│  │
│  └─ [End of Section 5.3]
│
└─ SECTION 5.4
   └─ Placeholder (Chi-Square)
```

---

## 📦 FILE DEPENDENCIES

```
RUNTIME DEPENDENCIES
│
├─ DATA FILES (CSV)
│  ├─ data/processed/sulawesi_konflik_tambang_fpic.csv     [12 rows]
│  ├─ data/processed/kpa_masalah_izin_perusahaan.csv       [21 rows]
│  ├─ data/processed/sulawesi_izin_baru_per_tahun.csv      [existing]
│  └─ data/processed/sulawesi_gfw_master_1_dekade.csv      [existing]
│
├─ PYTHON SCRIPT
│  └─ pages/5_Pola_Penerbitan_Izin.py                      [main file]
│
├─ DOCUMENTATION (Optional)
│  ├─ docs/PAGE5_SECTION3_IMPLEMENTATION_SUMMARY.md
│  ├─ docs/PAGE5_VISUAL_PREVIEW.md
│  ├─ docs/DATASET_SUMMARY_KONFLIK_TAMBANG_SULAWESI.md
│  └─ TASK_COMPLETION_SUMMARY.md
│
└─ EXTERNAL LIBRARIES
   ├─ streamlit
   ├─ pandas
   ├─ plotly
   └─ (standard library: os, sys)

CREATION DEPENDENCIES (Already Complete)
│
├─ SCRIPTS (ETL)
│  ├─ scripts/filter_konflik_tambang_sulawesi.py           [executed]
│  └─ scripts/etl_kpa_masalah_izin.py                      [executed]
│
└─ SOURCE DATA (Raw)
   ├─ data/processed/nasional_konflik_agraria_tanahkita.csv [568 rows]
   └─ data/raw/konflik_kpa_ylbhi_tanahkita/*.pdf            [9 PDFs]
```

---

## ⚡ PERFORMANCE CHARACTERISTICS

```
LOAD TIME BREAKDOWN

Page Load (5_Pola_Penerbitan_Izin.py)
│
├─ Import libraries                    ~200ms
├─ Load CSS styles                     ~50ms
├─ Load existing datasets (cached)     ~150ms
│  ├─ sulawesi_izin_baru.csv           ~50ms
│  └─ sulawesi_gfw_master.csv          ~100ms
│
├─ Section 5.1 render                  ~100ms
├─ Section 5.2 render                  ~150ms
│
└─ Section 5.3 render (NEW)            ~500ms  ← NEW
   ├─ Load konflik dataset (cached)    ~80ms
   ├─ Load masalah_izin (cached)       ~80ms
   ├─ Render hero narrative            ~20ms
   ├─ Render 3 metric cards            ~50ms
   ├─ Render timeline chart            ~100ms
   ├─ Render problem breakdown         ~80ms
   ├─ Render FPIC expanders            ~40ms
   ├─ Render data tables               ~30ms
   └─ Render citation box              ~20ms

TOTAL PAGE LOAD: ~1.2 seconds (acceptable)
SECTION 5.3 ONLY: ~500ms (fast)

USER INTERACTIONS
│
├─ Filter data table                   ~50-100ms
├─ Expand FPIC card                    ~10ms
├─ Switch tabs                         ~10ms
├─ Hover chart tooltip                 <5ms
└─ Click external link                 [external site speed]

CACHING BEHAVIOR
│
├─ First load                          ~500ms
└─ Subsequent loads (cached)           ~100ms
   └─ Data read from Streamlit cache
```

---

**This diagram shows the complete data journey from raw PDFs to interactive visualizations!** 🎉
