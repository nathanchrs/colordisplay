# Color Display

Program kendali DSP16128 Dot Matrix Display yang dijalankan dari Raspberry Pi.

## Hardware

1. DSP16128 Dot Matrix Display + kabel power
2. Kabel serial dengan adapter USB-to-serial atau koneksi langsung ke Raspberry Pi melalui pin GPIO
3. Raspberry Pi + MicroSD card kosong (minimal 4 GB) + kabel power
4. Kabel Ethernet untuk koneksi Raspberry Pi ke jaringan

DSP 16128 Dot Matrix Display adalah display LED dengan ukuran 21x2 karakter. Display ini menggunakan protokol Modbus RTU untuk kendali. Display ini dihubungkan dengan koneksi serial ke Raspberry Pi menggunakan koneksi langsung ke pin GPIO di Raspberry Pi atau adapter USB-to-serial. Program ini mengasumsikan koneksi serial dengan konfigurasi *default* sebagai berikut:

- Port serial: `/dev/ttyUSB0` (menggunakan adapter USB-to-serial)
- *Modbus address*: 1 (DIP switch 1 on, 2-7 off)
- *Baud rate*: 9600 bps (DIP switch 8 off)

Jika diperlukan, konfigurasi koneksi serial tersebut dapat diubah (lihat bagian Pengaturan).

Raspberry Pi dapat dihubungkan ke jaringan menggunakan kabel Ethernet. OS pada Raspberry Pi akan mencoba mendapatkan alamat IP secara otomatis melalui DHCP. Pengaturan jaringan akan dibahas lebih lanjut pada bagian 'Pengaturan jaringan' di bawah. *Hostname* Raspberry Pi pada jaringan bernama `leddisplay.local`.

## Software

Berikut adalah langkah-langkah untuk memasang program ini pada Raspberry Pi:

### Menyiapkan OS

