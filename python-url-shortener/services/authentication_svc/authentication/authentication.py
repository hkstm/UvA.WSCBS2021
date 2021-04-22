from authentication.kvstore import (
    AlreadyExistsException,
    NotFoundException,
    WrongPasswordException,
)
import jwt

import os

secretkey = "verysecret"


class Authentication:
    def __init__(self, kvstore=None):
        self.kvstore = kvstore

    def get(self, username, password):
        stored = self.kvstore.get(username)
        if stored is not None and stored == password:
            return jwt.encode({"username": username}, secretkey, algorithm="HS256")
        else:
            raise WrongPasswordException()

    def post(self, username, password):
        self.kvstore.set(username, password, exists_ok=False)
