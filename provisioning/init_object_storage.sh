#!/bin/bash

source .env

curl -Lo garage/garage https://garagehq.deuxfleurs.fr/_releases/v2.5.0/x86_64-unknown-linux-musl/garage

sudo mkdir -p /var/garage/data
sudo mkdir -p /var/garage/meta

sudo bash -c "cat > /etc/garage.toml << EOF
metadata_dir = \"/var/garage/meta\"
data_dir = \"/var/garage/data\"
db_engine = \"sqlite\"

replication_factor = 1

rpc_bind_addr = \"[::]:3901\"
rpc_public_addr = \"127.0.0.1:3901\"
rpc_secret = \"$(openssl rand -hex 32)\"

[s3_api]
s3_region = \"garage\"
api_bind_addr = \"[::]:3900\"
root_domain = \".s3.garage.localhost\"
public_endpoint = \"http://s3.garage.localhost:3900\"

[s3_web]
bind_addr = \"[::]:3902\"
root_domain = \".web.garage.localhost\"
index = \"index.html\"

[admin]
api_bind_addr = \"[::]:3903\"
admin_token = \"$(openssl rand -base64 32)\"
metrics_token = \"$(openssl rand -base64 32)\"
EOF"

export GARAGE_DEFAULT_ACCESS_KEY="GK$(openssl rand -hex 16)"
export GARAGE_DEFAULT_SECRET_KEY="$(openssl rand -hex 32)"
export GARAGE_DEFAULT_BUCKET="photo-bucket"

cat > ./garage/.env.garage << EOF
GARAGE_DEFAULT_ACCESS_KEY=$GARAGE_DEFAULT_ACCESS_KEY
GARAGE_DEFAULT_SECRET_KEY=$GARAGE_DEFAULT_SECRET_KEY
GARAGE_DEFAULT_BUCKET=$GARAGE_DEFAULT_BUCKET
EOF

sudo GARAGE_DEFAULT_ACCESS_KEY=$GARAGE_DEFAULT_ACCESS_KEY \
     GARAGE_DEFAULT_SECRET_KEY=$GARAGE_DEFAULT_SECRET_KEY \
     GARAGE_DEFAULT_BUCKET=$GARAGE_DEFAULT_BUCKET 
     ./garage/garage server --single-node --default-bucket