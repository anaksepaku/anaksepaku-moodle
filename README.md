# anaksepaku-moodle

Moodle self-host siap pakai untuk materi belajar bahasa Jepang "Bulan Pertama".
Dirancang supaya **mudah direplikasi**: satu folder, satu `.env`, satu course `.mbz`, dan installer one-liner.

## Status

- Image: `oksigenia/moodle:5.3` (LTS, code Moodle asli, auto-install & auto-upgrade lewat env)
- DB: `mariadb:11.4`
- Bind: `127.0.0.1` + opsional IP Tailscale — **tidak diekspos ke LAN**
- Domain contoh: `elearning.example.com` (ganti sesuai kebutuhan Anda)

## Instalasi cepat

```bash
curl -fsSL https://raw.githubusercontent.com/anaksepaku/anaksepaku-moodle/main/install-moodle.sh | sudo bash
```

Variabel yang bisa diset sebelum paste:

```bash
export MOODLE_DIR=/srv/moodle-elearning          # default
export WG_BIND_IP=127.0.0.1                      # default
export WG_PORT=8090                              # default
export TAILSCALE_IP=192.0.2.10                   # contoh RFC5737, opsional
export MOODLE_WWWROOT=https://elearning.example.com
```

Installer akan:
1. mengunduh repo ke folder sementara,
2. menyalin file ke `$MOODLE_DIR`,
3. membuat `.env` + `CREDENTIALS.txt` dengan password acak (mode `0600`),
4. menjalankan `docker compose up -d`,
5. menunggu Moodle selesai install,
6. mengaktifkan timer cron,
7. mengimpor `course/*.mbz` kalau tersedia.

## URL & kredensial

- Web: `$MOODLE_WWWROOT`
- User/password admin: lihat `$MOODLE_DIR/CREDENTIALS.txt`
- **Jangan pernah commit `.env` atau `CREDENTIALS.txt`**

## Cloudflare Tunnel (manual)

Tambahkan di Zero Trust → Tunnels → Public Hostname:

```
Hostname : elearning.example.com
Service  : HTTP
URL      : 127.0.0.1:8090
```

Ingat: `127.0.0.1` diartikan **di mesin connector**, bukan di browser.
Kalau connector tidak satu host dengan Moodle, pakai IP Tailscale host tersebut.

## Pindah server

Ada tiga level:

1. **Course saja** — salin `course/bahasa-jepang.mbz` ke Moodle mana pun (termasuk Moodle UT).
2. **Site + data** — salin folder `$MOODLE_DIR`, lalu ubah `.env` (`MOODLE_WWWROOT`, `WG_BIND_IP`, `TAILSCALE_IP`).
3. **Host baru dari nol** — jalankan installer di server baru, lalu impor `.mbz`.

Untuk pindah data yang aman, pakai dump DB — jangan copy file MariaDB mentah:

```bash
cd "$MOODLE_DIR"
./scripts/backup.sh
# pindahkan file di backups/ ke host baru, lalu:
./scripts/restore.sh backups/moodle-YYYYMMDD.sql.gz
```

## Backup

```bash
./scripts/backup.sh
```

Isi backup: dump MariaDB + daftar file `moodledata/`. Cache `moodledata/cache/` dan `moodledata/localcache/` sengaja dilewati.

Simpan hasil backup di luar host kalau bisa (rsync ke server lain / storage lain).

## Update

```bash
cd "$MOODLE_DIR"
git pull origin main      # atau unduh rilis terbaru
docker compose pull
docker compose up -d
```

Image `oksigenia/moodle` melakukan backup DB + code otomatis sebelum naik versi.

## Uninstall

```bash
sudo ./uninstall.sh
```

Secara default folder dibuat `.bak` dulu, tidak langsung dihapus.

## FAQ

**`Permission denied` saat menjalankan script**
```bash
chmod +x install-moodle.sh uninstall.sh scripts/*.sh
```

**`env file .env not found`**
Anda berada di folder yang salah. Masuk ke `$MOODLE_DIR` (default `/srv/moodle-elearning`), atau pakai `docker compose -f /srv/moodle-elearning/docker-compose.yml ...`.

**Butuh token REST untuk otomasi**

```bash
./scripts/create_ws_token.sh
```

Token tersimpan di `.ws_token` (mode `0600`) dan **tidak boleh di-commit**.

**Course ada tapi tidak muncul di Dashboard**

Moodle dashboard hanya menampilkan course tempat user ter-enrol. Admin tidak otomatis ter-enrol.
Enrol lewat PHP CLI (bootstrap Moodle + `enrol_get_plugin('manual')->enrol_user(...)`), atau lewat
*Site administration → Courses → Enrolments*. Untuk akun komunitas, aktifkan *Self enrolment*
pada course tersebut.

**Akses Tailscale hilang setelah `docker-compose.yml` ditimpa**
Installer menyisipkan baris tailscale pada marker `# TAILSCALE_PORT`. Kalau compose diganti manual,
jalankan ulang installer dengan `TAILSCALE_IP=192.0.2.10`, atau tambahkan lagi baris:

```yaml
- "192.0.2.10:8090:8080"   # ganti dengan IP tailscale0 host
```

**Moodle tidak bisa login setelah pindah host**
Cek `MOODLE_WWWROOT` di `.env`. Harus sama persis dengan URL yang dibuka browser, termasuk `https://`.

**Forum/badge tidak jalan**
Cek timer cron: `systemctl list-timers | grep moodle`.

## Keamanan

- IP privat tidak ditulis di repo — pakai placeholder RFC5737 di contoh.
- Password dibuat acak oleh installer, tidak pernah dikirim ke chat.
- Port 3306 tidak dibuka ke host/internet.
- Self-registration disarankan mati; akun komunitas dibuat manual.

Lisensi: materi bebas dipakai dengan atribusi ke OnnoWiki/SpeedyWiki.
