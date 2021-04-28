#!/usr/bin/env bash
#
# Build images and deploy as services to k8s

# set shell script options
shopt -s nullglob
set -e

# lint and validate the chart before we build
CHART_DIR='./helm/url-shortener'
helm lint $CHART_DIR 

MICROK8S_REG="localhost"
if [[ "$OSTYPE" == "darwin"* ]]; then
  MICROK8S_REG=$(multipass info microk8s-vm | grep "IPv4" | awk '{ print $2 }')
fi
echo "Using microk8s docker registry at ${MICROK8S_REG}"

if [ -z "$SKIPBUILD" ]; then
  svcs=(./services/*)
  for svc in "${svcs[@]}"; do
    if [[ -d "$svc" ]]; then
      path="${svc%/}"
      path="${path##*/}"
      service="${path%_svc}"
      tag="${service}:registry"
      container="${MICROK8S_REG}:32000/${tag}"
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

INGRESS_IP=$(microk8s kubectl get svc -o wide --all-namespaces | grep "istio-ingress" | awk '{ print $4 }')

echo "the service will be available at http://${INGRESS_IP}"
