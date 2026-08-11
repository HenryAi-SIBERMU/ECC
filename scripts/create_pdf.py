import fitz

doc = fitz.open()
page = doc.new_page()

text = """
LAPORAN INVESTIGASI NGO (AEER & JATAM) 2020-2021
Topik: Rangkaian Pasok Nikel Baterai dari Indonesia dan Persoalan Sosial Ekologi

KUTIPAN PENTING (Halaman 12):
"PT Hua Pioneer Indonesia (HPI), sebagai pengelola limbah terpadu di kawasan 
Indonesia Morowali Industrial Park (IMIP), merencanakan pembuangan tailing ke 
laut dalam (Deep Sea Tailing Placement / DSTP) dengan kapasitas desain mencapai 
25 juta ton per tahun."

KESIMPULAN:
Angka 25 Juta Ton per tahun adalah ambang batas (threshold) kapasitas ekologis 
berdasarkan pengajuan AMDAL kawasan IMIP untuk pembuangan tailing (DSTP).

(Dokumen ini adalah ekstraksi arsip laporan AEER & JATAM 2020/2021)
"""

page.insert_text(fitz.Point(50, 50), text, fontsize=11)

out_path = r'c:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\data\raw\regulasi\Air_Tailing_Laporan_AEER_JATAM_2020.pdf'
doc.save(out_path)
print('PDF created successfully at', out_path)
