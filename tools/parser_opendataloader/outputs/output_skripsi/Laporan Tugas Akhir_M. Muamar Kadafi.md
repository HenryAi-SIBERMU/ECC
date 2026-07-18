### PROPOSAL TUGAS AKHIR SIMULASI PROFIL PENYERAPAN ENERGI PADA PENGELASAN PADUAN ALUMINIUM 3003 DALAM PENGUJIAN IMPACT CHARPY

Diajukan untuk memenuhi persyaratan melaksanakan Tugas Akhir

![image 1](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile1.png>)

Disusun Oleh: Muhammad Muamar Kadafi 20210130074

PROGRAM STUDI TEKNIK MESIN FAKULTAS TEKNIK UNIVERSITAS MUHAMMADIYAH YOGYAKARTA 2025

HALAMAN PENGESAHAN TUGAS AKHIR SIMULASI PROFIL PENYERAPAN ENERGI PADA PENGELASAN PADUAN ALUMINIUM 3003 DALAM PENGUJIAN IMPACT CHARPY

SIMULATION OF ENERGY ABSORPTION PROFILE IN WELDED 3003 ALUMINUM ALLOY DURING CHARPY IMPACT TESTING

Disusun Oleh: Muhammad Muamar Kadafi 20210130074

Dosen Pembimbing I Dosen Pembimbing II

Dr. Ir. Bambang Riyanta, S.T., M.T NIK. 19710124 199603 123025

Fitroh Anugrah Kusuma Yudha, S.T., M.Eng. NIK. 201 430

ii

### HALAMAN PERNYATAAN

Saya yang bertanda tangan dibawah ini: Nama : Muhammad Muamar Kadafi Nim : 20210130074 Program Studi : Teknik Mesin Fakultas : Teknik Judul Penelitian : Simulasi Profil Penyerapan Energi pada Pengelasan Paduan Aluminium 3003 dalam Pengujian Impact Charpy

Menyatakan dengan ini bahwa tugas akhir yang saya tulis benar-benar merupakan hasil dari karya saya sendiri dan belum pernah diajukan untuk memperoleh gelar sarjana di perguruan tinggi manapun. Semua sumber yang berasal dari penulis lain sudah disebutkan dalam teks dan tercantum pada daftar Pustaka dibagian akhir dari tugas ini.

Apabila dikemudian hari tugas akhir yang saya buat terbukti merupakan hasil jiplakan maka saya bersedia menerima sanksi.

Yogyakarta, Agustus 2025 Penulis

Muhammad Muamar Kadafi 20210130074

iii

### MOTTO

![image 2](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile2.png>)

“Allah memang tidak pernah menjanjikan hidup seorang hamba-Nya akan selalu mudah, tapi dua kali allah berjanji bahwa; fa inna ma’al-‘usri yusra, inna ma’al-‘usri yusra”

### (QS. Al-Insyirah 94: 5-6)

iv

### UCAPAN TERIMAKASIH

Puji syukur panjatkan ke hadirat Allah SWT atas segala rahmat, hidayah dan karunia-Nya sehingga penulis dapat menyelesaikan tugas akhir ini yang berjudul “Simulasi Profil Penyerapan Energi pada Pengelasan Paduan Aluminium 3003 dalam Pengujian Impact Charpy” sebagai salah satu syarat untuk memperoleh gelar Sarjana Teknik pada Program Studi Teknik Mesin, Fakultas Teknik, Universitas Muhammadiyah Yogyakarta.

Dalam penyusunan tugas akhir ini, penulis menyadari bahwa banyak pihak yang telah memberikan dukungan, bimbingan dan motivasi, baik secara langsung maupun tidak langsung. Oleh karena itu, penulis ingin menyampaikan terima kasih yang sebesar-besarnya kepada:

- 1. Kedua orang tua tercinta Bapak Sun’an dan ibu Atin atas doa yang tiada henti, cinta yang tulus, serta dukungan moral dan material yang tak tergantikan.
- 2. Ucapan terima kasih saya sampaikan kepada Dr. Ir. Bambang Riyanta, S.T., M.T., selaku dosen pembimbing I, atas bimbingan, arahan, serta motivasi yang sangat berharga selama proses penelitian dan penyusunan tugas akhir ini."
- 3. Ucapan terima kasih saya sampaikan kepada Fitroh Anugrah Kusuma Yudha, S.T., M.Eng., selaku dosen pembimbing II, atas kesabaran membimbing saya dalam memahami proses simulasi dan metodologi penelitian.
- 4. Terima kasih kepada seluruh teman-teman anggota Domum Or Casa yang tidak dapat disebutkan namanya satu per satu. Terima kasih telah menjadi rekan seperjuangan bagi saya.


v

### KATA PENGANTAR

Alhamdulillaahi Robbil’aalamiin, puji syukur kehadirat Allah SWT yang telah melimpahkan rahmat dan karunia-Nya sehingga penulis dapat menyelesaikan Tugas Akhir yang berjudul “Simulasi Profil Penyerapan Energi Pada Pengelasan Paduan Aluminium 3003 Dalam Pengujian Impact Charpy”. Penulis merasa sangat bersyukur atas berhasil menyelesaikan tugas akhir ini, yang merupakan salah satu persyaratan untuk mendapatkan gelar sarjana, serta sebagai bukti penyelesaian pendidikan sarjana di Program Studi Teknik Mesin, Fakultas Teknik, Universitas Muhammadiyah Yogyakarta. Di samping itu, penulis ingin mengucapkan terima kasih kepada semua individu yang telah memberikan bantuan dan dukungan selama proses penyusunan Tugas Akhir ini.

Dalam penulisan Tugas Akhir ini, penulis memahami bahwa laporan ini belum mencapai tingkat kesempurnaan. Oleh karena itu, penulis sangat mengharapkan kritik dan saran yang bersifat konstruktif dari semua pihak demi meningkatkan kualitas laporan Tugas Akhir ini. Penulis berharap bahwa laporan Tugas Akhir ini akan membawa manfaat, baik bagi penulis sendiri maupun bagi para pembaca, dan diharapkan dapat menjadi referensi yang berguna untuk penelitian masa depan.

Yogyakarta, Agustus 2025 Penulis

Muhammad Muamar Kadafi 20210130074

vi

DAFTAR ISI HALAMAN PENGESAHAN...............................................................................................ii HALAMAN PERNYATAAN..............................................................................................iii MOTTO................................................................................................................................iv UCAPAN TERIMAKASIH .................................................................................................. v KATA PENGANTAR..........................................................................................................vi DAFTAR ISI .......................................................................................................................vii DAFTAR GAMBAR............................................................................................................ix DAFTAR TABEL ................................................................................................................xi LAMPIRAN ........................................................................................................................xii INTISARI...........................................................................................................................xiii ABSTRAK .........................................................................................................................xiv

- BAB I PENDAHULUAN ..................................................................................................... 1

- 1.1. Latar Belakang............................................................................................................ 1
- 1.2. Rumusan Masalah ...................................................................................................... 2
- 1.3. Batasan Masalah......................................................................................................... 2
- 1.4. Tujuan Penelitian........................................................................................................ 3
- 1.5. Manfaat Penelitian...................................................................................................... 3


- BAB II TINJAUAN PUSTRAKA DAN DASAR TEORI ................................................... 4

- 2.1. Tinjauan Pustaka ........................................................................................................ 4
- 2.2. Dasar Teori ................................................................................................................. 8

- 2.2.1. Pengelasan........................................................................................................... 8
- 2.2.2. Aluminium ........................................................................................................ 11
- 2.2.3. Pengujian Impact ............................................................................................... 15
- 2.2.4. Software Ansys .................................................................................................. 18


BAB III METODOLOGI .................................................................................................... 21

- 3.1. Diagram Alir............................................................................................................. 21




- 3.2. Studi Literatur........................................................................................................... 21
- 3.3. Alat dan Bahan ......................................................................................................... 22

- 3.3.1. Alat.................................................................................................................... 22
- 3.3.2. Bahan................................................................................................................. 22


- 3.4. Langkah Penelitian ................................................................................................... 22


- 3.3.1. Pre-processing .................................................................................................. 23


vii

- viii
- 3.3.2. Processing ......................................................................................................... 26
- 3.3.3. Post-processing ................................................................................................. 27

BAB IV HASIL DAN PEMBAHASAN............................................................................. 26

- 4.1. Hasil Perhitungan ..................................................................................................... 26


- 4.2. Hasil Simulasi Pengujian Impact Charpy ................................................................. 26

- 4.2.1. Weld Metal ........................................................................................................ 26
- 4.2.2. Base Metal ......................................................................................................... 30
- 4.2.3. Heat Affected Zone ............................................................................................ 34


- 4.3. Perbandingan Hasil Simulasi Impact Charpy per zona............................................ 39

- 4.3.1. Total Deformasi................................................................................................. 39
- 4.3.2. Equivalent Stress ............................................................................................... 40
- 4.3.3. Equivalent Elastic Strain ................................................................................... 41
- 4.3.4. Energi Probe ..................................................................................................... 42

4.4. Grafik Laju Serapan Energi...................................................................................... 43 4.5. Validasi Data Hasil Simulasi Uji Impact Charpy ..................................................... 44 BAB V PENUTUP............................................................................................................. 38

- 5.1. Kesimpulan............................................................................................................... 38




- 5.2. Saran......................................................................................................................... 38 DAFTAR PUSTAKA.......................................................................................................... 40 LAMPIRAN ........................................................................................................................ 43


### DAFTAR GAMBAR

- Gambar 2. 1. Gas Tungsten Arc Welding ............................................................................. 9
- Gambar 2. 2. Gas Metal Arc Welding................................................................................... 9
- Gambar 2. 3. Resistance Welding ....................................................................................... 10
- Gambar 2. 4. Friction Stir Welding..................................................................................... 10
- Gambar 2. 5. Laser Beam Welding ..................................................................................... 11
- Gambar 2. 6. Tempa (wrought) dan Tuang (cast) ............................................................... 11
- Gambar 2. 7. Metode Charpy dan Metode Izod (Mildayati Nurdin dkk., 2021)................. 15
- Gambar 2. 8. Alat Uji Impact dan Ukuran Spesimen (Murugan, 2020).............................. 16
- Gambar 2. 9. Grafik Daerah Ulet, Getas dan Transisi......................................................... 18


- Gambar 3. 1. Diagram Alir 1............................................................................................... 21
- Gambar 3. 2. Desain Geometri 3D ...................................................................................... 22
- Gambar 3. 3. Desain dan Ukuran Spesimen........................................................................ 23
- Gambar 3. 4. Point Mass ..................................................................................................... 24
- Gambar 3. 5. Meshing ......................................................................................................... 25
- Gambar 3. 6. End Time atau Time Step .............................................................................. 25
- Gambar 3. 7. Initial Condition............................................................................................. 26
- Gambar 3. 8. Processing Error, B Processing Berjalan dan C Processing Berhasil............ 26
- Gambar 3. 9. Gambar Visualisasi Hasil Simulasi ............................................................... 27


- Gambar 4. 1. Visualisasi Total Deformasi .......................................................................... 26
- Gambar 4. 2. Grafik Total Deformasi.................................................................................. 27
- Gambar 4. 3. Visualisasi Equivalen Stress.......................................................................... 27
- Gambar 4. 4. Grafik Hubungan Tegangan dan Waktu........................................................ 28
- Gambar 4. 5. Visualisasi Equivalent Strain......................................................................... 28
- Gambar 4. 6. Grafik Hubungan Regangan dan Waktu........................................................ 29
- Gambar 4. 7. Visualisasi Energi Internal............................................................................. 29
- Gambar 4. 8. Grafik Hubungan Energi Internal dan Waktu................................................ 30
- Gambar 4. 9. Visualisasi total deformasi............................................................................. 30
- Gambar 4. 10. Grafik Hubungan Total Deformasi dan Waktu ........................................... 31
- Gambar 4. 11. Visualisasi equivalent stress ........................................................................ 31
- Gambar 4. 12. Grafik Hubungan Tegangan dan Waktu...................................................... 32
- Gambar 4. 13.Visualisasi equivalent elastic strain.............................................................. 32
- Gambar 4. 14. Grafik Hubungan Regangan dan Waktu...................................................... 33


ix

- Gambar 4. 15. Visualisasi Energi Internal........................................................................... 33
- Gambar 4. 16. Grafik Hubungan Energi Internal dan Waktu.............................................. 34
- Gambar 4. 17. Visualisasi Total Deformasi ........................................................................ 34
- Gambar 4. 18. Grafik Hubungan Total Deformasi dan Waktu ........................................... 35
- Gambar 4. 19. Visualisasi Equivalent Stress....................................................................... 35
- Gambar 4. 20. Grafik Hubungan Tegangan dan Waktu...................................................... 36
- Gambar 4. 21. Visualisasi Equivalent Elastic Srain ............................................................ 36
- Gambar 4. 22. Grafik Hubungan Regangan dan Waktu...................................................... 37
- Gambar 4. 23. Visualisasi Energi Internal........................................................................... 38
- Gambar 4. 24. Grafik Hubungan Energi Internal dan Waktu.............................................. 38
- Gambar 4. 25. Grafik Perbandingan Total Deformasi dan Waktu ...................................... 39
- Gambar 4. 26. Grafik Perbandingan Equivalent Stress dan Waktu..................................... 40
- Gambar 4. 27. Grafik Perbandingan Equivalent Elastic Strain dan Waktu......................... 41
- Gambar 4. 28. Grafik Perbanding Energi Internal dan Waktu ............................................ 42
- Gambar 4. 29. Grafik Laju Serapan Energi, Fenomena Overshoot Negatif a dan Variasi Cacah Puncak b ................................................................................................................... 43


- x


### DAFTAR TABEL

- Tabel 2. 1. Sifat Fisik Aluminum 3003 ............................................................................... 12
- Tabel 2. 2. Sifat Mekanik Aluminium 3003........................................................................ 12
- Tabel 2. 3. Kandungan Unsur Aluminium 3003 ................................................................. 15


- Tabel 3. 1. Spesifikasi Komputer ........................................................................................ 22
- Tabel 3. 2. Property Aluminium 3003................................................................................. 24


- xi


### LAMPIRAN

- Lampiran 1. Parameter spesimen weld metal...................................................................... 43
- Lampiran 2. Property Filler ER4043................................................................................... 43
- Lampiran 3. Visualisasi Energi Probe................................................................................. 43
- Lampiran 4. Data Hasil Simulasi......................................................................................... 44
- Lampiran 5. Parameter HAZ ............................................................................................... 45
- Lampiran 6. Property HAZ.................................................................................................. 45
- Lampiran 7. Visualisasi Energi Probe................................................................................. 46
- Lampiran 8. Data Hasil Simulasi......................................................................................... 46
- Lampiran 9. Parameter Base Metal ..................................................................................... 47
- Lampiran 10. Property Base Metal...................................................................................... 48
- Lampiran 11. Visualisasi Energi Probe............................................................................... 48
- Lampiran 12. Data Hasil Simulasi....................................................................................... 48
- Lampiran 13. Parameter Validasi Aluminium 5052............................................................ 50
- Lampiran 14. Property Aluminium 5052 ............................................................................ 50
- Lampiran 15. Data Hasil Simulasi Al 5052......................................................................... 50


xii

### INTISARI

Aluminium 3003 merupakan material non-heat-treatable yang tergolong logam ringan, tahan korosi, kekuatan sedang dan mudah dalam proses pembentukan. Material ini memiliki kandungan mangan (Mn) sebagai unsur utama yang memberikan sifat-sifat unggul, sehingga dapat diproses dengan berbagai metode pengelasan. Tujuan penelitian ini adalah memperoleh hasil simulasi profil penyerapan energi pada aluminium 3003 hasil pengelasan dalam uji impact charpy menggunakan metode Finite Element Method (FEM) yang diimplementasikan melalui perangkat lunak ansys.

