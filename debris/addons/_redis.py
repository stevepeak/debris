import redis

from debris.asset import encode
from debris.asset import decode


class Redis(object):
    def __init__(self, config):
        if config.get('url'):
            self.service = redis.Redis(config.get("url"))
        else:
            self.service = redis.Redis()

    def get(self, key):
        return decode(self.service.get(key))

    def getmany(self, keys):
        values = self.service.mget(keys)
        return zip(tuple(keys), tuple(map(decode, values)))

    def set(self, key, data, **kwargs):
        return self.service.set(str(key), encode(data, kwargs))

    def remove(self, *keys):
        if keys[0] == '*':
            self.service.flush_all()
        for key in keys:
            self.service.delete(key)

    def stats(self):
        return self.service.stats()
