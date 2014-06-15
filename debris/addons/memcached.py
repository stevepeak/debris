import os
import bmemcached

from debris.asset import encode
from debris.asset import decode


class Memcached(object):
    def __init__(self, config=None):
        if not config:
            servers = os.getenv('MEMCACHE_SERVERS', 'localhost:11211').split(',')
            username = os.getenv('MEMCACHE_USERNAME')
            password = os.getenv('MEMCACHE_PASSWORD')
            self.service = bmemcached.Client(servers, username, password)

    def get(self, key):
        return decode(self.service.get(key))

    def getmany(self, keys):
        assets = self.service.get_multi(keys)
        return [(key, decode(assets[key])) for key in assets]

    def set(self, key, data, **kwargs):
        return self.service.set(str(key), encode(data, kwargs))

    def remove(self, *keys):
        if keys[0] == '*':
            self.service.flush_all()
        for key in keys:
            self.service.delete(key)

    def stats(self):
        return self.service.stats()
