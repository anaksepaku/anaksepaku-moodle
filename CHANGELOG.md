# anaksepaku-moodle

## [Unreleased]

### Ditambahkan
- Installer one-liner dengan generated `.env` dan password acak.
- Compose stack: `oksigenia/moodle:5.3` + `mariadb:10.11`.
- Bind loopback + opsional Tailscale, tanpa LAN exposure.
- Skrip backup/restore dan systemd timer cron.
- Bank soal GIFT untuk materi "Bulan Pertama".
- Dokumentasi pindah server: course `.mbz`, site folder, host bootstrap.

### Perbaikan
- MariaDB dinaikkan ke 11.4 karena Moodle 5.3 mensyaratkan minimal 11.4.0.

### Course
- `course/bahasa-jepang.mbz`: 5 topik, 16 soal GIFT, forum, dan 28 entri glossary.
- Skrip `scripts/create_ws_token.sh` untuk otomasi REST (token tidak di-commit).

### Tampilan
- `coursedisplay=1` + `hiddensections=0`: course tampil per sesi, bukan satu halaman panjang.
- Seksi General berisi **Daftar Sesi** (tautan Minggu 1–4 + Latihan) untuk navigasi mobile.

### Auto-enrol
- Plugin `local/autoenrol`: enrol otomatis ke course saat first login (role Student).

### Mail final
- From name email jadi `anaksepaku.my.id` (supportuserid + supportname + emailfromvia=0, admin ikut disamakan).
- Autoconfirm timer dinonaktifkan; signup pakai verifikasi email asli via SMTP SG.
- Gmail `250 2.0.0 OK` terverifikasi (PTR/SPF/DKIM/DMARC valid).

### Retirement v1
- Quiz v1 dan kategori soalnya dihapus; kategori lama dinonaktifkan jadi `V1 Legacy (kosong)`.
- Buku v2 & quiz v2 di-rename jadi nama final tanpa embel-embel “v2”.
- Ringkasan seksi disederhanakan jadi penunjuk ke Buku.

### Import v2
- Buku 14 bab diimpor sebagai Book module.
- Quiz tambahan XML v2: 11 soal unik (33 entri termasuk sub-soal cloze).
- `.mbz` diregenerasi.

### Fitur aktif
- Mailpit SMTP sink + `scripts/autoconfirm.sh`: signup jalan tanpa email nyata.
- Self-registration (`registerauth=email`) + self-enrolment role student.
- H5P: 2 activity shell (kana match, susun kalimat).
- Badges: Pemula Kana & Kanji 20, kriteria manual.

### Catatan
- FAQ: course tidak muncul di dashboard karena user belum ter-enrol.
- FAQ: compose yang ditimpa dari repo menghilangkan baris tailscale; cara mengembalikannya.
- Belum menyertakan `.mbz`; akan dibuat setelah Moodle berjalan di prau.
- Contoh IP memakai RFC5737, bukan IP privat asli.
- Contoh hostname memakai `elearning.example.com`, bukan domain produksi.
