#!/bin/bash
set -e

# Load variables from .env (or .env.example if .env does not exist)
if [ -f .env ]; then
    source .env
else
    source .env.example
fi

# Install Python packages
sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib python3-venv python3-pip

# Start PostgreSQL
sudo systemctl start postgresql

# Create the target database and restricted user
sudo -u postgres psql -c "CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';"
sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};"

# Apply Security Hardening (Limits & Network bindings)
sudo -u postgres psql -c "ALTER ROLE ${DB_USER} WITH NOSUPERUSER NOCREATEDB NOCREATEROLE CONNECTION LIMIT 50;"
sudo -u postgres psql -c "ALTER SYSTEM SET listen_addresses = '127.0.0.1, ${ALLOWED_IPS}';"
sudo systemctl restart postgresql

# Setup Python Environment
python3 -m venv venv
source venv/bin/activate
pip install SQLAlchemy psycopg2-binary python-dotenv

# Initialize first migration creating a structure for the target table
python3 models.py

# Clean up temporary Python environment and packages
deactivate
rm -rf venv
sudo apt-get remove --purge -y python3-venv python3-pip
sudo apt-get autoremove -y