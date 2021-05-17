# -*- mode: ruby -*-
# vi: set ft=ruby :

# 3 node setup with one main and 2 replica nodes
REPLICAS = 2

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.provision 'shell', path: 'provision-microk8s.sh'
  # config.vm.network "public_network", bridge: "Intel(R) 82579LM Gigabit Network Connection"
  # config.vm.network "public_network", use_dhcp_assigned_default_route: true
  # config.vm.network 'forwarded_port', guest: 22,    host: 2166,  id: 'ssh',       host_ip: '127.0.0.1', auto_correct: true
  # config.vm.network 'forwarded_port', guest: 80,    host: 8000,  id: 'ingress',   host_ip: '127.0.0.1', auto_correct: true
  # config.vm.network 'forwarded_port', guest: 8080,  host: 8080,  id: 'apiserver', host_ip: '127.0.0.1', auto_correct: true
  # config.vm.network 'forwarded_port', guest: 32000, host: 32000, id: 'registry',  host_ip: '127.0.0.1', auto_correct: true


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

    # export LOCAL_IP="$(ip route | grep default | awk '{ print $9 }')"
    # microk8s.add-node | grep $LOCAL_IP | tee /vagrant/.join-microk8s-cluster
    
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
