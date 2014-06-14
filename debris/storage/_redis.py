from debris.asset import encode
from debris.asset import decode


class Redis(object):
    def __init__(self, url=None):
        try:
            import redis
        except ImportError:
            self._bank = None
        else:
            self._bank = redis.Redis()

    def get(self, key):
        return decode(self._bank.get(key))

    def getmany(self, keys):
        values = self._bank.mget(keys)
        return zip(tuple(keys), tuple(map(decode, values)))

    def set(self, key, data, **kwargs):
        return self._bank.set(str(key), encode(data, kwargs))

    def remove(self, *keys):
        if keys[0] == '*':
            self._bank.flush_all()
        for key in keys:
            self._bank.delete(key)

    def stats(self):
        return self._bank.stats()
