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
from authentication.utils.utils import User, REDIS_ADDRESS

storage_backend = (
    PersistentKeyValueStore(
        address=REDIS_ADDRESS
    )
)
authenticator = Authentication(storage_backend)

@app.route("/users", methods=["POST"])
def create_user():
    user = User(request)
    try:
        authenticator.post(user.username, user.password, user.user_id)
    except AlreadyExistsException as e:        
        return str(e), 400
    return "Created user", 200

@app.route("/login", methods=["POST"])
def validate_user():
    user = User(request)
    try:
        jwt_token = authenticator.get(user.username, user.password, user.user_id)     
    except NotFoundException as e:        
        return str(e), 403        
    except WrongPasswordException as e:        
        return str(e), 403
    return jsonify(jwt_token), 200 
