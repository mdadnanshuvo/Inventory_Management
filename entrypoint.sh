#!/bin/bash

# Function to check if the database is already initialized
check_database() {
  echo "Checking if the database is already initialized..."
  if psql -h db -U your_db_user -d your_db_name -c '\dt' | grep -q 'No relations found'; then
    echo "Database is empty. Proceeding with restoration..."
    return 0
  else
    echo "Database already initialized. Skipping restoration."
    return 1
  fi
}

# Function to restore the database
restore_database() {
  echo "Restoring database from backup..."
  /bin/bash /app/restore_database.sh
  if [ $? -eq 0 ]; then
    echo "Database restoration completed successfully."
  else
    echo "Database restoration failed."
    exit 1
  fi
}

# Wait for the database to be ready
echo "Waiting for the database to be ready..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Database is ready."

# Check and restore the database if needed
check_database && restore_database

# Apply migrations (if needed)
python manage.py migrate

# Collect static files (optional)
python manage.py collectstatic --noinput

# Start the Django application
exec "$@"
