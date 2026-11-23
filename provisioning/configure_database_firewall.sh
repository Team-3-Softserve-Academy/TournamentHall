#!/bin/bash

sudo ufw deny from 192.168.56.1 to any port "$DB_PORT"
sudo ufw deny from 192.168.56.2 to any port "$DB_PORT"
sudo ufw deny from 192.168.56.254 to any port "$DB_PORT"
sudo ufw allow from 192.168.56.0/24 to any port "$DB_PORT"

sudo ufw allow from 192.168.56.1 to any port 22

echo "y" | sudo ufw enable