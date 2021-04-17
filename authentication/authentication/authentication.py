from authentication.kvstore import AlreadyExistsException, NotFoundException, WrongPasswordException
import jwt

import os
secretkey = "verysecret"


class Authentication:
    
    def __init__(self, kvstore=None):
        self.kvstore = kvstore

    def get(self, username, password):

        try:
            storedpass = self.kvstore.get(username)
            if storedpass == password:
                token = jwt.encode({'user': username}, secretkey)
                return token
           
            else:
                raise WrongPasswordException()

        except WrongPasswordException as e:
            raise e
        except NotFoundException as e:
            raise e

    def post(self, username, password):

        key = username
        try:
            self.kvstore.set(key, password, exists_ok=False)
        except:
            print("here")
            raise AlreadyExistsException(username)
