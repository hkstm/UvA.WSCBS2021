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

storage_backend = PersistentKeyValueStore(
    address=os.environ.get("REDIS_ADDRESS", "localhost"),
    db=os.environ.get("REDIS_DATABASE", 3),
    clean=os.environ.get("CLEAN_DATABASE") is not None,
)


authenticator = Authentication(storage_backend)


@app.route("/users", methods=["POST"])
def create_user():
    username = request.values.get("username")
    password = request.values.get("password")
    if username is None or password is None:
        return "username and password must be specified", 400

    try:
        print("adding user %s" % username)
        authenticator.post(username, password)
    except AlreadyExistsException as e:
        return "", 200
    except Exception as e:
        print("unexpected error:", str(e))
        return "error", 500

    return "", 200


@app.route("/users/login", methods=["POST"])
def validate_user():
    username = request.values.get("username")
    password = request.values.get("password")
    if username is None or password is None:
        return "username and password must be specified", 400

    try:
        jwt_token = authenticator.get(username, password)

    except NotFoundException as e:
        return str(e), 403
    except WrongPasswordException as e:
        return str(e), 403
    except Exception as e:
        print("unexpected error:", str(e))
        return "error", 500

    return jsonify(jwt_token), 200
