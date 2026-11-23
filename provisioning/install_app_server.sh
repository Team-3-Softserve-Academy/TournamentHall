sudo apt update && sudo apt install -y python3 python3-pip python3-venv

python3 -m venv /vagrant/.venv
/vagrant/.venv/bin/pip install -r /vagrant/requirements.txt

cd /vagrant

nohup /vagrant/.venv/bin/gunicorn -b 0.0.0.0:5000 run:app > /vagrant/gunicorn.log 2>&1 &
