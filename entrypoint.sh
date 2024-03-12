#!/bin/bash

# Wait for the database to be available
echo "Waiting for DB to be ready..."
while ! mariadb-admin ping -h"mysql-service" --silent; do
    sleep 1
done

# Initialize the database
echo "Initializing the database..."
mariadb -h mysql-service -uadmin -padmin < /docker-entrypoint-initdb.d/init-db.sql

# Start the FastAPI application
exec "$@"
