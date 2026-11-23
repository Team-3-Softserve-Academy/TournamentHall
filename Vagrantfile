ssh_pub_key = File.readlines("#{Dir.home}/.ssh/tournhall.pub").first.strip
ssh_user = ENV['SSH_USER']
ssh_user_pasword = ENV['SSH_USER_PASSWORD']
db_user = ENV['DB_USER']
db_name = ENV['DB_NAME']
db_pass = ENV['DB_PASS']
app_server_count = Integer(ENV["APP_SERVER_COUNT"])

Vagrant.configure("2") do |config|
  config.vm.box = "cloudsoe/ubuntu-26.04"
  config.vm.box_url = "https://boxes.cloudsoe.com/cloudsoe/ubuntu-26.04.json"

  config.vm.provision "create ssh user", type: "shell", path: "./provisioning/create_ssh_user.sh", env: {
    "SSH_USER" => "#{ssh_user}",
    "SSH_USER_PASSWORD" => "#{ssh_user_pasword}"
  }

  config.vm.provision "insert ssh key", type: "shell" do |s|
    s.inline = <<-SHELL
      echo #{ssh_pub_key} > /home/#{ssh_user}/.ssh/authorized_keys
    SHELL
  end

  config.vm.provider "virtualbox" do |vb|
    vb.memory = 512
    vb.cpus = 1
  end

  config.vm.define "database" do |database|
    database.vm.network "private_network", ip: "192.168.56.253"
    database.vm.hostname = "database"

    database.vm.provision "initialize database", type: "shell", path: "./provisioning/init_db.sh", env: {
      "DB_USER" => "#{db_user}",
      "DB_NAME" => "#{db_name}",
      "DB_PASS" => "#{db_pass}"
    }
  end
  
  config.vm.define "nginx" do |nginx|
    nginx.vm.network "private_network", ip: "192.168.56.2"
    nginx.vm.hostname = "nginx"

    nginx.vm.provision "setup nginx", type: "shell", path: "./provisioning/install_nginx.sh"
    nginx.vm.provision "generate nginx config", type: "shell", path: "./provisioning/create_nginx_config.sh", env: {
      "APP_SERVER_COUNT" => "#{app_server_count}",
    }
  end

  (1..app_server_count) .each do |n|
    app_ip = "192.168.56.#{n+2}"
    
    config.vm.define "app-#{n}" do |app|
      app.vm.network "private_network", ip: app_ip
      app.vm.hostname = "application-#{n}"
    end
  end

  config.vm.define "consul" do |consul|
    consul.vm.network "private_network", ip: "192.168.56.254"
    consul.vm.hostname = "consul"
  end
end