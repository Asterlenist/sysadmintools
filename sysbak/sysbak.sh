#!/bin/bash

set -u

if [ "$EUID" -ne 0 ]; then
  echo "Warning: Run with sudo to backup /etc and /var/log completely."
fi

echo "SysBak"

BACKUP_DIR="$HOME/backups/sysbak"
mkdir -p "$BACKUP_DIR"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
ARCHIVE_NAME="sysbak_backup_${TIMESTAMP}.tar.gz"
ARCHIVE_PATH="$BACKUP_DIR/$ARCHIVE_NAME"

sources=(
  "/etc"
  "/var/log"
  "$HOME/.config"
  "$HOME/.bashrc"
  "$HOME/.vimrc"
  "$HOME/.ssh"
  "$HOME/.gitconfig"
  "$HOME/.zshrc"
)

valid_sources=()
for source in "${sources[@]}"; do
  if [ -e "$source" ] || [ -L "$source" ]; then
    valid_sources+=("$source")
  fi
done

if [ "${#valid_sources[@]}" -eq 0 ]; then
  echo "No valid backup sources found."
  exit 1
fi

echo "Creating backup archive: $ARCHIVE_NAME"
if tar -czf "$ARCHIVE_PATH" --ignore-failed-read "${valid_sources[@]}" 2>/dev/null; then
  echo "Backup completed successfully. Archive saved to: $ARCHIVE_PATH"
else
  echo "Backup failed."
  exit 1
fi