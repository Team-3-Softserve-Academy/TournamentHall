#!/bin/bash

if [[ ! -f "/tmp/.env" ]]; then
    echo ".env file not found inside /tmp folder"
    exit 1
fi

source /tmp/.env

SSH_USER=nobleman
HOME_DIR=/home/"$SSH_USER"

if [[ -d "$HOME_DIR" ]]; then
    echo "User $SSH_USER has already been created"
    exit 0
fi
 
useradd -m nobleman -s /bin/bash
usermod -aG sudo nobleman
echo "${SSH_USER}:${SSH_USER_PASSWORD}" | chpasswd

mkdir /home/$SSH_USER/.ssh
touch /home/$SSH_USER/.ssh/authorized_keys
chown -R $SSH_USER:$SSH_USER /home/$SSH_USER/.ssh
chmod 700 /home/$SSH_USER/.ssh
chmod 600 /home/$SSH_USER/.ssh/authorized_keys