#!/bin/bash

# Load environment variables from .env file
source /app/.env

# Wait for the database to be available
echo "Waiting for DB to be ready..."
until mariadb -h db -u${MARIADB_USER} -p${MARIADB_PASSWORD} -e 'SELECT 1' > /dev/null 2>&1; do
    sleep 1
    echo "Waiting for MariaDB to become available..."
done
echo "MariaDB is up - initializing database if needed..."

# Initialize the database
if mariadb -h db -u${MARIADB_USER} -p${MARIADB_PASSWORD} ${MARIADB_DATABASE} < /docker-entrypoint-initdb.d/init-db.sql; then
    echo "Database initialized and sample tasks inserted successfully."
else
    echo "Failed to initialize the database."
    exit 1
fi

echo "Starting the application..."
exec "$@"
