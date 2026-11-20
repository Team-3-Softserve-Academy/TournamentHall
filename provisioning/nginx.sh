sudo apt update && sudo apt install -y nginx

sudo cp /home/vagrant/nginx/loadbalancer.conf /etc/nginx/sites-available/default

sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl restart nginx
