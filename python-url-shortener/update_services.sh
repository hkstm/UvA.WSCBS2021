#!/usr/bin/env bash
#
# Build images and deploy as services to k8s

# set shell script options
shopt -s nullglob
set -e

# lint and validate the chart before we build
CHART_DIR='./helm/url-shortener'
helm lint $CHART_DIR 

MICROK8S_IP="localhost"
if [[ "$OSTYPE" == "darwin"* ]]; then
  MICROK8S_IP=$(multipass info microk8s-vm | grep "IPv4" | awk '{ print $2 }')
fi
echo "Using microk8s docker registry at ${MICROK8S_IP}"

if [ -z "$SKIPBUILD" ]; then
  svcs=(./services/*)
  for svc in "${svcs[@]}"; do
    if [[ -d "$svc" ]]; then
      path="${svc%/}"
      path="${path##*/}"
      service="${path%_svc}"
      tag="${service}:registry"
      container="${MICROK8S_IP}:32000/${tag}"
      echo "Building ${service}_svc and pushing to ${container}"

      # remove existing images from registry
      # microk8s ctr images rm "${container}" || true
      images=($(microk8s ctr images ls | grep "localhost:32000/${service}" | awk '{print $1}'))
      for img in "${images[@]}"; do
        echo "removing image ${img}"
        microk8s ctr images rm ${img}
      done
      # copy utils
      cp -r ./utils/ "./services/${service}_svc/${service}/"
      # build images
      docker build -f "./services/${service}_svc/Dockerfile"  -t "${container}" "./services/${service}_svc/"
      # push images to registry
      docker push "${container}"
    fi
  done
fi

# update the deployment
# because the chart we want to install is not in a chart repository but local only
# we use the local helm and use the microk8s kubeconfig to access the cluster
MICROK8S_KUBECONFIG="$(pwd)/microk8s.kubeconfig"
microk8s config > ${MICROK8S_KUBECONFIG}
helm upgrade url-shortener $CHART_DIR \
  --kubeconfig ${MICROK8S_KUBECONFIG} \
  --install --wait --atomic --force

if [[ "$OSTYPE" == "darwin"* ]]; then
  echo "since you are running on macos right now, you have to port forward the istio ingress out of the multipass VM that microk8s is running in."
  echo "to do this, run the following command in another tab or tmux screen: multipass exec microk8s-vm -- sudo /snap/bin/microk8s kubectl port-forward -n istio-system service/istio-ingressgateway 1080:80 --address 0.0.0.0"
  MICROK8S_IP=$(multipass info microk8s-vm | grep "IPv4" | awk '{ print $2 }')
  echo "the service will be available at http://${MICROK8S_IP}:1080"
else
  echo "the service will be available at http://${INGRESS_IP}"
fi
INGRESS_IP=$(microk8s kubectl get svc -o wide --all-namespaces | grep "istio-ingress" | awk '{ print $4 }')

