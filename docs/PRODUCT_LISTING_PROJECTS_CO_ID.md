# Draf listing internal — Chocobot Guardian

> Belum siap dipublikasikan sebagai listing berbayar. Gunakan hanya setelah gerbang rilis pada `docs/RELEASE_CHECKLIST.md` selesai.

## Judul sementara
Chocobot Guardian — Paket Utilitas Windows Lokal

## Deskripsi
Chocobot Guardian adalah aplikasi desktop Windows dengan beberapa utilitas lokal untuk memeriksa struktur tautan, menghitung hash file, melihat metadata file, meringkas isi folder, serta menjalankan diagnostik DNS/ping/TCP dasar. Fokus MVP adalah pemeriksaan yang dapat dijelaskan, berjalan di perangkat sendiri, tanpa unggah dokumen atau file.

## Fitur MVP yang bisa dijelaskan
- Inspektur URL tanpa membuka tautan.
- Pemeriksaan struktur host, skema, path, port, dan indikator heuristik.
- Metadata file dan SHA-256.
- Ringkasan folder dengan batas penelusuran dan daftar file terbesar.
- Pemeriksaan ekstensi/signature sederhana pada file.
- Resolusi DNS sistem, satu ping, dan satu tes koneksi TCP dengan timeout.
- Log dan konfigurasi lokal dalam direktori data pengguna.

## Batasan yang wajib dicantumkan
- Bukan antivirus dan tidak menyediakan proteksi real-time atau jaminan file aman.
- Tidak melakukan pemindaian reputasi URL online.
- Tidak mengarantina atau menghapus file otomatis.
- Sebagian modul UI, konversi dokumen, dan kontrol keamanan lanjutan belum berfungsi sebagai fitur rilis.
- Hasil heuristik dapat salah; pengguna perlu memeriksa temuan sendiri.
- Hanya didukung pada Windows yang telah diuji secara manual; kompatibilitas Windows lama belum diverifikasi.

## Isi paket rilis yang direncanakan
- Installer atau paket portable Windows.
- Panduan pengguna berbahasa Indonesia.
- Checksum SHA-256.
- Catatan versi dan batasan.
- Lisensi penggunaan dan kontak dukungan.

## Gerbang publish
Uji clean install, launch, user-data location, fungsi alat, timeout, error handling, uninstall, dan pemulihan konfigurasi sebelum harga serta kompatibilitas dipublikasikan.
