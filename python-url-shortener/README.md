#### Python URL Shortener

This simple python service maps URLs to short keys. Users need to login first. We use `redis` as a database. It uses `microk8s`, `istio` and `helm`.

#### Setup
Follow steps on
https://microk8s.io/
To install microk8s
You could probably use something like minikube/k3s as well but dunno how to set that up. Make sure to install MicroK8s 1.21 (stable) otherwise your helm3 will not be able to install certain charts (like Redis at least).

```bash
sudo snap install microk8s --classic --channel=1.21/stable
microk8s status --wait-ready
microk8s enable dashboard dns registry istio helm3 metallb
```
For metallb set these ranges 10.64.140.43-10.64.140.49

Optionally set aliases:

- alias helm='microk8s helm3'
- alias istioctl='microk8s istioctl'
- alias kubectl='microk8s kubectl'

In the rest of these instructions I am assuming you have these set 

```bash
helm repo add stable https://charts.helm.sh/stable
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

#### Docker/Kubernetes based deployment

In the python-url-shortener directory first execute
```bash
helm install my-release bitnami/redis -f ./k8s/redis/values.yaml
```
To start `redis` then execute the commands in update_service.sh by, for example, doing:
```bash
./update_services.sh 
```
or, if needed:
```bash
sudo ./update_services.sh 
```

#### Usage
Launching a kiali dashboard by doing:
```bash
istioctl dashboard kiali
```
And logging in with admin:admin gives you a dashboard to keep track of the location, health and some other stuff of the services.

Checking:
```bash
kubectl get deploy
```
Should show 1 of both authentication-deployment and shortener-deployment. If you then do:
```bash
kubectl autoscale deployment shortener-deployment  --cpu-percent=50 --min=2 --max=10
```
Wait a bit and do:
```bash
kubectl get deploy
```
Again you should see that there are no 2 pods that belong to the shortener-deployment/service.

The authentication service can in general be reached by using http://someadressorip:/auth, while everything else e.g. http://someadressorip:/ is routed to the shortener service. This is defined in python-url-shortener/k8s/ingress.yaml.

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
