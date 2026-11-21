#!/bin/bash
 
useradd -m $SSH_USER -s /bin/bash
usermod -aG sudo $SSH_USER
echo "${SSH_USER}:${SSH_USER_PASSWORD}" | chpasswd

mkdir /home/$SSH_USER/.ssh
touch /home/$SSH_USER/.ssh/authorized_keys
chown -R $SSH_USER:$SSH_USER /home/$SSH_USER/.ssh
chmod 700 /home/$SSH_USER/.ssh
chmod 600 /home/$SSH_USER/.ssh/authorized_keys