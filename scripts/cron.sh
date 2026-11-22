#!/bin/bash
# Dipanggil systemd timer tiap menit. Bisa juga dipanggil manual.
set -euo pipefail
DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$DIR"
docker compose exec -T moodle php admin/cli/cron.php
