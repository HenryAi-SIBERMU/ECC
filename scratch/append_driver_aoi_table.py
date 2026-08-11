table_driver = '''
### 🚨 Kasus Khusus: Kesalahan AOI (Area of Interest) pada Data Faktor Pendorong (Driver)

Khusus untuk dataset **Loss by Driver (Faktor Pendorong Deforestasi)**, API GFW tidak menggunakan `Geostore ID`, melainkan menggunakan fitur *Area of Interest (AOI)* berbasis kodifikasi GADM tingkat Provinsi (disebut parameter `adm1`). 

Pada pengambilan data V2 (Lama), terjadi kesalahan fatal di mana sistem me-request **kode provinsi yang sepenuhnya salah sasaran**, karena kode tersebut bukan kodifikasi GADM resmi Indonesia. Berikut perbandingannya:

| Provinsi | Kode `adm1` V2 (Lama/Salah) | Kode `adm1` V3 (GADM Resmi) | Keterangan |
| :--- | :---: | :---: | :--- |
| **Gorontalo** | `11` | `6` | Data lama menarik data dari provinsi lain (seperti Jambi atau Jakarta) |
| **Sulawesi Barat** | `33` | `25` | Data lama menarik provinsi dari Sumatera atau Jawa |
| **Sulawesi Selatan** | `30` | `26` | Data lama menarik provinsi dari region yang salah total |
| **Sulawesi Tengah** | `29` | `27` | Data lama V2 justru menarik kode `adm1=29` (yang merupakan Sulawesi Utara di V3) |
| **Sulawesi Tenggara** | `32` | `28` | Data lama menyedot data dari luar Sulawesi |
| **Sulawesi Utara** | `31` | `29` | Data lama menyedot data dari Sumatera Selatan/lainnya |

**Dampak Kesalahan V2:** 
Sistem mengunduh emisi CO2 dan data deforestasi komoditas sawit dari pulau Sumatera atau Jawa, lalu mengklaimnya sebagai data Sulawesi. Inilah mengapa dataset *Loss by Driver* V3 sangat krusial, karena di V3 kita telah mengkalibrasi ulang `adm1` sehingga menarik 100% dari teritori Sulawesi yang tepat.
'''

with open('docs/gfw_comparison_report.md', 'r', encoding='utf-8') as f:
    content = f.read()

with open('docs/gfw_comparison_report.md', 'w', encoding='utf-8') as f:
    f.write(content + '\n' + table_driver)
