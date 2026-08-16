# Pipeline Skoring D3TLH: Diagram Alur Metodologi (Versi 1, 2, & 3)

Dokumen ini memuat diagram alur (*flowchart*) **Mermaid.js** khusus yang mendokumentasikan arsitektur pipeline skoring dan transformasi data empiris pada Dashboard Forensik ECC (Audit D3TLH). Pipeline dipisahkan secara rinci untuk **Versi 1**, **Versi 2**, dan **Versi 3** dalam dokumen ini.

---

## 1. Pipeline Skoring Versi 1: Baseline Plotly Model (Skala Kontinu 0.0 – 10.0)

> **Karakteristik Versi 1**: Model dasar menggunakan *Weighted Sum Model* (WSM) sederhana. Data mentah dinormalisasi secara linear tanpa pemisahan metrik spasial intensif/ekstensif dan ditampilkan menggunakan visualisasi dasar Plotly.

```mermaid
flowchart TD
    subgraph V1_S1["1. Data Ingestion (Raw Data)"]
        A1["NASA TROPOMI NO2 Data"]
        A2["Global Energy Monitor PLTU Data"]
        A3["Kemenkes ISPA & Diare Data"]
        A4["GFW Tree Loss & CO2 Data"]
        A5["BNPB Bencana Data"]
    end

    subgraph V1_S2["2. Linear Normalization (WSM 0-10)"]
        B1["Min-Max Scaling Direct Ratio"]
        B2["Formula Linear: (Nilai / Max_Baseline) * 10"]
    end

    subgraph V1_S3["3. Direct Aggregation"]
        C1["Unweighted Mean: (Sub1 + Sub2 + Sub3 + Sub4) / 4"]
        C2["Skor Kontinu Skala 0.0 s/d 10.0"]
    end

    subgraph V1_S4["4. Baseline Presentation"]
        D1["Plotly Choropleth Map Baseline"]
        D2["Card Metric (Nilai Desimal 0-10)"]
    end

    A1 & A2 & A3 & A4 & A5 --> B1
    B1 --> B2
    B2 --> C1
    C1 --> C2
    C2 --> D1 & D2
```

---

## 2. Pipeline Skoring Versi 2: Continuous WSM + Kinetic Tooltip Map (Skala Kontinu 0.0 – 10.0)

> **Karakteristik Versi 2**: Mengembangkan Versi 1 dengan menambahkan **pembobotan spasial (metrik intensif vs ekstensif)**, integrasi outlier deviasi ($Mean + 1 SD$), serta peta interaktif dengan *kinetic tooltip*.

```mermaid
flowchart TD
    subgraph V2_S1["1. Advanced Data Ingestion"]
        E1["NASA Satelit NO2 + Data PLTU Active/Planned"]
        E2["Kemenkes Morbiditas (Rasio Sentra vs Non-Sentra)"]
        E3["KLHK Limbah B3 (Proporsi Regional vs Nasional)"]
        E4["GFW Deforestasi & Driver Loss (Ha/Dekade)"]
        E5["BNPB Outlier Analysis (Mean + 1 SD)"]
    end

    subgraph V2_S2["2. Spatial Weighting & Transformation"]
        F1["Klasifikasi Metrik Intensif (Rasio/Indeks) vs Ekstensif (Luas/Jumlah)"]
        F2["Normalisasi Batas Toleransi & Outlier Deviasi"]
        F3["Continuous WSM Formula (Skala 0.0 - 10.0)"]
    end

    subgraph V2_S3["3. Multi-Matrix Aggregation"]
        G1["Matriks Udara (Sub 1-4) -> Skor Udara Kontinu"]
        G2["Matriks Air (Sub 1-5) -> Skor Air Kontinu"]
        G3["Matriks Lahan (Sub 1-4) -> Skor Lahan Kontinu"]
        G4["Matriks Sosial (Sub 1-4) -> Skor Sosial Kontinu"]
        G5["Matriks Veto (Sub 1-3) -> Indicator Thresholds"]
    end

    subgraph V2_S4["4. Kinetic Presentation Engine"]
        H1["Kinetic Tooltip Interactive Map"]
        H2["Presisi Desimal Card (Skor 0.0 - 10.0 / 10)"]
        H3["Breakdown Sub-Skor Real-Time Metric"]
    end

    E1 & E2 & E3 & E4 & E5 --> F1
    F1 --> F2
    F2 --> F3
    F3 --> G1 & G2 & G3 & G4 & G5
    G1 & G2 & G3 & G4 & G5 --> H1 & H2 & H3
```

