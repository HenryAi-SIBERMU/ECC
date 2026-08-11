table = '''
## 🚨 8. Laporan Investigasi Resolusi Spasial: BBox vs GADM (V2 vs V3)

Tabel berikut menunjukkan perbedaan *Geostore ID* (kode area poligon) yang digunakan API Global Forest Watch pada dataset V2 (Lama) dan V3 (Baru).

| Provinsi | Geostore ID V2 (Salah/BBox) | Geostore ID V3 (Resmi GADM) | Keterangan Fatalitas V2 |
| :--- | :--- | :--- | :--- |
| **Sulawesi Tengah** | `fce1e175169936334347ae17207381a0` | `70415db2d291955e71d4b08466cd6136` | Kotak imajiner terlalu besar (Overbounding). Menyerok wilayah laut dan pulau tetangga (Maluku/Kaltim). Angka deforestasi palsu meledak hingga 1.000%! |
| **Sulawesi Utara** | `89b35f128c9cfe7685e1738c89a0a730` | `8856238b97d25e076634ab9ddbb662b1` | Kotak imajiner terpotong (Underbounding). Tidak menjangkau pulau terluar seperti Sangihe & Talaud. Menyebabkan under-reporting deforestasi yang sangat masif. |
| **Sulawesi Tenggara** | `fe2e396191a0e8b6e70aa03dd225d7f7` | `3c79929a54bff963e7bf3a4762b803e9` | Kehilangan Kepulauan Wakatobi, Buton, dan Muna akibat batas kotak yang tidak meliuk. Saat direvisi (V3), angka deforestasi aslinya naik +124%. |
| **Sulawesi Barat** | `77f83070a9b4111e24a7cfdea73a5adb` | `796e2f453e81e409e183d833c586ff34` | Overbounding parah (terseret ke daratan Kalimantan). Angka Hutan Primer lama mencatat 53rb Ha, padahal aslinya 0 Ha. |
| **Sulawesi Selatan** | `abc6fc008f433d3dbdc65861bdcc8a87` | `33c45193c87f0505647dfae91a796b67` | Kepulauan Selayar dan Spermonde tidak tercakup akurat pada V2. |
| **Gorontalo** | `db937e7121c426140dd91072c14bbdaf` | `8d998ed751ba37bf689febf729f30304` | Batas darat utara yang bergerigi terseragamkan menjadi garis lurus di V2, merusak akurasi hektar di perbatasan. |

### Penjelasan Akar Masalah (Mengapa BBox Haram Digunakan)

1. **BBox (Bounding Box) pada V2:** 
   Sistem V2 menarik data satelit dengan memberikan koordinat *Min-Max Longitude/Latitude*. Ini menghasilkan bentuk **persegi panjang**. Karena bentuk Sulawesi itu rumit seperti huruf "K", kotak ini menabrak lautan dan pulau tetangga. Hutan yang terbakar di Maluku atau Kalimantan ikut terhitung sebagai deforestasi Sulawesi.
2. **GADM Geostore pada V3:**
   Sistem V3 tidak lagi memberikan koordinat kotak. Kita memberikan **ID Resmi dari GADM** (Database Area Administratif Global). GFW menggunakan ID ini untuk memotong peta satelit persis mengikuti lekukan pesisir pantai dan batas provinsi aslinya. Inilah data yang diakui dunia internasional secara *scientific*.
'''

with open('docs/gfw_comparison_report.md', 'r', encoding='utf-8') as f:
    content = f.read()

with open('docs/gfw_comparison_report.md', 'w', encoding='utf-8') as f:
    f.write(content + '\n' + table)