Penelitian ini menggunakan material aluminium 3003 sebagai bahan utama, filler ER4043 sebagai bahan tambahan untuk pengelasan dan structural steel. Bentuk bahan yang digunakan pada penelitian ini yaitu 3 dimensi dengan ukuran sesuai standar ASTM E23. Software yang digunakan untuk pembuatan geometri yaitu Solidworks 2025 dan untuk simulasi yaitu ANSYS Fluent 2025 R1. Beban yang diberikan pada pendulum adalah sebesar 5,8 kg dengan kecepatan awal 4989,57 mm/s, sebagai input parameter dalam simulasi untuk merepresentasikan kondisi uji impak secara realistis.

Hasil penelitian ini menunjukkan bahwa base metal memiliki performa terbaik dalam menyerap energi impak, ditandai dengan nilai deformasi maksimum sebesar 15.346 mm, tegangan maksimum 4.690,3 MPa, regangan maksimum 0,0773 mm/mm, serta energi internal maksimum 54,532 Joule. Sebaliknya, weld metal menunjukkan performa paling rendah dalam deformasi sebesar 5.058,6 mm, namun memiliki sifat keras dan kaku dengan tegangan maksimum 3.482,5 MPa, regangan maksimum 0,0617 mm/mm dan energi internal sebesar 37,966 Joule. Heat Affected Zone (HAZ) menunjukkan karakteristik sedang dengan deformasi sebesar 12.330 mm, tegangan maksimum 3.768,6 MPa, regangan maksimum 0,0618 mm/mm, tetapi memiliki energi internal paling rendah yaitu 31,929 Joule. Perbedaan performa ini disebabkan oleh pengaruh signifikan perubahan mikrostruktur akibat proses pengelasan.

Kata Kunci: Aluminium 3003, impact charpy, Finite Element Method, Ansys Fluent 2025, energi internal.

xiii

### ABSTRAK

Aluminum 3003 is a non-heat-treatable material classified as a lightweight metal, corrosion-resistant, with moderate strength and easy formability. This material contains manganese (Mn) as the primary element, which provides superior properties, making it suitable for various welding methods. The purpose of this study is to obtain simulation results of the energy absorption profile of welded aluminum 3003 in a Charpy impact test using the Finite Element Method (FEM) implemented through ANSYS software.

This research utilizes aluminum 3003 as the primary material, filler ER4043 as supplementary material for welding, and structural steel. The shape of the specimen used is three-dimensional, following the ASTM E23 standard. The geometry was created using Solidworks 2025, and the simulation was performed using ANSYS Fluent 2025 R1. A pendulum load of 5.8 kg with an initial velocity of 4989.57 mm/s was used as input parameters to realistically represent impact test conditions.

The results of this study indicate that the base metal exhibits the best performance in absorbing impact energy, evidenced by a maximum deformation of 15.346 mm, maximum stress of 4,690.3 MPa, maximum strain of 0.0773 mm/mm, and maximum internal energy of 54.532 Joules. Conversely, the weld metal exhibited the lowest deformation performance of

- 5.0586 mm but had hard and rigid properties with maximum stress of 3,482.5 MPa, maximum strain of 0.0617 mm/mm, and internal energy of 37.966 Joules. The Heat Affected Zone (HAZ) displayed moderate characteristics, with deformation of 12.330 mm, maximum stress of 3,768.6 MPa, maximum strain of 0.0618 mm/mm, yet the lowest internal energy of 31.929 Joules. These performance differences result significantly from microstructural changes due to the welding process.


Keywords: Aluminum 3003, impact Charpy, Finite Element Method, ANSYS Fluent 2025, internal energy.

xiv

- 1.1. Latar Belakang


BAB I PENDAHULUAN

Aluminium dan paduannya adalah material non-ferrous yang memiliki sifat ringan, tahan korosi dan fleksibel, sehingga dapat disesuaikan dengan berbagai kebutuhan industri. Material ini juga tergolong sebagai logam ringan dengan kekuatan yang dapat melebihi baja ringan (Riyanta dkk., 2024). Salah satu paduan aluminium yang banyak digunakan dalam industri adalah aluminium 3003 yang tergolong nonheat-treatable dan memiliki ketahanan korosi yang baik, kekuatan sedang, serta kemudahan dalam proses pembentukan. Kandungan mangan (Mn) sebagai unsur utama memberikan sifat-sifat unggulan tersebut (Lu dkk., 2024). Selain itu, paduan ini dapat diproses dengan berbagai metode pengelasan yang menghasilkan sambungan dengan ketahanan korosi tinggi serta deformasi yang rendah.

Pengelasan memainkan peran penting dalam meningkatkan efisiensi produksi serta kualitas hasil manufaktur di berbagai sektor industri, seperti perkapalan, otomotif, dan penerbanga (Wurdhani dkk., 2021). Pengelasan dapat diklasifikasikan berdasarkan metode yang digunakan, seperti pengelasan fusi, pengelasan tekanan dan pengelasan patri. Kualitas pengelasan yang optimal bergantung pada pengendalian proses pengelasan serta kesesuaian jenis material yang digunakan. Dalam berbagai proses pengelasan, paduan aluminium 3003 menjadi salah satu material yang memikat karena kemampuannya dalam membentuk sambungan yang kuat serta tahan terhadap korosi. Material berbasis paduan aluminium seringkali digunakan dalam struktur yang menerima pembebanan impak. Untuk mengevaluasi lebih lanjut mengenai ketangguhan material dan sambungan las terhadap pembebanan tersebut perlu dilakukan pengujian impact charpy.

Pengujian impact charpy adalah metode untuk mengetahui ketangguhan dan energi yang diserap oleh material saat patah akibat pembebanan mendadak. Tujuan pengujian ini adalah memahami kemampuan material dalam menahan beban tumbuk dengan mengukur energi yang dibutuhkan untuk mematahkan spesimen (Firmansyah, 2021). Pengujian ini dapat dimodifikasi dengan menambahkan sistem akuisisi data untuk meningkatkan efisiensi dan akurasi. Seperti penelitian yang dilakukan oleh

1

(Riyanta dkk., 2024) menunjukan bahwa metode ini dapat memberikan kesempatan untuk memahami profil penyerapan energi baik dalam kondisi base metal maupun setelah pengelasan selama tumbukan berlangsung. Namun, penerapan metode tersebut memerlukan upaya dan biaya yang lebih besar.

Sebagai alternatif, penggunaan simulasi numerik dengan metode Finite Element Method (FEM) dapat membantu untuk memahami profil penyerapan energi akibat pembebanan impak. Metode elemen hingga yang didukung software seperti ansys dan solidworks dapat memprediksi mekanika kontinu dengan membagi domain material menjadi elemen-elemen kecil melalui proses meshing (Wibawa, 2019). Seperti penelitian yang dilakukan oleh (Arif dkk., 2023) menggunakan metode elemen hingga untuk menganalisis distrbusi tegangan, deformasi, penyerapan energi dan faktor keamanan pada material aluminium 5052 setelah pengelasan selama tumbukan berlangsung.

Penelitian ini bertujuan untuk menganalisis profil penyerapan energi pada pengelasan paduan aluminium 3003 melalui simulasi numerik berbasis FEM dalam pengujian impact charpy. Simulasi ini diharapkan mampu memberikan pemahaman yang lebih mendalam mengenai perilaku material selama pembebanan impak, sehingga dapat menjadi referensi dalam penerapan material pada perancangan industri.

### 1.2. Rumusan Masalah

Berdasarkan latar belakang yang telah dijelaskan, rumusan masalah dalam penelitian ini yaitu bagaimana mendapatkan profil penyerapan energi pada pengelasan paduan aluminium 3003 melalui pengujian impact charpy untuk memahami karakteristik material tersebut terhadap pembebanan impak.

### 1.3. Batasan Masalah

Berdasarkan rumusan masalah diatas maka didapatkan batasan masalah, sebagai berikut:

- 1. Simulasi numerik menggunakan metode Finite Element Method (FEM) untuk menganalisis profil penyerapan energi dalam pengujian impact charpy.
- 2. Simulasi dilakukan dengan asumsi kondisi pembebanan impak ideal sesuai standar pengujian impact charpy.


### 1.4. Tujuan Penelitian

Penelitian ini bertujuan untuk mendapatkan hasil simulasi profil penyerapan energi pada paduan aluminium 3003 yang telah mengalami proses pengelasan dalam pengujian impact charpy menggunakan metode numerik berbasis Finite Element Method (FEM) yang diimplementasikan melalui perangkat lunak ansys.

#### 1.5. Manfaat Penelitian Adapun manfaat dilakukan penelitian ini, sebagai berikut:

- 1. Menyediakan informasi mengenai karakteristik penyerapan energi paduan aluminium 3003 yang dapat dimanfaatkan untuk mendukung perancangan dan pemilihan material dalam penerapan industri.
- 2. Menambah referensi ilmiah mengenai pengujian impak dan profil penyerapan energi pada material paduan aluminium 3003.
- 3. Menjadi dasar penelitian lebih lanjut mengenai simulasi numerik pengujian material.


BAB II TINJAUAN PUSTRAKA DAN DASAR TEORI

- 2.1. Tinjauan Pustaka


Penelitian yang dilakukan oleh Riyanta dkk., (2024) memodifikasi alat uji impact charpy GOTECH dengan menambahkan instrumen digital, termasuk load cell, amplifier, data acquisition device dan power supply, sesuai standar ASTM E23-02a. Penelitian ini mengevaluasi profil penyerapan energi aluminium 5052 dan 6061 pada spesimen logam dasar dan hasil pengelasan TIG dengan kampuh V 60°. Hasilnya menunjukkan bahwa aluminium 6061 memiliki ketangguhan impak lebih tinggi dibandingkan aluminium 5052, sementara aluminium 5052 memiliki keuletan yang lebih baik. Energi yang diserap oleh spesimen logam dasar lebih tinggi dibandingkan dengan spesimen hasil pengelasan yang memiliki nilai rata-rata deviasi antara pengukuran manual dan digital sebesar 11,716 J untuk aluminium 5052 logam dasar dan 0,729 J untuk aluminium 6061 logam dasar. Modifikasi alat ini dinyatakan efektif dalam meningkatkan akurasi dan konsistensi pengujian yang memungkinkan pengumpulan data energi serap secara lebih andal dan efisien.

Penelitian yang dilakukan oleh Mildayati Nurdin dkk., (2021) mengevaluasi pengaruh variasi temperatur terhadap kekuatan impak sambungan las listrik pada material besi plat ST 42 menggunakan metode charpy. Hasil penelitian menunjukkan bahwa pada temperatur tinggi (78–79 °C) kekuatan impak rata-rata spesimen mencapai 0,3902 J/mm², sementara pada temperatur rendah (-4 hingga -8 °C) kekuatan impak rata-rata menurun drastis menjadi 0,0106 J/mm². Spesimen pada temperatur tinggi mengalami patahan ulet dengan permukaan berserat dan buram, sedangkan pada temperatur rendah mengalami patahan getas dengan permukaan berbutir dan mengkilap. Penelitian ini menunjukan bahwa temperatur berpengaruh terhadap ketangguhan material pada kondisi suhu tinggi material lebih ulet dan pada suhu rendah material lebih getas.

Penelitian yang dilakukan oleh Arif dkk., (2023) menganalisis tegangan dan displacement pada material aluminium 5052 melalui simulasi numerik dengan perangkat lunak solidworks 2017 dengan variasi sudut kampuh (60°, 70°, 80° dan 90°). Berdasarkan hasil simulasi menunjukkan bahwa tegangan tertinggi terjadi pada sudut

4

60° sebesar 33,146 MPa, sedangkan tegangan terendah terjadi pada sudut 70° sebesar 0,193 MPa. Displacement maksimum tercatat sebesar 0,010 mm dengan perubahan yang diizinkan hingga 0,07 mm sebelum deformasi plastis terjadi. Material menunjukkan deformasi plastis pada displacement di atas 1 mm, tetapi tetap berada dalam batas aman pada displacement kurang dari 1 mm, sehingga dapat disimpulkan bahwa spesimen aman digunakan untuk aplikasi tertentu dalam kondisi pembebanan statis.

Penelitian oleh Ariyanto, (2024) mengevaluasi pengaruh variasi arus listrik pengelasan GMAW pada aluminium 5052 menggunakan elektroda ER4043 melalui uji impact charpy. Hasil penelitian menunjukkan bahwa pada arus 200A energi impak yang dihasilkan adalah 55,012 J dengan ketangguhan 0,687 J/mm², sementara pada arus 210 A energi impak meningkat menjadi 64,34 J dengan ketangguhan 0,804 J/mm². Penelitian ini menyimpulkan bahwa peningkatan arus listrik pengelasan menghasilkan sambungan las yang lebih ulet, sedangkan arus yang lebih rendah menghasilkan sambungan yang lebih keras namun cenderung mudah patah. Penelitian ini menegaskan pentingnya pengaturan arus listrik dalam pengelasan untuk mencapai kekuatan optimal.

Penelitian oleh Hardi & Umron, (2022) menggunakan simulasi numerik berbasis metode elemen hingga dengan perangkat lunak ansys explicit dynamics untuk menganalisis respon tabung silinder berdinding tipis dari aluminium alloy terhadap beban tumbukan aksial dengan variasi kecepatan (5–250 m/s). Hasil penelitian menunjukkan bahwa gaya reaksi maksimum meningkat seiring bertambahnya kecepatan tumbukan dari 8873,1 N dengan kecepatan 5 m/s hingga 10.275 N dengan kecepatan 150 m/s. Pola deformasi pada tabung tetap axis-symmetric meskipun kecepatan meningkat. Pada kecepatan tinggi, deformasi terjadi sepanjang tabung secara bersamaan yang dapat meningkatkan efisiensi penyerapan energi kinetik. Penelitian ini memberikan rekomendasi untuk pengembangan struktur berdinding tipis sebagai penyerap energi pada aplikasi dinamik.

Penelitian oleh Isworo dkk., (2020) mengevaluasi kekuatan mekanik dan struktur mikro aluminium 6061 setelah proses pengelasan TIG dengan variasi media pendingin, seperti air laut, air tawar dan udara alami. Hasilnya menunjukkan bahwa pendinginan dengan air laut menghasilkan nilai impak tertinggi sebesar 0,261 J/mm², sementara air tawar mencapai 0,237 J/mm² dan udara alami hanya 0,085 J/mm².

Kekuatan tarik tertinggi ditemukan pada spesimen dengan pendinginan air tawar sebesar 160,53 MPa dan regangan 25,26%, sedangkan air laut menghasilkan kekuatan tarik 160,09 MPa dan udara alami 150,01 MPa. Uji tekuk menunjukkan kekuatan bending tertinggi pada media air tawar (46,88 MPa), air laut (43,38 MPa) dan udara alami (34,11 MPa). Analisis mikrografi mengungkapkan bahwa struktur mikro pada spesimen dengan media pendingin lebih rapat dibandingkan pendinginan alami yang dapat meningkatkan kekerasan dan ketahanan material terhadap deformasi. Penelitian ini menegaskan bahwa media pendingin signifikan dalam mempengaruhi sifat mekanik aluminium 6061 paska pengelasan.

Penelitian oleh Sifa & Endarmawan, (2013) menggunakan simulasi numerik berbasis element hingga dengan software ABAQUS dilakukan untuk menguji spesimen aluminium 2024 dengan alat uji impak hasil rancang bangun uji. Hasil penelitian menunjukan bahwa tegangan dan regangan kritis terjadi pada node 9 dan 12 dengan perubahan nilai impak pada setiap kontur. Nilai impak maksimum tercatat sebesar 17,71 J, sementara nilai minimum mencapai -1,415 J. Pola patahan pada spesimen menunjukkan bahwa material Aluminium 2024 memiliki karakteristik patahan ulet (ductile fracture) ditandai dengan bidang pergeseran dan permukaan patahan yang berserat. Hasil simulasi dan pengujian aktual menunjukkan kesesuaian dan mengonfirmasi keandalan model yang digunakan.

