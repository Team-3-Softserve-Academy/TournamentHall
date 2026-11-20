#!/bin/bash
set -e

# Load variables from .env (or .env.example if .env does not exist)
if [ -f .env ]; then
    source .env
else
    source .env.example
fi

# Install PostgreSQL packages
sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib

# Start PostgreSQL
sudo systemctl start postgresql

# Create the target database and restricted user
sudo -u postgres psql -c "CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';"
sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};"

# Apply Security Hardening (Limits, Network bindings & pg_hba.conf firewall)
sudo -u postgres psql -c "ALTER ROLE ${DB_USER} WITH NOSUPERUSER NOCREATEDB NOCREATEROLE CONNECTION LIMIT 50;"
sudo -u postgres psql -c "ALTER SYSTEM SET listen_addresses = '127.0.0.1, ${DB_HOST}';"

PG_HBA=$(sudo -u postgres psql -t -P format=unaligned -c 'show hba_file')
for IP in ${ALLOWED_IPS} ${DB_HOST}; do
    echo "host ${DB_NAME} ${DB_USER} ${IP}/32 scram-sha-256" | sudo tee -a "$PG_HBA"
done
sudo systemctl restart postgresql
