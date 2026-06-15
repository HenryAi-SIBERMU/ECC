import pandas as pd
import csv

file_path = 'data/processed/sulawesi_limbah_b3_ngo_proxy.csv'

new_data = [
    {
        'Provinsi': 'Sulawesi Tengah',
        'Kawasan/Perusahaan': 'PT Huayue Nickel Cobalt (HNC) - Morowali',
        'Jenis Limbah B3': 'Tailing HPAL',
        'Estimasi Timbulan (Ton/Tahun)': 7000000,
        'Sumber Referensi': 'AEER HPAL Report (2024)',
        'Catatan': 'Hasil ekstraksi PDF. Menghasilkan 7 juta ton tailing dari 70.000 ton MHP pada tahun 2023.'
    },
    {
        'Provinsi': 'Sulawesi Tengah',
        'Kawasan/Perusahaan': 'PT QMB New Energy Materials - Morowali',
        'Jenis Limbah B3': 'Tailing HPAL',
        'Estimasi Timbulan (Ton/Tahun)': 5500000,
        'Sumber Referensi': 'AEER HPAL Report (2024)',
        'Catatan': 'Hasil ekstraksi PDF. Menghasilkan 5,5 juta ton tailing dari 55.000 ton MHP pada tahun 2023.'
    },
    {
        'Provinsi': 'Sulawesi Tengah',
        'Kawasan/Perusahaan': 'PT SCM (Sulawesi Cahaya Mineral)',
        'Jenis Limbah B3': 'Air Limbah Tambang',
        'Estimasi Timbulan (Ton/Tahun)': 800000,
        'Sumber Referensi': 'AEER HPAL Report (2024)',
        'Catatan': 'Hasil ekstraksi PDF. Melepaskan lebih dari 800.000 ton air limbah tambang ke Sungai Lalindu pada tahun 2022.'
    }
]

# Append the new data to the existing CSV
df_existing = pd.read_csv(file_path)
df_new = pd.DataFrame(new_data)

# To avoid duplicates, we can just append for now
df_combined = pd.concat([df_existing, df_new], ignore_index=True)
df_combined.to_csv(file_path, index=False)
print("Berhasil mengupdate CSV dengan data spesifik HNC, QMB, dan SCM.")
