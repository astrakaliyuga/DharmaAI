#!/bin/bash
# DharmaAI Automatic Backup Script

# Configuration
BACKUP_BASE="/mnt/kaliyuga/backups/DharmaAI"
SOURCE_DIR="/mnt/kaliyuga/DharmaAI"
BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_BASE}/DharmaAI_${BACKUP_DATE}.tar.gz"
LOG_FILE="${BACKUP_BASE}/backup.log"
RETENTION_DAYS=7

# Create backup folder if not exists
mkdir -p "${BACKUP_BASE}"

# Log start
echo "========================================" >> "${LOG_FILE}"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Backup started" >> "${LOG_FILE}"

# Create backup with exclusions
tar -czf "${BACKUP_FILE}" \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='logs' \
    --exclude='models' \
    --exclude='workspace' \
    --exclude='data' \
    --exclude='memory/chroma_db' \
    --exclude='*.tar.gz' \
    --exclude='*.onnx' \
    --exclude='*.pt' \
    --exclude='*.bin' \
    --exclude='*.safetensors' \
    --exclude='*.mp4' \
    --exclude='*.png' \
    --exclude='*.wav' \
    --exclude='*.jpg' \
    --exclude='*.jpeg' \
    -C "$(dirname ${SOURCE_DIR})" "$(basename ${SOURCE_DIR})" 2>> "${LOG_FILE}"

# Check if backup successful
if [ $? -eq 0 ]; then
    SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Backup successful: ${BACKUP_FILE} (${SIZE})" >> "${LOG_FILE}"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ Backup failed!" >> "${LOG_FILE}"
    exit 1
fi

# Delete old backups (older than RETENTION_DAYS)
find "${BACKUP_BASE}" -name "DharmaAI_*.tar.gz" -mtime +${RETENTION_DAYS} -delete
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Cleaned up backups older than ${RETENTION_DAYS} days" >> "${LOG_FILE}"

# Show total backups
TOTAL=$(ls -1 "${BACKUP_BASE}"/DharmaAI_*.tar.gz 2>/dev/null | wc -l)
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Total backups: ${TOTAL}" >> "${LOG_FILE}"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Backup finished" >> "${LOG_FILE}"
