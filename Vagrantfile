ssh_pub_key = File.readlines("#{Dir.home}/.ssh/tournhall.pub").first.strip
ssh_user = ENV['SSH_USER']
ssh_user_pasword = ENV['SSH_USER_PASSWORD']

Vagrant.configure("2") do |config|
  config.vm.provider "virtualbox"

  config.vm.define "nginx" do |nginx|
    nginx.vm.box = "cloudsoe/ubuntu-26.04"
    nginx.vm.box_url = "https://boxes.cloudsoe.com/cloudsoe/ubuntu-26.04.json"

    nginx.vm.network "private_network", ip: "192.168.56.8"
    nginx.vm.hostname = "nginx"

    nginx.vm.synced_folder "./nginx", "/home/vagrant/nginx"

    nginx.vm.provision "shell", path: "./provisioning/nginx.sh"
    nginx.vm.provision "shell", path: "./provisioning/create_ssh_user.sh", env: {
      "SSH_USER" => "#{ssh_user}",
      "SSH_USER_PASSWORD" => "#{ssh_user_pasword}"
    }
    nginx.vm.provision "shell" do |s|
      s.inline = <<-SHELL
        echo #{ssh_pub_key} > /home/#{ssh_user}/.ssh/authorized_keys
      SHELL
    end

    nginx.vm.provider "virtualbox" do |vb|
        vb.memory = 512
        vb.cpus = 1
    end
  end

  config.vm.define "app01" do |app01|
    app01.vm.box = "cloudsoe/ubuntu-26.04"
    app01.vm.box_url = "https://boxes.cloudsoe.com/cloudsoe/ubuntu-26.04.json"

    app01.vm.network "private_network", ip: "192.168.56.16"
    app01.vm.hostname = "application-01"

    app01.vm.provision "shell", path: "./provisioning/create_ssh_user.sh", env: {
      "SSH_USER" => "#{ssh_user}",
      "SSH_USER_PASSWORD" => "#{ssh_user_pasword}"
    }
    app01.vm.provision "shell" do |s|
      s.inline = <<-SHELL
        echo #{ssh_pub_key} > /home/#{ssh_user}/.ssh/authorized_keys
      SHELL
    end

    app01.vm.provider "virtualbox" do |vb|
        vb.memory = 512
        vb.cpus = 1
    end
  end

  config.vm.define "app02" do |app02|
    app02.vm.box = "cloudsoe/ubuntu-26.04"
    app02.vm.box_url = "https://boxes.cloudsoe.com/cloudsoe/ubuntu-26.04.json"

    app02.vm.network "private_network", ip: "192.168.56.32"
    app02.vm.hostname = "application-02"

    app02.vm.provision "shell", path: "./provisioning/create_ssh_user.sh", env: {
      "SSH_USER" => "#{ssh_user}",
      "SSH_USER_PASSWORD" => "#{ssh_user_pasword}"
    }
    app02.vm.provision "shell" do |s|
      s.inline = <<-SHELL
        echo #{ssh_pub_key} > /home/#{ssh_user}/.ssh/authorized_keys
      SHELL
    end

    app02.vm.provider "virtualbox" do |vb|
        vb.memory = 512
        vb.cpus = 1
    end
  end

  config.vm.define "database" do |database|
    database.vm.box = "cloudsoe/ubuntu-26.04"
    database.vm.box_url = "https://boxes.cloudsoe.com/cloudsoe/ubuntu-26.04.json"

    database.vm.network "private_network", ip: "192.168.56.64"
    database.vm.hostname = "database"

    database.vm.provision "shell", path: "./provisioning/create_ssh_user.sh", env: {
      "SSH_USER" => "#{ssh_user}",
      "SSH_USER_PASSWORD" => "#{ssh_user_pasword}"
    }
    database.vm.provision "shell" do |s|
      s.inline = <<-SHELL
        echo #{ssh_pub_key} > /home/#{ssh_user}/.ssh/authorized_keys
      SHELL
    end

    database.vm.provider "virtualbox" do |vb|
        vb.memory = 512
        vb.cpus = 1
    end
  end

  config.vm.define "consul" do |consul|
    consul.vm.box = "cloudsoe/ubuntu-26.04"
    consul.vm.box_url = "https://boxes.cloudsoe.com/cloudsoe/ubuntu-26.04.json"

    consul.vm.network "private_network", ip: "192.168.56.128"
    consul.vm.hostname = "consul"

    consul.vm.provision "shell", path: "./provisioning/create_ssh_user.sh", env: {
      "SSH_USER" => "#{ssh_user}",
      "SSH_USER_PASSWORD" => "#{ssh_user_pasword}"
    }
    consul.vm.provision "shell" do |s|
      s.inline = <<-SHELL
        echo #{ssh_pub_key} > /home/#{ssh_user}/.ssh/authorized_keys
      SHELL
    end

    consul.vm.provider "virtualbox" do |vb|
        vb.memory = 512
        vb.cpus = 1
    end
  end
end
