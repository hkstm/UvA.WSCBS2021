import os

from flask import jsonify, request

from python_url_shortener.app import app
from python_url_shortener.kvstore import InMemoryKeyValueStore, PersistentKeyValueStore
from python_url_shortener.shortener import URLShortener

storage_backend = (
    PersistentKeyValueStore(
        address=os.environ.get("REDIS_ADDRESS"),
        clean=os.environ.get("CLEAN_DATABASE") is not None,
    )
    if os.environ.get("PERSIST")
    else InMemoryKeyValueStore()
)
shortener = URLShortener(storage_backend)


@app.route("/<key>", methods=["GET"])
def get_entry(key):
    value = shortener.get(key)
    if value is not None:
        return value, 301
    return "", 404


@app.route("/<key>", methods=["PUT"])
def set_entry(key):
    # ... assuming that PUT updates a key value mapping (which needs a parameter that is not in the table)
    value = request.values.get("value")
    if not value or len(value) < 1:
        return "missing value", 400
    try:
        shortener.update(key, value, user_id=request.remote_addr)
    except ValueError as e:
        return str(e), 400
    except KeyError as e:
        return str(e), 404
    return "", 200


@app.route("/<key>", methods=["DELETE"])
def delete_entry(key):
    try:
        shortener.delete(key, user_id=request.remote_addr)
    except KeyError as e:
        return str(e), 404
    return "", 204


@app.route("/", methods=["GET"])
def get_all_entries():
    return jsonify(shortener.get_all(user_id=request.remote_addr)), 200


@app.route("/", methods=["POST"])
def add_new_entry():
    url = request.values.get("url")
    try:
        return shortener.add(url, user_id=request.remote_addr), 201
    except KeyError as e:
        return str(e), 400
    except ValueError as e:
        return str(e), 400


@app.route("/", methods=["DELETE"])
def delete_all_entries():
    shortener.delete_all(user_id=request.remote_addr)
    return "", 204
