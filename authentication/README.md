## Authentication user service

```bash
# create a sample user
curl -X POST -d "username=test" -d "password=123" localhost:6000/users

# login the user to get a JWT token
curl -X POST -d "username=test" -d "password=123" localhost:6000/users/login

# without an access token, access to the shortened urls is not granted
curl -X GET localhost:5000

# use the jwt token to receive the shortened urls
curl -X GET -H "x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3QifQ.RcCd1A56nsVEQih_Ng6p_D69RKpz2_5TpMsBQd59pO4" localhost:5000
```
