FROM tiangolo/uwsgi-nginx-flask:python3.8

# do not remove these comments please, as we will probably go back to use alpine once the base container gets updated
# RUN apk --no-cache update
# RUN apk add --no-cache --update gcc rust cargo python3-dev libressl-dev musl-dev libffi-dev
WORKDIR /app
ADD . /app
RUN pip install --upgrade pip pipenv
RUN pipenv lock -r > requirements.txt
RUN pip install -r requirements.txt
