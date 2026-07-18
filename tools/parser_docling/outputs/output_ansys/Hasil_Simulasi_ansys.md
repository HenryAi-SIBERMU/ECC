## HASIL SIMULASI PROFIL PENYERAPAN ENERGI PADA PENGELASAN PADUAN ALUMINIUM 3003 DALAM PENGUJIAN IMPACT CHARPY

## VALIDASI PERITUNGAN

1. Perhitungan energi serap

## Keterangan

m : Massa Pendulum (kg)

g  : Graviatasi (9,81 m/s 2 )

L  : Panjang lengan pendulum (meter)

α  : Sudut awal ketentuan

β  : Sudut akhir pengukuran

dengan Hasil

$$5 , 8 \times 9 , 8 1 \times 0 , 6 8 \left ( \cos 9 5 ^ { \cdot } - \cos 1 5 0 ^ { \cdot } \right ) = 3 0 , 1 3 4 9 7 \, J o u l e$$

2. Pembuatan Desain

![Image](c:\Users\yooma\OneDrive\Desktop\duniahub\client\18. duniahub-agenticdosen\tools\parser_docling\output_ansys_v3\Hasil_Simulasi_ansys_artifacts\image_000000_2545dddca38aad964b9de3aa3b115d5a14b7be947d4ba61d04d9abb8c1fa9d98.png)

## Keteranagan

- a. Pendulum
- b. Suport atau bantalan Spesimen
- c. Spesimen Benda uji dengan spesifikasi sesuai standar

$$m \times g \times L \left ( \cos \beta - \cos a \right )$$

## 3. Property Bahan

## a. Aluminium 3003

![Image](c:\Users\yooma\OneDrive\Desktop\duniahub\client\18. duniahub-agenticdosen\tools\parser_docling\output_ansys_v3\Hasil_Simulasi_ansys_artifacts\image_000001_56f3412bafac842bf1fb4050f266e13babce9a43b69ee6123e019cd956825cc1.png)

## b. Structural Steel

![Image](c:\Users\yooma\OneDrive\Desktop\duniahub\client\18. duniahub-agenticdosen\tools\parser_docling\output_ansys_v3\Hasil_Simulasi_ansys_artifacts\image_000002_be2a2e9763d86f99a8eba8ee87742ce6e33036d377254251c6719b5dce0d3734.png)

4. Pemodelan geomtry

Pendulum dan support ini didukung oleh material Structural Steel yang memiliki stiffness  behavior  rigid  untuk  memastikan  ketahanan  dan  kestabilan  struktur. Spesimen  benda  uji  menggunakan  Aluminium  3003  dengan  stiffness  behavior flexible untuk memungkinkan deformasi selama pengujian.

Untuk meningkatkan massa pendulum hingga 5,8 kg perlu adanya Point Mass yang ditempatkan pada bagian pendulum  berfungsi untuk menambah  inersia  dan mempengaruhi dinamika gerak pendulum.

![Image](c:\Users\yooma\OneDrive\Desktop\duniahub\client\18. duniahub-agenticdosen\tools\parser_docling\output_ansys_v3\Hasil_Simulasi_ansys_artifacts\image_000003_a5d6f52bab5cc884d99a63484ebeb418dbeed25b6da0a047643fc3345a8ea9dc.png)

5. Mesh

Mesh  pada  pendulum  dan  support  diberikan  ukuran  5  mm,  sedangkan  spesimen benda uji menggunakan mesh lebih halus yaitu 0,8 mm untuk meningkatkan akurasi hasil analisis.

Selanjutnya,  diterapkan  Sweep  Method  pada  geometry  di  bagian  body  spesimen benda uji dengan elemen order linier yang memastikan pemodelan lebih efisien dan sesuai dengan bentuk geometri spesimen.

![Image](c:\Users\yooma\OneDrive\Desktop\duniahub\client\18. duniahub-agenticdosen\tools\parser_docling\output_ansys_v3\Hasil_Simulasi_ansys_artifacts\image_000004_41fa4ade36fcbabf2be4f1ff084bc8b9f8ffad3a1856bb7496d061e189b11f24.png)

6. Velocity atau kecepatan

Kecepatan diberikan pada sumbu Y component di bagian pendulum sesuai dengan nilai  yang  telah  dihitung  sebelumnya.  Pemberian  kecepatan  ini  bertujuan  untuk mengontrol pergerakan awal pendulum, memastikan simulasi berjalan sesuai kondisi nyata, serta menganalisis respons spesimen benda uji terhadap gaya yang dihasilkan.

![Image](c:\Users\yooma\OneDrive\Desktop\duniahub\client\18. duniahub-agenticdosen\tools\parser_docling\output_ansys_v3\Hasil_Simulasi_ansys_artifacts\image_000005_d1969270e567ffffd474f389799f821e1b46dff233ee0686f5be7a24987f19e8.png)

Dengan perhitungan kecepatan sebagai berikut :

