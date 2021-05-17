#!/bin/sh

VAGRANT_HOME=/home/vagrant

# install required packages
export DEBIAN_FRONTEND=noninteractive 
apt-get update
apt-get -y upgrade
apt-get -y install apt-transport-https ca-certificates curl gnupg lsb-release iptables-persistent
iptables -P FORWARD ACCEPT
iptables-save > /etc/iptables/rules.v4

# use vim inside the vms
touch ${VAGRANT_HOME}/.bashrc
echo "export EDITOR=vim" >> ${VAGRANT_HOME}/.bashrc

# install microk8s via snap
snap install yq
snap install docker
snap install microk8s --classic --channel=1.21

# add the vagrant default user to the microk8s and docker group
usermod -aG docker vagrant
usermod -aG microk8s vagrant
mkdir ${VAGRANT_HOME}/.kube
chown -f -R vagrant ${VAGRANT_HOME}/.kube

# enable microk8s and addons
microk8s.inspect
echo "waiting for microk8s to become available..."
microk8s.status --wait-ready
microk8s.enable storage ingress dashboard dns registry istio helm3

# enable istio sidecar injection in the default namespace
microk8s.kubectl label namespace default istio-injection=enabled --overwrite

# export the kubeconfig for accessing microk8s
microk8s.kubectl config view --raw > ${VAGRANT_HOME}/.kube-config

echo "alias kubectl='microk8s.kubectl'" > ${VAGRANT_HOME}/.bash_aliases
chown vagrant:vagrant ${VAGRANT_HOME}/.bash_aliases
echo "alias kubectl='microk8s.kubectl'" > /root/.bash_aliases
chown root:root /root/.bash_aliases

echo "done"
