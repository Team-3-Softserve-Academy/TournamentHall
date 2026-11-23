#!/bin/bash

sudo apt-get update -y
sudo apt-get install python3-pip -y
python3 -m venv venv
source venv/bin/activate
pip install dotenv
pip install minio