import pandas as pd
import os

csv_path = r'data\processed\ika_ngo_cr6_gabungan.csv'

# Verbatim quotes mapped from the screenshots
quotes = {
    "Titik 1 (IMIP)": 'Tim AEER memilih delapan titik yang berbeda di sekitar kawasan IMIP guna mengambil sampel air yang kemudian diperiksa kadar Kromium Heksavalennya (Cr6+). Berdasarkan hasil analisis secara umum kualitas air laut di sekitar Kawasan IMIP sudah melebihi baku mutu baik untuk biota laut maupun untuk kegiatan wisata. Titik 1 mencatat kadar Cr6+ sebesar 0,004 mg/L yang melampaui baku mutu wisata bahari.',
    "Titik 2 (IMIP)": 'Tim AEER memilih delapan titik yang berbeda di sekitar kawasan IMIP guna mengambil sampel air yang kemudian diperiksa kadar Kromium Heksavalennya (Cr6+). Berdasarkan hasil analisis secara umum kualitas air laut di sekitar Kawasan IMIP sudah melebihi baku mutu baik untuk biota laut maupun untuk kegiatan wisata. Titik 2 mencatat kadar Cr6+ sebesar 0,028 mg/L yang melampaui baku mutu wisata bahari dan biota laut.',
    "Titik 3 (IMIP)": 'Tim AEER memilih delapan titik yang berbeda di sekitar kawasan IMIP guna mengambil sampel air yang kemudian diperiksa kadar Kromium Heksavalennya (Cr6+). Berdasarkan hasil analisis secara umum kualitas air laut di sekitar Kawasan IMIP sudah melebihi baku mutu baik untuk biota laut maupun untuk kegiatan wisata. Titik 3 mencatat kadar Cr6+ sebesar 0,07 mg/L yang melampaui baku mutu wisata bahari dan biota laut.',
    "Titik 4 (IMIP)": 'Tim AEER memilih delapan titik yang berbeda di sekitar kawasan IMIP guna mengambil sampel air yang kemudian diperiksa kadar Kromium Heksavalennya (Cr6+). Berdasarkan hasil analisis secara umum kualitas air laut di sekitar Kawasan IMIP sudah melebihi baku mutu baik untuk biota laut maupun untuk kegiatan wisata. Titik 4 mencatat kadar Cr6+ sebesar 0,01 mg/L yang melampaui baku mutu wisata bahari dan biota laut.',
    "Titik 5 (IMIP)": 'Tim AEER memilih delapan titik yang berbeda di sekitar kawasan IMIP guna mengambil sampel air yang kemudian diperiksa kadar Kromium Heksavalennya (Cr6+). Berdasarkan hasil analisis secara umum kualitas air laut di sekitar Kawasan IMIP sudah melebihi baku mutu baik untuk biota laut maupun untuk kegiatan wisata. Titik 5 mencatat kadar Cr6+ sebesar 0,005 mg/L yang melampaui baku mutu wisata bahari.',
    "Titik 6 (IMIP)": 'Tim AEER memilih delapan titik yang berbeda di sekitar kawasan IMIP guna mengambil sampel air yang kemudian diperiksa kadar Kromium Heksavalennya (Cr6+). Berdasarkan hasil analisis secara umum kualitas air laut di sekitar Kawasan IMIP sudah melebihi baku mutu baik untuk biota laut maupun untuk kegiatan wisata. Titik 6 mencatat kadar Cr6+ sebesar 0,004 mg/L yang melampaui baku mutu wisata bahari.',
    "Titik 7 (IMIP)": 'Tim AEER memilih delapan titik yang berbeda di sekitar kawasan IMIP guna mengambil sampel air yang kemudian diperiksa kadar Kromium Heksavalennya (Cr6+). Berdasarkan hasil analisis secara umum kualitas air laut di sekitar Kawasan IMIP sudah melebihi baku mutu baik untuk biota laut maupun untuk kegiatan wisata. Titik 7 mencatat kadar Cr6+ sebesar 0,021 mg/L yang melampaui baku mutu wisata bahari dan biota laut.',
    "Titik 8 (IMIP)": 'Tim AEER memilih delapan titik yang berbeda di sekitar kawasan IMIP guna mengambil sampel air yang kemudian diperiksa kadar Kromium Heksavalennya (Cr6+). Berdasarkan hasil analisis secara umum kualitas air laut di sekitar Kawasan IMIP sudah melebihi baku mutu baik untuk biota laut maupun untuk kegiatan wisata. Titik 8 mencatat kadar Cr6+ sebesar 0,023 mg/L yang melampaui baku mutu wisata bahari dan biota laut.',
    "Saluran Smelter Morosi": 'Sebagaimana Tabel 18 di atas, pengujian kualitas air yang bersumber dari saluran air di sekitar Smelter Nikel di Kecamatan Morosi... Hasil pengujian menunjukkan bahwa telah terjadi pencemaran air terutama kandungan Kromium Valensi VI (Cr6+), kandungan logam berbahaya tersebut terdeteksi sebanyak 0,1 mg/L atau sama dengan kadar maksimum yang dibolehkan dari aktivitas pengolahan nikel.',
    "Desa One Pute (Hulu)": 'Lokasi pengambilan titik berada di sungai Desa One Pute, di tiga titik lokasi yaitu hulu sungai titik 1, irigasi titik 2. Hasil Pengujian Kromium Heksavalen (Cr6+) Menunjukkan kontaminasi 0,1 mg/L yang dibolehkan dari aktivitas pengolahan nikel.',
    "Desa Dampala": 'Di Desa Dampala lokasi pengambilan titik berada di sungai utama. Hasil Pengujian Kromium Heksavalen (Cr6+) Menunjukkan kontaminasi 0,1 mg/L yang dibolehkan dari aktivitas pengolahan nikel.',
    "Desa Asuli (PT Vale)": 'Hasil uji kadar cemaran di tahun 2023 di sebuah aliran sungai kecil yang bermuara dekat dari laut ditemukan pencemaran kromium heksavalen sebesar 1 mg/L (ppm), angka ini melampaui 10 kali lipat ambang batas baku mutu lingkungan sebesar 0,1 mg/L.'
}

print("Loading CSV...")
df = pd.read_csv(csv_path)

# Update Kutipan_Lengkap based on Titik Sampling
for index, row in df.iterrows():
    titik = row['Titik Sampling']
    if titik in quotes:
        df.at[index, 'Kutipan_Lengkap'] = quotes[titik]

df.to_csv(csv_path, index=False)
print("CSV successfully updated with verbatim exact quotes from screenshots!")
