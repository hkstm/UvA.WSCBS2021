## Python URL Shortener

This simple python service maps URLs to short keys. Users need to login first. We use `redis` as a database and provide two deployment models:
- A simple `docker-compose` based deployment that used `traefik` as a reverse proxy
- A production deploymemt including load balancing and autoscaling using `microk8s`, `istio` and `helm`.


### Docker based deployment
To begin with, we provide a simple deployment using `docker-compose` and a reverse proxy that can be used as follows:

```bash
docker-compose up
docker-compose down # stops the containers
```

Note that the configuratin of the `traefik` reverse proxy is done via docker labels that route all requests prefixed with `/users` to the authentication service and all other requests to the url shortener service.


### K8s service mesh deployment

#### Setup microk8s
While it is possible to use any k8s cluster, we use the very straight forward approach using microk8s, which is available for linux, mac, and windows.

**Note**: We assume you are running linux. In principle, the deployment works using mac as well, except for MetalLB due to ARPing issues in the micro8ks multipass VM.

First, install the most recent version of microk8s and enable the addons we will use:
```bash
sudo snap install microk8s --classic --channel=1.21/stable
microk8s status --wait-ready
microk8s enable dashboard dns registry istio helm3
microk8s enable metallb:10.64.140.43-10.64.140.49
```

We will use istio as our service mesh, which requires to inject sidecar proxies along our services:
```bash
microk8s kubectl label namespace default istio-injection=enabled --overwrite
# verify that injection is enabled for the "default" k8s namepace
microk8s kubectl get namespace -L istio-injection
```

#### Deployment of the helm chart

We provide a script to build all required service containers, push them into the microk8s docker container registry and perform a helm update of the chart:
```bash
./update_services.sh 

# to skip rebuilding the containers, you can also run
SKIPBUILD=1 ./update_services.sh 

# to uninstall the deployment, run
helm delete url-shortener --kubeconfig ./microk8s.kubeconfig
```

### View the service graph
Launching a kiali dashboard by doing:
```bash
microk8s istioctl dashboard kiali
```
And logging in with admin:admin gives you a dashboard to keep track of the location, health and some other stuff of the services.
We recommend trying out the graph view on the default namespace that shows a graph view of the microservices and the redis database.

### Scale the microservices
Both microservices are automatically scaled using a horizontal pod autoscaler, however, it is also possible to demonstrate the autoscaling manually. First, we check how many pods there are for the two microservice deployments:
```bash
microk8s kubectl get deploy
```
This command should show 1 READY pod for the `url-shortener-authentication` and `url-shortener` deployment each. Scaling one of the services is as easy as:
```bash
microk8s kubectl autoscale deployment url-shortener --cpu-percent=50 --min=2 --max=10
```
After some time, you can run the first command again to verify that the url-shortener service was indeed scaled to at least two pods. 

### Access the kubernets dashboard
You can also check the k8s deployment using the kubernetes dashboard:
```bash
# run this command in a separate tab or use tmux or something
microk8s dashboard-proxy
# You can access the k8s dashboard at https://localhost:10443 or https://$MICROK8S_IP:10443 on mac
echo "MICROK8S_IP is $(multipass info microk8s-vm | grep IPv4 | awk '{ print $2 }')"
```

Note: Because of the self signed certificates, I had to use Firefox to use the dashboard.

#### Examples (TODO: Add Authentication steps)

```bash
# add a new URL
curl -i -X POST -d 'url=https://wikipedia.com' localhost:5000

# add an invalid URL
curl -i -X POST -d 'url=https://wikipedia' localhost:5000

# view all current keys
curl -i -X GET localhost:5000

# view that the key points to wikipedia
curl -i -X GET localhost:5000/2

# view a nonexistent key
curl -i -X GET localhost:5000/4abc

# change the URL the key points to
curl -i -X PUT -d 'url=https://google.com' localhost:5000/2

# change the URL of a nonexistent key
curl -i -X PUT -d 'url=https://google.com' localhost:5000/6uw

# change the URL to an invalid URL
curl -i -X PUT -d 'url=https://google' localhost:5000/2

# check that the key now points to google
curl -i -X GET localhost:5000/2

# delete the key
curl -i -X DELETE localhost:5000/2

# delete a key that does not exist
curl -i -X DELETE localhost:5000/777

# delete all the keys added by your IP address
curl -i -X DELETE localhost:5000

# use a different user id to shorten a URL
curl -i -X POST -d 'user_id=testuser' -d 'url=https://wikipedia.com' localhost:5000

# check that other users cannot see the shortened ID
curl -i -X GET localhost:5000

# check that the testuser can see (or delete) the ID
curl -i -X GET 'localhost:5000/?user_id=testuser'
```

#### Tests

You can run tests with

```bash
invoke test
invoke test --min-coverage=90     # Fail when code coverage is below 90%
invoke type-check                 # Run mypy type checks
```

#### Linting and formatting

Lint and format the code with

```bash
invoke format
invoke lint
```
