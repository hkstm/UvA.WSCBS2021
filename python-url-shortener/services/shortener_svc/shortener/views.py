import os
from functools import wraps

import jwt
import jwt.exceptions
from flask import jsonify, request

from shortener.app import app
from shortener.kvstore import (
    AlreadyExistsException,
    InMemoryKeyValueStore,
    MissingTokenException,
    NotFoundException,
    PersistentKeyValueStore,
)
from shortener.shortener import InvalidURLException, URLShortener
from shortener.utils.utils import User, REDIS_ADDRESS

secretkey = "verysecret"
storage_backend = (
    PersistentKeyValueStore(
        address="my-release-redis-master.default.svc.cluster.local"
        # clean=os.environ.get("CLEAN_DATABASE") is not None,
    )
    # if os.environ.get("PERSIST")
    # else InMemoryKeyValueStore()
)
shortener = URLShortener(storage_backend)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = User(request)
        token = request.values.get("token")
        try:
            data = jwt.decode(token, secretkey, audience=user.user_id, algorithms="HS256")
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
    user = User(request)

    if url is None or len(url) < 1:
        return "missing url", 400
    try:
        shortener.update(key, url, user_id=user.user_id)
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
    user = User(request)
    try:
        shortener.delete(key, user_id=user.user_id)
    except NotFoundException as e:
        return str(e), 404
    return "", 204


@app.route("/", methods=["GET"])
@token_required
def get_all_entries():
    user = User(request)
    return jsonify(shortener.get_all(user_id=user.user_id)), 200


@app.route("/", methods=["POST"])
@token_required
def add_new_entry():
    user = User(request)
    url = request.values.get("url")
    if url is None or len(url) < 1:
        return "missing url", 400
    try:
        return shortener.add(url, user_id=user.user_id), 201
    except (InvalidURLException, AlreadyExistsException) as e:
        return str(e), 400


@app.route("/", methods=["DELETE"])
@token_required
def delete_all_entries():
    user = User(request)
    url = request.values.get("url")
    shortener.delete_all(user_id=user.user_id)
    return "", 204
