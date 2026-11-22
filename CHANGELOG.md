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

### Catatan
- FAQ: compose yang ditimpa dari repo menghilangkan baris tailscale; cara mengembalikannya.
- Belum menyertakan `.mbz`; akan dibuat setelah Moodle berjalan di prau.
- Contoh IP memakai RFC5737, bukan IP privat asli.
- Contoh hostname memakai `elearning.example.com`, bukan domain produksi.
