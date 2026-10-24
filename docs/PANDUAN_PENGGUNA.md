# Panduan Pengguna Chocobot Guardian (MVP)

## Menjalankan aplikasi

Jalankan Chocobot Guardian dari executable Windows atau, untuk lingkungan pengembangan, jalankan `py main.py`. Bahasa dan konfigurasi disimpan secara lokal. Pada Windows, data operasional berada di `%LOCALAPPDATA%\ChocobotGuardian`; jangan menghapus folder ini ketika memperbarui aplikasi jika ingin mempertahankan konfigurasi dan log.

## Inspektur Tautan

1. Buka menu **Inspektur Tautan**.
2. Tempel URL lengkap atau nama domain pada kolom input.
3. Tekan **Analisis**.
4. Periksa skema, host, port, path, dan indikator yang dicantumkan.
5. Baca tiap alasan sebelum mengambil keputusan.

Pemeriksaan tidak membuka URL, tidak memeriksa reputasi online, dan tidak membuktikan tautan aman/berbahaya. HTTPS hanya berarti koneksi menggunakan TLS jika dibuka; bukan jaminan bahwa situsnya tepercaya.

## Utilitas File

1. Buka menu **Utilitas File**.
2. Pilih **Informasi file + SHA-256** untuk melihat metadata dan menghitung hash.
3. Pilih **Ringkasan folder** untuk menghitung jumlah file, ukuran yang terhitung, distribusi ekstensi, serta daftar hingga sepuluh file terbesar.

Analisis folder bersifat read-only, melewati symbolic link, dan membatasi penelusuran hingga 10.000 file secara default. File yang tidak bisa diakses dapat tidak terhitung. SHA-256 membantu membandingkan byte file; hash bukan pemindai malware.

## Pusat Pemeriksaan File

1. Buka menu **Pusat Pemeriksaan File**.
2. Pilih file untuk melihat metadata, SHA-256, dan indikator dasar.
3. Periksa alasan setiap indikator.

Pemeriksaan hanya meninjau beberapa ekstensi dan signature file yang umum. Tidak ada penghapusan, karantina otomatis, pemindaian antivirus, atau pemblokiran proses. File tanpa indikator tetap bisa berbahaya.

## Diagnostik Jaringan

1. Buka menu **Diagnostik Jaringan**.
2. Masukkan hostname atau alamat IP tanpa awalan `https://` atau path.
3. Pilih **DNS / IP lokal**, **Ping 1x**, atau **Tes port TCP**.
4. Untuk tes port, gunakan angka 1–65535.

Ping menjalankan satu permintaan echo. Tes TCP mencoba satu koneksi dengan timeout terbatas. Gunakan pemeriksaan port hanya pada perangkat yang memang berhak Anda periksa. Aplikasi ini tidak melakukan pemindaian massal atau mengubah pengaturan jaringan.

## Privasi dan batasan

- Pemeriksaan file dan URL berlangsung di perangkat dan tidak dikirim ke server.
- Tidak ada jaminan hasil selalu benar; indikator dapat melewatkan masalah atau menandai teks/file yang sebenarnya normal.
- Modul konversi dokumen, pemindaian keamanan menyeluruh, proteksi real-time, dan karantina otomatis belum termasuk dalam MVP ini.
- Buat backup sebelum mencoba fitur pengelolaan data baru atau mengganti versi aplikasi.

## Dukungan

Untuk pertanyaan dan masukan, hubungi The Choco Studios melalui `thechocostudio@gmail.com`. Jangan mengirimkan file pribadi, kredensial, atau data sensitif melalui laporan masalah kecuali benar-benar diperlukan dan kanalnya telah disepakati.
