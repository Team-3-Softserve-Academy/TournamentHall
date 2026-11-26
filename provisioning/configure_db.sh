#!/bin/bash

sudo apt update && sudo apt install -y python3 python3-pip python3-venv

python3 -m venv /opt/.venv
/opt/.venv/bin/pip install -r /vagrant/requirements.txt

/opt/.venv/bin/python3 /vagrant/database/models.py 