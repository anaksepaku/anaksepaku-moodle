#!/bin/bash
# Hentikan container, nonaktifkan timer, dan backup folder sebelum hapus.
set -euo pipefail
DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$DIR"

echo "[uninstall] Menjalankan backup terakhir"
./scripts/backup.sh || true

echo "[uninstall] Menhentikan container"
docker compose down || true

echo "[uninstall] Menonaktifkan timer"
systemctl disable --now anaksepaku-moodle-cron.timer >/dev/null 2>&1 || true
rm -f /etc/systemd/system/anaksepaku-moodle-cron.service /etc/systemd/system/anaksepaku-moodle-cron.timer
systemctl daemon-reload >/dev/null 2>&1 || true

echo "[uninstall] Memindahkan folder ke $DIR.bak"
cd /
mv "$DIR" "$DIR.bak"

echo "Selesai. Data ada di $DIR.bak — hapus manual kalau sudah tidak diperlukan."
