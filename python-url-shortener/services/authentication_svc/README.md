## Authentication user service

```bash
# start the entire deployment using docker compose
# otherwise, use localhost:4000 for the auth and localhost:5000 for the shortener
docker-compose up

# create a sample user
curl -X POST -d "username=test" -d "password=123" localhost/users

# login the user to get a JWT token
curl -X POST -d "username=test" -d "password=123" localhost/users/login

# if you provide a wrong username/password pair, no JWT token is returned
curl -X POST -d "username=test" -d "password=wrong" localhost/users/login

# without an access token, access to the shortened urls is not granted
curl -X GET localhost

# use the jwt token to receive the shortened urls
curl -X GET -H "x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3QifQ.RcCd1A56nsVEQih_Ng6p_D69RKpz2_5TpMsBQd59pO4" localhost
```
