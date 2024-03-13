#!/bin/bash

# Load environment variables from .env file
source /app/.env

echo "Waiting for DB to be ready..."
until mariadb -h db -u${MARIADB_USER} -p${MARIADB_PASSWORD} -e 'SELECT 1' > /dev/null 2>&1; do
    sleep 1
    echo "Waiting for MariaDB to become available..."
done
echo "MariaDB is up - initializing database if needed..."

# Dynamically granting permissions to the database user
mariadb -h db -u root -p${MARIADB_ROOT_PASSWORD} <<-EOSQL
    GRANT ALL ON ${MARIADB_DATABASE}.* TO '${MARIADB_USER}'@'%' IDENTIFIED BY '${MARIADB_PASSWORD}';
    FLUSH PRIVILEGES;
EOSQL

# Executing your database schema initialization and data insertion script
if mariadb -h db -u${MARIADB_USER} -p${MARIADB_PASSWORD} ${MARIADB_DATABASE} < /docker-entrypoint-initdb.d/init-db.sql; then
    echo "Database initialized successfully."
else
    echo "Failed to initialize the database."
    exit 1
fi

echo "Starting the application..."
exec "$@"
