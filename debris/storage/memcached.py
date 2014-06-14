import os

from debris.asset import encode
from debris.asset import decode


class Memcached(object):
    def __init__(self, servers=None, username=None, password=None):
        try:
            import bmemcached
        except ImportError:
            self._bank = None
        else:
            if servers is None:
                servers = os.getenv('MEMCACHE_SERVERS', 'localhost:11211').split(',')
                username = os.getenv('MEMCACHE_USERNAME')
                password = os.getenv('MEMCACHE_PASSWORD')

            assert type(servers) is list

            self._bank = bmemcached.Client(servers, username, password)

    def get(self, key):
        return decode(self._bank.get(key))

    def getmany(self, keys):
        assets = self._bank.get_multi(keys)
        return [(key, decode(assets[key])) for key in assets]

    def set(self, key, data, **kwargs):
        return self._bank.set(str(key), encode(data, kwargs))

    def remove(self, *keys):
        if keys[0] == '*':
            self._bank.flush_all()
        for key in keys:
            self._bank.delete(key)

    def stats(self):
        return self._bank.stats()
