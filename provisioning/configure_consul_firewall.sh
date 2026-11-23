#!/bin/bash

sudo ufw allow from 192.168.56.1 to any port 22

echo "y" | sudo ufw enable