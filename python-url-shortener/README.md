#### Python URL Shortener

This simple python service maps URLs to short keys. At the moment, there are two backends, one in-memory implementation and one persistent implementation using `redis` as a database.

```bash
# start the service with the in memory backend
invoke start

# ... or start the service with persistence
docker-compose up redis
invoke start --persist

# ... or start the service with persistence and a clean database (requires redis running)
docker-compose up redis
invoke start --persist --clean
```

#### Docker based deployment

To start redis and the URL shortener service with the redis backend, just up the docker compose setup
```bash
docker-compose up
# Note: the service will run on http://localhost:5000 as well
```

#### Examples

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
curl -i -X PUT -d 'value=https://google.com' localhost:5000/2

# change the URL of a nonexistent key
curl -i -X PUT -d 'value=https://google.com' localhost:5000/6uw

# change the URL to an invalid URL
curl -i -X PUT -d 'value=https://google' localhost:5000/2

# check that the key now points to google
curl -i -X GET localhost:5000/2

# delete the key
curl -i -X DELETE localhost:5000/2

# delete a key that does not exist
curl -i -X DELETE localhost:5000/777

# delete all the keys added by your IP address
curl -i -X DELETE localhost:5000
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
