import os

from flask import Blueprint, app, jsonify, render_template, request

from authentication.app import app
from authentication.authentication import Authentication
from authentication.kvstore import (AlreadyExistsException,
                                    InvalidCredentialsException,
                                    NotFoundException, PersistentKeyValueStore)
from authentication.utils.utils import REDIS_ADDRESS, User

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
    except InvalidCredentialsException as e:
        return str(e), 403
    except Exception as e:
        print("unexpected error:", str(e))
        return "error", 500

    return jwt_token, 200
