import sys

with open('scratch/all_comparisons.md', 'r', encoding='utf-8') as f:
    tables = f.read()

with open('docs/gfw_comparison_report.md', 'r', encoding='utf-8') as f:
    old_content = f.read()

driver_table = ''
capture = False
for line in old_content.split('\n'):
    if '2. Perbandingan Dataset Driver Loss' in line or '1. Perbandingan Dataset Driver Loss' in line:
        capture = True
        driver_table += '## 🚚 5. Perbandingan Dataset Driver Loss (V1 vs V3: 2001 - 2025)\n\n'
        continue
    if capture:
        if 'Temuan Fatal pada Algoritma' in line or 'Temuan Fatal pada Indikator' in line:
            break
        driver_table += line + '\n'

final_md = tables + '\n\n' + driver_table + '\n\n' + '''## 🔴 6. Temuan Fatal pada Algoritma Aggregasi Consolidate Lama

> [!CAUTION]
> **TEMUAN FATAL: `Deforestasi Hutan Primer` & `Kawasan Lindung` bernilai sama persis dengan `Total Deforestasi`**
>
> Pada dataset master lama hasil `consolidate_master_gfw.py` (dan ketika menjumlahkan semua baris raw API), angka untuk `Total Deforestasi`, `Deforestasi Hutan Primer`, dan `Deforestasi Kawasan Lindung` **sama persis**.
> 
> **Penyebab:** Script lama sekadar menjumlahkan **semua** kolom `area__ha` tanpa melakukan filter kondisi (`is__umd_regional_primary_forest_2001 == True`). GFW mengembalikan data untuk area primer (True) dan area sekunder/non-primer (False). Jika dijumlahkan keduanya, hasilnya adalah Total Deforestasi.
> 
> **Dampak:** Dashboard lama menampilkan overestimasi masif di mana seolah-olah 100% deforestasi terjadi di Hutan Primer dan Kawasan Lindung.

---

## 🛠️ Kesimpulan & Status Perbaikan

1. **Semua Dataset Raw V3:** 100% Selesai & Lengkap ditarik menggunakan Geostore ID resmi.
2. **Perbedaan Data Sangat Masif:** Kesalahan Bounding Box / ID pada V2 dan V1 membuat data lama kembung atau meleset hingga jutaan hektar (narik data Sumatera, Jawa, dll). V3 mengoreksi kesalahan ini menjadi data presisi resmi GADM 3.6.
3. **Langkah Berikutnya:** Memperbaiki logika agregasi di `clean_gfw_data_v3.py` dan `consolidate_master_gfw_v3.py` agar mengaplikasikan filter kondisi Hutan Primer (`is__umd_regional_primary_forest_2001 == True`) & Kawasan Lindung yang benar.
'''

with open('docs/gfw_comparison_report.md', 'w', encoding='utf-8') as f:
    f.write(final_md)
