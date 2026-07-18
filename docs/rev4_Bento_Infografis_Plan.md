# Revisi Rencana (Rev 5): Infografis Bento Card (Kurasi Viral Sosmed untuk Poster A4)

Tujuan: Mengkurasi 39 metrik riset menjadi hanya **12 Fakta Paling Mengejutkan (Viral Potential)** agar muat, terbaca jelas, dan estetis saat dicetak dalam format **1 Poster ukuran A4** atau di-posting di Instagram/Twitter.

## User Review Required

> [!IMPORTANT]
> Di bawah ini adalah 12 metrik yang saya pilih khusus karena memiliki "Daya Kejut" tinggi untuk memicu diskusi (viral) di media sosial. Mohon cek daftar ini. Jika Anda setuju dengan kurasinya, klik **Proceed** dan saya akan mengeksekusi kodenya.

## Rencana Struktur Bento Grid (12 Kartu)

Grid akan disusun secara padat namun rapi (misal format 3 kolom x 4 baris atau tata letak asimetris ala Bento). Semua akan dibalut dengan tema *Forest Green*. 

Berikut 12 metrik "Fakta Keras" yang dipilih:

### Kategori 1: Eksploitasi & Kejahatan Ekologis (Shock Value Tinggi)
1. **Lonjakan Gila Izin Tambang (246%)** 
   - *Viral Angle:* Pasca-pandemi dan Omnibus Law, izin tambang diobral tanpa rem.
2. **Sindikasi Izin Hantu & Ilegal**
   - *Viral Angle:* Puluhan korporasi beroperasi secara ilegal dan kebal hukum di kawasan hutan.
3. **Kawasan Lindung Dihancurkan**
   - *Viral Angle:* Ratusan ribu hektare area konservasi sakral secara legal dirobek demi tambang.
4. **Gunung Limbah Beracun (50 Juta Ton)**
   - *Viral Angle:* Bom waktu limbah B3 dan tailing nikel yang perlahan membunuh ekosistem pesisir.
5. **Hutan Primer (Purba) Musnah**
   - *Viral Angle:* Hilangnya jutaan hektare hutan perawan yang tidak bisa dikembalikan lagi.
6. **Kepunahan Spesies Kunci**
   - *Viral Angle:* Satwa endemik Sulawesi didorong ke jurang kepunahan (Daftar Merah IUCN).

### Kategori 2: Penderitaan Warga & Paradoks Ekonomi (Emotional Impact)
7. **Ledakan Bencana & Pengungsi Iklim**
   - *Viral Angle:* Ribuan insiden banjir/longsor memaksa jutaan jiwa menjadi pengungsi di tanah sendiri.
8. **Beban Penyakit ISPA & Diare**
   - *Viral Angle:* Warga lingkar tambang (Konawe/Morowali) dipaksa menghirup udara mematikan setiap hari.
9. **Kiamat Pertanian Rakyat**
   - *Viral Angle:* Lahan petani dirampas, kontribusi pertanian anjlok drastis digilas alat berat.
10. **Perampasan Tanah & Konflik Agraria (84 Kasus)**
    - *Viral Angle:* Kekerasan, kriminalisasi, dan pengusiran paksa warga demi melancarkan megaproyek.
11. **Pabrik Asap PLTU Captive (>6.000 MW)**
    - *Viral Angle:* Ironi hilirisasi "hijau" untuk EV, tapi disuplai oleh ribuan Megawatt batu bara kotor.
12. **Ilusi Kesejahteraan (PDRB Ekstraktif)**
    - *Viral Angle:* Uang triliunan berputar di tambang (58% PDRB), tapi warga lokal tetap miskin dan hanya jadi penonton.

## Proposed Changes

### [MODIFY] [pages/13_Infografis_Fakta.py](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/4.%20Celios2/pages/13_Infografis_Fakta.py)
Saya akan menggabungkan script ekstraksi variabel dari `12_Infografis_Summary.py` hanya untuk 12 variabel di atas. Kemudian saya akan merender HTML murni (seperti skrip awal) untuk 12 kartu tersebut dengan penyesuaian font dan *spacing* agar terlihat sangat proporsional di aspek rasio kertas A4 (potret).