Penelitian oleh (Kori dkk., 2025) menggunakan simulasi numerik berbasis elemen hingga dengan software ANSYS 2022R1 berbasis explicit dynamics dan model material Johnson–Cook untuk menganalisis perilaku mekanisme patah pada baja multiphase Q&P dengan kandungan mangan sedang (5 wt.% Mn), pengaruh geometria notch, waktu partitioning dan ketebalan plat terhadap energi serap, distribusi tegangan dan proses fraktur selama kondisi beban dinamis. Hasil penelitian ini menunjukan bahwa mikro struktur pada baja Q&P dengan kandungan mangan 5 wt.% terdiri dari martensit primer, retained austenite dan sebagian martensit sekunder yang relatif tidak terlalu dipengaruhi oleh waktu partitioning antara 300 hingga 900 detik. Simulasi menggunakan model Johnson–Cook berhasil memprediksi respon uji impak charpy secara akurat dengan konsentrasi tegangan tinggi terfokus di area sekitar takik, seperti pada radius 0,1 mm yang menyebabkan retak lebih awal dibanding radius 0,25 mm. Meskipun perbedaan radius takik tidak berdampak signifikan terhadap energi serap,

akan tetapi pelat dengan ketebalan 7 mm dan 12 mm mampu meningkatkan energi serap sebesar 12–14%. Waktu partitioning hanya memberikan pengaruh kecil terhadap kekuatan tarik, tetapi cenderung mengurangi ketangguhan dan keuletan, terutama pada pelat 7 mm. Secara keseluruhan, kombinasi parameter proses, geometri takik dan ketebalan pelat sangat berperan dalam menentukan distribusi tegangan dan energi serap, sehingga pemahaman faktor-faktor ini penting untuk meningkatkan performa baja Q&P dalam aplikasi struktural dan industri berkebutuhan tinggi.

Penelitian oleh (Parthiban dkk., 2018) menganalisi karakteristik energi tumbukan dan perilaku fraktur baja lunak tipe C1018 melalui simulasi numerik berbasis metode elemen hingga menggunakan perangkat lunak Abaqus 6.14 dan model kerusakan Johnson–Cook. Model numerik yang dikembangkan divalidasi melalui hasil uji impact Charpy secara eksperimen dengan tingkat kecocokan yang signifikan antara simulasi dan data eksperimen. Hasil simulasi menunjukkan bahwa energi tumbukan yang diserap mencapai 95,33 Joule untuk base metal dan meningkat menjadi 106,85 Joule pada spesimen hasil pengelasan dengan tegangan maksimum masing-masing sebesar 401,4 MPa dan 405,4 MPa. Pola deformasi selama tumbukan memperlihatkan konsistensi antara hasil numerik dan eksperimen, serta menunjukkan deformasi aksial yang tetap simetris meskipun kecepatan tumbukan bertambah. Temuan ini menegaskan bahwa proses pengelasan seperti spin arc welding mampu meningkatkan kapasitas serapan energi material. Secara keseluruhan, hasil studi ini memberikan kontribusi penting bagi pengembangan struktur berdinding tipis yang efisien dalam menyerap energi pada kondisi dinamis dan kecepatan tinggi.

Berbagai penelitian menunjukkan bahwa pengujian impak secara eksperimental maupun simulasi numerik efektif dalam mengevaluasi sifat mekanik dan karakteristik penyerapan energi pada material logam, seperti aluminium dan baja dalam berbagai kondisi. Modifikasi instrumen uji impak meningkatkan akurasi pengukuran energi serap, sedangkan variasi parameter seperti temperatur, arus listrik pengelasan, sudut kampuh, media pendinginan, geometri spesimen dan kecepatan tumbukan secara signifikan mempengaruhi ketangguhan, keuletan, serta mekanisme fraktur material. Secara umum, temperatur tinggi, arus pengelasan optimal, pendinginan cepat dan desain struktur tertentu dapat meningkatkan sifat ulet dan ketahanan material terhadap beban dinamis. Simulasi numerik berbasis metode elemen hingga, seperti yang dilakukan

menggunakan perangkat lunak ANSYS, ABAQUS, maupun SolidWorks terbukti mampu secara akurat memprediksi respon mekanik, distribusi tegangan, deformasi dan energi serap, serta memberikan rekomendasi penting dalam pengembangan struktur dan material untuk aplikasi industri yang membutuhkan ketahanan terhadap beban impak atau tumbukan.

### 2.2. Dasar Teori

- 2.2.1. Pengelasan Pengelasan merupakan proses penyambungan material dua atau lebih dengan


memanfaatkan energi panas untuk melelehkan material, sehingga tercipta sambungan yang kuat. Proses ini dapat diartikan sebagai penyambungan material melalui pemanasan hingga suhu yang diperlukan tanpa menggunakan tekanan atau logam pengisi, sehingga menghasilkan sambungan yang kontinu (Zulfadly & Ghony, 2022). Energi yang digunakan untuk melelehkan material dalam pengelasan dapat berasal dari berbagai sumber, seperti listrik, gas, laser atau gesekan.

Pengelasan umumnya dibagi menjadi beberapa kategori utama, yaitu:

- 1. Pengelasan Oksi-Gas (Oxy Fuel Welding) merupakan pengelasan yang memanfaatkan gas oksigen dan acetylene untuk menghasilkan panas.
- 2. Pengelasan Listrik (Arc Welding) merupakan proses pengelasan yang memanfaatkan arus listrik sebagai sumber panas untuk melelehkan material.
- 3. Pengelasan Fisik (Solid-state Welding) merupakan proses pengelasan yang memanfaatkan gesekan atau tekanan untuk melelehkan material.


Untuk menghasilkan pengelasan berkualitas, pentingnya untuk memperhatikan proses pengelasan serta kesesuaian jenis material yang akan digunakan. Pada penelitian ini, material yang digunakan yaitu aluminium 3003 yang dikenal dengan sifat tahan terhadap korosi dan konduktivitas yang baik. Namun, sifat-sifat ini juga menghadirkan beberapa tantangan dalam proses pengelasan, seperti potensi terjadinya porositas, retak panas dan fusi yang tidak sempurna (Olabode dkk., 2013).

Adapun jenis-jenis metode untuk mengelas aluminium yang sering digunakan untuk penelitian, sebagai berikut:

- 1. Gas Tungsten Arc Welding (GTAW/TIG) Gas Tungsten Arc Welding (TIG) adalah metode pengelasan busur listrik

yang menggunakan gas inert sebagai pelindung dan tungsten atau wolfram untuk menghantarkan arus listrik guna menghasilkan sambungan las yang berkualitas baik (Kastanto dkk., 2020). Metode ini unggul dalam menghasilkan hasil las yang bersih, terutama untuk material aluminium tipis, namun memiliki kelemahan berupa proses yang lebih lambat dan membutuhkan operator yang terampil.

- 2. Gas Metal Arc Welding (GMAW/MIG) Gas Metal Arc Welding (MIG) adalah metode pengelasan aluminium

yang menggunakan kawat elektroda pengisi mencair dengan gas pelindung untuk mencegah oksidasi. Proses ini lebih cepat dan efisien dibandingkan GTAW, ideal untuk material aluminium tebal, namun memiliki risiko porositas tinggi jika gas pelindung tidak optimal.

- 3. Resistance Welding Metode ini memanfaatkan tekanan dan arus listrik untuk menghasilkan


![image 3](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile3.png>)

Gambar 2. 1. Gas Tungsten Arc Welding

|Sumber: https://www.allpro.co.id/pengelasan/gtaw/<br><br>|
|---|


![image 4](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile4.png>)

Gambar 2. 2. Gas Metal Arc Welding

|Sumber: https://skupmigas.id/gmaw/<br><br>|
|---|


panas pada titik kontak material, sehingga cocok untuk pengelasan aluminium

tipis dalam produksi massal. Teknik ini cepat, efisien dan tidak memerlukan logam pengisi, namun terbatas pada material dengan ketebalan tertentu.

![image 5](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile5.png>)

- Gambar 2. 3. Resistance Welding

- Gambar 2. 4. Friction Stir Welding


|Sumber: https://teknikmesinmanufaktur.blogspot.com<br><br>|
|---|


- 4. Friction Stir Welding Friction Stir Welding adalah metode pengelasan dalam keadaan padat

(solid-state) yang memanfaatkan panas akibat gesekan dari alat yang berputar tanpa mencairkan material dasar, sehingga menghasilkan sambungan yang sangat kuat dan minim resiko porositas. Metode ini unggul karena minim distorsi termal, namun membutuhkan peralatan khusus dan kurang cocok untuk material aluminium tipis.

- 5. Laser Beam Welding Laser Beam Welding adalah teknik pengelasan yang menggunakan energi laser untuk mencairkan aluminium, menawarkan presisi tinggi dan cocok untuk sambungan kecil atau kompleks. Metode ini cepat dan efisien, namun memiliki biaya peralatan yang sangat tinggi dan membutuhkan pengendalian yang presisi.


![image 6](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile6.png>)

|Sumber: https://images.app.goo.gl/RGo9GxRiUdzxywPEA<br><br>|
|---|


![image 7](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile7.png>)

Gambar 2. 5. Laser Beam Welding

|Sumber: https://www.mechanicalfunda.com/2017/05/laserbeam-welding.html<br><br>|
|---|


- 2.2.2. Aluminium Aluminium adalah material non-ferrous yang memiliki konduktivitas listrik


dan panas yang sangat baik. Sebagai logam dengan struktur Face Center Cubic (FCC) aluminium juga memiliki ketahanan korosi yang tinggi berkat lapisan oksidanya serta keuletan yang baik pada suhu rendah. Hal ini menjadikannya banyak digunakan dalam berbagai bidang, seperti peralatan kimia, konstruksi, kelistrikan, serta penyimpanan dan transportasi (Riyanta dkk., 2024). Aluminium memiliki ciri khas berwarna putih keperakan dan memiliki massa jenis yang rendah sekitar 2,720 g/cm³ sekitar sepertiga dari berat jenis baja. Keunggulan utama aluminium adalah kemampuannya untuk dibentuk dan didaur ulang tanpa kehilangan kualitas yang menjadikannya bahan ideal untuk berbagai aplikasi. Secara umum, aluminium diklasifikasikan menjadi dua kategori utama: aluminium tempa (wrought) dan aluminium tuang (cast), seperti Gambar 2.6.

![image 8](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile8.png>)

![image 9](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile9.png>)

Gambar 2. 6. Tempa (wrought) dan Tuang (cast)

Penggunaan aluminium murni saat ini cukup terbatas karena sifatnya yang terlalu lunak. Oleh karena itu, aluminium murni biasanya dipadu dengan elemen

lain, seperti seng (Zn), tembaga (Cu), nikel (Ni), magnesium (Mg), mangan (Mn) dan silikon (Si). Penambahan elemen paduan ini bertujuan untuk meningkatkan sifat mekanik dan fisik aluminium, seperti kekuatan, ketahanan terhadap korosi dan kemampuan pembentukan (Bashori, 2020). Karakteristik sifat fisik dan mekanik aluminium 3003 dapat dilihat pada Tabel 2.1 dan Tabel 2.2 berikut ini.

Tabel 2. 1. Sifat Fisik Aluminum 3003 sumber: Alloys International, INC.

|Sifat Fisik|Nilai|
|---|---|
|Kepadatan|2,73 g/cm3|
|Titik leleh|643 - 654 °C|


Tabel 2. 2. Sifat Mekanik Aluminium 3003 sumber: Alloys International, INC

|Sifat Mekanik|Nilai|
|---|---|
|Kekuatan Tarik (Ultimate)|200 MPa|
|Kekuatan Tarik (Yield)|186 MPa|
|Modulus Elastisitas|69 GPa|
|Kekuatan Geser|110 MPa|
|Kekerasan Brinell|55 HB|
|Kelonggaran (Elongation)|10 %|
|Tegangan Maksimum|130 MPa|


Berdasarkan tabel diatas, berikut adalah penjelasan untuk masing-masing sifat mekanik:

- a. Kekuatan Tarik (Ultimate) Kekuatan Tarik (Ultimate), kekuatan maksimum yang mengacu pada kemampuan aluminium menahan gaya tarik yang relevan tanpa kerusakan permanen pada aplikasi struktural.
- b. Kekuatan Tarik (Yield) Yield yaitu tegangan minimum dimana aluminium mengalami deformasi plastis permanen. Hal ini menunjukan batas elastis dimana material akan kembali ke bentuk semula jika beban tidak melebihi batas tersebut.


- c. Modulus Elastisitas Modulus elastisitas menggambarkan kemampuan suatu bahan untuk menerima tegangan tanpa mengalami terjadinya perubahan bentuk yang permanen setelah tegangan tersebut dilepaskan.
- d. Kekuatan Geser Kekuatan Geser mengacu pada batas maksimum kemampuan suatu material dalam menahan gaya geser sebelum mengalami kegagalan.
- e. Kekerasan Brinell Kekerasan Brinell dapat didefinisikan sebagai ukuran ketahanan permukaan material terhadap tegangan dan deformasi lokal.
- f. Kelonggaran (Elongation) Elongation, menyatakan kemampuan suatu material untuk meregang tanpa patah dan menunjukkan tingkat keuletan.
- g. Tegangan Maksimum Tegangan maksimum merupakan Tegangan tertinggi yang dapat ditahan suatu material tanpa mengalami kerusakan.


Menurut standar American National Standard Institute (ANSI) H35.1 dan Aluminium Association (AA) sistem klasifikasi paduan aluminium menggunakan empat digit angka, di mana digit pertama menunjukkan unsur utama atau dominan yang terkandung dalam paduan tersebut LiU, (2022), seperti:

- a) Seri 1xxx terdiri atas aluminium murni dengan kadar minimal 99%. Paduan ini memiliki sifat mekanik rendah, ketahanan korosi, konduktivitas termal dan listrik yang sangat baik, serta mudah dikerjakan, sehingga banyak digunakan di industri listrik dan kimia, seperti plat aluminium 1100 untuk distribusi daya.
- b) Seri 2xx adalah paduan aluminium yang mengandung tembaga dan magnesium sebagai tambahan, memiliki perbandingan kekuatan terhadap berat yang tinggi (kekuatan luluh hingga 455 MPa), sehingga cocok untuk pesawat terbang dan komponen ringan. Contoh umumnya adalah aluminium 2024.
- c) Seri 3xxx adalah paduan aluminium yang mengandung mangan. Paduan ini digunakan untuk aplikasi berkekuatan sedang dengan kemampuan kerja baik, seperti peralatan memasak dan aplikasi arsitektur. Contoh yang umum digunakan adalah aluminium 3003.


- d) Seri 4xxx adalah paduan aluminium yang mengandung silikon. Paduan ini memiliki titik leleh rendah yang meningkatkan fluiditas saat dicairkan, sehingga cocok untuk batang dan pelat las.
- e) Seri 5xxx adalah paduan aluminium yang mengandung magnesium. Paduan ini memiliki kekuatan tarik tinggi, kemampuan bentuk yang baik, serta ketahanan korosi terhadap atmosfer laut, sehingga cocok untuk lambung kapal, tangga, tangka dan jembatan. Contoh umumnya adalah aluminium 5083.
- f) Seri 6xxx adalah paduan aluminium yang mengandung magnesium dan silikon. Paduan ini memiliki kekuatan sedang dengan kemampuan bentuk, las, mesin, dan ketahanan korosi yang baik, menjadikannya cocok untuk ekstrusi arsitektur dan komponen otomotif. Contoh umumnya adalah aluminium 6061 untuk industri semikonduktor.
- g) Seri 7xxx adalah paduan aluminium yang mengandung seng dan tambahan kecil elemen seperti tembaga dan magnesium. Paduan ini dikenal sebagai salah satu yang paling kuat dengan kekuatan luluh ≥500 MPa. Secara umum, paduan ini digunakan dalam komponen struktural pesawat, kendaraan militer, serta berbagai aplikasi berkekuatan tinggi lainnya. Contoh umumnya adalah aluminium 7050 untuk kedirgantaraan dan 7085 untuk kendaraan militer.
- h) Seri 8xxx adalah paduan aluminium dengan kandungan unsur komposisi beragam yang umumnya terdiri atas unsur, seperti besi, timah atau lithium.


