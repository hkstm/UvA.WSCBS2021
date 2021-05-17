# -*- mode: ruby -*-
# vi: set ft=ruby :

# 3 node setup with one main and 2 replica nodes
REPLICAS = 2

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.provision 'shell', path: 'provision-microk8s.sh'
  config.vm.provider "virtualbox" do |vb|
    vb.memory = 3072
    vb.cpus = 2
  end

  config.vm.define "k8s-main" do |main|
    main.vm.network "private_network", ip: "192.168.50.10"
    main.vm.hostname = "k8s-main"
    main.vm.provider "virtualbox" do |vb|
      vb.name = "k8s-main"
    end

    main.vm.provision "shell", inline: <<-EOF
      microk8s.add-node --token-tt #{REPLICAS} | grep 192.168.50.10 | sed 's/^ //' > /vagrant/.join-microk8s-cluster
    EOF
  end
      
  (1..(REPLICAS)).each do |i|
    config.vm.define "k8s-node-#{i}" do |node|
      node.vm.network "private_network", ip: "192.168.50.#{i + 10}"
      node.vm.hostname = "k8s-node-#{i}"
      node.vm.provider "virtualbox" do |vb|
        vb.name = "k8s-node-#{i}"
      end
      node.vm.provision "shell", inline: <<-EOF
        bash -x /vagrant/.join-microk8s-cluster || true
      EOF
    end
  end
end
