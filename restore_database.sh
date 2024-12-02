#!/bin/bash

# Ensure containers are running
docker-compose up -d

# Wait for the database container to be ready
echo "Waiting for PostgreSQL to be ready..."
sleep 10  # Adjust time as needed based on your environment

# Restore the database
echo "Restoring the database..."
docker exec -i postgres_postgis1 psql -U myuser mydatabase < mydatabase_backup.sql

echo "Database restored successfully!"
