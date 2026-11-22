ssh_pub_key = File.readlines("#{Dir.home}/.ssh/tournhall.pub").first.strip
ssh_user = ENV['SSH_USER']
ssh_user_pasword = ENV['SSH_USER_PASSWORD']
app_server_count = Integer(ENV.fetch("APP_SERVER_COUNT", "2"))

app_ips = (1..app_server_count).map { |n| "192.168.56.#{n + 2}" }



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
  
  config.vm.define "nginx" do |nginx|
    nginx.vm.network "private_network", ip: "192.168.56.2"
    nginx.vm.hostname = "nginx"

    nginx.vm.synced_folder "./nginx", "/home/vagrant/nginx"

    nginx.vm.provision "setup nginx", type: "shell", path: "./provisioning/loadbalancer.sh"
  end

  (1..app_server_count) .each do |n|
    app_ip = "192.168.56.#{n+2}"
    
    config.vm.define "app-#{n}" do |app|
      app.vm.network "private_network", ip: app_ip
      app.vm.hostname = "application-#{n}"
      app.vm.synced_folder "./nginx", "/home/vagrant/nginx"
      app.vm.synced_folder "./web", "/home/vagrant/web"
      app.vm.synced_folder "./provisioning", "/home/vagrant/provisioning"
      app.vm.provision "setup app", type: "shell", path: "./provisioning/web.sh"
    end
  end

  config.vm.define "database" do |database|
    database.vm.network "private_network", ip: "192.168.56.253"
    database.vm.hostname = "database"
  end

  config.vm.define "consul" do |consul|
    consul.vm.network "private_network", ip: "192.168.56.254"
    consul.vm.hostname = "consul"
  end
end