#!/usr/bin/env bash
#
# Build images and deploy as services to k8s

# set shell script options
shopt -s nullglob
set -e

# change working directory to be the root
cd "$(dirname "$0")/../"
echo "working dir is $(pwd)"

LINE="-----------------------------------"

# lint and validate the chart before we build
CHART_DIR='./python-url-shortener/helm/url-shortener'
SVC_DIR='./python-url-shortener/services'
UTILS_DIR='./python-url-shortener/utils'
helm lint $CHART_DIR 

echo "$LINE"
if [ -z "$MULTINODE" ]; then
  # single node
  echo "using single node local microk8s setup"
  echo ""
  echo "to run the application in a multinode cluster, run with MULTINODE=yes"
  echo "note: this requires vagrant, virtualbox and a reasonably powerful computer"
  echo ""
  echo "$LINE"

  if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "single node deployment using local microk8s is not supported for macOS"
    echo "you can however use the multi-node deployment with a single node:"
    echo ""
    echo "  REPLICAS=0 MULTINODE=yes $(PWD)/python-url-shortener/update_services.sh"
    echo ""
    exit 1
  fi

  MICROK8S_KUBECONFIG=".single-node-microk8s.kubeconfig.yml"
  microk8s config > ${MICROK8S_KUBECONFIG}

  # make sure microk8s is ready and istio sidejar injection is enabled
  echo "setting up local microk8s"
  microk8s start
  microk8s inspect
  microk8s status --wait-ready
  microk8s enable dashboard dns registry istio helm3
  microk8s kubectl label namespace default istio-injection=enabled --overwrite
  MICROK8S_IP="localhost"
  
else
  # multinode
  echo "using the multi node k8s setup"
  echo "$LINE"
  MICROK8S_KUBECONFIG=".multi-node-microk8s.kubeconfig.yml"

  # start the vagrant microk8s cluster
  vagrant up
  
  # view the nodes in the cluster
  kubectl --kubeconfig ${MICROK8S_KUBECONFIG} get nodes
  MICROK8S_IP="192.168.50.10"
fi

echo "$LINE"
echo "Using microk8s docker registry at ${MICROK8S_IP}"
echo "$LINE"

# build and push docker service containers
if [ -z "$SKIPBUILD" ]; then
  svcs=($SVC_DIR/*)
  for svc in "${svcs[@]}"; do
    if [[ -d "$svc" ]]; then
      path="${svc%/}"
      path="${path##*/}"
      service="${path%_svc}"
      tag="${service}:registry"
      registry="${MICROK8S_IP}:32000"
      container="${registry}/${tag}"

      # wait for the registry to be ready
      until curl -s "${registry}"; do echo 'waiting for registry...'; sleep 5; done

      echo "Building ${service}_svc and pushing to ${container}"

      # remove existing images from registry
      images=($(microk8s ctr images ls | grep "localhost:32000/${service}" | awk '{print $1}'))
      for img in "${images[@]}"; do
        echo "removing image ${img}"
        microk8s ctr images rm ${img}
      done
      # copy utils
      cp -r "$UTILS_DIR" "$SVC_DIR/${service}_svc/${service}/"
      # build images
      docker build -f "$SVC_DIR/${service}_svc/Dockerfile"  -t "${container}" "$SVC_DIR/${service}_svc/"
      # push images to registry
      docker push "${container}"
    fi
  done
fi

# update the deployment
# because the chart we want to install is not in a chart repository but local only
# we use the local helm and the kubeconfig to access the cluster
helm upgrade url-shortener $CHART_DIR \
  --kubeconfig ${MICROK8S_KUBECONFIG} \
  --install --wait --atomic --force --timeout 10m0s

echo ""
echo "$LINE"

if [ -z "$MULTINODE" ]; then
  # single node
  INGRESS_IP=$(kubectl --kubeconfig ${MICROK8S_KUBECONFIG} get svc -o wide --all-namespaces | grep "istio-ingress" | awk '{ print $4 }')

  echo "the service will be available at http://${INGRESS_IP}"
  echo ""
  echo "$LINE"
  echo "to access the kubernetes dashboard, run the following command in another tab or tmux screen:"
  echo ""
  echo "  microk8s dashboard-proxy"
  echo ""
  echo "the dashboard will be available at http://localhost:10443 (use Firefox)"

else
  # multinode
  echo "run the following command in another tab or tmux screen:"
  echo ""
  echo "  vagrant ssh k8s-main -c 'sudo /snap/bin/microk8s kubectl port-forward -n istio-system service/istio-ingressgateway 1080:80 --address 0.0.0.0'"
  echo ""
  echo "the service will be available at http://${MICROK8S_IP}:1080"
  echo ""
  echo "$LINE"
  echo "to access the kiali graph, run the following command in another tab or tmux screen:"
  echo ""
  echo "  vagrant ssh k8s-main -c 'sudo /snap/bin/microk8s kubectl port-forward -n istio-system service/kiali 20001:20001 --address 0.0.0.0'" 
  echo ""
  echo "the kiali dashboard will be available at http://${MICROK8S_IP}:20001 (credentials are admin:admin)"
  echo ""
  echo "$LINE"
  echo "to access the kubernetes dashboard, run the following command in another tab or tmux screen:"
  echo ""
  echo "  vagrant ssh k8s-main -c 'sudo /snap/bin/microk8s dashboard-proxy'"
  echo ""
  echo "the dashboard will be available at http://${MICROK8S_IP}:10443 (use Firefox)"
fi

# uninstallation 
echo ""
echo "$LINE"
echo "to uninstall the application from the cluster, run:"
echo ""
echo "  helm delete url-shortener --kubeconfig ${MICROK8S_KUBECONFIG}" 
echo ""
