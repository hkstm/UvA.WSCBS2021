import os

from flask import jsonify, request, render_template, app, Blueprint

from authentication.app import app
from authentication.kvstore import (
    AlreadyExistsException,
    WrongPasswordException,
     NotFoundException,
     PersistentKeyValueStore,
)

from authentication.authentication import Authentication

storage_backend = (
    PersistentKeyValueStore(
        address="127.0.0.1"
       
    ))


authenticator = Authentication(storage_backend)



@app.route("/users", methods=["POST"])
def create_user():
    username = request.values.get("username")
    password = request.values.get("password")
    
    user_id = request.values.get("user_id") or request.remote_addr
    try:
        authenticator.post(username, password, user_id)

    except AlreadyExistsException as e:        
        return str(e), 400

    return "", 200



@app.route("/login", methods=["POST"])
def validate_user():
    username = request.values.get("username")
    password = request.values.get("password")
    user_id = request.values.get("user_id") or request.remote_addr
    try:
        jwt_token = authenticator.get(username, password, user_id)     
       

    except NotFoundException as e:        
        return str(e), 403        
    except WrongPasswordException as e:        
        return str(e), 403
    
    return jsonify(jwt_token), 200 

