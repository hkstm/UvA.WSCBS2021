import os

import jwt
from passlib.hash import sha256_crypt

from authentication.kvstore import (AlreadyExistsException,
                                    InvalidCredentialsException,
                                    NotFoundException)

secretKey = os.environ.get("SECRET_KEY", "changeme")


class Authentication:
    def __init__(self, kvstore=None):
        self.kvstore = kvstore

    @staticmethod
    def hash_password(pw):
        return sha256_crypt.encrypt(pw)

    @staticmethod
    def valid_password(hashed=None, clear=None):
        if hashed is None or clear is None:
            return False
        return sha256_crypt.verify(clear, hashed)

    def get(self, username, password):
        hashed_password = self.kvstore.get(username)
        if hashed_password is not None and self.valid_password(
            clear=password, hashed=hashed_password
        ):
            return jwt.encode({"username": username}, secretKey, algorithm="HS256")
        else:
            raise InvalidCredentialsException()

    def post(self, username, password):
        self.kvstore.set(username, self.hash_password(password), exists_ok=False)
