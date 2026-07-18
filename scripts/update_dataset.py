import pandas as pd

# 1. Update sulawesi_limbah_b3.csv
df1 = pd.read_csv('data/processed/sulawesi_limbah_b3.csv')

# Remove hallucinated 'Unknown' rows
df1 = df1[~df1['Provinsi'].str.contains('Unknown')]

updates1 = {
    'IMIP (Morowali)': "Teks: 'Pada 2023, sekitar 12,5 juta ton limbah dengan kandungan besi dan mangan tersebut telah dikirim ke fasilitas penyimpanan yang oleh kedua perusahaan menyebutnya dalam dokumen AMDAL sebagai bendungan tailing.' (Hlm. 37, Laporan AEER 2024)",
    'VDNI (Konawe) & Sekitarnya': "Teks: 'Pada tahun 2020, PT. VDNI mengolah ore nikel sebanyak 7.28 juta ton.' (Hlm. 6, Riset Final WALHI SULTRA)",
    'Huadi Nickel Alloy (Bantaeng)': "Teks: 'Timbulan slag ini sudah diprediksi dalam dokumen AMDAL PT Huadi. Nickel Alloy. Volume yang dihasilkan pun tidak sedikit, jumlahnya mencapai kurang lebih 90% dari total bahan baku yang diproses di tungku EAF.' (Kajian JATAM 2023)",
    'PT Huayue Nickel Cobalt (HNC) - Morowali': "Teks: 'Jika produksi 1 ton logam nikel menghasilkan 100 ton tailing, maka dengan menghasilkan 70.000 ton MHP pada 2023, HNC telah memproduksi 7 juta ton tailing.' (Hlm. 37, Laporan AEER 2024)",
    'PT QMB New Energy Materials - Morowali': "Teks: 'Di tahun yang sama, jika QMB menghasilkan 55.000 ton MHP sesuai kapasitas produksinya, maka sekitar 5,5 juta tailing sudah diproduksi perusahaan itu.' (Hlm. 37, Laporan AEER 2024)",
    'PT SCM (Sulawesi Cahaya Mineral)': "Teks: 'SCM sendiri mengaku telah melepaskan lebih dari 800.000 ton air limbah tambang dan domestik ke Sungai Lalindu pada tahun 2022.' (Hlm. 36, Laporan AEER 2024)"
}

for kw, text in updates1.items():
    df1.loc[df1['Kawasan/Perusahaan'] == kw, 'Catatan'] = text

df1.to_csv('data/processed/sulawesi_limbah_b3.csv', index=False)

# 2. Update sulawesi_limbah_b3_ngo_proxy.csv
df2 = pd.read_csv('data/processed/sulawesi_limbah_b3_ngo_proxy.csv')

for kw, text in updates1.items():
    if kw in df2['Kawasan/Perusahaan'].values:
        df2.loc[df2['Kawasan/Perusahaan'] == kw, 'Catatan'] = text

df2.to_csv('data/processed/sulawesi_limbah_b3_ngo_proxy.csv', index=False)

print("Datasets updated successfully without hallucinations.")
