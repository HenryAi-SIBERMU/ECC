# 📊 Rekapitulasi Data Emisi CO2 Deforestasi Sulawesi (GFW 2001-2023)

Dokumen ini berisi rincian data emisi karbon akibat *Tree Cover Loss* (Kehilangan Tutupan Pohon) di seluruh daratan Pulau Sulawesi hasil query API Global Forest Watch (GFW / University of Maryland).

---

## 📈 Tabel Rincian Emisi Tahunan vs Akumulasi Kumulatif

| Tahun | Emisi Tahunan (Megaton CO2e) | Akumulasi Kumulatif (Megaton CO2e) | Catatan / Status Periode |
| :---: | :---: | :---: | :--- |
| **2001** | 63.64 Mt | 63.64 Mt | Pra-Hilirisasi Nikel |
| **2002** | 80.39 Mt | 144.03 Mt | Pra-Hilirisasi Nikel |
| **2003** | 45.91 Mt | 189.94 Mt | Pra-Hilirisasi Nikel |
| **2004** | 127.91 Mt | 317.85 Mt | Pra-Hilirisasi Nikel |
| **2005** | 132.58 Mt | 450.43 Mt | Pra-Hilirisasi Nikel |
| **2006** | 209.40 Mt | 659.83 Mt | Pra-Hilirisasi Nikel |
| **2007** | 231.19 Mt | 891.02 Mt | Pra-Hilirisasi Nikel |
| **2008** | 224.69 Mt | 1,115.71 Mt | Pra-Hilirisasi Nikel |
| **2009** | 256.86 Mt | 1,372.57 Mt | Pra-Hilirisasi Nikel |
| **2010** | 169.08 Mt | 1,541.65 Mt | Pra-Hilirisasi Nikel |
| **2011** | 201.42 Mt | 1,743.07 Mt | Pra-Hilirisasi Nikel |
| **2012** | 369.29 Mt | 2,112.36 Mt | Pra-Hilirisasi Nikel |
| **2013** | 122.05 Mt | 2,234.41 Mt | Pra-Hilirisasi Nikel |
| **2014** | **181.18 Mt** | **2,415.59 Mt** | 🚩 **Baseline Hilirisasi Nikel (UU Minerba)** |
| **2015** | 182.44 Mt | 2,598.03 Mt | Era Ekspansi Kawasan Industri Nikel |
| **2016** | **319.83 Mt** | **2,917.86 Mt** | ⚡ **Puncak Deforestasi Hilirisasi** |
| **2017** | 159.73 Mt | 3,077.59 Mt | Era Ekspansi Kawasan Industri Nikel |
| **2018** | 133.60 Mt | 3,211.19 Mt | Era Ekspansi Kawasan Industri Nikel |
| **2019** | 108.61 Mt | 3,319.80 Mt | Disahkannya Moratorium Ekspor Bijih Nikel |
| **2020** | 106.55 Mt | 3,426.35 Mt | Pengesahan UU Cipta Kerja (Omnibus Law) |
| **2021** | 94.77 Mt | 3,521.12 Mt | Era Eksploitasi Operasi Produksi |
| **2022** | 99.78 Mt | 3,620.90 Mt | Era Eksploitasi Operasi Produksi |
| **2023** | **135.20 Mt** | **3,756.10 Mt** | 📌 **Tahun Terkini Dataset GFW v3** |

---

## 🔍 Temuan Forensik & Penjelasan Angka 3,756.10 Megaton

1. **Kenapa Angka 3,756.10 Mt Terlihat Sangat Raksasa?**
   - Angka `3,756.10 Megaton` (3.75 Gigaton) **bukan emisi 1 tahun di tahun 2024**, melainkan **total penjumlahan (akumulasi kumulatif) seluruh emisi deforestasi di Sulawesi selama 23 tahun (2001–2023)**.
   - Di tampilan frontend sebelumnya, terjadi bug di mana angka emisi tahunan 2014 (181.18 Mt) disandingkan langsung dengan angka akumulasi 23 tahun (3,756.10 Mt), sehingga menghasilkan angka persentase anomali (+1,973%).

2. **Perbandingan Emisi Tahunan Riil (Apple-to-Apple):**
   - **Tahun 2014 (Baseline Hilirisasi):** `181.18 Megaton CO2e` / tahun.
   - **Tahun 2023 (Terkini):** `135.20 Megaton CO2e` / tahun.
   - **Total Akumulasi 1 Dekade Hilirisasi (2014–2023):** `1,521.70 Megaton CO2e` (1.52 Gigaton).
   - **Total Akumulasi Historis GFW (2001–2023):** `3,756.10 Megaton CO2e` (3.75 Gigaton).

3. **Cakupan Emisi:**
   - **GFW Murni Biomass Carbon Loss (LULUCF)**: Menghitung pelepasan karbon akibat pembabatan tutupan hutan/pohon.
   - **Belum Termasuk Cerobong PLTU & Smelter**: Emisi operasional pembakaran batubara pada PLTU captive dan fasilitas smelter tidak termasuk dalam angka GFW ini.
