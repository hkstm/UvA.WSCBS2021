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
        address="localhost"
       
    ))


authenticator = Authentication(storage_backend)



@app.route("/users", methods=["POST"])
def create_user():
    username = request.values.get("username")
    password = request.values.get("password")

    try:
        authenticator.post(username, password)

    except AlreadyExistsException as e:        
        return str(e), 400

    return "", 200



@app.route("/login", methods=["POST"])
def validate_user():
    username = request.values.get("username")
    password = request.values.get("password")

    try:
        jwt_token = authenticator.get(username, password)     
       

    except NotFoundException as e:        
        return str(e), 403        
    except WrongPasswordException as e:        
        return str(e), 403
    
    return jsonify(jwt_token), 200 

