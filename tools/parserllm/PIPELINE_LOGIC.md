# ParserLLM (LLM-Based PDF/Text Extractor)

Folder ini berisi arsitektur *pipeline* **ParserLLM**, sebuah alat berbasis *Large Language Model* (AI) yang dirancang khusus untuk mem-parsing, menalar, dan mengekstrak nilai-nilai spesifik dari dokumen PDF / teks laporan (*Annual Report* / Profil Kesehatan) yang strukturnya hancur atau sangat berantakan.

Alat ini adalah "Senjata Pamungkas" jika teknik ekstraksi klasik gagal, seperti:
- **Regex / Mode (Frequency):** Sering menangkap sampah teks seperti Daftar Isi ("Gambar 3.1 Jumlah Puskesmas") atau subset data ("14 Puskesmas PONED").
- **PDF Table Parsers (Docling/OpenDataLoader):** Gagal merekonstruksi tabel kolom menjadi baris, sering mengorbankan hierarki baris akibat format *layout* PDF instansi pemerintah yang tidak berstandar. Atau menyebabkan *Out of Memory* (OOM).

## Data Provenance (Peta Arus Data)

Agar proses audit data transparan, berikut adalah pemetaan file dari hulu ke hilir:

1. **Source / Input (Raw Data):**
   - **Lokasi:** `data/raw/profil kesehatan provinsi_kemenkes/*.md`
   - **Asal Usul:** Berasal dari dokumen PDF *Annual Report* Profil Kesehatan setiap provinsi (2019-2024) yang dikonversi menjadi format Markdown mentah.
2. **Mesin Pemroses (Processor):**
   - **Lokasi Skrip:** `tools/parserllm/extract_faskes_llm.py`
   - **Alat Bantu Utama:** `openai` (GPT-4o-mini via API) dan `python-dotenv`.
3. **Destination / Output (Processed Data):**
   - **Lokasi:** `data/processed/sulawesi_faskes_agregat_v2.csv`
   - **Status:** Data bersih (*clean data*) berbentuk *tabular* (CSV) yang memuat jumlah definitif fasilitas kesehatan (Puskesmas & Rumah Sakit) per provinsi per tahun, siap divisualisasikan oleh Dasbor Analitik (Streamlit).

---

## Alur Logika Pipeline (Pipeline Logic)

Skrip utama `extract_faskes_llm.py` menggunakan **OpenAI GPT-4o-mini** (via API) dengan alur kerja berikut:

### 1. Ingest Data (Pembacaan Input)
Skrip membaca seluruh file berekstensi `.md` (Raw Data) yang ada di folder `data/raw/profil kesehatan provinsi_kemenkes/`.

### 2. Smart Text Chunking (Pemotongan Konteks)
File *annual report* sangat panjang (bisa 100+ halaman) dan mengonsumsi *token* API yang mahal serta memperlambat performa LLM. Skrip tidak membaca secara pasif seluruh teks, melainkan:
- Mencari baris-baris (lines) yang mengandung kata kunci spesifik (misal: `"jumlah rumah sakit"`, `"jumlah puskesmas"`).
- Jika ditemukan, skrip akan mengambil jendela teks (*context window*) berupa **10 baris ke atas** dan **10 baris ke bawah** dari baris penemuan kata kunci tersebut.
- Potongan-potongan teks tersebut lalu dijahit (*concatenated*) menjadi satu dokumen *summary* singkat.
- **Fail-safe:** Jika *keyword* sama sekali tidak ditemukan, alat ini akan mengambil 200 baris terakhir dari laporan (karena biasanya *Tabel Resume* berada di lampiran akhir dokumen).

### 3. Prompting & LLM Reasoning (Ekstraksi Nalar)
*Chunk text* yang ringkas namun padat konteks tadi dikirimkan ke model **GPT-4o-mini** dengan *prompt* (*System Instruction*) yang sangat *strict*:
> *"Baca teks di bawah, cari tahu TOTAL KESELURUHAN Puskesmas dan Rumah Sakit. Abaikan rasio, abaikan subset (seperti puskesmas rawat inap / PONED), dan abaikan nomor urut gambar. Kembalikan HANYA dalam bentuk format JSON murni: `{"puskesmas": X, "rumah_sakit": Y}`."*

Karena LLM memahami bahasa manusia, ia bisa membedakan mana angka yang merujuk pada "total fasilitas di satu provinsi" dan mana angka yang sekadar "nomor bab" atau "fasilitas khusus".

### 4. Output Formatting & Persistence (Penyimpanan)
- LLM membalas dengan struktur JSON yang valid (contoh: `{"puskesmas": 93, "rumah_sakit": 20}`).
- Python *script* akan mem-parsing JSON tersebut.
- Data lalu ditambahkan *(append)* ke dalam agregasi *Dataframe* Pandas.
- Di akhir iterasi seluruh provinsi dan tahun, agregat final diekspor bersih ke `data/processed/sulawesi_faskes_agregat_v2.csv`.

## Keunggulan
- **Anti-Noise:** Tidak terpengaruh kalimat pengecoh dari *Table of Contents*.
- **Cepat & Murah:** Menggunakan `GPT-4o-mini` dipadukan dengan teknik *text-chunking* membuat biayanya hampir gratis.
- **Standar Output:** Memaksa luaran berupa tabel *clean* yang siap dicolok langsung ke dalam Dasbor Analitik (Streamlit/Celios).
