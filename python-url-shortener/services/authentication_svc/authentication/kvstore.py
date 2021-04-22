from abc import ABC
from collections import defaultdict
import redis

class KVStoreException(Exception):
    pass


class WrongPasswordException(KVStoreException):
      def __init__(self):
        super().__init__("Wrong password")


class NotFoundException(KVStoreException):
    def __init__(self):
        super().__init__("User name or password invalid")


class AlreadyExistsException(KVStoreException):
    def __init__(self, key):
        super().__init__("Username %s does already exist" % key)


class KeyValueStore(ABC):
    """ Abstract interface of a key value store """

    def set(self, key, value, user_id, exists_ok=False):
        pass

    def get(self, key):
        pass
    

class InMemoryKeyValueStore(KeyValueStore):
    """ In memory key value store """

    def __init__(self):
        self.data = dict()

    def set(self, key, value, exists_ok=False):
        if not exists_ok and key in self.data:
            raise AlreadyExistsException(key)
        self.data[key] = value
        return value

    def get(self, key):
        return self.data.get(key)

class PersistentKeyValueStore(KeyValueStore):
    """ Redis based persistent key value store """

    def __init__(self, address="localhost", db=0, clean=False):
        self.db = redis.Redis(address, db=db)
        if clean:
            print("cleaning the database")
            self.db.flushdb()

    def set(self, key, value, exists_ok=False):
        if not exists_ok and (
            self.db.exists(key) and self.db.get(key).decode("utf8") != value
        ):
            raise AlreadyExistsException(key)
        self.db.set(key, value)
        return value

    def get(self, key):
        value = self.db.get(key)
        if value is not None:
            return value.decode("utf8")
        return None
