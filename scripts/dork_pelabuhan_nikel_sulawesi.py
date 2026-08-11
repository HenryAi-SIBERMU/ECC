"""
DORKING SCRIPT: Pelabuhan Ekspor Nikel Sulawesi
================================================
Target: Mengumpulkan data logistik pelabuhan untuk 3 Dataset Cards di Section 1.5

CARD 1: Fasilitas Pelabuhan Ekspor
- node_label: Nama lokasi industri
- port_facility: Jenis fasilitas pelabuhan
- export_channel: Saluran ekspor

CARD 2: Status Proyek Strategis Nasional (PSN)
- node_label: Nama lokasi industri  
- psn_status: Status PSN (terkonfirmasi/belum_ditemukan)
- psn_detail: Detail referensi PSN

CARD 3: Detail Kapasitas Pelabuhan
- node_label: Nama lokasi industri
- port_detail: Spesifikasi teknis dan kapasitas

6 NODES TARGET:
1. IMIP — Bahodopi Morowali (Sulawesi Tengah)
2. GNI — Petasia Morowali Utara (Sulawesi Tengah)
3. VDNI — Morosi Konawe (Sulawesi Tenggara)
4. OSS — Morosi Konawe (Sulawesi Tenggara)
5. ANTAM — Pomalaa Kolaka (Sulawesi Tenggara)
6. Vale — Sorowako Luwu Timur (Sulawesi Selatan)

DORKING QUERIES:
===============

## CARD 1: Fasilitas Pelabuhan Ekspor

### IMIP Morowali
site:imip.co.id pelabuhan OR dermaga OR port OR jetty
site:indonesiainvestments.com IMIP pelabuhan
site:katadata.co.id IMIP "pelabuhan" morowali
"IMIP" "pelabuhan" "bulk carrier" OR "jetty"
"Indonesia Morowali Industrial Park" port facility

### GNI Petasia
site:gunbusternickelindustry.com pelabuhan OR port
site:katadata.co.id GNI Petasia pelabuhan
"GNI Petasia" "pelabuhan" "50.000 ton" OR "50000 ton"
"Gunbuster Nickel" port capacity morowali

### VDNI Konawe
site:vdni.co.id pelabuhan OR port OR dermaga
"Virtue Dragon" Konawe pelabuhan OR port
site:esdm.go.id VDNI pelabuhan sulawesi tenggara
"VDNI" "Desa Porara" pelabuhan OR jetty

### OSS Konawe  
"Obsidian Stainless Steel" Konawe pelabuhan OR port
site:katadata.co.id OSS morowali pelabuhan
"OSS" "berbagi jetty VDNI" OR "shared port"

### ANTAM Pomalaa
site:antam.com pomalaa pelabuhan OR dermaga
"ANTAM" "Pomalaa" "Kolaka" pelabuhan OR jetty
site:pertambangan.esdm.go.id ANTAM pomalaa port

### Vale Sorowako
site:vale.com sorowako pelabuhan OR port
"Vale" "Sorowako" "Luwu Timur" pelabuhan balantang malili
site:katadata.co.id Vale sorowako pelabuhan ekspor

## CARD 2: Status PSN (Proyek Strategis Nasional)

### General PSN Queries
site:kppip.go.id proyek strategis nasional nikel sulawesi
site:bappenas.go.id PSN smelter nikel sulawesi
filetype:pdf Perpres 58/2017 proyek strategis nasional nikel
filetype:pdf Perpres 12/2025 proyek strategis nasional
"Proyek Strategis Nasional" smelter nikel sulawesi tengah tenggara

### Specific Company + PSN
"IMIP" "Proyek Strategis Nasional" OR "PSN"
"GNI Petasia" "Proyek Strategis Nasional" OR "PSN"  
"VDNI" "Proyek Strategis Nasional" OR "PSN"
"ANTAM Pomalaa" "Proyek Strategis Nasional" OR "PSN"
"Vale Sorowako" "Proyek Strategis Nasional" OR "PSN"

### Perpres Documents
site:peraturan.go.id Perpres 58 2017 nikel
site:jdih.setneg.go.id Perpres PSN smelter
filetype:pdf "Peraturan Presiden" "58" "2017" smelter
filetype:pdf "Perpres 12/2025" industri nikel

## CARD 3: Detail Kapasitas Pelabuhan

### Technical Specifications
"IMIP" "seaport" "jetty" "bulk carrier" capacity
"GNI" "pelabuhan" "50.000 ton" kapasitas kapal
"VDNI" "jetty" "tongkang" "kapal besar" kapasitas
"ANTAM Pomalaa" "jetty" "12.000 DWT" OR "unloading"
"Vale" "pelabuhan" "Balantang" "Malili" kapasitas

### Port Infrastructure
"Indonesia Morowali" "integrated port" "stockpile"
"Petasia Morowali" "port access" "shared service"
"Virtue Dragon" "Desa Porara" "belt conveyor" jetty
"Obsidian Stainless" berbagi "shared" port VDNI
"Pomalaa" "pelabuhan Nuha" "Balantang" "Malili" "rute"

### Capacity & Vessel Size
site:marinetraffic.com IMIP morowali vessel
site:vesseltracker.com GNI petasia port calls
"bulk carrier" "airport" "1.800m" IMIP
"port access" "shared service" Tsingshan morowali
"Pelabuhan Vale Nuha + Pelabuhan Balantang Malili" "Sorowako" "Malili" "Balantang"

SEARCH STRATEGY:
================
1. Gunakan Google Custom Search API atau manual dorking
2. Prioritaskan situs resmi perusahaan & pemerintah
3. Cross-validate dengan media kredibel (Katadata, Kompas, Tempo)
4. Ekstrak PDF dokumen perpres untuk data PSN
5. Gunakan archive.org jika situs tidak accessible
6. Verifikasi dengan Google Maps / Satellite imagery

OUTPUT FORMAT:
=============
CSV dengan 3 sections seperti yang ada di screenshot:
- Section 1: node_label, port_facility, export_channel
- Section 2: node_label, psn_status, psn_detail  
- Section 3: node_label, port_detail

EXECUTION NOTES:
===============
- Jalankan dorking secara manual atau via API
- Simpan hasil mentah di data/raw/osint_logistik_pelabuhan/
- Dokumentasikan semua sumber dengan URL lengkap
- Tandai data yang belum terverifikasi
"""

import os

# Create output directory
output_dir = "data/raw/osint_logistik_pelabuhan"
os.makedirs(output_dir, exist_ok=True)

print("="*70)
print("DORKING GUIDE: Pelabuhan Ekspor Nikel Sulawesi")
print("="*70)
print("\nFile panduan dorking telah dibuat.")
print(f"Output directory: {output_dir}")
print("\nLangkah selanjutnya:")
print("1. Jalankan queries di atas secara manual atau via Google CSE API")
print("2. Simpan hasil ekstraksi per-node di folder output")
print("3. Dokumentasikan sumber data dengan detail")
print("4. Compile menjadi sulawesi_logistik_simpul_nikel.csv")
print("\nREFERENSI SUMBER UTAMA:")
print("- KPPIP: https://kppip.go.id")
print("- Perpres: https://peraturan.go.id")  
print("- GNI: https://gunbusternickelindustry.com")
print("- IMIP: https://imip.co.id")
print("- Vale: https://vale.com")
print("- ANTAM: https://antam.com")
print("- Media: Katadata, Kompas, Tempo")
print("="*70)
