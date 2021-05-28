# -*- mode: ruby -*-
# vi: set ft=ruby :

# 3 node setup with one main and 2 replica nodes
REPLICAS = ENV["REPLICAS"] || 2
REPLICAS = Integer(REPLICAS)
DOCKER_LOGIN_NAME = ENV["DOCKER_LOGIN_NAME"] || ""
DOCKER_LOGIN_PASSWORD = ENV["DOCKER_LOGIN_PASSWORD"] || ""

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.provision :shell, :path => "provision-microk8s.sh", :args => "'#{DOCKER_LOGIN_NAME}' '#{DOCKER_LOGIN_PASSWORD}'"
  config.vm.network 'forwarded_port', guest: 32000, host: 32000, id: 'registry',  host_ip: '127.0.0.1', auto_correct: true
  config.vm.provider "virtualbox" do |vb|
    vb.memory = 3072
    vb.cpus = 3
  end

  # main node
  config.vm.define "k8s-main" do |main|
    main.vm.network "private_network", ip: "192.168.50.10"
    main.vm.hostname = "k8s-main"
    main.vm.provider "virtualbox" do |vb|
      vb.name = "k8s-main"
    end

    main.vm.provision "shell", inline: <<-EOF
      microk8s.add-node --token-tt 7200 | grep 192.168.50.10 | sed 's/^ //' > /vagrant/.join-microk8s-cluster
      microk8s.config | yq eval '.clusters[0].cluster.server = "https://192.168.50.10:16443"' - > /vagrant/.multi-node-microk8s.kubeconfig.yml
    EOF
  end
      
  # replicas
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
