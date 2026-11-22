#!/bin/bash
# Backup Moodle: dump DB + daftar moodledata (tanpa cache).
set -euo pipefail
DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$DIR"
set -a; . ./.env; set +a
STAMP="$(date +%Y%m%d-%H%M%S)"
OUT="$DIR/backups"
mkdir -p "$OUT"

log() { echo "[backup] $*"; }

log "Dump MariaDB"
docker compose exec -T db mariadb-dump -uroot -p"$DB_ROOT_PASS" "$DB_NAME" \
  | gzip > "$OUT/moodle-$STAMP.sql.gz"

log "Salin daftar moodledata (cache dilewati)"
tar czf "$OUT/moodledata-$STAMP.tar.gz" \
  --exclude='cache/*' --exclude='localcache/*' --exclude='temp/*' \
  -C "$DIR" moodledata 2>/dev/null || true

log "Selesai: $OUT/moodle-$STAMP.sql.gz"