$$\sqrt { 2 } \times g \times l \left ( \cos \beta - \cos a \right )$$

## Keterangan

g  : Graviatasi (9,81 m/s 2 )

L  : Panjang lengan pendulum (meter)

α  : Sudut awal ketentuan

β  : Sudut akhir Pengukuran

dengan hasil

$$\sqrt { 2 } \times 9 , 8 1 \times 0 , 6 5 \left ( \cos 9 5 \cdot - \cos 1 5 0 \cdot \right ) = 3 , 2 2 3 5 6 \, m / s - 3 2 2 3 , 6 \, m m / s$$

## 7. Solution

- a. Total Deformasi

Total Deformasi adalah besarnya perubahan bentuk atau perpindahan total suatu benda  akibat  beban  yang  diberikan  dalam  analisis  struktural.  Hasil  Total deformasi maximum yaitu 2561 mm dengan kondisi specimen patah.

![Image](c:\Users\yooma\OneDrive\Desktop\duniahub\client\18. duniahub-agenticdosen\tools\parser_docling\output_ansys_v3\Hasil_Simulasi_ansys_artifacts\image_000006_98b36580e71d44640cae67077ea4fa7be48c70d5b3d8277f9d02f9317f3ac4cc.png)

![Image](c:\Users\yooma\OneDrive\Desktop\duniahub\client\18. duniahub-agenticdosen\tools\parser_docling\output_ansys_v3\Hasil_Simulasi_ansys_artifacts\image_000007_dd4f8f3355a0d2a4de321ddf412bf0d7a8b7891d7dfdf406fa46f164779b95cf.png)

## b. Starain

Equivalent  Elastic  Strain  adalah  ukuran  regangan  total  yang  terjadi  dalam material  akibat  beban  yang  diberikan,  tanpa  mempertimbangkan  deformasi plastis. Hasil Equivalent Elastic Strain maximum yaitu 0,0052199 mm/mm atau 0,52199%.

![Image](c:\Users\yooma\OneDrive\Desktop\duniahub\client\18. duniahub-agenticdosen\tools\parser_docling\output_ansys_v3\Hasil_Simulasi_ansys_artifacts\image_000008_213790cfd2adde7e43e66a2cad9e8e4cd432c10078dc4b9b8763ce108a410aad.png)

## c. Stress

Equivalent  Stress  adalah  tegangan  ekuivalen  yang  digunakan  dalam  analisis kegagalan  material  berdasarkan  teori  distorsi  energi.  Hasil  Equivalent  Stress yaitu minimum 1,0246MPa dan maximum 284,82 MPa.

![Image](c:\Users\yooma\OneDrive\Desktop\duniahub\client\18. duniahub-agenticdosen\tools\parser_docling\output_ansys_v3\Hasil_Simulasi_ansys_artifacts\image_000009_15bbe8895fd8abc61f3317b36f9deda590205400862a6e61737da9b405a56a72.png)

## d. Energi Probe

Energi Probe adalah metode analisis energi dalam simulasi elemen hingga yang digunakan untuk mengevaluasi distribusi dan perubahan energi pada suatu sistem selama proses deformasi atau interaksi gaya. Hasil Energi internal yaitu 73,581 joule Joule dan energi kinetic yaitu maximum 60,513 Joule dan minimum 30,190 Joule.

![Image](c:\Users\yooma\OneDrive\Desktop\duniahub\client\18. duniahub-agenticdosen\tools\parser_docling\output_ansys_v3\Hasil_Simulasi_ansys_artifacts\image_000010_0cd15cdd00e52d3e2bc5853265eb03349967be780a3295d60d81aeace5301f32.png)

![Image](c:\Users\yooma\OneDrive\Desktop\duniahub\client\18. duniahub-agenticdosen\tools\parser_docling\output_ansys_v3\Hasil_Simulasi_ansys_artifacts\image_000011_3004808494673b637047a960536b87fb4eddf8eed47cdfdd063531cad9da02fe.png)

8. Parameter
9. Kesimpulan

![Image](c:\Users\yooma\OneDrive\Desktop\duniahub\client\18. duniahub-agenticdosen\tools\parser_docling\output_ansys_v3\Hasil_Simulasi_ansys_artifacts\image_000012_96f6f861d0b1668ba047902993624aaf47a5fecc50b9fd8da2fbdf7a3480cc00.png)

Hasil perhitungan teoritis menunjukkan bahwa energi serap sebesar 30,13497 Joule. Dalam simulasi, energi kinetik maksimum tercatat 60,522 Joule, sedangkan energi kinetik  minimum  adalah  30,190  Joule  dan  energi  internal  yang  diperoleh  adalah 73,581  Joule.  Untuk  menentukan  energi  serap  dalam  simulasi  digunakan  selisih antara energi kinetik maksimum dan minimum yaitu 30,332 Joule. Dengan demikian error yang dihasilkan dalam perbandingan antara hasil teoritis dan simulasi adalah 0,62%.