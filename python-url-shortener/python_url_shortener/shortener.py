import hashlib

import validators

from python_url_shortener.kvstore import InMemoryKeyValueStore


def hash_url(url, user_id=None):
    key = (user_id or "") + ":" + url
    return hashlib.md5(key.encode("utf-8")).hexdigest()


def is_valid_url(url):
    return validators.url(url)


class URLShortener:
    def __init__(self, kvstore=None):
        self.kvstore = kvstore or InMemoryKeyValueStore()

    def get(self, key):
        return self.kvstore.get(key)

    def get_all(self, user_id=None):
        return self.kvstore.get_all(user_id=user_id)

    def delete(self, key, user_id=None):
        return self.kvstore.delete(key, user_id=user_id)

    def update(self, key, value, user_id=None):
        return self.kvstore.update(key, value, user_id=user_id)

    def delete_all(self, user_id=None):
        return self.kvstore.delete_all(user_id=user_id)

    def add(self, url, user_id=None):
        if not is_valid_url(url):
            raise ValueError("invalid url: %s" % url)

        # we attempt to use the shortest possible key
        # this is not as efficient as just permuting keys
        # of increasing lengths for keys, but scales well
        # because there is no need for synchronization
        hashed = hash_url(url)
        for length in range(1, len(hashed) + 1):
            key = hashed[:length]
            try:
                self.kvstore.set(key, url, user_id=user_id, exists_ok=False)
                return key
            except KeyError:
                continue
        # Note: this should never be reached
        raise KeyError("key could not be stored")
