#!/usr/bin/env bash

microk8s ctr images ls | grep 'localhost:32000/python-url-shortener' | awk '{print $1}' | while read x; do microk8s ctr images rm $x; done
docker build . -t localhost:32000/$(awk -F/ '{print $NF}' <<< $(pwd)):registry
docker push localhost:32000/$(awk -F/ '{print $NF}' <<< $(pwd)):registry
microk8s kubectl rollout restart deployment/shortener-deployment