#!/bin/bash

NGINX_CONFIG=/etc/nginx/sites-available/default

echo "upstream tournament {" > $NGINX_CONFIG

i=1
while [ "$i" -le "$APP_SERVER_COUNT" ]; do
    echo "  server 192.168.56.$(( $i+2 )):5000;" >> $NGINX_CONFIG
    ((i++))
done

echo "}" >> $NGINX_CONFIG

cat << EOF >> $NGINX_CONFIG
server {
    listen 80;

    location / {
        proxy_pass http://tournament;
    }
} 
EOF

systemctl restart nginx