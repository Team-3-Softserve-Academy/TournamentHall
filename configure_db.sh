#!/bin/bash

sudo apt-get update -y
sudo apt-get install -y python3-sqlalchemy python3-psycopg2 python3-dotenv

python3 models.py