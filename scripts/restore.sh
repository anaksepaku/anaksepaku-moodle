#!/bin/bash
# Pulihkan dump DB. Package moodledata dibalik manual kalau perlu.
# Usage: ./scripts/restore.sh backups/moodle-YYYYMMDD-HHMMSS.sql.gz
set -euo pipefail
DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$DIR"
set -a; . ./.env; set +a

DUMP="${1:-}"
if [ -z "$DUMP" ] || [ ! -f "$DUMP" ]; then
  echo "Usage: $0 backups/moodle-YYYYMMDD-HHMMSS.sql.gz" >&2
  exit 1
fi

echo "[restore] Mengembalikan $DUMP ke database $DB_NAME"
gunzip -c "$DUMP" | docker compose exec -T db mariadb -uroot -p"$DB_ROOT_PASS" "$DB_NAME"
echo "[restore] Selesai. Jalankan: docker compose restart moodle"
