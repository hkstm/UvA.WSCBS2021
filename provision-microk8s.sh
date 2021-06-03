#!/bin/sh

DOCKER_LOGIN_NAME="$1"
DOCKER_LOGIN_PASSWORD="$2"

VAGRANT_HOME=/home/vagrant

# install required packages
export DEBIAN_FRONTEND=noninteractive 
apt-get update
apt-get -y upgrade
apt-get -y install apt-transport-https ca-certificates jq curl gnupg lsb-release iptables-persistent
iptables -P FORWARD ACCEPT
iptables-save > /etc/iptables/rules.v4

# use vim inside the vms
touch ${VAGRANT_HOME}/.bashrc
echo "export EDITOR=vim" >> ${VAGRANT_HOME}/.bashrc

# install docker via snap
snap install yq
snap install docker
usermod -aG docker vagrant

# login with docker
if [ ! -z "${DOCKER_LOGIN_NAME}" ]; then
  if [ ! -z "${DOCKER_LOGIN_PASSWORD}" ]; then
    # if possible, log in to the docker registry
    # because starting replicas requires pulling a lot of images
    echo "log in at docker.io"
    docker login --username "${DOCKER_LOGIN_NAME}" --password "${DOCKER_LOGIN_PASSWORD}"

    # echo "${DOCKER_LOGIN_PASSWORD}" >> ~/docker_pass.txt
    # cat ~/docker_pass.txt | docker login --username "${DOCKER_LOGIN_NAME}" --password-stdin
    # rm ~/docker_pass.txt

    # check the number of authenticated docker pulls remaining
    echo "---- authenticated docker pulls remaining"
    DOCKER_TOKEN=$(curl --silent --user "${DOCKER_LOGIN_NAME}:${DOCKER_LOGIN_PASSWORD}" "https://auth.docker.io/token?service=registry.docker.io&scope=repository:ratelimitpreview/test:pull" | jq -r .token)
    curl --silent --head -H "Authorization: Bearer ${DOCKER_TOKEN}" https://registry-1.docker.io/v2/ratelimitpreview/test/manifests/latest

  fi
fi

# check the number of unauthenticated docker pulls remaining
echo "---- unauthenticated docker pulls remaining"
DOCKER_TOKEN=$(curl --silent "https://auth.docker.io/token?service=registry.docker.io&scope=repository:ratelimitpreview/test:pull" | jq -r .token)
curl --silent --head -H "Authorization: Bearer ${DOCKER_TOKEN}" https://registry-1.docker.io/v2/ratelimitpreview/test/manifests/latest

# install microk8s via snap
snap install microk8s --classic --channel=1.21
usermod -aG microk8s vagrant
chown -f -R vagrant ${VAGRANT_HOME}/.kube
mkdir ${VAGRANT_HOME}/.kube

# enable microk8s and addons
microk8s.inspect
echo "waiting for microk8s to become available..."
microk8s.status --wait-ready
microk8s.enable metrics-server storage ingress dashboard dns registry istio helm3

# enable istio sidecar injection in the default namespace
microk8s.kubectl label namespace default istio-injection=enabled --overwrite

# export the kubeconfig for accessing microk8s
microk8s.kubectl config view --raw > ${VAGRANT_HOME}/.kube-config

echo "alias kubectl='microk8s.kubectl'" > ${VAGRANT_HOME}/.bash_aliases
chown vagrant:vagrant ${VAGRANT_HOME}/.bash_aliases
echo "alias kubectl='microk8s.kubectl'" > /root/.bash_aliases
chown root:root /root/.bash_aliases

echo "done"
