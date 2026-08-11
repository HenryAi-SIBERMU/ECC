import re

with open('docs/gfw_comparison_report.md', 'r', encoding='utf-8') as f:
    content = f.read()

old_table = '''| Provinsi | Kode `adm1` V2 (Lama/Salah) | Kode `adm1` V3 (GADM Resmi) | Keterangan |
| :--- | :---: | :---: | :--- |
| **Gorontalo** | `11` | `6` | Data lama menarik data dari provinsi lain (seperti Jambi atau Jakarta) |
| **Sulawesi Barat** | `33` | `25` | Data lama menarik provinsi dari Sumatera atau Jawa |
| **Sulawesi Selatan** | `30` | `26` | Data lama menarik provinsi dari region yang salah total |
| **Sulawesi Tengah** | `29` | `27` | Data lama V2 justru menarik kode `adm1=29` (yang merupakan Sulawesi Utara di V3) |
| **Sulawesi Tenggara** | `32` | `28` | Data lama menyedot data dari luar Sulawesi |
| **Sulawesi Utara** | `31` | `29` | Data lama menyedot data dari Sumatera Selatan/lainnya |'''

new_table = '''| Provinsi | Kode `adm1` V2 (Lama/Salah) | Kode `adm1` V3 (GADM Resmi) | Keterangan (Tujuan Asli Kode V2) |
| :--- | :---: | :---: | :--- |
| **Gorontalo** | `11` | `6` | Data lama menarik data deforestasi dari **Sumatera Barat** |
| **Sulawesi Barat** | `33` | `25` | Data lama menarik data deforestasi dari **Nusa Tenggara Timur (NTT)** |
| **Sulawesi Selatan** | `30` | `26` | Data lama menarik data deforestasi dari **Jawa Timur** |
| **Sulawesi Tengah** | `29` | `27` | Data lama menarik data deforestasi dari **Jawa Tengah** |
| **Sulawesi Tenggara** | `32` | `28` | Data lama menarik data deforestasi dari **Bali** |
| **Sulawesi Utara** | `31` | `29` | Data lama menarik data deforestasi dari **DI Yogyakarta** |'''

content = content.replace(old_table, new_table)

with open('docs/gfw_comparison_report.md', 'w', encoding='utf-8') as f:
    f.write(content)
