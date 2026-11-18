#!/bin/bash
set -e

# Load variables from .env (or .env.example if .env does not exist)
if [ -f .env ]; then
    source .env
else
    source .env.example
fi

# 1. Install and start PostgreSQL & Python packages
sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib python3-venv python3-pip
sudo systemctl start postgresql

# 2. Create the target database and restricted user
sudo -u postgres psql -c "CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';"
sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};"

# 3. Apply Security Hardening (Limits & Network bindings)
sudo -u postgres psql -c "ALTER ROLE ${DB_USER} WITH NOSUPERUSER NOCREATEDB NOCREATEROLE CONNECTION LIMIT 50;"
sudo -u postgres psql -c "ALTER SYSTEM SET listen_addresses = '127.0.0.1, ${ALLOWED_IPS}';"
sudo systemctl restart postgresql

# 4. Setup Python Environment & Initialize Schema
python3 -m venv venv
source venv/bin/activate
pip install SQLAlchemy psycopg2-binary python-dotenv
python3 models.py

# 5. Clean up temporary Python environment and packages
deactivate
rm -rf venv
sudo apt-get remove --purge -y python3-venv python3-pip
sudo apt-get autoremove -y