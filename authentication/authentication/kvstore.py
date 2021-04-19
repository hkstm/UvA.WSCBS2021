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

    def get_all(self, user_id):
        pass

    def update(self, key, value, user_id):
        pass

    def delete(self, key, user_id):
        pass

    def delete_all(self, user_id):
        pass


class InMemoryKeyValueStore(KeyValueStore):
    """ In memory key value store """

    def __init__(self):
        self.data = dict()
        self.users = defaultdict(set)

    def _check_has_permission(self, key, user_id):
        return key in self.users[user_id]

    def set(self, key, value, user_id, exists_ok=False):
        if not exists_ok and (key in self.data and not self.data[key] != value):
            raise AlreadyExistsException(key)
        self.users[user_id].add(key)
        self.data[key] = value
        return value

    def get(self, key):
        return self.data.get(key)

    def get_all(self, user_id):
        return sorted(list(self.users[user_id]))

    def update(self, key, value, user_id):
        if not self._check_has_permission(key, user_id):
            raise NotFoundException()
        self.data[key] = value

    def delete(self, key, user_id):
        if key not in self.users[user_id]:
            raise NotFoundException()
        self.users[user_id].remove(key)
        return self.data.pop(key)

    def delete_all(self, user_id):
        for key in self.users[user_id]:
            self.data.pop(key)
        self.users[user_id] = set()


class PersistentKeyValueStore(KeyValueStore):
    """ Redis based persistent key value store """

    def __init__(self, address="127.0.0.1", clean=False):
        self.db = redis.Redis(address, db=3)
        self.users = redis.Redis(address, db=4)
        if clean:
            print("cleaning the database")
            self.db.flushdb()
            self.users.flushdb()

    def set(self, key, value, user_id, exists_ok):
        if not exists_ok and (
            self.db.exists(key) and self.db.get(key).decode("utf8") != value
        ):
            raise AlreadyExistsException(key)
        self.users.sadd(user_id, key)
        return self.db.set(key, value)

    def get(self, key):
        value = self.db.get(key)
        if value is not None:
            return value.decode("utf8")
        return None

    def get_all(self, user_id):
        return sorted(
            [mem.decode("utf8") for mem in list(self.users.smembers(user_id))]
        )

    # def _check_has_permission(self, key, user_id):
    #     return self.users.sismember(user_id, key)

    # def delete(self, key, user_id):
    #     if not self._check_has_permission(key, user_id):
    #         raise NotFoundException()
    #     self.users.srem(user_id, key)
    #     return self.db.delete(key)

    # def update(self, key, value, user_id):
    #     if not self._check_has_permission(key, user_id):
    #         raise NotFoundException()
    #     return self.db.set(key, value)

    # def delete_all(self, user_id):
    #     for key in self.users.sscan_iter(user_id, match="*"):
    #         self.db.delete(key)
    #     self.users.delete(user_id)
