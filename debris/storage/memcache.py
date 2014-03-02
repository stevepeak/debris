import re
import os
import bmemcached

from debris.asset import Asset


class memcache:
    STOCKPILE = {}
    SETTINGS = {}
    _CASHIER = None

    @classmethod
    def setup(self, servers=None, username=None, password=None):
        if servers is None:
            servers = os.getenv('MEMCACHE_SERVERS', '').split(',')
            username = os.getenv('MEMCACHE_USERNAME')
            password = os.getenv('MEMCACHE_PASSWORD')

        assert type(servers) is list

        self._CASHIER = bmemcached.Client(servers, username, password)

    @classmethod
    def get(self, *keys):
        if len(keys) > 0:
            assets = self._CASHIER.get_multi(keys)
            return [Asset.foreign(data).data for data in assets]

        elif len(keys) == 1:
            return Asset.foreign(self._CASHIER.get(keys[0])).data

    @classmethod
    def set(self, key, data, **kwargs):
        self._CASHIER.set(str(key), Asset(data, **kwargs).dump())

    @classmethod
    def keys(self, search=None):
        if search:
            keys = self.STOCKPILE.keys()
            rc = re.compile(search)
            return [key for key in keys if re.search(rc, key, re.I)]
        else:
            return self.STOCKPILE.keys()

    @classmethod
    def remove(self, key, **reasons):
        if key == '*':
            return self._CASHIER.flush_all()
        elif key in self.STOCKPILE:
            pass
        return False

    @classmethod
    def empty(self, tags, **reasons):
        """Destroy Assets based on the tags
        provide additional `**reasons` to inform
        the assets why they will be destroyed
        """
        pass

    @classmethod
    def stats(self, key=None):
        return self._CASHIER.stats(key)

    @classmethod
    def default(self, **settings):
        self.SETTINGS.update(settings)
