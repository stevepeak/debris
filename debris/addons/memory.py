import re

from debris.asset import encode
from debris.asset import decode


class Memory(object):
    def __init__(self, config=None):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key, None)

    def set(self, key, data):
        self.cache[key] = data

    def keys(self, search=None):
        if search:
            keys = self.cache.keys()
            rc = re.compile(search)
            return [key for key in keys if re.search(rc, key, re.I)]
        else:
            return self.cache.keys()

    def remove(self, key, **reasons):
        if key == '*':
            self.cache = {}
            return None
        elif key in self.cache:
            self.cache[key].destroy(reasons)
            del self.cache[key]
            return True
        return False

    def empty(self, tags, **reasons):
        """Destroy Assets based on the tags
        provide additional `**reasons` to inform
        the assets why they will be destroyed
        """
        tags = set(tags)
        for key, asset in self.cache.items():
            if tags & asset.tags:
                asset.destroy(reasons)
                del self.cache[key]
