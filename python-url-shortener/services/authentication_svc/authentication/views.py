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

storage_backend = PersistentKeyValueStore(
    address=os.environ.get("REDIS_ADDRESS", "localhost"),
    db=os.environ.get("REDIS_DATABASE", 3),
    clean=os.environ.get("CLEAN_DATABASE") is not None,
)

authenticator = Authentication(storage_backend)


@app.route("/health", methods=["GET"])
def health_check():
    return "healthy", 200


@app.route("/users", methods=["POST"])
def create_user():
    user = User(request)
    if user.username is None or user.password is None:
        return "username and password must be specified", 400
    try:
        print("adding user %s" % user.username)
        authenticator.post(user.username, user.password)
    except AlreadyExistsException as e:
        return "", 200
    except Exception as e:
        print("unexpected error:", str(e))
        return "error", 500
    return "created user", 200


@app.route("/users/login", methods=["POST"])
def validate_user():
    user = User(request)
    try:
        jwt_token = authenticator.get(user.username, user.password)
    except NotFoundException as e:
        return str(e), 403
    except WrongPasswordException as e:
        return str(e), 403
    except Exception as e:
        print("unexpected error:", str(e))
        return "error", 500

    return jsonify(jwt_token), 200
