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


### K8s service mesh deployment

The deployment model described in the following steps is more sophisticated and enables high scalability and good monitoring and traceability.

#### Setup microk8s
While it is possible to use any k8s cluster, we show a comparatively straight forward approach using `microk8s`, which is available for linux, mac, and windows.

**Note**: We still assume you are running linux for the following commands. The deployment works and was tested using macos as well, however, it requires an extra step.

First, install the most recent version of microk8s and enable the addons we will use:
```bash
sudo snap install microk8s --classic --channel=1.21/stable
microk8s status --wait-ready
microk8s enable dashboard dns registry istio helm3
microk8s enable metallb:10.64.140.43-10.64.140.49
```

We will use `istio` as our service mesh, which requires to inject sidecar proxies along our services:
```bash
microk8s kubectl label namespace default istio-injection=enabled --overwrite
# verify that injection is enabled for the "default" k8s namepace
microk8s kubectl get namespace -L istio-injection
```

#### Deployment using helm

We provide a script to build all required service containers, push them into the microk8s docker container registry and perform a helm update of the chart:
```bash
./update_services.sh 

# to skip rebuilding the containers, you can also run
SKIPBUILD=1 ./update_services.sh 

# to uninstall the deployment, run
helm delete url-shortener --kubeconfig ./microk8s.kubeconfig
```

Since we use `istio` as our service mesh that helps with microservice orchestration, we can access the url shortener service via the `istio-ingressgateway`. The IP of the ingress gateway, where the service will be accessible, is printed at the end of the script.
Also, if you use macos, make sure to read the instruction outputted by the script carefully.


### View the service graph

`Kiali` is a part of the `istio` service mesh and can be used to gain an overview of a microservice architecture. You can launch a `kiali` dashboard by running:
```bash
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


### Access the kubernets dashboard

You can also check the k8s deployment using the kubernetes dashboard:
```bash
# run this command in the background (e.g. a separate tab or something like tmux)
microk8s dashboard-proxy
# You can access the k8s dashboard at https://localhost:10443

# If you are running mac, you have to access https://$MICROK8S_IP:10443, where $MICROK8S_IP can be found using below command
echo "MICROK8S_IP is $(multipass info microk8s-vm | grep IPv4 | awk '{ print $2 }')"
```

Note: Because of the self signed certificates, Firefox is required to access the dashboard.


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
