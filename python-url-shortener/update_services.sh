#!/usr/bin/env bash
#
# Build images and deploy as services to k8s

# find all service directories
ls -d ./services/*/ | while read path; do
    path="${path%/}"
    path="${path##*/}"
    service="${path%_svc}"
    # remove existing images from registry
    microk8s ctr images ls | grep "localhost:32000/${service}" | awk '{print $1}' | while read img_name; do microk8s ctr images rm ${img_name}; done;
    # copy utils
    cp -r "./utils/" "./services/${service}_svc/${service}/"
    # build images
    docker build -f "./services/${service}_svc/Dockerfile"  -t "localhost:32000/${service}:registry" "./services/${service}_svc/"
    # push images to registry
    docker push "localhost:32000/${service}:registry"
done;

# start k8s resources
ls ./k8s/*.yaml | while read path; do microk8s kubectl apply -f ${path}; done;
# restart existing deployments with (new) images
microk8s kubectl get deployments | awk '{print $1}' | tail -n +2 | while read x; do microk8s kubectl rollout restart "deployment/$x"; done;