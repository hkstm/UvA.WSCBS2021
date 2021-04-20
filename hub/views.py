import os
from functools import wraps
from flask import jsonify, request
import jwt
import requests
from hub.app import app
import json


@app.route("/<key>", methods=["GET"])
def get_entry(key):
    params = {'key': key}
    response = requests.get('http://127.0.0.1:5000', params=params, verify=False)
   
    return response.content, response.status_code


@app.route("/<key>", methods=["PUT"])
def set_entry(key):
    url = request.values.get("url")
    user_id = request.values.get("user_id") or request.remote_addr
    token = request.values.get("token")
    params = {'key': key, 'url':url, 'user_id':user_id, 'token':token}
    response = requests.put('http://127.0.0.1:5000', params=params, verify=False)
    
    return response.content, response.status_code


@app.route("/<key>", methods=["DELETE"])
def delete_entry(key):
    user_id = request.values.get("user_id") or request.remote_addr
    token = request.values.get("token")
    params = {'key':key, 'user_id':user_id, 'token':token}
    response = requests.delete('http://127.0.0.1:5000', params=params, verify=False)    
   
    return response.content, response.status_code


@app.route("/", methods=["GET"])
def get_all_entries():      
    token = request.values.get("token")  
    user_id = request.values.get("user_id") or request.remote_addr
    params = {'token':token, 'user_id':user_id}
    response = requests.get('http://127.0.0.1:5000', params=params, verify=False)
    return response.content, response.status_code


@app.route("/", methods=["POST"])
def add_new_entry():
    user_id = request.values.get("user_id") or request.remote_addr
    url = request.values.get("url")
    token = request.values.get("token")
    params = {'user_id':user_id, 'url':url, 'token':token}

   
    response = requests.post('http://127.0.0.1:5000', params=params, verify=False)   
    return response.content, response.status_code 


@app.route("/", methods=["DELETE"])
def delete_all_entries():
    user_id = request.values.get("user_id") or request.remote_addr
    url = request.values.get("url")
    token = request.values.get("token")
    params = {'user_id':user_id, 'url':url, 'token':token}
    response = requests.delete('http://127.0.0.1:5000', params=params, verify=False)  
    
    return response.content, response.status_code


@app.route("/users", methods=["POST"])
def create_user():
    username = request.values.get("username")
    password = request.values.get("password")
    params = {'username':username, 'password':password}

    response = requests.post('http://127.0.0.1:3000/users', params=params, verify=False)  
    return response.content, response.status_code


@app.route("/login", methods=["POST"])
def validate_user():
    username = request.values.get("username")
    password = request.values.get("password")
    params = {'username':username, 'password':password}

    response = requests.post('http://127.0.0.1:3000/login', params=params, verify=False)  
    
    return response.content, response.status_code
