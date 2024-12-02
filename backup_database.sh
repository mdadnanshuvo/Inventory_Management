#!/bin/bash

# Define backup filename with timestamp
BACKUP_FILE="mydatabase_backup_$(date +%Y%m%d%H%M%S).sql"

# Perform the database backup
echo "Backing up the database..."
docker exec postgres_postgis1 pg_dump -U myuser mydatabase > $BACKUP_FILE

echo "Database backup completed: $BACKUP_FILE"
