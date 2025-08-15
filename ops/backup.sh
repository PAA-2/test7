#!/usr/bin/env bash
set -euo pipefail
BACKUP_DIR="${1:-/backups}"
PASSPHRASE="${2:-changeme}"
TS="$(date +%Y%m%d_%H%M%S)"
F="paa_${TS}.sql"
docker compose exec -T db pg_dump -U paa paa > "/tmp/${F}"
mkdir -p "${BACKUP_DIR}"
openssl enc -aes-256-cbc -salt -pbkdf2 -pass pass:"${PASSPHRASE}" -in "/tmp/${F}" -out "${BACKUP_DIR}/${F}.enc"
shred -u "/tmp/${F}"
echo "Backup écrit: ${BACKUP_DIR}/${F}.enc"
