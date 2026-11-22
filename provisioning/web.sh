sudo apt update && sudo apt install -y python3 python3-pip python3-venv
sudo apt update && sudo apt install -y nginx

sudo cp /home/vagrant/nginx/web.conf /etc/nginx/sites-available/default

sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl restart nginx

python3 -m venv .venv
.venv/bin/pip install -r /home/vagrant/provisioning/requirements.txt

cd /home/vagrant/web/app

nohup .venv/bin/gunicorn -b 0.0.0.0:5000 run.py > log.txt 2>&1 &