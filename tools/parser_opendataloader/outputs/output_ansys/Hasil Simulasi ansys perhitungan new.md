# HASIL SIMULASI PROFIL PENYERAPAN ENERGI PADA PENGELASAN PADUAN ALUMINIUM 3003 DALAM PENGUJIAN IMPACT CHARPY

VALIDASI PERITUNGAN

- 1. Perhitungan energi serap 𝑚 × 𝑔 × 𝐿 ( 𝐶𝑜𝑠 𝛽 − 𝐶𝑜𝑠 𝑎 )

Keterangan

m : Massa Pendulum (kg) g : Graviatasi (9,81 m/s2) L : Panjang lengan pendulum (meter) α : Sudut awal ketentuan β : Sudut akhir pengukuran dengan Hasil

5,8 × 9,81 × 0,68 ( 𝐶𝑜𝑠 95˙ − 𝐶𝑜𝑠 150˙ ) = 30,13497 𝐽𝑜𝑢𝑙𝑒

- 2. Pembuatan Desain


![image 1](<Hasil Simulasi ansys perhitungan new_images/imageFile1.png>)

Keteranagan

- a. Pendulum
- b. Suport atau bantalan Spesimen
- c. Spesimen Benda uji dengan spesifikasi sesuai standar


# 3. Property Bahan

- a. Aluminium 3003
- b. Structural Steel


![image 2](<Hasil Simulasi ansys perhitungan new_images/imageFile2.png>)

![image 3](<Hasil Simulasi ansys perhitungan new_images/imageFile3.png>)

# 4. Pemodelan geomtry Pendulum dan support ini didukung oleh material Structural Steel yang memiliki stiffness behavior rigid untuk memastikan ketahanan dan kestabilan struktur. Spesimen benda uji menggunakan Aluminium 3003 dengan stiffness behavior flexible untuk memungkinkan deformasi selama pengujian. Untuk meningkatkan massa pendulum hingga 5,8 kg perlu adanya Point Mass yang ditempatkan pada bagian pendulum berfungsi untuk menambah inersia dan mempengaruhi dinamika gerak pendulum.

![image 4](<Hasil Simulasi ansys perhitungan new_images/imageFile4.png>)

- 5. Mesh Mesh pada pendulum, support dan specimen face yang tidak termasuk di sizing diberikan ukuran 1,1 mm, sedangkan spesimen benda uji yang diberi sizing di face/permukaan menggunakan mesh lebih halus yaitu 0,6 mm untuk meningkatkan akurasi hasil analisis sperti gambar dibawah ini.


![image 5](<Hasil Simulasi ansys perhitungan new_images/imageFile5.png>)

Face depan bagian Notch takik 1

![image 6](<Hasil Simulasi ansys perhitungan new_images/imageFile6.png>)

|Face atas bagian terkena tumbukan|
|---|


![image 7](<Hasil Simulasi ansys perhitungan new_images/imageFile7.png>)

|Face belakang bagian Notch takik|
|---|


![image 8](<Hasil Simulasi ansys perhitungan new_images/imageFile8.png>)

|Hasil Mesh|
|---|


Selanjutnya, diterapkan Sweep Method pada geometry di bagian body spesimen benda uji dengan elemen order linier yang memastikan pemodelan lebih efisien dan sesuai dengan bentuk geometri spesimen.

![image 9](<Hasil Simulasi ansys perhitungan new_images/imageFile9.png>)

- 6. Velocity atau kecepatan Kecepatan diberikan pada sumbu Y component di bagian pendulum sesuai dengan nilai yang telah dihitung sebelumnya. Pemberian kecepatan ini bertujuan untuk mengontrol pergerakan awal pendulum, memastikan simulasi berjalan sesuai kondisi nyata, serta menganalisis respons spesimen benda uji terhadap gaya yang dihasilkan.


![image 10](<Hasil Simulasi ansys perhitungan new_images/imageFile10.png>)

Dengan perhitungan kecepatan sebagai berikut : √2 × 𝑔 × 𝑙 ( 𝐶𝑜𝑠 𝛽 − 𝐶𝑜𝑠 𝑎 )

Keterangan g : Graviatasi (9,81 m/s2) L : Panjang lengan pendulum (meter) α : Sudut awal ketentuan β : Sudut akhir Pengukuran dengan hasil √2 × 9,81 × 0,65 ( 𝐶𝑜𝑠 95˙ − 𝐶𝑜𝑠 150˙ ) = 3,22356 m/s – 3223,6 mm/s

- 7. Solution


- a. Total Deformasi Total Deformasi adalah besarnya perubahan bentuk atau perpindahan total suatu benda akibat beban yang diberikan dalam analisis struktural. Hasil Total deformasi maximum yaitu 1163,9 mm dengan kondisi specimen patah.


![image 11](<Hasil Simulasi ansys perhitungan new_images/imageFile11.png>)

![image 12](<Hasil Simulasi ansys perhitungan new_images/imageFile12.png>)

- b. Starain Equivalent Elastic Strain adalah ukuran regangan total yang terjadi dalam material akibat beban yang diberikan, tanpa mempertimbangkan deformasi plastis. Hasil Equivalent Elastic Strain maximum yaitu 0,0051939 mm/mm atau 0,51939%.


![image 13](<Hasil Simulasi ansys perhitungan new_images/imageFile13.png>)

![image 14](<Hasil Simulasi ansys perhitungan new_images/imageFile14.png>)

- c. Stress Equivalent Stress adalah tegangan ekuivalen yang digunakan dalam analisis kegagalan material berdasarkan teori distorsi energi. Hasil Equivalent Stress yaitu minimum 0,19621 MPa dan maximum 292,5 MPa.
- d. Energi Probe Energi Probe adalah metode analisis energi dalam simulasi elemen hingga yang digunakan untuk mengevaluasi distribusi dan perubahan energi pada suatu sistem selama proses deformasi atau interaksi gaya. Hasil Energi internal (Energi Serap)


![image 15](<Hasil Simulasi ansys perhitungan new_images/imageFile15.png>)

![image 16](<Hasil Simulasi ansys perhitungan new_images/imageFile16.png>)

# yaitu 29935 milijoule atau 29,935 Joule dan energi kinetic yaitu 30538 milijoulr atau 30,538 joule.

![image 17](<Hasil Simulasi ansys perhitungan new_images/imageFile17.png>)

![image 18](<Hasil Simulasi ansys perhitungan new_images/imageFile18.png>)

- 8. Parameter
- 9. Analisis Hasil Hasil perhitungan teoritis menunjukkan bahwa energi yang diserap dengan sudut pengukur 95° dan kecepatan tumbukan 3,2236 m/s adalah 30,13497 Joule. Sementara itu, hasil simulasi menunjukkan 29,935 Joule dengan selisih hanya sekitar 0,66%. Perbedaan yang kecil ini menunjukkan bahwa hasil simulasi sangat mendekati perhitungan manual.


![image 19](<Hasil Simulasi ansys perhitungan new_images/imageFile19.png>)

