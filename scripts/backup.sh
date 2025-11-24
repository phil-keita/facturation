#!/usr/bin/env bash
set -euo pipefail

# Simple backup helper for the facturation Docker Compose setup.
# - Dumps Postgres DB from the `db` service
# - Archives the `receipts` directory from the `web` service
# - Prunes backups older than $KEEP_DAYS

BACKUP_DIR=${BACKUP_DIR:-/opt/facturation_backups}
KEEP_DAYS=${KEEP_DAYS:-30}

DATE=$(date +%F-%H%M)
mkdir -p "$BACKUP_DIR"

echo "[+] Backing up Postgres to $BACKUP_DIR/facturation-$DATE.sql"
docker compose exec -T db pg_dump -U facturation facturation > "$BACKUP_DIR/facturation-$DATE.sql"

echo "[+] Backing up receipts to $BACKUP_DIR/receipts-$DATE.tar.gz"
# Use the web service to read the receipts volume and stream a tarball to host
docker compose run --rm --no-deps web sh -c "tar czf - -C /app/receipts ." > "$BACKUP_DIR/receipts-$DATE.tar.gz"

echo "[+] Pruning backups older than $KEEP_DAYS days in $BACKUP_DIR"
find "$BACKUP_DIR" -type f -mtime +$KEEP_DAYS -print -delete || true

echo "[+] Backup finished: $DATE"

echo "Tip: make the script executable with: chmod +x scripts/backup.sh"
echo "Run with: sudo BACKUP_DIR=/opt/facturation_backups ./scripts/backup.sh"
