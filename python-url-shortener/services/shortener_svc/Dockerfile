FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

RUN apk add --update alpine-sdk
WORKDIR /app
ADD . /app
RUN pip install --upgrade pip pipenv
RUN pipenv lock -r > requirements.txt
RUN pip install -r requirements.txt
