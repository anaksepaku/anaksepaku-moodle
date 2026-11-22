#!/bin/bash
# Buat token REST untuk admin (userid 2) pada layanan mobile. Token disimpan di .ws_token (0600).
set -euo pipefail
DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$DIR"
set -a; . ./.env; set +a

TOKEN="$(openssl rand -hex 32)"
TS="$(date +%s)"

docker compose exec -T db mariadb -uroot -p"$DB_ROOT_PASS" -e "
INSERT IGNORE INTO moodle.mdl_external_services_functions (externalserviceid, functionname)
  VALUES (1, 'core_course_create_courses');
INSERT INTO moodle.mdl_external_tokens
  (token, tokentype, userid, externalserviceid, contextid, creatorid, timecreated, name)
  VALUES ('$TOKEN', 0, 2, 1, 1, 2, $TS, 'hermes-local');
"

printf '%s' "$TOKEN" > .ws_token
chmod 600 .ws_token
echo "Token tersimpan di $DIR/.ws_token (0600)"
