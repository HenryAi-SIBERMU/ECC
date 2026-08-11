import sys

with open('docs/gfw_comparison_report.md', 'r', encoding='utf-8') as f:
    content = f.read()

new_section = '''
## 🌳 7. Catatan Kritis Ekologis: Bahaya Bug Hutan Primer & Kawasan Lindung

Di dalam algoritma lama (yang sayangnya sempat terbawa ke script konsolidasi V3 awal), terdapat bug fatal di mana angka **Deforestasi Hutan Primer** dan **Kawasan Lindung** bernilai sama persis dengan **Total Deforestasi**. 

Berikut adalah penjelasan ekologis mengapa bug ini sangat membahayakan kredibilitas riset jika tidak diperbaiki:

### A. Perbedaan Mendasar Hutan Primer vs Hutan Sekunder (Biasa)

1. **Hutan Primer (Primary Forest / Hutan Alam Asli):**
   * **Definisi:** Hutan perawan yang belum pernah dirusak atau dieksploitasi masif oleh manusia (Berdasarkan baseline Margono et al. 2014).
   * **Nilai Ekologis:** Sangat tinggi. Biodiversitas endemik (habitat anoa, babirusa, dll) dan stok karbon purba ada di sini.
   * **Implikasi Hilangnya:** Deforestasi di area ini adalah **bencana ekologis permanen**. Menghancurkan paru-paru bumi yang tak tergantikan.

2. **Hutan Sekunder / Hutan Tanaman (Termasuk dalam 'Tree Cover' GFW):**
   * **Definisi:** Hutan yang tumbuh kembali setelah tebangan masa lalu, atau Hutan Tanaman Industri (HTI) dan Perkebunan (misal: kelapa sawit, karet, akasia).
   * **Karakteristik Sensor GFW:** Satelit GFW menganggap *semua* vegetasi setinggi lebih dari 5 meter sebagai "Tutupan Pohon" (Tree Cover). Artinya, jika perusahaan kelapa sawit menebang pohon sawitnya sendiri untuk peremajaan (*replanting*), sensor GFW akan merekamnya sebagai *Tree Cover Loss* (Deforestasi).

### B. Analomi Bug pada Script Konsolidasi

Ketika API GFW mengembalikan data *Primary Forest Loss*, mereka memberikan seluruh total deforestasi, namun melabelinya:
* `True` = Terjadi di Hutan Primer.
* `False` = Terjadi di Hutan Biasa / Perkebunan.

**Kesalahan Script Lama:** 
Script melakukan `groupby` dan `sum()` tanpa memfilter label `True`. Akibatnya, tebangan sawit (*replanting*) atau pembukaan semak belukar ikut dijumlahkan dan dilaporkan sebagai **Kehilangan Hutan Primer**.

### C. Mengapa Ini Harus Segera Difilter? (Dampak terhadap Narasi Celios)

Jika Celios merilis laporan menggunakan script yang belum difilter ini, narasi yang muncul adalah:
> *"100% dari X Juta Hektar deforestasi Sulawesi terjadi di Hutan Alam Asli!"*

Pemerintah dan pihak industri akan sangat mudah membantah dan menghancurkan kredibilitas data ini dengan berkata:
> *"Data Celios salah besar. Sebagian besar dari angka tersebut hanyalah aktivitas tebang pilih di hutan produksi atau replanting sawit masyarakat/perusahaan, bukan pembabatan hutan perawan."*

Oleh karena itu, penyaringan (`df = df[df['is__umd_regional_primary_forest_2001'] == True]`) bersifat **wajib dan krusial**. Dengan data yang sudah disaring dengan benar, Celios dapat menyajikan fakta empiris yang kebal bantahan: memisahkan mana yang sekadar hilangnya *tutupan pohon biasa/industri*, dan mana yang benar-benar **Tragedi Ekologis** (hilangnya Hutan Alam Asli Sulawesi).
'''

with open('docs/gfw_comparison_report.md', 'w', encoding='utf-8') as f:
    f.write(content + new_section)
