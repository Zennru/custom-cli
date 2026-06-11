# Proyek Custom CLI Shell - Kelompok 7

Repositori ini dibuat untuk memenuhi tugas kelompok pada mata kuliah Sistem Operasi. Proyek ini berfokus pada implementasi sebuah *Command Line Interface* (CLI) atau *custom shell* sederhana menggunakan bahasa pemrograman Python.

## Deskripsi Tugas
Tujuan utama dari proyek ini adalah membangun aplikasi shell kustom yang berjalan dalam mekanisme REPL (*Read-Evaluate-Print Loop*) serta mampu menangani manajemen proses, perintah internal (*built-in*), eksekusi program eksternal, hingga manipulasi I/O tingkat rendah pada sistem operasi.

Proyek ini dibagi menjadi 6 tahap pengembangan utama:

### Tahap 1: Membangun REPL (Read-Evaluate-Print Loop)
* Membuat struktur utama program yang berjalan dalam perulangan tanpa henti (*infinite loop*).
* Menampilkan prompt kustom dan membaca input string secara terus-menerus.
* Program hanya akan berhenti jika pengguna mengetik perintah `exit`.

### Tahap 2: Parsing Perintah (Command Tokenization)
* Memecah string input yang dimasukkan pengguna berdasarkan karakter spasi menjadi komponen argumen (perintah utama dan parameter/argumen pendukung).

### Tahap 3: Implementasi Built-in Commands
* Menangani perintah dasar yang dieksekusi langsung oleh shell tanpa membuat proses baru:
  * `cd <direktori>`: Mengubah direktori aktif.
  * `pwd`: Menampilkan jalur direktori aktif saat ini.

### Tahap 4: Implementasi Forking & Eksekusi Perintah Eksternal
* Memanfaatkan mekanisme manajemen proses untuk menjalankan perintah bawaan OS (seperti `ls`, `mkdir`, `clear`, dll.).
* Menggunakan duplikasi proses untuk membuat proses anak (*child process*) yang akan dioverlay dengan program baru, sementara proses induk (*parent process*) menunggu hingga proses anak selesai dieksekusi.

### Tahap 5: Implementasi Fitur Advanced (Piping / Redirection) - Nilai Bonus
* **I/O Redirection (`>` atau `<`)**: Mengarahkan output dari suatu perintah ke dalam file teks atau sebaliknya melalui manipulasi file deskriptor.
* **Piping (`|`)**: Menghubungkan output dari proses pertama agar langsung menjadi input bagi proses kedua melalui jalur komunikasi antar-proses (*Inter-Process Communication*).

### Tahap 6: Pengujian Beban & Penanganan Eror
* Memastikan ketahanan aplikasi agar tidak mengalami *force close* atau *crash* ketika menerima kesalahan input, seperti menekan Enter tanpa karakter, memasukkan perintah tidak dikenal (*Command not found*), atau argumen dengan spasi berlebih.
