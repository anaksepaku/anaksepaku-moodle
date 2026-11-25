#!/bin/bash
# Pasang theme Academi 5.3 pada Moodle 5.3.x di prau.
# JALANKAN BACKUP DULU: cd /srv/moodle-elearning && ./scripts/backup.sh
set -euo pipefail

ZIP=/tmp/theme_academi-v5.3.zip
EXTRACT=/tmp/academi-extract
CTR=moodle-elearning-moodle
WWW=/var/www/moodle/public/theme/academi
URL=https://github.com/lmsace/academi/releases/download/v5.3.0/theme_academi-v5.3.zip

curl -sSL --max-time 120 -o "$ZIP" "$URL"
rm -rf "$EXTRACT" && mkdir -p "$EXTRACT"
python3 - "$ZIP" "$EXTRACT" <<'PY'
import sys, zipfile
zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])
PY

docker exec "$CTR" sh -c "rm -rf $WWW"
docker cp "$EXTRACT/theme_academi-v5.3" "$CTR:$WWW" >/dev/null
docker exec "$CTR" sh -c "chown -R www-data:www-data $WWW"

docker exec "$CTR" php /var/www/moodle/admin/cli/upgrade.php --non-interactive
docker exec "$CTR" php /var/www/moodle/admin/cli/cfg.php --name=theme --set=academi
docker exec "$CTR" php /var/www/moodle/admin/cli/cfg.php --name=forcelogin --set=0
docker exec "$CTR" php /var/www/moodle/admin/cli/cfg.php --name=guestaccess --set=1
docker exec "$CTR" php /var/www/moodle/admin/cli/cfg.php --name=enablemyhome --set=1
docker exec "$CTR" php /var/www/moodle/admin/cli/purge_caches.php

echo "Theme academi aktif. Lanjutkan dengan scripts/configure_academi.php untuk slider."
