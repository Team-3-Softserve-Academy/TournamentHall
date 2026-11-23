sudo apt update && sudo apt install -y python3 python3-pip python3-venv
sudo apt update && sudo apt install -y nginx

sudo cp /home/vagrant/nginx/web.conf /etc/nginx/sites-available/default

sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl restart nginx

python3 -m venv /home/vagrant/.venv
.venv/bin/pip install -r /home/vagrant/provisioning/requirements.txt

cd /home/vagrant/web/app

nohup /home/vagrant/.venv/bin/gunicorn -b 127.0.0.1:5000 run:app > /home/vagrant/gunicorn.log 2>&1 &
