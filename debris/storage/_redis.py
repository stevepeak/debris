from debris.asset import Asset


class Redis(object):
    def __init__(self, url=None):
        try:
            import redis
        except ImportError:
            self._bank = None
        else:
            self._bank = redis.Redis()

    def get(self, key):
        return Asset.foreign(self._bank.get(key)).data

    def getmany(self, keys):
        assets = self._bank.get_multi(keys)
        return [Asset.foreign(assets[key]).data for key in assets]

    def set(self, key, data, **kwargs):
        return self._bank.set(str(key), Asset(data, **kwargs).dump())

    def remove(self, *keys):
        if keys[0] == '*':
            self._bank.flush_all()
        for key in keys:
            self._bank.delete(key)

    def stats(self):
        return self._bank.stats()
