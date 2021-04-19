import os
from functools import wraps
from flask import jsonify, request
import jwt

import jwt.exceptions
from python_url_shortener.app import app
from python_url_shortener.kvstore import (
    AlreadyExistsException,
    InMemoryKeyValueStore,
    NotFoundException,
    PersistentKeyValueStore,
    MissingTokenException

)
from python_url_shortener.shortener import InvalidURLException, URLShortener
secretkey = "verysecret"
storage_backend = (
    PersistentKeyValueStore(
        address="localhost"
        # clean=os.environ.get("CLEAN_DATABASE") is not None,
    )
    # if os.environ.get("PERSIST")
    # else InMemoryKeyValueStore()
)
shortener = URLShortener(storage_backend)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        token = request.values.get('token')  
        print(token)
        

        try:
            data = jwt.decode(token, secretkey, algorithms="HS256")          
            print(data)
        
        except jwt.DecodeError:
            return "DecodeError", 403

        except jwt.InvalidTokenError:
            return "Forbidden", 403

      
        return f(*args, **kwargs)
        
    return decorated




@app.route("/<key>", methods=["GET"])
def get_entry(key):
    value = shortener.get(key)
    if value is not None:
        return value, 301
    return "", 404


@app.route("/<key>", methods=["PUT"])
@token_required
def set_entry(key):
    # NOTE: We assume that the PUT call is supposed to update the value for a key
    # This needs a parameter that is not in the table
    url = request.values.get("url")
    user_id = request.values.get("user_id") or request.remote_addr
    if url is None or len(url) < 1:
        return "missing url", 400
    try:
        shortener.update(key, url, user_id=user_id)
    except NotFoundException as e:
        return str(e), 404
    except InvalidURLException as e:
        return str(e), 400
    except AlreadyExistsException as e:
        return str(e), 400
    except MissingTokenException as e:
        return str(e), 403


    return "", 200




@app.route("/<key>", methods=["DELETE"])
@token_required
def delete_entry(key):
    user_id = request.values.get("user_id") or request.remote_addr
    try:
        shortener.delete(key, user_id=user_id)
    except NotFoundException as e:
        return str(e), 404
    return "", 204


@app.route("/", methods=["GET"])
@token_required
def get_all_entries():
    user_id = request.values.get("user_id") or request.remote_addr
    return jsonify(shortener.get_all(user_id=user_id)), 200


@app.route("/", methods=["POST"])
@token_required
def add_new_entry():
    user_id = request.values.get("user_id") or request.remote_addr
    url = request.values.get("url")
    if url is None or len(url) < 1:
        return "missing url", 400
    try:
        return shortener.add(url, user_id=user_id), 201
    except (InvalidURLException, AlreadyExistsException) as e:
        return str(e), 400


@app.route("/", methods=["DELETE"])
@token_required
def delete_all_entries():
    user_id = request.values.get("user_id") or request.remote_addr
    url = request.values.get("url")
    shortener.delete_all(user_id=user_id)
    return "", 204
