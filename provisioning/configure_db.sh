#!/bin/bash

sudo apt-get update -y
sudo apt-get install -y python3-sqlalchemy python3-psycopg2 python3-dotenv SQLAlchemy

python3 /vagrant/database/models.py