Material yang digunakan dalam simulasi profil penyerapan energi pada uji impak charpy menggunakan aluminium seri 3003. Jenis aluminium ini tergolong dalam paduan aluminium seri 3xxx yang terkenal dengan ketahanan korosinya yang baik, kekuatan sedang dan kemudahan dalam pembentukan. Paduan ini mengandung mangan (Mn) sebagai unsur utama yang memberikan sifat-sifat tersebut (Lu dkk., 2024) . Kandungan unsur maksimum dalam aluminium 3003 ditampilkan pada Tabel 2.3 di bawah ini

.

Tabel 2. 3. Kandungan Unsur Aluminium 3003 sumber: Alloys International, INC

|Unsur|Kandungan (%)|
|---|---|
|Aluminium (Al)|96,7– 99 %|
|Mangan (Mn)|1 – 1,5 %|
|Tembaga (Cu)|0,05 – 0,20 %|
|Besi (Fe)|Maks. 0,7 %|
|Silikon (Si)|Maks. 0,6 %|
|Seng (Zn)|Maks. 0,1 %|
|Residu|Maks. 0,15 %|


- 2.2.3. Pengujian Impact Uji impak adalah metode pengujian yang digunakan untuk menentukan


ketangguhan material atau kemampuannya dalam menyerap energi sebelum terjadinya beban tumbukan secara tiba-tiba. Tujuan utama dari pengujian impak adalah untuk mengevaluasi kondisi logam yang diuji melalui pengukur nilai impak yang diperoleh menggunakan alat uji (Boangmanalu dkk., 2023). Pengujian ini memberikan informasi penting mengenai kelayakan material dalam menghadapi kondisi dinamis yang membantu menentukan aplikasi material yang tepat dalam berbagai lingkungan operasional.

Secara umum, pengujian impak dibagi menjadi dua metode utama, yaitu metode charpy dan metode izod. Pada metode charpy, spesimen uji diletakkan pada tumpuan horizontal dengan arah pembebanan berlawanan dengan takik. Sementara itu, pada metode izod spesimen uji diletakkan secara vertikal dengan penjepit dan arah pembebanan sejajar dengan arah takikan (Jalil dkk., 2017). Skema peletakan posisi spesimen pada kedua metode ini dapat dilihat pada Gambar 2.7.

![image 10](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile10.png>)

Gambar 2. 7. Metode Charpy dan Metode Izod (Mildayati Nurdin dkk., 2021)

Dalam penelitian ini, digunakan metode charpy untuk mengukur ketangguhan material terhadap benturan dinamis secara efektif. Pengujian impact charpy mengikuti standar yang ditetapkan oleh ASTM, khususnya ASTM E23 yang berlaku untuk logam. Standar ini mencakup persyaratan mengenai dimensi spesimen, posisi takik berbentuk V, kecepatan tumbukan, serta kondisi pengujian lainnya. Spesimen yang digunakan umumnya berbentuk balok dengan dimensi panjang 55 mm, lebar 10 mm, serta takikan berbemtuk V sedalam 2 mm (Murugan, 2020).

![image 11](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile11.png>)

![image 12](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile12.png>)

Gambar 2. 8. Alat Uji Impact dan Ukuran Spesimen (Murugan, 2020)

Penelitian ini menggunakan spesimen dengan posisi takik V charpy sesuai dengan standar ASTM E23 yang dirancang untuk memberikan kondisi optimal dalam pengujian patah getas. Berdasarkan standar ini, diperoleh rumus untuk menghitung energi yang diserap selama pengujian impact charpy (Nuhgraha dkk., 2020).

- Ek1 = 12 × 𝑚 × 𝑣² ..............................................................................(2.1) Untuk mendapat nilai kecepatan menggunakan persamaan berikut:

𝑣 = √2 × 𝑔 × ℎ ...........................................................................(2.2)

Untuk mendapat nilai sisa energi kinetik menggunakan persamaan berikut:

- Ek2 = Ek1 – Ei ...................................................................................(2.3) Untuk mengetahui nilai tinggi sisa energi kinetik menggunakan persamaan berikut:


h = 𝑚.𝑔𝐸𝑘2 .............................................................................................(2.4)

Untuk mendapat nilai sudut β meggunakan persamaan berikut:

β = arccos (1 - hL) .............................................................................(2.5) Keterangan: Ei = Energi yang diserap (J)

- Ek1 = Energi Kinetik Awal (J)
- Ek2 = Energi kinetik Akhir (J) m = Massa (kg)


- g = Gravitasi (m/s2)
- h = Tinggi Pendulum (m) L = Panjang Pendulum (m) v = Kecepatan (m/s)


Faktor – faktor yang mempengerahui penyerapan energi

- 1. Temperatur: Material dapat menunjukkan perubahan ketangguhan yang signifikan pada berbagai suhu. Misalnya, beberapa material menjadi lebih getas pada suhu rendah.
- 2. Kecepatan Tumbukan: Laju regangan yang tinggi selama tumbukan dapat mempengaruhi mekanisme deformasi dan penyerapan energi material.
- 3. Geometri dan Ukuran Takik: Bentuk dan ukuran takik mempengaruhi konsentrasi tegangan dan inisiasi retak yang pada gilirannya mempengaruhi energi yang diserap selama fraktur.


Pengujian impact charpy menurut standar ASTM E23 bertujuan untuk menentukan energi yang diserap oleh material saat mengalami patahan akibat beban dinamis. Grafik yang dihasilkan dari pengujian ini umumnya menampilkan hubungan antara energi yang diserap (sumbu Y) dan temperatur pengujian (sumbu X). Seperti Gambar 2.9 ini membantu mengidentifikasi temperatur transisi material dari perilaku ulet ke getas.

![image 13](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile13.png>)

Gambar 2. 9. Grafik Daerah Ulet, Getas dan Transisi

Pada grafik Gambar 2.9 material yang diuji akan menunjukkan penyerapan energi yang berbeda pada berbagai temperatur. Biasanya, pada temperatur rendah energi yang diserap cenderung rendah yang menunjukkan sifat getas. Sebaliknya, pada temperatur yang lebih tinggi energi yang diserap meningkat yang menunjukkan sifat ulet. Poin transisi antara perilaku getas dan ulet dikenal sebagai temperatur transisi.

- 2.2.4. Software Ansys Ansys merupakan perangkat lunak Computer Aided Engineering (CAE) yang


memanfaatkan metode elemen hingga Finite Element Method (FEM) untuk keperluan pemodelan dan analisis. Software ini dapat mensimulasikan berbagai jenis proses termasuk dinamika fluida, struktur, perpindahan panas, serta analisis statis, dinamis dan elektromagnetik (Erikman dkk., 2022). Dalam industri dan teknik eksperimen sering dilakukan untuk mengumpulkan data yang digunakan sebagai acuan penelitian. Namun, eksperimen ini memerlukan waktu dan biaya yang tinggi serta seringkali harus dilakukan berulang kali untuk menghasilkan data yang akurat. Ansys sering dimanfaatkan untuk memprediksi hasil suatu proses sebelum eksperimen fisik dilakukan, sehingga dapat mengoptimalkan dan meminimalkan eksperimen langsung.

Penelitian ini menerapkan metode Finite Element Method (FEM), yang memprediksi masalah mekanika kontinu dengan membagi domain menjadi elemen-

elemen kecil (meshing) melalui software ansys versi student. Secara umum, langkah-langkah penggunaan software ansys meliputi:

- 1. Menentukan spesifikasi masalah (Problem Specifications)
- 2. Mendefinisikan material (Define Materials)
- 3. Menyusun deskripsi masalah (Problem Descriptions)
- 4. Membangun geometri (Build Geometry)
- 5. Membuat mesh (Generate Mesh)
- 6. Memberikan atribut mesh pada model (Attribute Mesh to Model)
- 7. Menetapkan kondisi batas (Boundary Condition)
- 8. Mendapatkan solusi (Obtain Solutions)
- 9. Meninjau hasil (Review Result).


Secara garis besar penelitian ini dibagi menjadi 3 tahap yaitu sebagai berikut:

- 1. Pre-processing Pre-processing merupakan tahap awal dalam melakukan simulasi


menggunakan software ansys. Pada tahap ini, beberapa fungsi perlu didefinisikan untuk memungkinkan perhitungan yang tepat pada objek yang akan dianalisis. Proses ini mencakup beberapa langkah penting, seperti pemodelan geometri, penentuan jenis elemen yang digunakan, pemilihan material yang sesuai, serta pembuatan mesh (Gadayu, 2023). Langkah-langkah ini sangat penting karena menentukan kualitas dan akurasi hasil simulasi. Berikut merupakan tahapan umum yang dilakukan pada tahap pre-processing.

- A. Modeling adalah tahapan untuk membuat seluruh geometri yang diperlukan dalam simulasi. Material dapat dimodelkan dalam bentuk 2D maupun 3D. Untuk geometri yang kompleks, ansys memudahkan untuk impor model CAD dari software lain misalnya CATIA dan solidworks.
- B. Elemen type adalah tahapan untuk menentukan jenis elemen dan atribut bentuk pada objek yang akan dianalisis, seperti elemen solid, balok (beam) atau pelat (shell). Pemilihan elemen akan memengaruhi tahapan analisis berikutnya.
- C. Material properties adalah tahapan untuk menetapkan sifat material pada objek yang dianalisis, seperti massa jenis (densitas), modulus elastisitas dan parameter lain yang relevan.


- D. Meshing adalah proses pembagian objek menjadi area-area kecil (elemen) yang akan dianalisis secara numerik. Meshing merupakan salah satu tahap krusial dalam metode elemen hingga (FEM).


- 2. Solution Tahap berikutnya dalam metode elemen hingga adalah Solution. Pada

proses ini metode Elemen Hingga (FEM) mencakup proses perhitungan dan analisis yang melibatkan beberapa tahapan penting seperti pembebanan dan evaluasi respons struktur (Gadayu, 2023). Beberapa parameter umumnya didefinisikan pada tahap Solution, antara lain:

- A. Constrain merupakan tahap untuk menetapkan pembatasan gaya yang bekerja pada objek yang dianalisis. Pada tahap constraints, derajat kebebasan dari objek tersebut akan ditentukan.
- B. Pada opsi Define Load, besar pembebanan dapat ditentukan dan diterapkan pada material yang dianalisis.
- C. Bagian Solve digunakan untuk menjalankan penyelesaian simulasi setelah seluruh parameter didefinisikan.


- 3. Post-processing Setelah tahap pemodelan dan analisis diselesaikan, langkah berikutnya


adalah post-processing. Tahap ini digunakan untuk meninjau hasil analisis, khususnya tegangan geser, deformasi, serta faktor koreksi yang dihasilkan (Gadayu, 2023).

- 3.1. Diagram Alir


BAB III METODOLOGI

Pada Gambar 3.1 dan Gambar 3.2 adalah diagram alir penelitian dan uraiannya yang bertujuan untuk mempermudah dalam pelaksanakan penelitian dan memperjelas tahapan-tahapannya, sebagai berikut:

![image 14](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile14.png>)

Gambar 3. 1. Diagram Alir 1

### 3.2. Studi Literatur

Studi literatur dilakukan dengan mengacu pada jurnal, buku, dan dokumendokumen ilmiah terkait metode pengelasan, sifat aluminium 3003, serta pengujian impact charpy. Penelitian ini juga memanfaatkan referensi mengenai simulasi numerik berbasis metode elemen hingga atau Finite Element Method (FEM) dengan

21

menggunakan perangkat lunak Ansys. Literatur digunakan untuk memahami karakteristik material, metode uji dan teknik simulasi yang relevan.

### 3.3. Alat dan Bahan

- 3.3.1. Alat Penelitian ini menggunakan perangkat keras berupa komputer berspesifikasi

tinggi untuk menjalankan software Ansys versi student. Perangkat lunak ini digunakan untuk simulasi numerik dalam pengujian impact charpy. Spesifikasi komputer dapat dilihat Tabel 3.1.

- 3.3.2. Bahan Bahan yang digunakan pada penelitian ini berupa geometri benda uji dalam


Tabel 3. 1. Spesifikasi Komputer

|Komponen Hardware|Perangkat Komputasi|
|---|---|
|processor|Intel Core i7-11800H|
|metherboard|ASUS TUF Gaming F15|
|RAM|16GB DDR4 3200MHz (dualchannel)|
|Storage|512GB SSD NVMe PCIe Gen 3.0.|


bentuk 3 dimensi CAD dan bahan material pada spesimen yaitu aluminium 3003, filler ER4043 dan structural steel. Geometri dapat dilihat pada Gambar 3.3.

![image 15](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile15.png>)

Gambar 3. 2. Desain Geometri 3D

### 3.4. Langkah Penelitian

Berdasarkan hasil studi literatur yang didapatkan, penelitian ini secara umum dibagi menjadi 3 tahap yaitu pre-processing, processing dan post-processing.

- 3.3.1. Pre-processing Pre-processing merupakan tahap awal dalam memulai simulasi tang terdiri


input data, batasan, serta variasi lain dari simulasi ditentukan pada proses ini. Tahap ini terdiri atas beberapa langkah berikut.

- A. Geometry

Pada tahap ini, geometri spesimen, seperti Gambar 3.4 dibuat sesuai dimensi standar spesifikasi ASTM E23 untuk uji impact charpy, seperti panjang 55 mm, lebar 10, ketebalan 10 mm, sudut takik V 45° dan sudut pengelasan 60° sesuai standar pengelasan. Spesimen dapat dimodelkan dalam bentuk dua dimensi (2D) maupun tiga dimensi (3D) sesuai dengan kebutuhan simulasi. Software seperti solidworks digunakan untuk membuat model yang kemudian diimpor ke ansys untuk simulasi lebih lanjut.

- B. Property Material Pada tahap Property Material, material dipilih dari pustaka atau


![image 16](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile16.png>)

Gambar 3. 3. Desain dan Ukuran Spesimen

ditambahkan baru dengan mendefinisikan sifat-sifat seperti densitas, modulus elastisitas, dan sifat termal. Material tersebut kemudian diterapkan ke geometri model, diverifikasi dan disimpan untuk memastikan simulasi berjalan sesuai dengan karakteristik material yang ditentukan. Properti material dapat dilihat pada Tabel 3.2.

Tabel 3. 2. Property Aluminium 3003

|Property|Value|Unit|
|---|---|---|
|Density|2,73|g/cm3|
|Young’a Modulus|69|GPa|
|Poisson’s Ratio|0,33|N/A|
|Bulk Modulus|6,7549 x 1010|Pa|
|Shear Modulus|2,5902 x 1010|Pa|
|Specfic Heat Constant Pressure|0,893|J/g-1|


- C. Model Geometri Tahap selanjutnya, assign pada model geometri yang berfungsi untuk

memastikan pada bagian model memiliki sifat karakteristik yang sesuai dengan kondisi nyata, misalnya:

