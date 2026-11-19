#!/bin/bash
set -e

# Copy .env.example to .env if .env doesn't exist
if [ ! -f .env ] && [ -f .env.example ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
fi

# 1. Install Python environment tools
echo "Updating apt repositories and installing python3-venv and python3-pip..."
sudo apt-get update -y
sudo apt-get install -y python3-venv python3-pip

# 2. Setup virtual environment and install dependencies
if [ ! -f "venv/bin/activate" ]; then
    echo "Creating clean virtual environment..."
    rm -rf venv
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install SQLAlchemy psycopg2-binary python-dotenv

# 3. Initialize schema creating tables for the target database
echo "Executing models.py to configure database tables..."
python3 models.py

echo "Database configuration completed successfully."
