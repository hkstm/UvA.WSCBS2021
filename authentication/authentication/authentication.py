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
            print(storedpass)
            if storedpass == password:
                token = jwt.encode({'user': username}, secretkey, algorithm="HS256")
                return token
           
            else:
                raise WrongPasswordException()

        except WrongPasswordException as e:
            raise e
        except NotFoundException as e:
            raise e
        except Exception:
            print("somtheing else is wrong")

    def post(self, username, password, user_id):

        
        try:
            
            self.kvstore.set(username, password, user_id, exists_ok=False)
            return username
        except Exception as e:
            print(e)
            #raise AlreadyExistsException(username)