- - Spesimen benda uji, data material yang telah dikumpulkan sebelumnya dipilih agar ansys dapat mengenali karakteristik fisik dan mekanik dari spesimen tersebut dan biasanya bersifat fleksibel atau tidak kaku.
- - Pendulum dan support (penyangga) biasanya dibuat rigit body atau kaku agar tidak mengalami deformasi saat simulasi berjalan dan hanya fokus pada spesimen benda uji.
- - Penambahan point mass pada pendulum, point mass ini dibuat agar pendulum memiliki massa yang sesuai dengan spesifikasi pengujian nyata. Massa yang diberikan dipendulum pada penelitian ini bisa dilihat pada Gambar 3.5.


Pengaturan dan penambahan yang dibahas diatas dilakukan pada tahap “Model” dengan memilih bagian mana yang akan dijadikan rigit body, fleksibel atau menggunakan properti material dan penambahan point mass yang ditempatkan pada titik pussat massa pendulum.

- D. Mesh Meshing merupakan proses membagi model geometri menjadi elemen-


![image 17](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile17.png>)

Gambar 3. 4. Point Mass

elemen berukuran kecil guna memungkinkan perhitungan numerik yang rinci.

Elemen-elemen ini memiliki bentuk tertentu, seperti segitiga atau persegi tergantung pada kompleksitas model. Kualitas mesh, seperti ukuran elemen sangat mempengaruhi kecepatan dan akurasi simulasi. Mesh yang terlalu kasar dapat menghasilkan perhitunag yang kurang akurat, sedangkan mesh yang terlalu halus memerlukan waktu komputasi lebih lama.

![image 18](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile18.png>)

Gambar 3. 5. Meshing

- E. Time Step Pada tahap selanjutnya menentukan time step yang berfungsi untuk

memastikan beberapa lama simulasi berjalan. Time step pada uji impak umumnya diatur sangat kecil agar dapat terekam jelas peristiwa fraktuk yang dialami. Pada penelitian ini time step yang ditetapkan bisa dilihat pada Gambar 3.7.

- F. Boundry Condition dan Initial Condition Pada tahap selanjutnya, ditetapkan kondisi batas (boundary condition) pada bagian penopang spesimen yang bersifat rigid, serta kondisi awal (initial condition) berupa kecepatan awal pada pendulum. Kedua pengaturan ini berfungsi untuk memastikan model simulasi merepresentasikan kondisi nyata pengujian, di mana support tetap diam dan pendulum memiliki energi kinetik sesuai spesifikasi uji. Kondisi kecapatan awal pada penelitian ini bisa dilihat pada Gambar 3.7.


![image 19](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile19.png>)

Gambar 3. 6. End Time atau Time Step

![image 20](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile20.png>)

Gambar 3. 7. Initial Condition

- 3.3.2. Processing Processing adalah tahap utama dalam simulasi numerik menggunakan


metode elemen hingga atau Finite Element Method (FEM) dimana perangkat lunak melakukan perhitungan untuk memodelkan respons material dan geometri terhadap data yang telah dibuat pada tahap pre-processing. Pada tahap ini, model akan dianalisis secara numerik untuk menentukan respon terhadap beban, seperti menghitung total deformasi, tegangan dan regangan, serta penyerapan energi yang terjadi selama proses simulasi berjalan pada setiap langkah waktu (time step). Tahap ini bertujuan untuk menghasilkan data numerik yang menunjukkan parameter-parameter seperti distribusi tegangan, deformasi dan energi yang diserap oleh spesimen.

|A|
|---|


![image 21](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile21.png>)

![image 22](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile22.png>)

|B|
|---|


|C|
|---|


![image 23](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile23.png>)

Gambar 3. 8. Processing Error, B Processing Berjalan dan C Processing Berhasil

Pada Gambar 2.6 dapat dilihat tiga kondisi berbeda pada proses solution (processing) di Ansys Explicit Dynamics, yaitu A, B dan C. Pada bagian A ditunjukkan adanya processing error yang ditandai dengan ikon peringatan dan

keterangan error pada jendela detail yang menandakan terdapat kesalahan pada input atau parameter simulasi yang harus diperbaiki. Pada bagian B status menunjukkan "Solve Required" yang berarti simulasi sudah siap dijalankan dan seluruh konfigurasi telah benar, namun proses komputasi belum dimulai. Sementara pada bagian C seluruh output solution telah berhasil dihitung dan ditandai dengan ikon centang hijau yang menandakan proses simulasi berjalan lancar tanpa error dan hasil perhitungan siap dianalisis lebih lanjut.

- 3.3.3. Post-processing Post-processing adalah tahap analisis lanjutan terhadap data hasil simulasi.


Data numerik yang diperoleh dianalisis untuk memahami distribusi tegangan, regangan, deformasi, serta pola penyerapan energi spesimen. Hasil divisualisasikan dalam bentuk grafik, animasi dan kontur warna untuk mempermudah interpretasi. Evaluasi ini memberikan wawasan mendalam tentang kemampuan spesimen menyerap energi tumbukan dan mengidentifikasi titik-titik kritis yang rentan terhadap kegagalan. Gambar Visualisasi dapat dilihat pada Gambar 3.10.

![image 24](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile24.png>)

Gambar 3. 9. Gambar Visualisasi Hasil Simulasi

### BAB IV HASIL DAN PEMBAHASAN

- 4.1. Hasil Perhitungan Sebelum dilakukan simulasi, terlebih dahulu dilakukan perhitungan teoritis


terhadap energi kinetik awal yang dimiliki oleh pendulum. Perhitungan ini bertujuan untuk menjadi acuan dan validasi terhadap hasil simulasi yang akan dilakukan. Perhitungan energi kinetik dilakukan berdasarkan massa pendulum 5,8 kg, panjang lengan 0,68 m dan sudut ayun awal sebesar 150° terhadap garis vertikal. Energi kinetik sebelum tumbukan dapat dihitung melalui persamaan (2.1) dan (2.2).

