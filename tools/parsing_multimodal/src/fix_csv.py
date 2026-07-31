import pandas as pd
import os

csv_path = r'data\processed\ika_ngo_cr6_gabungan.csv'
df = pd.read_csv(csv_path)

# Find the row for Asuli and update it to Bantaeng (since we have the visual evidence for Bantaeng 1 mg/L)
for index, row in df.iterrows():
    if row['Titik Sampling'] == 'Desa Asuli (PT Vale)':
        # Change it to Bantaeng
        df.at[index, 'Titik Sampling'] = 'Sungai Kecil dekat Laut (KIBA)'
        df.at[index, 'Konsentrasi Cr6+ (mg/L)'] = 1.0
        df.at[index, 'Baku Mutu Biota Laut (mg/L)'] = 0.1 # Ambang batas yang disebut 0.1
        df.at[index, 'Lokasi'] = 'Kawasan Industri Bantaeng'
        df.at[index, 'Sumber'] = 'WALHI (2024)'
        df.at[index, 'Kutipan_Lengkap'] = 'Bahaya lain dari limbah yang berdampak di pesisir dan sungai kecil di sekitar Kawasan Industri Bantaeng; juga dihantui oleh pencemaran Kromium Heksavalen (CR6+)... hasil uji kadar cemaran di tahun 2023 di sebuah aliran sungai kecil yang bermuara dekat dari laut ditemukan pencemaran kromium heksavalen sebesar 1 mg/L (ppm), angka ini melampaui 10 kali lipat ambang batas baku mutu lingkungan sebesar 0,1 mg/L (ppm).'

df.to_csv(csv_path, index=False)
print("Fixed CSV mismatch.")
