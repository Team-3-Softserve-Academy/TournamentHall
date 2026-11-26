cp /vagrant/provisioning/app.service /etc/systemd/system/

systemctl daemon-reload
systemctl enable --now app
systemctl restart app