---

## 3. Pipeline Skoring Versi 3: Verified MCDA-Likert Model (Skala Diskret 1 – 5)

> **Karakteristik Versi 3**: Model standar yang **terverifikasi 100% secara hukum dan empiris**. Menggunakan *Multi-Criteria Decision Analysis* (MCDA) dengan ambang batas (*threshold*) baku dari 19 regulasi PDF/CSV, lalu dipetakan ke **Skala Ordinal Diskret 1 s/d 5** untuk memberikan status eksekutif (misal: *STATUS: KRITIS / PERLU PENGAWASAN*).

```mermaid
flowchart TD
    subgraph V3_S1["1. Ingestion Data Mentah & Berkas Hukum Legal (Raw + PDF)"]
        I1["NASA TROPOMI & GEM Data PLTU (11.165 MW)"]
        I2["BNPB Bencana (877 Outlier) & GFW (513.561 Ha Sultra)"]
        I3["KPA CATAHU 2023 (135.608 KK) & Satya Bumi (57 Insiden)"]
        I4["19 PDF Regulasi Primair (PermenLHK 27/2021, PP 22/2021, UU 41/1999, dll)"]
    end

    subgraph V3_S2["2. Validation & Regulatory Thresholding Engine"]
        J1["Uji Threshold Spasial Multi-Skala (Pulau vs Provinsi)"]
        J2["Validasi Verbatim Pasal & Halaman Dokumen PDF"]
        J3["Klasifikasi Status: Verified (15) / Defensible (4)"]
    end

    subgraph V3_S3["3. MCDA-Likert Discrete Mapping Engine"]
        K1["Multi-Criteria Decision Analysis (MCDA) Threshold Test"]
        K2["Kalkulasi Level Ancaman Diskret Ordinal (Skala 1 - 5)"]
        K3["1 = Aman | 2 = Waspada | 3 = Siaga | 4 = Perlu Pengawasan | 5 = Kritis"]
    end

    subgraph V3_S4["4. 19-Indicator Matrix Integration"]
        L1["Udara (PLTU/IKU, ISPA, B3, Emisi CO2) -> Likert 1-5"]
        L2["Air (IKA/Cr6+, Diare, Pesisir, Tailing) -> Likert 1-5"]
        L3["Lahan (Bencana, Deforestasi, Lindung, Driver) -> Likert 1-5"]
        L4["Sosial (FPIC, Jiwa Terdampak, Kriminalisasi, Faskes) -> Likert 1-5"]
        L5["Veto (Izin Baru, Pemutihan Hutan, PLTU Captive) -> Likert 1-5 / Veto"]
    end

    subgraph V3_S5["5. Dashboard Streamlit Output & Executive Audit"]
        M1["Summary Executive Card (Skor 4 / 5 - Status Kritis/Perlu Pengawasan)"]
        M2["Choropleth Map Spasial Model Terverifikasi"]
        M3["Tabel Audit Forensik D3TLH & Bukti Verbatim PDF Expander"]
    end

    I1 & I2 & I3 & I4 --> J1
    J1 --> J2
    J2 --> J3
    J3 --> K1
    K1 --> K2
    K2 --> K3
    K3 --> L1 & L2 & L3 & L4 & L5
    L1 & L2 & L3 & L4 & L5 --> M1 & M2 & M3
```

---

## 📊 Perbandingan Sintesis 3 Versi Pipeline

| Komponen Pipeline | Versi 1 (Plotly Baseline) | Versi 2 (Continuous WSM) | Versi 3 (MCDA-Likert Spasial) |
|---|---|---|---|
| **Skala Skoring** | Kontinu Desimal ($0.0 \text{--} 10.0$) | Kontinu Desimal ($0.0 \text{--} 10.0$) | Diskret Ordinal ($1 \text{--} 5$) |
| **Model Matematis** | Unweighted Linear Mean | Continuous Weighted Sum (WSM) | Multi-Criteria Decision Analysis (MCDA) |
| **Penyesuaian Spasial** | Tidak Ada (Nasion-wide Aggregate) | Bobot Lanskap & Deviasi Outlier | Threshold Spasial Multi-Skala (Pulau vs Prov) |
| **Landasan Regulasi** | Arbitrari / Ad-hoc | Arbitrari / Trend-based | **100% Terverifikasi 19 PDF & CSV Primair** |
| **Output Card Status** | Nilai Angka $0 \text{--} 10$ | Nilai Angka Desimal + Kinetic Tooltip | **Nilai Diskret (mis. 4 / 5) + Status Kritis** |
