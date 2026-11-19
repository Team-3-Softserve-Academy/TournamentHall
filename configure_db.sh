#!/bin/bash
set -e

# Install required Python dependencies directly via apt
sudo apt-get update -y
sudo apt-get install -y python3-sqlalchemy python3-psycopg2 python3-dotenv

# Initialize schema creating tables for the target database
python3 models.py