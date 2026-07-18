HASIL SIMULASI PROFIL PENYERAPAN ENERGI PADA PENGELASAN PADUAN ALUMINIUM 3003 DALAM PENGUJIAN IMPACT CHARPY

VALIDASI PERITUNGAN

- 1. Perhitungan energi serap 𝑚 × 𝑔 × 𝐿 ( 𝐶𝑜𝑠 𝛽 − 𝐶𝑜𝑠 𝑎 )

Keterangan

m : Massa Pendulum (kg) g : Graviatasi (9,81 m/s2) L : Panjang lengan pendulum (meter) α : Sudut awal ketentuan β : Sudut akhir pengukuran dengan Hasil

5,8 × 9,81 × 0,68 ( 𝐶𝑜𝑠 95˙ − 𝐶𝑜𝑠 150˙ ) = 30,13497 𝐽𝑜𝑢𝑙𝑒

- 2. Pembuatan Desain


![image 1](<Hasil Simulasi ansys perhitungan_images/imageFile1.png>)

Keteranagan

- a. Pendulum
- b. Suport atau bantalan Spesimen
- c. Spesimen Benda uji dengan spesifikasi sesuai standar


# 3. Property Bahan

- a. Aluminium 3003
- b. Structural Steel


![image 2](<Hasil Simulasi ansys perhitungan_images/imageFile2.png>)

![image 3](<Hasil Simulasi ansys perhitungan_images/imageFile3.png>)

# 4. Pemodelan geomtry Pendulum dan support ini didukung oleh material Structural Steel yang memiliki stiffness behavior rigid untuk memastikan ketahanan dan kestabilan struktur. Spesimen benda uji menggunakan Aluminium 3003 dengan stiffness behavior flexible untuk memungkinkan deformasi selama pengujian. Untuk meningkatkan massa pendulum hingga 5,8 kg perlu adanya Point Mass yang ditempatkan pada bagian pendulum berfungsi untuk menambah inersia dan mempengaruhi dinamika gerak pendulum.

![image 4](<Hasil Simulasi ansys perhitungan_images/imageFile4.png>)

- 5. Mesh Mesh pada pendulum dan support diberikan ukuran 5 mm, sedangkan spesimen benda uji menggunakan mesh lebih halus yaitu 0,8 mm untuk meningkatkan akurasi hasil analisis. Selanjutnya, diterapkan Sweep Method pada geometry di bagian body spesimen benda uji dengan elemen order linier yang memastikan pemodelan lebih efisien dan sesuai dengan bentuk geometri spesimen.
- 6. Velocity atau kecepatan Kecepatan diberikan pada sumbu Y component di bagian pendulum sesuai dengan nilai yang telah dihitung sebelumnya. Pemberian kecepatan ini bertujuan untuk mengontrol pergerakan awal pendulum, memastikan simulasi berjalan sesuai kondisi nyata, serta menganalisis respons spesimen benda uji terhadap gaya yang dihasilkan.


![image 5](<Hasil Simulasi ansys perhitungan_images/imageFile5.png>)

![image 6](<Hasil Simulasi ansys perhitungan_images/imageFile6.png>)

Dengan perhitungan kecepatan sebagai berikut : √2 × 𝑔 × 𝑙 ( 𝐶𝑜𝑠 𝛽 − 𝐶𝑜𝑠 𝑎 )

Keterangan g : Graviatasi (9,81 m/s2) L : Panjang lengan pendulum (meter) α : Sudut awal ketentuan β : Sudut akhir Pengukuran dengan hasil √2 × 9,81 × 0,65 ( 𝐶𝑜𝑠 95˙ − 𝐶𝑜𝑠 150˙ ) = 3,22356 m/s – 3223,6 mm/s

- 7. Solution


- a. Total Deformasi Total Deformasi adalah besarnya perubahan bentuk atau perpindahan total suatu benda akibat beban yang diberikan dalam analisis struktural. Hasil Total deformasi maximum yaitu 2561 mm dengan kondisi specimen patah.


![image 7](<Hasil Simulasi ansys perhitungan_images/imageFile7.png>)

![image 8](<Hasil Simulasi ansys perhitungan_images/imageFile8.png>)

- b. Starain Equivalent Elastic Strain adalah ukuran regangan total yang terjadi dalam material akibat beban yang diberikan, tanpa mempertimbangkan deformasi plastis. Hasil Equivalent Elastic Strain maximum yaitu 0,0052199 mm/mm atau 0,52199%.
- c. Stress Equivalent Stress adalah tegangan ekuivalen yang digunakan dalam analisis kegagalan material berdasarkan teori distorsi energi. Hasil Equivalent Stress yaitu minimum 1,0246MPa dan maximum 284,82 MPa.


![image 9](<Hasil Simulasi ansys perhitungan_images/imageFile9.png>)

![image 10](<Hasil Simulasi ansys perhitungan_images/imageFile10.png>)

![image 11](<Hasil Simulasi ansys perhitungan_images/imageFile11.png>)

![image 12](<Hasil Simulasi ansys perhitungan_images/imageFile12.png>)

- d. Energi Probe Energi Probe adalah metode analisis energi dalam simulasi elemen hingga yang digunakan untuk mengevaluasi distribusi dan perubahan energi pada suatu sistem selama proses deformasi atau interaksi gaya. Hasil Energi internal yaitu 73,581 joule Joule dan energi kinetic yaitu maximum 60,513 Joule dan minimum 30,190 Joule.


![image 13](<Hasil Simulasi ansys perhitungan_images/imageFile13.png>)

![image 14](<Hasil Simulasi ansys perhitungan_images/imageFile14.png>)

- 8. Parameter
- 9. Kesimpulan Hasil perhitungan teoritis menunjukkan bahwa energi serap sebesar 30,13497 Joule. Dalam simulasi, energi kinetik maksimum tercatat 60,522 Joule, sedangkan energi kinetik minimum adalah 30,190 Joule dan energi internal yang diperoleh adalah 73,581 Joule. Untuk menentukan energi serap dalam simulasi digunakan selisih antara energi kinetik maksimum dan minimum yaitu 30,332 Joule. Dengan demikian error yang dihasilkan dalam perbandingan antara hasil teoritis dan simulasi adalah 0,62%.


![image 15](<Hasil Simulasi ansys perhitungan_images/imageFile15.png>)

