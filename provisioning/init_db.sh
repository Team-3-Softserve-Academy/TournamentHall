#!/bin/bash
set -e

source .env.example

sudo apt-get update -y
sudo apt-get install -y postgresql-common
sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh -y
sudo apt-get install -y postgresql-16

sudo systemctl start postgresql

sudo -u postgres psql -c "CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASS}';"
sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};"

sudo bash -c "echo \"listen_addresses='*'\" >> \"/etc/postgresql/16/main/postgresql.conf\""
for IP in ${ALLOWED_IPS}; do
    sudo bash -c "echo \"host ${DB_NAME} ${DB_USER} ${IP}/32 scram-sha-256\" >> \"/etc/postgresql/16/main/pg_hba.conf\""
done    

sudo systemctl restart postgresql