𝑣 = √2 × 9,81 × 0,68(1 − cos(150°) .................................................(2.2) 𝑣 = 4,98957 𝑚/𝑠 − 4989,57mm/s

Ek1 = 12 × 5,8 × 4,98957² ......................................................................(2.1) Ek1 = 72,1978 Joule − 72197,8 milijoule Keterangan: Ek1 = Energi Kinetik Awal (J) m = Massa (kg)

- g = Gravitasi (m/s2)
- h = Tinggi Pendulum (m) v = Kecepatan (m/s)


- 4.2. Hasil Simulasi Pengujian Impact Charpy


- 4.2.1. Weld Metal


- 1. Total Deformasil


![image 25](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile25.png>)

Gambar 4. 1. Visualisasi Total Deformasi

Pada Gambar 4.1 menunjukan hasil visualisasi total deforamasi pada spesimen pengelasan yang disimulasikan dengan metode explicite dynamics di

26

ANSYS. Berdasarkan hasil simulasi dapat dilihat bahwa deformasi maksimum sebesar 5058,6 mm yang terjadi diarea tengah tepat dibawah titik tumbukan pendulum. Grafik hubungan total deformasi dan waktu dapat dilihat pada Gambar 4.2.

|0<br><br>1000<br><br>2000<br><br>3000<br><br>4000<br><br>5000<br><br>6000<br><br>0.00E+00 5.00E-03 1.00E-02 1.50E-02 2.00E-02 2.50E-02<br><br>Deformasi<br><br>Waktu (s)<br><br>Grafik Hubungan Total Deformasi & Waktu<br><br>Total Deformasi|
|---|


##### Deformasi

Gambar 4. 2. Grafik Total Deformasi

Berdasarkan Gambar grafik 4.2 dapat dilihat bahwa pada spesimen hasil pengelasan mengalami deformasi yang meningkat secara linier dalam waktu singkat selama simulasi berjalan. Pola ini menunjukan bahwa material mengalami perubahan bentuk yang relatif besar saat diberikan beban. Nilai maksimum deformasi ini menandakan besarnya perubahan bentuk permanen yang terjadi pada spesimen akibat beban impak, serta mengindikasikan respons material hasil pengelasan dalam menerima energi benturan secara dinamis. Besar total deformasi ini terjadi karena adanya perubahan struktur mikro akibat proses pengelasan yang mempengaruhi kemampuan spesimen dalam menahan beban impak secara efektif.

- 2. Equivalent Stress


![image 26](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile26.png>)

Gambar 4. 3. Visualisasi Equivalen Stress

Pada Gambar 4.3 menunjukan hasil visualisasi tegangan pada spesimen pengelasan yang disimulasikan dengan metode explicite dynamics di ANSYS.

Berdasarkan hasil simulasi dapat dilihat bahwa tegangan maksimum sebesar 3482,5 MPa yang terjadi diarea tengah tepat dibawah titik tumbukan pendulum. Grafik hubungan tegangan dan waktu dapat dilihat pada Gambar 4.4.

|0<br><br>1000<br><br>2000<br><br>3000<br><br>4000<br><br>0.00E+00 5.00E-03 1.00E-02 1.50E-02 2.00E-02 2.50E-02<br><br>Tegangan(MPa)<br><br>Waktu (s)<br><br>Grafik Hubungan Tegangan & Waktu<br><br>Grafik Hubungan Tegangan & Waktu|
|---|


##### Tegangan(MPa)

Gambar 4. 4. Grafik Hubungan Tegangan dan Waktu

Berdasarkan Gambar grafik 4.4 dapat dilihat bahwa pada spesimen hasil pengelasan memiliki kekuatan awal yang tinggi, sehingga tegangan meningkat tajam hingga titik maksimum. Setelah mencapai nilai puncak maksimum, tegangan mengalami penerunan drastis dan kemudian stabil pada nilai rendah akibat adanya kerusakan atau keretakan pada daerah las. Pola tegangan seperti ini terjadi karena adanya perubahan struktur mikro akibat proses pengelasan dan adanya zona heterogen di sekitar daerah las yang mempengaruhi distribusi tegangan.

- 3. Equivalent Elastic Strain


![image 27](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile27.png>)

Gambar 4. 5. Visualisasi Equivalent Strain

Pada Gambar 4.5 menunjukan hasil visualisasi regangan pada spesimen pengelasan yang disimulasikan dengan metode explicite dynamics di ANSYS. Berdasarkan hasil simulasi dapat dilihat bahwa regangan maksimum sebesar 0,0617 mm/mm yang terjadi diarea tengah tepat dibawah titik tumbukan pendulum. Grafik hubungan regangan dan waktu dapat dilihat pada Gambar 4.6.

|0.000<br><br>0.020<br><br>0.040<br><br>0.060<br><br>0.080<br><br>0.00E+00 5.00E-03 1.00E-02 1.50E-02 2.00E-02 2.50E-02<br><br>Reganganmm/mm<br><br>Waktu (s)<br><br>Grafik Hubungan Regangan & Waktu|
|---|


Reganganmm/mm

Gambar 4. 6. Grafik Hubungan Regangan dan Waktu

Berdasarkan Gambar grafik 4.6 dapat dilihat bahwa pada spesimen hasil pengelasan memiliki kekuatan awal yang tinggi, sehingga regangan meningkat tajam hingga titik maksimum. Setelah mencapai nilai puncak maksimum, regangan mengalami penerunan drastis dan kemudian stabil pada nilai rendah akibat adanya kerusakan atau keretakan pada daerah las. Pola regangan ini terjadi karena sifat mekanik daerah las terpengaruh oleh efek termal selama proses pengelasan dan struktur mikro pada daerah las menyebabkan perubahan karakteristik kekuatan pada material, sehingga mempengaruhi pola distribusi regangan saat menerima beban impak.

- 4. Energi Probe


![image 28](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile28.png>)

Gambar 4. 7. Visualisasi Energi Internal

Pada Gambar 4.7 menunjukan hasil visualisasi penyerapan energi pada spesimen hasil pengelasan yang disimulasikan dengan metode explicite dynamics di ANSYS. Berdasarkan hasil simulasi dapat dilihat bahwa energi internal maksimum sebesar 37,966 Joule yang terjadi diarea tengah tepat dibawah titik tumbukan pendulum. Grafik hubungan energi internal dan waktu dapat dilihat pada Gambar 4.8.

|0<br><br>10<br><br>20<br><br>30<br><br>40<br><br>0.00E+00 5.00E-03 1.00E-02 1.50E-02 2.00E-02 2.50E-02<br><br>Energi(J)<br><br>Waktu (s)<br><br>Grafik Hubungan Energi Internal & waktu|
|---|


##### Energi(J)

Gambar 4. 8. Grafik Hubungan Energi Internal dan Waktu

Berdasarkan Gambar grafik 4.8 dapat dilihat bahwa spesimen hasil pengelasan mampu menyerap energi pada awal tahapan yang signifikan sampai titik maksimum. Setelah mencapai nilai maksimum, energi internal menurun dan kemudian stabil akibat kerusakan atau keretakan pada daerah las. Pola energi internal ini terjadi karena karakteristik struktur mikro pada daerah las mengalami efek termal selama proses pengelasan dan kualitas sambungan las juga berkontribusi pada efisiensi penyerapan energi selama uji impak.

### 4.2.2. Base Metal

- 1. Total Deformasi


![image 29](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile29.png>)

Gambar 4. 9. Visualisasi total deformasi

Pada Gambar 4.9 menunjukan hasil visualisasi total deforamasi pada spesimen base metal yang disimulasikan dengan metode explicite dynamics di ANSYS. Berdasarkan hasil simulasi dapat dilihat bahwa deformasi maksimum sebesar 15346 mm yang terjadi diarea tengah tepat dibawah titik tumbukan pendulum. Grafik hubungan total deformasi dan waktu dapat dilihat pada Gambar 4.10.

|-5000<br><br>0<br><br>5000<br><br>10000<br><br>15000<br><br>20000<br><br>0.00E+00<br><br>| | | | | |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |
|5.00E|-03 1.00E|-02 1.50E|-02 2.00E|-02|
<br><br>2.50E-02<br><br>Deformasi<br><br>Waktu (s)<br><br>Grafik Hubungan Total Deformasi & Waktu|
|---|


##### Deformasi

Gambar 4. 10. Grafik Hubungan Total Deformasi dan Waktu

Berdasarkan Gambar grafik 4.10 dapat dilihat bahwa base metal mengalami deformasi yang meningkat secara linier dalam waktu singkat selama simulasi berjalan. Pola ini menunjukan bahwa base metal mampu menyerap energi tumbukan melalui deformasi plastis sampai tercapai nilai maksimum. Nilai deformasi total yang besar ini menandakan kemampuan material base metal untuk menahan beban dan mengalami perubahan bentuk yang signifikan selama uji impak. Besar total deformasi ini terjadi karena base metal memiliki sifat mekanik daktilitas, kekuatan luluh relatif rendah dan struktur mikro pada material base metal belum terpengaruh oleh proses termal atau pencampuran material lain.

- 2. Equivalent Stress


![image 30](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile30.png>)

Gambar 4. 11. Visualisasi equivalent stress

Pada Gambar 4.11 menunjukan hasil visualisasi tegangan pada spesimen base metal yang disimulasikan dengan metode explicite dynamics di ANSYS. Berdasarkan hasil simulasi dapat dilihat bahwa tegangan maksimum sebesar 4690,3 MPa yang terjadi diarea tengah tepat dibawah titik tumbukan pendulum. Grafik hubungan total deformasi dan waktu dapat dilihat pada Gambar 4.12.

|0<br><br>1000<br><br>2000<br><br>3000<br><br>4000<br><br>5000<br><br>0.00E+00 5.00E-03 1.00E-02 1.50E-02 2.00E-02 2.50E-02<br><br>Tegangan(MPa)<br><br>Waktu (s)<br><br>Grafik Hubungan Tegangan & Waktu|
|---|


##### Tegangan(MPa)

- Gambar 4. 12. Grafik Hubungan Tegangan dan Waktu

- Gambar 4. 13.Visualisasi equivalent elastic strain


Berdasarkan Gambar grafik 4.12 dapat dilihat bahwa pada spesimen base metal memiliki kekuatan awal yang tinggi, sehingga tegangan meningkat tajam hingga titik maksimum. Setelah mencapai nilai puncak maksimum, tegangan mengalami penerunan drastis dan kemudian stabil pada nilai rendah akibat adanya kerusakan atau keretakan. Pola tegangan ini terjadi karena material base metal memiliki daktilitas tinggi dan kekuatan luluh relatif rendah dan struktur mikro pada material base metal belum terpengaruhi oleh proses termal. Sehingga mampu menahan beban impak di awal dan kemudian mengalami deformasi plastis setelah melewati batas elastis.

- 3. Equivalent Elastic Strain


![image 31](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile31.png>)

Pada Gambar 4.13 menunjukan hasil visualisasi regangan pada spesimen base metal yang disimulasikan dengan metode explicite dynamics di ANSYS. Berdasarkan hasil simulasi dapat dilihat bahwa regangan maksimum sebesar 0,0773 mm/mm yang terjadi diarea tengah tepat dibawah titik tumbukan pendulum. Grafik hubungan regangan dan waktu dapat dilihat pada Gambar 4.14.

|0.0000<br><br>0.0200<br><br>0.0400<br><br>0.0600<br><br>0.0800<br><br>0.1000<br><br>0.00E+00 5.00E-03 1.00E-02 1.50E-02 2.00E-02 2.50E-02<br><br>Reganganmm/mm<br><br>Waktu (s)<br><br>Grafik Hubungan Regangan & Waktu|
|---|


##### Reganganmm/mm

Gambar 4. 14. Grafik Hubungan Regangan dan Waktu

Berdasarkan Gambar grafik 4.14 dapat dilihat bahwa pada spesimen base metal memiliki kekuatan awal yang tinggi, sehingga regangan meningkat tajam hingga titik maksimum. Setelah mencapai nilai puncak maksimum, regangan mengalami penurunan drastis dan kemudian stabil pada nilai rendah akibat adanya kerusakan atau keretakan pada daerah las. Pola regangan ini terjadi karena sifat mekanik material base metal memiliki dektilitas tinggi dan kekuatan luluh relatif rendah dan struktur mikro belum terpengaruh efek termal dari proses pengelasan, sehingga material mengalami deformasi besar di bawah beban impak.

- 4. Energi Probe


![image 32](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile32.png>)

Gambar 4. 15. Visualisasi Energi Internal

Pada Gambar 4.15 menunjukan hasil visualisasi regangan pada spesimen base metal yang disimulasikan dengan metode explicite dynamics di ANSYS. Berdasarkan hasil simulasi dapat dilihat bahwa energi internal maksimum sebesar 54,532 Joule yang terjadi diarea tengah tepat dibawah titik tumbukan pendulum. Grafik hubungan energi internal dan waktu dapat dilihat pada Gambar 4.16

|0<br><br>10<br><br>20<br><br>30<br><br>40<br><br>50<br><br>60<br><br>0.00E+00 5.00E-03 1.00E-02 1.50E-02 2.00E-02 2.50E-02<br><br>Energi(J)<br><br>Waktu (s)<br><br>Grafik Hubungan Energi Internal & Waktu|
|---|


##### Energi(J)

Gambar 4. 16. Grafik Hubungan Energi Internal dan Waktu

Berdasarkan Gambar grafik 4.16 dapat dilihat bahwa spesimen base metal mampu menyerap energi pada awal tahapan yang signifikan sampai titik maksimum. Setelah mencapai nilai maksimum, energi internal menurun dan kemudian stabil akibat kerusakan atau keretakan. Pola energi ineternal ini terjadi karena sifat mekanik base metal memiliki dektilitas tinggi dan kekuatan luluh relatif rendah dan struktur mikro pada material base metal belum terpengaruh proses pengelasan, sehingga karakteristik pada material tersebut tidak mengalami perubahan dan mampu menyerap energi dalam jumlah tinggi melalui deformasi plastis sebelum mengalami kegagalan.

### 4.2.3. Heat Affected Zone

- 1. Total Deformasi


![image 33](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile33.png>)

Gambar 4. 17. Visualisasi Total Deformasi

Pada Gambar 4.17 menunjukan hasil visualisasi total deforamasi pada spesimen Heat Affected Zone (HAZ) yang disimulasikan dengan metode explicite dynamics di ANSYS. Berdasarkan hasil simulasi dapat dilihat bahwa deformasi maksimum sebesar 12330 mm yang terjadi diarea tengah tepat dibawah titik tumbukan pendulum. Grafik hubungan total deformasi dan waktu dapat dilihat pada Gambar 4.18

|0<br><br>5000<br><br>10000<br><br>15000<br><br>0.00E+00 5.00E-03 1.00E-02 1.50E-02 2.00E-02 2.50E-02<br><br>TotalDeformasi(mm)<br><br>Waktu (s)<br><br>Grafik Hubungan Total Deformasi & Waktu|
|---|


TotalDeformasi(mm)

Gambar 4. 18. Grafik Hubungan Total Deformasi dan Waktu

Berdasarkan Gambar grafik 4.18 dapat dilihat bahwa Heat Affected Zone (HAZ) mengalami deformasi yang meningkat secara hampir linier dalam waktu singkat selama simulasi berlangsung. Pola ini menunjukkan bahwa HAZ mampu menyerap energi tumbukan melalui mekanisme deformasi plastis hingga mencapai nilai maksimum. Nilai total deformasi yang sangat besar ini menggambarkan kemampuan material di HAZ untuk menahan beban sekaligus mengalami perubahan bentuk signifikan saat menerima beban impak. Besarnya deformasi ini terjadi karena HAZ memiliki sifat mekanik dengan daktilitas tinggi dan kekuatan luluh yang relatif rendah akibat pengaruh panas proses pengelasan, sehingga struktur mikronya berbeda dari logam dasar dan lebih mudah terdeformasi ketika terkena beban dinamis.

- 2. Equivalent Stress


![image 34](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile34.png>)

Gambar 4. 19. Visualisasi Equivalent Stress

Pada Gambar 4.19 menunjukan hasil visualisasi tegangan pada spesimen Heat Affected Zone (HAZ) yang disimulasikan dengan metode explicite dynamics di ANSYS. Berdasarkan hasil simulasi dapat dilihat bahwa tegangan maksimum sebesar 3768,6 MPa yang terjadi diarea tengah tepat dibawah titik tumbukan pendulum. Grafik hubungan tegangan dan waktu dapat dilihat pada Gambar 4.20.

|0<br><br>1000<br><br>2000<br><br>3000<br><br>4000<br><br>5000<br><br>0.00E+00 5.00E-03 1.00E-02 1.50E-02 2.00E-02 2.50E-02<br><br>Tegangan(MPa)<br><br>Waktu (s)<br><br>Grafik Hubungan Grafik Tegangan & Waktu|
|---|


##### Tegangan(MPa)

Gambar 4. 20. Grafik Hubungan Tegangan dan Waktu

Berdasarkan Gambar grafik 4.20 dapat dilihat bahwa pada spesimen Heat Affected Zone (HAZ) terjadi peningkatan tegangan yang sangat tajam hingga mencapai titik maksimum, menunjukkan bahwa material HAZ masih mampu menahan beban impak awal. Namun setelah mencapai puncak tegangan, grafik memperlihatkan penurunan drastis disertai fluktuasi tegangan yang menandakan terjadinya keretakan atau kerusakan lokal pada material. Setelah fase tersebut, tegangan stabil pada nilai yang lebih rendah. Pola tegangan ini terjadi karena material HAZ telah mengalami perubahan mikrostruktur akibat proses termal pengelasan, sehingga memiliki kekuatan luluh yang relatif lebih rendah dan tingkat daktilitas yang dapat memicu deformasi plastis lebih cepat saat menerima beban impak. Kondisi ini menyebabkan HAZ tetap dapat menahan beban awal, tetapi segera mengalami penurunan kemampuan menahan tegangan begitu melewati batas elastisnya.

- 3. Equivalent Elastic Strain


![image 35](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile35.png>)

Gambar 4. 21. Visualisasi Equivalent Elastic Srain

Pada Gambar 4.21 menunjukan hasil visualisasi tegangan pada spesimen Heat Affected Zone (HAZ) yang disimulasikan dengan metode explicite

dynamics di ANSYS. Berdasarkan hasil simulasi dapat dilihat bahwa regangan maksimum sebesar 0,0618 mm/mm yang terjadi diarea tengah tepat dibawah titik tumbukan pendulum. Grafik hubungan regangan dan waktu dapat dilihat pada Gambar 4.22.

|0.0000<br><br>0.0100<br><br>0.0200<br><br>0.0300<br><br>0.0400<br><br>0.0500<br><br>0.0600<br><br>0.0700<br><br>0.00E+00 5.00E-03 1.00E-02 1.50E-02 2.00E-02 2.50E-02<br><br>Reganganmm/mm<br><br>Waktu (s)<br><br>Grafik Hubungan Regangan & Waktu|
|---|


##### Reganganmm/mm

Gambar 4. 22. Grafik Hubungan Regangan dan Waktu

Berdasarkan Gambar grafik 4.22 dapat dilihat bahwa pada spesimen Heat Affected Zone (HAZ) terjadi peningkatan regangan yang sangat tajam hingga mencapai titik maksimum, menunjukkan bahwa material HAZ masih mampu menahan beban impak awal dan mengalami deformasi yang cukup besar. Setelah mencapai nilai puncak maksimum, regangan mengalami penurunan drastis dan kemudian stabil pada nilai yang lebih rendah dan mengindikasikan telah terjadi keretakan atau kerusakan pada daerah HAZ. Pola regangan ini muncul karena sifat mekanik material di HAZ memiliki kekuatan luluh yang lebih rendah akibat perubahan mikrostruktur dari proses pengelasan, meskipun masih mempertahankan tingkat daktilitas yang membuatnya mampu mengalami deformasi besar di bawah beban impak. Struktur mikro yang telah terpengaruh efek panas ini menyebabkan material HAZ lebih cepat masuk fase deformasi plastis dan kehilangan kemampuan menahan regangan tinggi setelah melewati batas elastisnya.

- 4. Energi Probe


![image 36](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile36.png>)

- Gambar 4. 23. Visualisasi Energi Internal

|0<br><br>5<br><br>10<br><br>15<br><br>20<br><br>25<br><br>30<br><br>35<br><br>0.00E+00 5.00E-03 1.00E-02 1.50E-02 2.00E-02 2.50E-02<br><br>Energi(J)<br><br>Waktu (s)<br><br>Grafik Hubungan Energi Internal & Waktu|
|---|


- Gambar 4. 24. Grafik Hubungan Energi Internal dan Waktu


Pada Gambar 4.23 menunjukan hasil visualisasi regangan pada spesimen Heat Affected Zone (HAZ) yang disimulasikan dengan metode explicite dynamics di ANSYS. Berdasarkan hasil simulasi dapat dilihat bahwa energi internal maksimum sebesar 31,929 Joule yang terjadi diarea tengah tepat dibawah titik tumbukan pendulum. Grafik hubungan energi internal dan waktu dapat dilihat pada Gambar 4.24.

Berdasarkan Gambar grafik 4.24 di atas dapat dilihat bahwa spesimen Heat Affected Zone (HAZ) mampu menyerap energi internal dalam jumlah yang signifikan pada tahap awal pengujian hingga mencapai titik maksimum. Setelah mencapai nilai puncak tersebut, energi internal mengalami sedikit penurunan dan kemudian stabil pada nilai yang lebih rendah dan mengindikasikan telah terjadi kerusakan atau keretakan pada area HAZ akibat beban impak. Pola energi internal ini muncul karena sifat mekanik material di HAZ memiliki kekuatan luluh yang relatif lebih rendah dan daktilitas yang masih cukup tinggi, namun struktur mikronya telah terpengaruh oleh proses pengelasan. Kondisi ini menyebabkan HAZ tetap mampu menyerap energi dalam jumlah besar melalui

deformasi plastis pada awal pembebanan, tetapi lebih cepat mencapai kondisi retak sehingga energi internal tidak lagi meningkat dan stabil setelah melewati titik maksimum sebelum akhirnya mengalami kegagalan.

- 4.3. Perbandingan Hasil Simulasi Impact Charpy per zona


- 4.3.1. Total Deformasi


|-2000<br><br>0<br><br>2000<br><br>4000<br><br>6000<br><br>8000<br><br>10000<br><br>12000<br><br>14000<br><br>16000<br><br>18000<br><br>0.00E+00 5.00E-03 1.00E-02 1.50E-02 2.00E-02 2.50E-02<br><br>TotalDeformasi(mm)<br><br>Waktu (s)<br><br>Total Deformasi WM Total Deformasi BM Total Deformasi Haz<br><br>|
|---|


##### TotalDeformasi(mm)

Gambar 4. 25. Grafik Perbandingan Total Deformasi dan Waktu

Berdasarkan Gambar grafik 4.25 dapat dilihat bahwa spesimen base metal mengalami deformasi yang paling besar dibandingkan Heat Affected Zone (HAZ) dan weld metal. Base metal cenderung memiliki karakteristik material yang relatif lebih rendah, akan tetapi dapat menyerap banyak energi impak karena deformasi plastis. Heat affected zone (HAZ) cenderung memiliki karakteristik material yang lebih keras dan sedikit lebih kuat akibat pengaruh panas dari proses pengelasan yang menyebabkan perubahan struktur mikro. Sedangkan weld metal cenderung memiliki deformasi paling kecil yang menunjukkan sifat lebih kaku dan keras akibat proses pengelasan, akan tetapi cenderung lebih getas jika menerima beban impak melebihi kapasitasnya. Nilai deformasi yang dihasilkan dari proses pembebanan umumnya lebih kecil jika materialnya lebih kaku dan lebih besar jika materialnya lebih lemah (Wibawa, 2020).

### 4.3.2. Equivalent Stress

|0<br><br>500<br><br>1000<br><br>1500<br><br>2000<br><br>2500<br><br>3000<br><br>3500<br><br>4000<br><br>4500<br><br>5000<br><br>0.00E+00 5.00E-03 1.00E-02 1.50E-02 2.00E-02 2.50E-02<br><br>Tegangan(MPa)<br><br>Waktu (s)<br><br>Tegangan WM Tegangan BM Tegangan Haz<br><br>|
|---|


##### Tegangan(MPa)

Gambar 4. 26. Grafik Perbandingan Equivalent Stress dan Waktu

Berdasarkan Gambar 4.26 dapat dilihat bahwa pada awal pembebanan material base metal, Heat Affected Zone (HAZ) dan weld metal mengalami lonjakan tegangan yang tinggi. Lonjakan tersebut diakibatkan oleh tingkat tegangan pada titik dimana pendulum mengenai spesimen pada daerah sekitar takik sebelum terjadi fraktur. Base metal merupakan material yang memiliki tegangan tertinggi, karena base metal mampu mempertahankan struktur kristal homogen dan tidak terpengaruh oleh siklus panas. HAZ memperlihatkan fluktuasi lebih banyak setelah puncak utama, karena adanya penurunan kekutan pada HAZ yang menyebabkan mekanisme fraktur bertahap. Sedangkan weld metal menunjukan pola tegangan yang lebih stabil setelah puncak yang mengindekasikan bahwa weld metal memiliki deformasi plastis lebih lanjut akibat penguatan presiptasi. Pola grafik tegangan ini sejalan dengan penelitian(Kori dkk., 2025) bahwa peningkatan waktu semula akan menikan kekuatan tegangan, regangan dan kemudian menurun akibat adanya deformasi plastis.

### 4.3.3. Equivalent Elastic Strain

|0.0000<br><br>0.0100<br><br>0.0200<br><br>0.0300<br><br>0.0400<br><br>0.0500<br><br>0.0600<br><br>0.0700<br><br>0.0800<br><br>0.0900<br><br>0.00E+00 5.00E-03 1.00E-02 1.50E-02 2.00E-02 2.50E-02<br><br>Regangan(mm/mm)<br><br>Waktu (s)<br><br>Regangan WM Regangan BM Regangan HAZ<br><br>|
|---|


##### Regangan(mm/mm)

Gambar 4. 27. Grafik Perbandingan Equivalent Elastic Strain dan Waktu

Berdasarkan Gambar grafik 4.27 dapat dilihat bahwa pada awal pembebanan material base metal, Heat Affected Zone (HAZ) dan weld metal mengalami lonjakan regangan yang tinggi seperti pola grafik tegangan. Lonjakan tersebut diakibatkan oleh tingkat regangan pada titik dimana pendulum mengenai spesimen pada daerah sekitar takik. Base metal merupakan material yang memiliki regangan tertinggi, karena base metal mampu mempertahankan struktur kristal homogen dan tidak terpengaruh oleh siklus panas. HAZ memperlihatkan fluktuasi lebih banyak setelah puncak utama, karena adanya penurunan kekutan pada HAZ yang menyebabkan mekanisme fraktur bertahap dan deformasi yang kompleks. Sedangkan weld metal menunjukan pola tegangan yang lebih rendah dan stabil setelah puncak yang mengindekasikan bahwa weld metal memiliki sifat kaku akibat penguatan presiptasi selama proses pengelaan. Pola grafik tegangan ini sejalan dengan penelitian (Kori dkk., 2025) bahwa peningkatan waktu semula akan menikan kekuatan tegangan, regangan dan kemudian menurun akibat adanya deformasi plastis.

### 4.3.4. Energi Probe

|0<br><br>10<br><br>20<br><br>30<br><br>40<br><br>50<br><br>60<br><br>0.00E+00 5.00E-03 1.00E-02 1.50E-02 2.00E-02 2.50E-02<br><br>Energi(J)<br><br>Waktu (s)<br><br>| | | | | | |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
<br><br>Welding Base Metal HAZ|
|---|


##### Energi(J)

Gambar 4. 28. Grafik Perbanding Energi Internal dan Waktu

Berdasarkan Gambar 4.28 dapat dilihat bahwa pada awal pembebanan material base metal, Heat Affected Zone (HAZ) dan weld metal mengalami lonjakan penyerapan energi yang tinggi. Lonjakan ini terjadi akibat proses penyerapan energi oleh spesimen pada saat pendulum mengenai daerah takik. Material yang menyerap energi paling besar yaitu base metal diikuti weld metal dan HAZ. Peningkatan energi internal yang berbeda pada setiap zona (base metal, weld metal, HAZ) utamanya dipengaruhi oleh variasi mikrostruktur, komposisi kimia, serta mekanisme deformasi dan fraktur masing-masing zona. Weld metal memiliki mikrostruktur lebih tough akibat presipitat dan penguatan dislokasi, sehingga energi internal diserap lebih sedang dan stabil selama proses impak. Sebaliknya, base metal cenderung lebih mudah mengalami deformasi besar, sehingga energi internal lebih tinggi dan stagnan. HAZ berada di antara kedua perilaku tersebut karena efek panas yang menyebabkan campuran sifat tough dan brittle. Variasi ini memperlihatkan bagaimana kondisi metalurgi lokal sangat mempengaruhi kemampuan spesimen dalam menyerap energi saat mengalami impak. Pola grafik energi internal pada hasil simulasi uji impak merupakan grafik akumulasi, di mana setiap nilai pada sumbu Y menggambarkan total energi yang telah diserap dan tertahan di dalam spesimen selama proses pembebanan sebagaimana telah diuraikan oleh (Kori dkk., 2025).

- 4.4. Grafik Laju Serapan Energi Berdasarkan hasil simulasi tegangan dan regangan dapat dihitung juga untuk


mendapatkan laju serapan energi. Grafik laju serapan energi menggambarkan seberapa cepat energi yang diserap oleh spesimen selama proses impak, serta dapat memumgkinkan untuk mengamati fenomen seperti overshoot negatif dan cacah puncak sebagaimana telah diuraikan oleh (Riyanta dkk., 2017).

![image 37](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile37.png>)

![image 38](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile38.png>)

![image 39](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile39.png>)

Gambar 4. 29. Grafik Laju Serapan Energi, Fenomena Overshoot Negatif a dan Variasi Cacah Puncak b

Berdasarkan Grafik 4.27 dapat dilihat bahwa laju serapan energi mampu mengidentifikasi fenomena pada laju serapan energi. Pada puncak pertama merupakan overshoot negatif a yang menunjukan deformasi plastis dan cacah puncak menunjukan adanya mekanisme fraktur, seperti perambatan retak yang tidak langsung, adanya benturan setelah material patah dan retakan pada struktur mikro. Fenomena ini biasanya lebih banyak terjadi pada weld metal dan HAZ, dikarenakan struktur mikro yang heterogen akibat proses pengelasan.

- 4.5. Validasi Data Hasil Simulasi Uji Impact Charpy Berdasarkan hasil perhitungan teoritis, energi yang dimiliki pendulum sebelum


tumbukan adalah 72,197 Joule. Hasil simulasi menunjukkan bahwa energi kinetik awal pada masing-masing spesimen, yaitu weld metal, HAZ dan base metal berkisar antara 72,3 Joule. Nilai hasil ini diperoleh setelah menjalankan simulasi secara berulang dengan menerapkan variasi mesh dari terkasar sampai terhalus hingga menemukan energi kinetik awal yang sesuai dengan hasil perhitungan teoritis. Selisih kecil antara nilai teoritis dan simulasi ini muncul akibat pembulatan data atau pendekatan numerik, namun tetap berada dalam batas toleransi yang wajar. Energi kinetik yang ditransfer dan kemudian diserap sebagai energi internal oleh masing-masing spesimen diperoleh sebesar weld metal 37,966 Joule, HAZ 31,929 Joule dan base metal 54,532 Joule yang berarti bahwa nilai ini merupakan estimasi energi yang diserap oleh spesimen selama tumbukan. Penelitian ini turut melakukan simulasi terhadap hasil eksperimen yang telah dilakukan oleh (Riyanta dkk., 2024) sebagai bentuk validasi utama dan mengingat penelitian ini belum melakukan pengujian eksperimental secara langsung. Dari simulasi yang dilakukan, diperoleh nilai sebesar 55,976 Joule, sedangkan hasil eksperimen dengan digital measurement menunjukkan nilai 55,452 Joule selisih 0,95 %.

### BAB V PENUTUP

- 5.1. Kesimpulan Profil penyerapan energi pada pengelasan paduan aluminium 3003 dalam


pengujian impact charpy berhasil dianalisis melalui simulasi numerik menggunakan metode elemen hingga (Finite Element Method). Berdasarkan hal tersebut, dapat disimpulkan bahwa base metal memiliki kemampuan paling unggul dalam menyerap energi impak ditandai oleh deformasi maksimum sebesar 15,346 mm, tegangan maksimum 4.690,3 MPa, regangan maksimum 0,0773 mm/mm, serta energi internal maksimum sebesar 54,532 Joule yang mencerminkan kekuatan awal tinggi dan daktilitas tinggi dalam menyerap energi impak melalui deformasi plastis signifikan. Weld metal menunjukkan deformasi terkecil sebesar 5,058.6 mm dengan tegangan maksimum 3.482,5 MPa, regangan maksimum 0,0617 mm/mm dan energi internal sebesar 37,966 Joule yang menunjukkan bahwa karakteristik material yang lebih keras dan kaku namun rentan terhadap keretakan saat beban impak. Sementara Heat Affected Zone (HAZ) memiliki deformasi yang cukup besar 12,330 mm, tegangan maksimum 3.768,6 MPa, regangan maksimum 0,0618 mm/mm, namun memiliki energi internal terendah 31,929 Joule yang mencerminkan ketahanan rendah terhadap energi impak akibat perubahan signifikan mikrostruktur akibat pengaruh termal dari proses pengelasan. Perbedaan nilai energi internal pada setiap zona menegaskan bahwa proses pengelasan memengaruhi kemampuan penyerapan energi material secara signifikan.

### 5.2. Saran

- 1. Penelitian ini dapat dikembangkan lebih lanjut dengan memvariasikan metode pengelasan atau jenis paduan aluminium untuk membandingkan efisiensi penyerapan energi antar metode dan material.
- 2. Validasi hasil simulasi dengan uji eksperimental langsung sangat dianjurkan untuk memastikan keakuratan model numerik serta meningkatkan relevansi hasil terhadap kondisi aktual di lapangan.
- 3. Pemodelan dengan mempertimbangkan efek termal, mikrostruktur dan fraktur dapat ditambahkan untuk memperoleh pemahaman lebih dalam terhadap mekanisme kegagalan material selama tumbukan.
- 4. Hasil simulasi ini dapat digunakan sebagai referensi awal dalam perancangan komponen struktural berbahan aluminium yang bekerja di bawah beban impak atau dinamis.


38

### DAFTAR PUSTAKA

Arif, J., Pungkas Prayitno, & Halan Al Hafidh. (2023). Analisis Static pada Aluminium 5052 dengan Variasi Sudut Menggunakan Solidworks. Teknosains : Jurnal Sains, Teknologi dan Informatika, 10(1), 38–50. https://doi.org/10.37373/tekno.v10i1.269

Ariyanto. (2024). Analisa Pengaruh Arus Listrik Pengelasan Gmaw Alumunium 5052. Jurnal Ilmiah Teknik, 3(1), 38–43. https://doi.org/10.56127/juit.v3i1.1159

Bashori, H. (2020). Uji Material Aluminium Paduan dengan Metode Kekerasan Rockwell. Angewandte Chemie International Edition, 6(11), 951–952.

Boangmanalu, E. P. D., Pratama, A. B., Qadry, A., Saragi, J. F. H., & Sinaga, F. T. H. (2023). Charpy and Izod Method Impak Strength Analysis on ST 37 Steel with Temperature Variations. Formosa Journal of Science and Technology, 2(12), 3329–3342. https://doi.org/10.55927/fjst.v2i12.7074

Erikman, E., Gunawan, Y., & Aksar, P. (2022). Analisis Distorsi Berbasis Metode Elemen Hingga Pada Proses Pengelasan Kampuh U dan V. Enthalpy : Jurnal Ilmiah Mahasiswa Teknik Mesin, 7(3), 129. https://doi.org/10.55679/enthalpy.v7i3.27124

Firmansyah. (2021). Impact Test. DETECH. https://www.detech.co.id/impact-test/ Gadayu, R. (2023). Analisa Perancangan Poros Roda Pengerak Mobil Emisia Borneo

Menggunakan Finite Element Method. Jurnal Ilmiah Momentum, 19(1), 33. https://doi.org/10.36499/jim.v19i1.8390

Hardi, W., & Umron, A. (2022). Response of Thin-walled Cylidrical Tubes Subjected to Axial Loading Under Dynamic Conditions. Seminar nasional Inovasi Teknologi UN PGRI Kediri, 42–46.

Isworo, A., Budiarto, U., & Budi, A. W. (2020). Analisis Perbandingan Kekuatan Impak,

Tarik, Tekuk dan Mikrogafi Pada Alumunium 606. Teknik Perkapalan, 5(2), 421–430. Jalil, S. A., Zulfikri, & Rahayu, T. (2017). Analisa Kekuatan Impak Pada Penyambungan.

15(2), 58–63.

Kastanto, R., Budiarto, U., & Jokosisworo, S. (2020). Perbandingan Kekuatan Impak, Tarik, dan Mikrografi Sambungan Las MIG dan TIG pada Aluminium 6061 dengan Variasi Media Pendingin Udara dan Air Tawar. Jurnal Teknik Perkapalan, 8(4), 560–570.

40

https://ejournal3.undip.ac.id/index.php/naval

Kori, T. H., Kassaye, F. T., Kozłowska, A., & Grajcar, A. (2025). Numerical Modeling of Charpy Impact Toughness Behavior and Stress Distribution of Quenching and Partitioning Steel. Symmetry, 17(1). https://doi.org/10.3390/sym17010053

LiU, I. (2022). Panduan Sistem Penomoran Paduan Aluminium. thyssenkrupp. https://tkcopperandbrass.com/2022/04/07/a-guide-to-the-aluminum-alloy-numberingsystem/

Lu, Q., Zhao, Y., Wang, Q., & Li, D. (2024). Investigation on the Corrosion Resistance of 3003 Aluminum Alloy in Acidic Salt Spray under Different Processing States. Metals, 14(2). https://doi.org/10.3390/met14020196

Mildayati Nurdin, Muhsin Z., & Badaruddin Anwar. (2021). Pengaruh Temperatur terhadap Kekuatan Impak Sambungan Las Listrik pada Material Besi Plat ST 42. Teknologi, 22(1), 35–42.

Murugan, S. S. (2020). Mechanical Properties of Materials: Definition, Testing and Application. International Journal of Modern Studies in Mechanical Engineering (IJMSME), 6(2), 28–38. https://doi.org/10.20431/2454-9711.0602003

Nuhgraha, Y., Rosa, M. K. A., & Agustian, I. (2020). Perancangan Alat Uji Impak Digital dengan Metode Charpy Untuk Mengukur Kekuatan Material Polimer. Jurnal Amplifier : Jurnal Ilmiah Bidang Teknik Elektro Dan Komputer, 10(2), 15–19. https://doi.org/10.33369/jamplifier.v10i2.15316

Olabode, M., Kah, P., & Martikainen, J. (2013). Aluminium alloys welding processes: Challenges, joint types and process selection. Proceedings of the Institution of Mechanical Engineers, Part B: Journal of Engineering Manufacture, 227(8), 1129– 1137. https://doi.org/10.1177/0954405413484015

Parthiban, K., Siva Shanmugam, N., & Sankaranarayanasamy, K. (2018). Experimental and Numerical Investigation of Charpy Impact Test of Spin Arc Welded C1018 plates. IOP Conference Series: Materials Science and Engineering, 455(1). https://doi.org/10.1088/1757-899X/455/1/012069

Riyanta, B., Nugroho, H., & Rahman, B. N. (2024). Modification Of Impact Testing Tools

For Research Of Aluminum Alloys Energy Absorption Profile. JMPM (Jurnal Material dan Proses Manufaktur), 8(1), 35–44. https://doi.org/10.18196/jmpm.v8i1.21883

Riyanta, B., Wardana, I. N. G., Irawan, Y. S., & Choiron, M. A. (2017). AISI 304 welding fracture resistance by a charpy impact test with a high speed sampling rate. Metals, 7(12), 1–15. https://doi.org/10.3390/met7120543

Sifa, A., & Endarmawan, T. (2013). Pemodelan Impak Test dengan Metode Charpy. Industrial Research Workshop and National Seminar, 4(08), 185–188.

- Wibawa, L. A. N. (2019). Prediksi Umur Fatik Struktur Crane Kapasitas 10 Ton Menggunakan Metode Elemen Hingga. Media Mesin: Majalah Teknik Mesin, 21(1), 18–24. https://doi.org/10.23917/mesin.v21i1.9422
- Wibawa, L. A. N. (2020). Simulasi umur fatik rangka main landing gear menggunakan metode elemen hingga. Jurnal Keilmuan dan Terapan Teknik Mesin, 10(2), 120–126. https://mechanicalbrothers.wordpress.com/2011/01/30/metode-elemen-hingga/


Wurdhani, R., Budiarto, U., & Amiruddin, W. (2021). Pengaruh Perlakuan Panas (Heat Treatment) Normalizing Terhadap Kekuatan Impak Aluminium 6061 Pengelasan MIG dengan Variasi Posisi dan Bentuk Kampuh. Jurnal Teknik Perkapalan, 9(1), 70. https://ejournal3.undip.ac.id/index.php/naval

Zulfadly, Z., & Ghony, M. A. (2022). Variasi Ampere Terhadap Kekuatan Tarik Pada Hasil Pengelasan Dengan Posisi Down Hand. Hexatech: Jurnal Ilmiah Teknik, 1(01), 39–50. https://doi.org/10.55904/hexatech.v1i01.75

### LAMPIRAN

- Lampiran 1. Parameter spesimen weld metal

![image 40](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile40.png>)

![image 41](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile41.png>)

- Lampiran 2. Property Filler ER4043

![image 42](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile42.png>)

- Lampiran 3. Visualisasi Energi Probe


43

#### Lampiran 4. Data Hasil Simulasi

|Weld Metal| | | | | |
|---|---|---|---|---|---|
|Waktu (s)|Total Deformasi|Tegangan|Regangan|Energi Internal|Energi Kinetik|
|1.18E-38|0|0|0,000|0|72330|
|4.08E-04|0,49897|674,53|0,011|1330,1|72458|
|8.16E-04|0,99829|1446,6|0,024|7005,5|72515|
|1.22E-03|1,5251|2197,6|0,035|17999|72386|
|1.63E-03|7,0914|3238,4|0,053|32379|74054|
|2.04E-03|32,725|3482,1|0,060|37966|73957|
|2.45E-03|58,481|3482,5|0,062|36268|73476|
|2.86E-03|84,249|864,8|0,015|33810|72785|
|3.27E-03|110,02|909,5|0,016|34077|72879|
|3.67E-03|135,79|583,99|0,010|33626|72722|
|4.08E-03|161,56|579,13|0,010|33479|72778|
|4.49E-03|187,34|555,31|0,009|33395|72767|
|4.90E-03|213,11|565,26|0,009|33493|72673|
|5.31E-03|238,89|573,81|0,010|33456|72714|
|5.71E-03|264,66|579,17|0,010|33513|72661|
|6.12E-03|290,43|580,28|0,010|33532|72646|
|6.53E-03|316,21|560,61|0,009|33470|72711|
|6.94E-03|341,98|560,29|0,009|33517|72666|
|7.35E-03|367,75|562,34|0,010|33490|72694|
|7.76E-03|393,53|574,73|0,010|33476|72709|
|8.16E-03|419,3|580|0,010|33540|72646|
|8.57E-03|445,07|569,61|0,010|33514|72672|
|8.98E-03|470,85|562,98|0,010|33539|72648|
|9.39E-03|496,62|558,44|0,010|33570|72617|
|9.80E-03|522,4|570,08|0,010|33528|72659|
|1.02E-02|548,17|578,66|0,010|33555|72632|
|1.06E-02|573,95|578,79|0,010|33551|72636|
|1.10E-02|599,72|572,58|0,010|33539|72648|
|1.14E-02|625,49|563,68|0,010|33585|72601|
|1.18E-02|651,27|566,63|0,010|33568|72619|
|1.22E-02|677,04|570,4|0,010|33569|72618|
|1.27E-02|702,81|575,2|0,010|33596|72591|
|1.31E-02|728,59|572,75|0,010|33575|72612|
|1.35E-02|754,36|568,04|0,010|33596|72591|
|1.39E-02|780,14|568,29|0,010|33604|72583|
|1.43E-02|805,91|570,07|0,010|33585|72603|
|1.47E-02|831,68|574|0,010|33213|72582|
|1.51E-02|857,46|572,35|0,010|33149|72592|
|1.55E-02|883,23|571,41|0,010|33146|72595|


|1.59E-02|909,01|570,6|0,010|33164|72577|
|---|---|---|---|---|---|
|1.63E-02|934,78|572,59|0,010|33157|72585|
|1.67E-02|960,55|574,27|0,010|33171|72571|
|1.71E-02|986,33|571,73|0,010|33179|72564|
|1.76E-02|1012,1|569,6|0,010|33175|72568|
|1.80E-02|1037,9|568,61|0,010|33182|72561|
|1.84E-02|1063,7|572,11|0,010|33174|72569|
|1.88E-02|1089,4|574,65|0,010|33176|72568|
|1.92E-02|1115,2|574,06|0,010|33180|72565|
|1.96E-02|1141|571,04|0,010|33179|72566|
|2.00E-02|1166,7|569,29|0,010|33191|72555|


Lampiran 5. Parameter HAZ

![image 43](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile43.png>)

- Lampiran 6. Property HAZ


![image 44](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile44.png>)

- Lampiran 7. Visualisasi Energi Probe


![image 45](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile45.png>)

Lampiran 8. Data Hasil Simulasi

|Heat Affected Zone (HAZ)| | | | | |
|---|---|---|---|---|---|
|Waktu (s)|Total Deformasi|Tegangan|Regangan|Energi Internal|Energi Kinetik|
|1.18E-38|0|0|0,000|0|72330|
|4.08E-04|0,49914|950,04|0,022|1859|72377|
|8.16E-04|1,0649|1413,6|0,032|7718,2|72419|
|1.22E-03|1,7039|2107|0,045|19113|72435|
|1.63E-03|9,6274|2398,1|0,041|23484|73218|
|2.04E-03|41,216|3682,4|0,060|24706|73587|
|2.45E-03|72,826|3768,6|0,062|29294|73005|
|2.86E-03|104,44|585,92|0,011|29329|72821|
|3.27E-03|136,05|1096,6|0,019|29377|72659|
|3.67E-03|167,67|502,4|0,010|29016|72571|
|4.08E-03|199,28|1550,7|0,025|27925|72626|
|4.49E-03|230,89|504,6|0,009|31929|72925|
|4.90E-03|262,5|509|0,010|31893|72907|
|5.31E-03|294,12|503,93|0,011|31865|72902|
|5.71E-03|325,73|502,98|0,011|31892|72926|
|6.12E-03|357,34|518,21|0,013|31863|72926|
|6.53E-03|388,96|794,24|0,014|31793|72922|
|6.94E-03|420,57|766,06|0,013|31705|72936|
|7.35E-03|471,61|769,6|0,013|31680|72941|
|7.76E-03|536,77|770,25|0,013|31680|72947|
|8.16E-03|601,93|770,42|0,013|31659|72946|
|8.57E-03|667,08|772,83|0,013|31661|72944|
|8.98E-03|732,23|774|0,013|31663|72945|
|9.39E-03|797,39|773,35|0,013|31597|72958|
|9.80E-03|862,54|772,27|0,013|31467|72958|
|1.02E-02|927,7|773,27|0,013|31431|72956|
|1.06E-02|992,85|765,72|0,013|31343|72949|
|1.10E-02|1058|772,42|0,013|31268|72944|


|1.14E-02|1123,2|772,51|0,013|31256|72945|
|---|---|---|---|---|---|
|1.18E-02|1188,3|772,57|0,013|31216|72945|
|1.22E-02|1253,5|772,89|0,013|31217|72944|
|1.27E-02|1318,6|772,56|0,013|31216|72943|
|1.31E-02|1383,8|771,85|0,013|31217|72943|
|1.35E-02|1448,9|771,65|0,013|31217|72942|
|1.39E-02|1514,1|771,94|0,013|31211|72941|
|1.43E-02|1579,2|771,62|0,013|31212|72941|
|1.47E-02|1644,4|771,03|0,013|31211|72943|
|1.51E-02|1709,6|771|0,013|31212|72944|
|1.55E-02|1774,7|771,24|0,013|31212|72943|
|1.59E-02|1839,9|770,95|0,013|31205|72942|
|1.63E-02|1905|770,45|0,013|31179|72942|
|1.67E-02|1970,2|770,49|0,013|31031|72941|
|1.71E-02|2035,3|770,65|0,013|31025|72941|
|1.76E-02|2100,5|770,32|0,013|31019|72942|
|1.80E-02|2165,6|769,87|0,013|30845|72969|
|1.84E-02|2230,8|769,92|0,013|30747|72968|
|1.88E-02|2295,9|770,01|0,013|30676|72968|
|1.92E-02|2361,1|769,65|0,013|30676|72967|
|1.96E-02|2426,2|769,22|0,013|30677|72967|
|2.00E-02|2491,4|769,26|0,013|30671|72966|


#### Lampiran 9. Parameter Base Metal

![image 46](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile46.png>)

#### Lampiran 10. Property Base Metal

![image 47](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile47.png>)

#### Lampiran 11. Visualisasi Energi Probe

![image 48](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile48.png>)

Lampiran 12. Data Hasil Simulasi

|Base Metal| | | | | |
|---|---|---|---|---|---|
|Waktu (s)|Total Deformasi|Tegangan|Regangan|Energi Internal|Energi Kinetik|
|1.18E-38|0|0|0,000|0|72330|
|4.08E-04|0,49898|660,5|0,011|1352,8|72410|
|8.16E-04|0,99795|1481,5|0,025|7055,5|72477|
|1.22E-03|1,4969|2288|0,038|17491|72472|
|1.63E-03|1,9958|3133|0,053|32782|72413|
|2.04E-03|2,5771|4690,3|0,077|54532|72560|
|2.45E-03|63,87|1851,3|0,029|50085|74407|
|2.86E-03|136,42|1933,1|0,031|50271|73656|
|3.27E-03|208,99|833,64|0,014|49547|73325|
|3.67E-03|286,11|622,33|0,011|49000|73237|
|4.08E-03|364,96|571,34|0,010|48811|73201|
|4.49E-03|443,79|572,87|0,009|48725|73161|
|4.90E-03|522,64|460,41|0,007|48298|73166|
|5.31E-03|601,49|451,42|0,007|48117|73168|
|5.71E-03|680,33|285,09|0,006|47045|73156|


|6.12E-03|759,18|283,53|0,007|46405|73151|
|---|---|---|---|---|---|
|6.53E-03|838,02|281,24|0,007|45855|73145|
|6.94E-03|916,88|278,58|0,007|45757|73135|
|7.35E-03|995,72|276,38|0,007|45553|73137|
|7.76E-03|1074,6|274,25|0,006|45226|73132|
|8.16E-03|1153,4|271,93|0,006|44745|73128|
|8.57E-03|1232,3|268,42|0,006|43651|73131|
|8.98E-03|1311,1|265,28|0,006|43101|73124|
|9.39E-03|1390|262,15|0,006|42939|73119|
|9.80E-03|1468,8|258,93|0,006|42638|73122|
|1.02E-02|1547,6|255,64|0,006|42597|73123|
|1.06E-02|1626,5|251,83|0,006|42546|73120|
|1.10E-02|1705,3|248,33|0,006|42546|73122|
|1.14E-02|1784,2|245,02|0,006|42328|73117|
|1.18E-02|1863|241,95|0,006|42334|73113|
|1.22E-02|1941,9|239,24|0,006|42197|73116|
|1.27E-02|2020,7|237,08|0,006|42055|73111|
|1.31E-02|2099,6|235,34|0,006|41949|73108|
|1.35E-02|2178,4|234,99|0,006|41831|73110|
|1.39E-02|2257,3|235,32|0,005|41837|73106|
|1.43E-02|2336,1|236,16|0,005|41840|73105|
|1.47E-02|2415|237,23|0,005|41842|73104|
|1.51E-02|2493,8|238,47|0,005|41846|73103|
|1.55E-02|2572,7|239,87|0,005|41393|73099|
|1.59E-02|2651,5|241,19|0,005|41290|73102|
|1.63E-02|2730,4|242,54|0,005|41296|73098|
|1.67E-02|2809,2|243,83|0,005|41189|73097|
|1.71E-02|2888|257,84|0,005|40584|73068|
|1.76E-02|2966,9|266,37|0,005|39996|73066|
|1.80E-02|3045,7|264,43|0,005|39789|73065|
|1.84E-02|3124,6|263,69|0,005|39789|73066|
|1.88E-02|3203,4|262,63|0,005|39651|73063|
|1.92E-02|3282,3|271,73|0,005|39575|73063|
|1.96E-02|3361,1|272,23|0,005|39463|73064|
|2.00E-02|3440|272,98|0,005|39422|73061|


- Lampiran 13. Parameter Validasi Aluminium 5052
- Lampiran 14. Property Aluminium 5052
- Lampiran 15. Data Hasil Simulasi Al 5052


![image 49](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile49.png>)

![image 50](<Laporan Tugas Akhir_M. Muamar Kadafi_images/imageFile50.png>)

|Aluminium 5052| | | | | |
|---|---|---|---|---|---|
|Waktu (s)|Total Deformasi|Tegangan|Regangan|Energi Internal|Energi Kinetik|
|1.18E-38|0|0|0,000|0|72330|
|4.08E-04|0,49902|680,9|0,011|1361,6|72450|
|8.16E-04|0,99795|1473,9|0,024|7149,9|72499|
|1.22E-03|1,4969|2338|0,039|17786|72414|
|1.63E-03|1,9959|3202,1|0,053|33273|72370|
|2.04E-03|2,5806|4771,8|0,082|55976|72599|
|2.45E-03|32,327|5106,6|0,073|51064|73886|
|2.86E-03|66,672|5287,7|0,076|50927|73208|
|3.27E-03|101,04|5247|0,075|51095|72716|


|3.67E-03|135,42|5260,6|0,076|49615|72620|
|---|---|---|---|---|---|
|4.08E-03|169,8|5238,3|0,075|49359|72617|
|4.49E-03|204,19|3919,2|0,065|49623|72598|
|4.90E-03|238,57|4782,3|0,078|49760|72586|
|5.31E-03|272,96|5360,4|0,085|50033|72604|
|5.71E-03|307,34|5145,8|0,083|49592|72716|
|6.12E-03|341,73|2811,1|0,041|46423|72740|
|6.53E-03|376,11|2218,9|0,032|53026|73308|
|6.94E-03|410,5|3515,7|0,065|50733|73317|
|7.35E-03|520,38|3605,6|0,052|50547|73290|
|7.76E-03|700,71|2103,2|0,030|50929|73284|
|8.16E-03|881,05|1817,1|0,026|50202|73285|
|8.57E-03|1061,4|1821,8|0,026|50208|73291|
|8.98E-03|1241,8|1823,3|0,026|49977|73290|
|9.39E-03|1422,1|1824,6|0,026|49888|73291|
|9.80E-03|1602,5|1825,1|0,026|49830|73290|
|1.02E-02|1782,8|1824,6|0,026|49750|73291|
|1.06E-02|1963,2|1824,6|0,026|49610|73292|
|1.10E-02|2143,5|1816,6|0,026|48162|73293|
|1.14E-02|2323,8|1815,9|0,026|48130|73299|
|1.18E-02|2504,2|1815,9|0,026|48132|73300|
|1.22E-02|2684,6|1821,8|0,026|48136|73300|
|1.27E-02|2864,9|1821,1|0,026|48138|73300|
|1.31E-02|3045,3|1820,6|0,026|47997|73301|
|1.35E-02|3225,6|1820,1|0,026|48000|73301|
|1.39E-02|3405,9|1819,4|0,026|47803|73302|
|1.43E-02|3586,3|1818,8|0,026|47806|73303|
|1.47E-02|3766,7|1818,1|0,026|47809|73304|
|1.51E-02|3947|1817|0,026|47678|73305|
|1.55E-02|4127,4|1816|0,026|47554|73307|
|1.59E-02|4307,7|1814,8|0,026|47558|73308|
|1.63E-02|4488,1|1813,4|0,026|47502|73310|
|1.67E-02|4668,4|1811,8|0,026|47261|73313|
|1.71E-02|4848,8|1810,2|0,026|47265|73315|
|1.76E-02|5029,1|1808,3|0,026|47269|73318|
|1.80E-02|5209,5|1808,2|0,026|47273|73321|
|1.84E-02|5389,8|1807,7|0,026|47235|73325|
|1.88E-02|5570,2|1807,4|0,026|47190|73329|
|1.92E-02|5750,5|1807|0,026|47050|73333|
|1.96E-02|5930,9|1806,7|0,026|46849|73338|
|2.00E-02|6111,2|1806,2|0,026|46394|73344|


