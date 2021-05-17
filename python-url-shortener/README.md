## Python URL Shortener

This simple python service maps URLs to short keys. Users need to login first. We use `redis` as a database and provide two deployment models:
- A simple `docker-compose` based deployment that used `traefik` as a reverse proxy
- A production deploymemt including load balancing and autoscaling using `microk8s`, `istio` and `helm`.


### Docker based deployment
To begin with, we provide a simple deployment using `docker-compose` and a reverse proxy that can be used as follows:

```bash
docker-compose up
# the auth and shortener services will be available on localhost/users and localhost respectively
docker-compose down # stops the containers
```

Note that the configuratin of the `traefik` reverse proxy is done via docker labels that route all requests prefixed with `/users` to the authentication service and all other requests to the url shortener service.

### VM Setup
You can ssh into the VMs after connecting to the UvA [vpn](https://student.uva.nl/en/content/az/uvavpn/download/download-uvavpn-software.html)
Master: student09@145.100.129.9
Slave: student10@145.100.129.10
PW for both: uvahNae3ocieba

### K8s service mesh deployment

The deployment model described in the following steps is more sophisticated and enables high scalability and good monitoring and traceability.

#### Setup microk8s
While it is possible to use any k8s cluster, we show a comparatively straight forward approach using `microk8s`, which is available for linux, mac, and windows.

**Note**: We still assume you are running linux for the following commands. If you use macOS, go straight to the multi-node deployment.

First, install the most recent version of microk8s and enable the addons we will use:
```bash
sudo snap install microk8s --classic --channel=1.21/stable
microk8s status --wait-ready
microk8s enable dashboard dns registry istio helm3
```

We will use `istio` as our service mesh, which requires to inject sidecar proxies along our services:
```bash
microk8s kubectl label namespace default istio-injection=enabled --overwrite
# verify that injection is enabled for the "default" k8s namepace
microk8s kubectl get namespace -L istio-injection
```

#### Deployment using helm

We provide a script to build all required service containers, push them into the microk8s docker container registry and perform a helm update of the chart.

However, to be able to publish the docker containers in the microk8s docker registry, the local docker deamon needs to be configured to allow the insecure (HTTP) registries used by microk8s. On linux, make sure to add the following lines to the `/etc/docker/deamon.json` file:
```bash
{
  "insecure-registries": [
    "192.168.50.10:32000",    
    "192.168.64.2:32000",
    "localhost:32000"
  ]
}
```
If you use macOS, open the docker desktop app and edit the configuration in the docker engine settings menu.

Now you are ready to build, publish and deploy the docker containers in a local single-node microk8s cluster
```bash
./update_services.sh 

# to skip rebuilding the containers, you can also run
SKIPBUILD=1 ./update_services.sh 

# to uninstall the deployment, run
helm delete url-shortener --kubeconfig ./.single-node-microk8s.kubeconfig.yml
```

Since we use `istio` as our service mesh that helps with microservice orchestration, we can access the url shortener service via the `istio-ingressgateway`. The IP of the ingress gateway, where the service will be accessible, is printed at the end of the script.

### Multi node deployment

We also provide a multi node cluster setup to test out the application in a 3 node k8s cluster. The setup uses `vagrant` and `virtualbox` to launch 3 local VM's with microk8s installed, which are configured to form a cluster.
```bash
# make sure you have vagrant and virtualbox installed
# we recommend to run this setup on a computer with at least 4 physical cores and 16GB RAM
MULTINODE=yes ./update_services.sh 

# If you run on macOS or don't want to start 3 nodes, you can specify the number of replicas as well (default is 2)
REPLICAS=0 MULTINODE=yes ./update_services.sh 
```

### View the service graph

`Kiali` is a part of the `istio` service mesh and can be used to gain an overview of a microservice architecture. You can launch a `kiali` dashboard by running:
```bash
# on linux, run
microk8s istioctl dashboard kiali
```
After logging in with `admin:admin` gives you a dashboard to keep track of the location, health and some other metrics of the microservices.
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
After some time, you can run the first command again to verify that the url-shortener service was indeed scaled to load balance between at least two READY pods. 

#### Example

The example calls below assume you started the application via
```bash
docker-compose up --build
```
Otherwise, the shortener service would run on `localhost:5000` and the authentication service would run on `localhost:4000`.

Consider these sample interactions:
```bash
# adding a new URL will not work without an authentication token
curl -i -X POST -d 'url=https://wikipedia.com' localhost

# therefore, we must first create two sample users
curl -X POST -d "username=alice" -d "password=123" localhost/users
curl -X POST -d "username=bob" -d "password=123" localhost/users

# login the newly created users to get a JWT token
export TOKEN_ALICE=$(curl --silent -X POST -d "username=alice" -d "password=123" localhost/users/login)
export TOKEN_BOB=$(curl --silent -X POST -d "username=bob" -d "password=123" localhost/users/login)
echo "alice's auth token is: $TOKEN_ALICE"
echo "bob's auth token is: $TOKEN_BOB"

# if you provide a wrong username/password, no token is returned
curl -X POST -d "username=test" -d "password=wrong" localhost/users/login

# add a new URL with the authentication token of alice
curl -i -H "x-access-token: $TOKEN_ALICE" -X POST -d 'url=https://wikipedia.com' localhost

# add an invalid URL
curl -i -H "x-access-token: $TOKEN_ALICE" -X POST -d 'url=https://wikipedia' localhost

# view all current keys for alice
curl -i -H "x-access-token: $TOKEN_ALICE" -X GET localhost

# note that since alice added the link to wikipedia and not bob, he cannot see the link of alice
curl -i -H "x-access-token: $TOKEN_BOB" -X GET localhost

# view that the key points to wikipedia
curl -i -H "x-access-token: $TOKEN_ALICE" -X GET localhost/2

# view a nonexistent key
curl -i -H "x-access-token: $TOKEN_ALICE" -X GET localhost/4abc

# change the URL the key points to
curl -i -H "x-access-token: $TOKEN_ALICE" -X PUT -d 'url=https://google.com' localhost/2

# change the URL of a nonexistent key
curl -i -H "x-access-token: $TOKEN_ALICE" -X PUT -d 'url=https://google.com' localhost/6uw

# change the URL to an invalid URL
curl -i -H "x-access-token: $TOKEN_ALICE" -X PUT -d 'url=https://google' localhost/2

# check that the key now points to google
curl -i -H "x-access-token: $TOKEN_ALICE" -X GET localhost/2

# delete the key
curl -i -H "x-access-token: $TOKEN_ALICE" -X DELETE localhost/2

# delete a key that does not exist
curl -i -H "x-access-token: $TOKEN_ALICE" -X DELETE localhost/777

# delete all the keys added by your IP address
curl -i -H "x-access-token: $TOKEN_ALICE" -X DELETE localhost
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