1. Unduh *image* OS [Raspbian Jessie Lite](https://downloads.raspberrypi.org/raspbian_lite_latest) (disarankan versi 2017-07-05). Versi ini merupakan versi tanpa GUI dari OS Raspbian. OS Raspbian sendiri adalah sebuah distribusi OS Debian Linux yang telah disesuaikan untuk Raspberry Pi.
2. Salin isi dari file *image* tersebut ke MicroSD card yang akan digunakan untuk Raspberry Pi dengan menggunakan program [Etcher](https://etcher.io/) atau sejenisnya.
3. Buat sebuah file kosong bernama `ssh` (tanpa *extension*) pada partisi `boot` di MicroSD card tersebut.
4. Masukkan MicroSD card tersebut ke Raspberry Pi, kemudian nyalakan dan sambungkan ke jaringan.

Raspberry Pi tersebut akan mencari alamat IP secara otomatis dengan DHCP. Pada titik ini, Raspberry Pi tersebut memiliki pengaturan sebagai berikut:

- *Hostname*: `raspberrypi.local`
- User: `pi`
- Password: `raspberry`

5. Akses terminal pada Raspberry Pi.

Terminal *command-line* Linux pada Raspberry Pi dapat diakses dengan cara memasang monitor (HDMI) dan keyboard (USB) pada Raspberry Pi, lalu login dengan user dan password diatas, atau menggunakan SSH dari komputer lain.

Untuk mengakses *terminal* dengan SSH, dibutuhkan program SSH client. Pada Windows, umumnya dapat menggunakan program [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html). Masukkan *hostname*, user dan password diatas. Jika muncul dialog 'Security Alert', klik 'Yes'. Jika koneksi gagal, coba kembali dengan memasukkan alamat IP Raspberry Pi pada bagian *hostname*.

Beberapa *command* yang umum dipakai pada terminal Linux antara lain:
- `ls`: melihat file/direktori apa saja yang ada di direktori ini (mirip `dir` pada *command-line* Windows)
- `cd <nama_direktori>`: pindah ke direktori tersebut. Untuk kembali ke direktori sebelumnya, masukkan nama direktori `..` (dua titik).
- `pwd`: melihat alamat direktori ini
- `nano` atau `nano <namafile>`: membuka *text editor* sederhana bernama `nano`. Gunakan tombol panah untuk memindahkan kursor, `Ctrl+o` untuk menyimpan file dan `Ctrl+x` untuk keluar.

Beberapa *command* yang bersifat memodifikasi sistem (mengedit file settings, dll.) harus dijalankan sebagai superuser (administrator) dengan cara menambahkan `sudo ` di depan *command* yang ingin dijalankan. Contohnya, untuk mengedit file `/etc/network/interfaces` sebagai superuser, *command* yang harus dijalankan adalah `sudo nano /etc/network/interfaces`.

6. Jalankan *command* `sudo raspi-config` untuk menjalankan program raspi-config. Gunakan tombol panah atas/bawah untuk memilih menu, tab untuk memilih tombol lain, dan spasi untuk mencentang *checkbox* jika diperlukan. Menggunakan program tersebut, jalankan hal-hal berikut:

- (Opsional) Update tool
- Advanced - expand filesystem
- Change hostname (mengubah *hostname*, contohnya menjadi `leddisplay`)
- Change password (mengubah password, contohnya menjadi `passwordpi`. Sangat disarankan untuk meningkatkan keamanan)
- Change timezone (umumnya menjadi Asia/Jakarta)
- Enable serial - login shell over serial: NO, serial hardware interface: YES

7. Keluar dari program raspi-config, lalu *restart* Raspberry Pi dengan *command* `sudo reboot`.

Pada titik ini, Raspberry Pi tersebut memiliki pengaturan sebagai berikut:

- *Hostname*: *hostname* yang sudah diset sebelumnya, misalnya `leddisplay.local`
- User: `pi`
- Password: password yang sudah diset sebelumnya, misalnya `passwordpi`

### Memasang *file server* Samba untuk *file sharing*

8. Akses kembali terminal Raspberry Pi dengan monitor atau SSH.
9. Pastikan Raspberry Pi terkoneksi ke Internet sehingga dapat mengunduh program tambahan dan *library* yang diperlukan.
10. Jalankan `sudo apt update` untuk memperbaharui daftar program yang dapat diinstall.
11. Install *file server* Samba dengan *command* `sudo apt install samba`. Jika ditanya apakah ingin mengunduh file-file yang diperlukan, tekan `y` kemudian Enter.
12. Buat direktori tempat share dengan *command* `mkdir -m 1777 /home/pi/colordisplay`.
13. Edit file *settings* Samba dengan *command* `sudo nano /etc/samba/smb.conf`. Tambahkan bagian berikut ini di akhir file:

```
[colordisplay]
comment = Color display control
path = /home/pi/colordisplay
browseable = yes
writeable = yes
only guest = no
create mask = 0777
directory mask = 0777
public = yes
guest ok = yes
```

Simpan (Ctrl+o, kemudian tekan Enter) lalu keluar (Ctrl+x).

14. Jalankan perintah `sudo smbpasswd -a pi`, lalu masukkan password baru untuk file share (disarankan password yang sama dengan password Raspberry Pi yang sudah diatur diatas, contohnya `passwordpi`).
15. Restart proses Samba dengan *command* `sudo /etc/init.d/samba restart`

Folder `colordisplay` pada Raspberry Pi sekarang dapat diakses dari Windows Explorer, di bagian Network/Workgroup atau dengan memasukkan *hostname* atau alamat IP Raspberry Pi ke *address bar*.

### Memasang program dan *library* pendukung

16. Akses kembali terminal Raspberry Pi dengan monitor atau SSH, jika belum terhubung.
17. Jalankan *commnad* `sudo apt install python python-dev python-pip supervisor` untuk memastikan Python dan komponen lainnya yang diperlukan sudah terinstall.
18. Jalankan *command* `sudo pip install pyserial modbus-tk` untuk menginstall *library* pendukung.
19. Tempatkan file-file kode program dalam direktori `colordisplay` yang sudah di-*share* diatas.
20. Jalankan *command* `sudo cp /home/pi/colordisplay.conf /etc/supervisor/conf.d/` untuk menyalin file konfigurasi *service*.
21. Pastikan Raspberry Pi sudah terhubung dengan Dot Matrix Display.
22. Jalankan *command* `sudo supervisorctl reread`, lalu `sudo supervisorctl reload` untuk menjalankan program sebagai *service*.

Display akan menampilkan halaman-halaman secara berurutan selama selang waktu tertentu.

### Pengaturan *display*

Untuk mengatur teks dan warna pada halaman-halaman display, edit file `display.txt` pada folder `config` di *file share* `colordisplay`. Setiap halaman direpresentasikan oleh 4 baris teks dalam format berikut:

```
Teks baris 1 hal 1
Warna baris 1 hal 1
Teks baris 2 hal 1
Warna baris 2 hal 1

Teks baris 1 hal 2
Warna baris 1 hal 2
Teks baris 2 hal 2
Warna baris 2 hal 2

...
```

Teks per baris maksimum sepanjang 21 karakter. Warna untuk setiap baris direpresentasikan oleh teks yang terdiri dari karakter-karakter huruf kecil `r`, `g`, `b`, `c`, `y`, `m`, dan `w`, yang masing-masing melambangkan warna merah, hijau, biru, biru muda, kuning, ungu, dan putih secara berurutan untuk posisi karakter tersebut. Karakter warna tersebut juga dapat ditulis dalam huruf besar untuk menghasilkan efek *blink*. Karakter spasi atau lainnya akan mengakibatkan teks pada posisi tersebut tidak ditampilkan (hitam).

Contoh file `display.txt`:

```
Teks baris 1 hal 1
rrrrrrrrrrrr ggg b
Teks baris 2 hal 1
cccc mmmmm y yyy w

Teks baris 1 hal 2
wwwwwwwwwwwwwwwwww
Teks baris 2 hal 2
RRRR wwwww w
```

Contoh diatas akan menghasilkan:

```
Halaman 1:
Teks baris 1 hal 1 (warna merah, hijau, biru)
Teks baris 2 hal 1 (warna biru muda, ungu, kuning, putih)

Halaman 2:
Teks baris 1 hal 2 (warna putih)
Teks baris 2 (warna merah berkedip, putih, 'hal 2' tidak tampak)
```

Untuk mengatur *display interval* atau selang waktu antar pergantian halaman, edit file `display_interval.txt` pada folder `config` di *file share* `colordisplay`. File ini berisi sebuah angka dalam satuan detik.

Perubahan akan langsung diaplikasikan oleh program.

### Pengaturan variabel program

Terdapat beberapa variabel program yang bisa diatur dalam file `variables.py` pada *file share* `colordisplay`:

- `DISPLAY_FILE_PATH`: file pengaturan display, *default*: `config/display.txt`
- `DISPLAY_INTERVAL_FILE_PATH`: file pengaturan display interval, *default*: `config/display_interval.txt`
- `FILE_CHECK_INTERVAL`: selang waktu antar pengecekan file pengaturan (dalam detik), *default*: `3`
- `DEVICE`: nama koneksi serial yang digunakan, *default*: `/dev/ttyUSB0` (menggunakan USB-to-serial adapter)
- `DEVICE_ADDRESS`: alamat Modbus dari display, *default*: `1`
- `DEVICE_BAUD_RATE`: *baud rate* dari koneksi serial, *default*: `9600`

Setelah mengubah variabel program atau bagian program lainnya, *restart* Raspberry Pi untuk mengaplikasikan perubahan.

### Pengaturan jaringan

Pengaturan jaringan pada Raspberry Pi dapat dilakukan dengan mengakses terminal Raspberry Pi melalui monitor atau SSH, dan mengedit file `/etc/network/interfaces` sebagai superuser dengan *command* `sudo nano /etc/network/interfaces`.

Pengaturan jaringan yang direkomendasikan adalah untuk menggunakan DHCP terlebih dahulu untuk mencoba mendapatkan alamat IP, tetapi menggunakan alamat IP *static* jika gagal: ganti baris `iface eth0 inet manual` dalam file `/etc/network/interfaces` menjadi baris-baris berikut:

```
iface eth0 inet dhcp

auto eth0:1
iface eth0:1 inet static
address <alamat_ip_static_yang_diinginkan, contohnya 192.168.1.10>
netmask <netmask_ip_static_yang_diinginkan, contohnya 255.255.255.0>
```

Simpan, kemudian *restart* Raspberry Pi dengan *command* `sudo reboot`.


## Referensi

- [Setup Raspberry Pi - Raspbian Lite melalui SSH](https://hackernoon.com/raspberry-pi-headless-install-462ccabd75d0)
- [Cara menggunakan PuTTY untuk koneksi SSH pada Windows](https://www.ssh.com/ssh/putty/windows/)
- [Dasar-dasar penggunaan *command-line* Linux](https://www.linux.com/learn/how-use-linux-command-line-basics-cli)
- [Memasang Samba pada Raspberry Pi](https://www.raspberrypi.org/magpi/samba-file-server/)
- [*Library* PySerial](https://pythonhosted.org/pyserial/)
- [*Library* modbus-tk](https://github.com/ljean/modbus-tk)
- [Referensi Supervisor untuk menjalankan program sebagai *service*](http://supervisord.org/introduction.html)
