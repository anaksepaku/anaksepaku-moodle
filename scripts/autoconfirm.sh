#!/bin/bash
# Auto-confirm akun self-registration. Email dikirim ke Mailpit (SMTP sink),
# tapi verifikasi tidak perlu dibuka pengguna — langsung dikonfirmasi di DB.
set -euo pipefail
DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$DIR"
set -a; . ./.env; set +a

docker compose exec -T db mariadb -uroot -p"$DB_ROOT_PASS" -e "
UPDATE moodle.mdl_user
SET confirmed = 1, secret = ''
WHERE auth = 'email' AND confirmed = 0 AND deleted = 0;
"
