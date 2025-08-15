#!/usr/bin/env bash
set -euo pipefail
ENC_FILE="${1:?enc file}"
PASSPHRASE="${2:?passphrase}"
TMP="/tmp/restore_$$.sql"
openssl enc -d -aes-256-cbc -salt -pbkdf2 -pass pass:"${PASSPHRASE}" -in "${ENC_FILE}" -out "${TMP}"
docker compose exec -T db psql -U paa -c "DROP DATABASE IF EXISTS paa_restore_test;"
docker compose exec -T db createdb -U paa paa_restore_test
cat "${TMP}" | docker compose exec -T db psql -U paa paa_restore_test
shred -u "${TMP}"
echo "Restauration test OK -> DB paa_restore_test"
