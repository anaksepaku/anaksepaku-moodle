#!/bin/bash
# anaksepaku-moodle — installer one-liner.
# curl -fsSL https://raw.githubusercontent.com/anaksepaku/anaksepaku-moodle/main/install-moodle.sh | sudo bash
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  exec sudo bash "$0" "$@"
fi

REPO="${REPO:-anaksepaku/anaksepaku-moodle}"
DIR="${MOODLE_DIR:-/srv/moodle-elearning}"
WG_BIND_IP="${WG_BIND_IP:-127.0.0.1}"
WG_PORT="${WG_PORT:-8090}"
TAILSCALE_IP="${TAILSCALE_IP:-}"
WWWROOT="${MOODLE_WWWROOT:-https://elearning.anaksepaku.my.id}"
ADMIN_EMAIL="${ADMIN_EMAIL:-admin@example.invalid}"

log() { echo "[anaksepaku-moodle] $*"; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

log "Mengunduh repo $REPO"
curl -fsSL "https://github.com/$REPO/archive/refs/heads/main.tar.gz" -o "$TMP/repo.tgz"
tar xzf "$TMP/repo.tgz" -C "$TMP"
SRC="$TMP/anaksepaku-moodle-main"

mkdir -p "$DIR"
cp -a "$SRC/." "$DIR/"
cd "$DIR"

if [ ! -f .env ]; then
  log "Membuat .env dan kredensial acak"
  DB_PASS="$(openssl rand -base64 24 | tr -d '/+=')"
  DB_ROOT_PASS="$(openssl rand -base64 24 | tr -d '/+=')"
  ADMIN_PASS="$(openssl rand -base64 18 | tr -d '/+=' | cut -c1-16)"

  cp .env.example .env
  sed -i "s|^MOODLE_DIR=.*|MOODLE_DIR=$DIR|" .env
  sed -i "s|^MOODLE_WWWROOT=.*|MOODLE_WWWROOT=$WWWROOT|" .env
  sed -i "s|^WG_BIND_IP=.*|WG_BIND_IP=$WG_BIND_IP|" .env
  sed -i "s|^WG_PORT=.*|WG_PORT=$WG_PORT|" .env
  sed -i "s|^TAILSCALE_IP=.*|TAILSCALE_IP=$TAILSCALE_IP|" .env
  sed -i "s|^DB_PASS=.*|DB_PASS=$DB_PASS|" .env
  sed -i "s|^DB_ROOT_PASS=.*|DB_ROOT_PASS=$DB_ROOT_PASS|" .env
  sed -i "s|^ADMIN_EMAIL=.*|ADMIN_EMAIL=$ADMIN_EMAIL|" .env
  sed -i "s|^ADMIN_PASS=.*|ADMIN_PASS=$ADMIN_PASS|" .env

  cat > CREDENTIALS.txt <<EOF
URL      : $WWWROOT
User     : admin
Password : $ADMIN_PASS
DB user  : moodleuser
DB pass  : $DB_PASS
DB root  : $DB_ROOT_PASS
EOF
  chmod 600 .env CREDENTIALS.txt
else
  log ".env sudah ada — tidak ditimpa"
fi

if [ -n "$TAILSCALE_IP" ]; then
  sed -i "s|# TAILSCALE_PORT|- \"$TAILSCALE_IP:$WG_PORT:8080\"   # tailscale|" docker-compose.yml
else
  sed -i '/# TAILSCALE_PORT/d' docker-compose.yml
fi

mkdir -p db moodledata backups course
chown -R 33:33 moodledata 2>/dev/null || true
chmod +x uninstall.sh scripts/*.sh 2>/dev/null || true

log "Menulis timer cron"
cat > /etc/systemd/system/anaksepaku-moodle-cron.service <<EOF
[Unit]
Description=Onno Moodle cron
After=docker.service

[Service]
Type=oneshot
WorkingDirectory=$DIR
ExecStart=/usr/bin/docker compose -f $DIR/docker-compose.yml exec -T moodle php admin/cli/cron.php
EOF

cat > /etc/systemd/system/anaksepaku-moodle-cron.timer <<'EOF'
[Unit]
Description=Run Onno Moodle cron every minute

[Timer]
OnBootSec=2min
OnUnitActiveSec=1min
AccuracySec=10s
Persistent=true

[Install]
WantedBy=timers.target
EOF

systemctl daemon-reload
systemctl enable --now anaksepaku-moodle-cron.timer >/dev/null 2>&1 || true

log "Menjalankan container"
docker compose up -d

log "Menunggu Moodle siap (maks 5 menit)"
for i in $(seq 1 60); do
  if curl -fsS -o /dev/null "http://$WG_BIND_IP:$WG_PORT/" 2>/dev/null; then
    break
  fi
  sleep 5
done

MBZ=$(find course -maxdepth 1 -name '*.mbz' -print -quit 2>/dev/null || true)
if [ -n "$MBZ" ]; then
  log "Mengimpor course $MBZ (manual via UI bila CLI tidak tersedia)"
  cp "$MBZ" moodledata/repository/ 2>/dev/null || true
fi

cat <<EOF

SELESAI
Buka       : $WWWROOT
Kredensial : $DIR/CREDENTIALS.txt (0600)
Folder     : $DIR
Cron       : systemctl list-timers | grep anaksepaku-moodle

Langkah manual tersisa:
1. Buat DNS + Public Hostname Cloudflare ke http://127.0.0.1:$WG_PORT
2. Impor course/*.mbz lewat Site administration → Courses → Restore
3. Ganti password admin setelah login pertama
EOF
