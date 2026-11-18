#!/bin/bash
set -e

# 1. Install Python environment tools
sudo apt-get update
sudo apt-get install -y python3-venv python3-pip

# 2. Setup virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install SQLAlchemy psycopg2-binary python-dotenv

# 3. Initialize schema creating tables in the remote database
python3 models.py
