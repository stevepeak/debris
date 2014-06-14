import re

from debris.asset import encode
from debris.asset import decode



class Memory(object):
    def __init__(self):
        self._bank = {}

    def get(self, key):
        return self._bank.get(key, None)

    def set(self, key, data):
        self._bank[key] = data

    def keys(self, search=None):
        if search:
            keys = self._bank.keys()
            rc = re.compile(search)
            return [key for key in keys if re.search(rc, key, re.I)]
        else:
            return self._bank.keys()

    def remove(self, key, **reasons):
        if key == '*':
            self._bank = {}
            return None
        elif key in self._bank:
            self._bank[key].destroy(reasons)
            del self._bank[key]
            return True
        return False

    def empty(self, tags, **reasons):
        """Destroy Assets based on the tags
        provide additional `**reasons` to inform
        the assets why they will be destroyed
        """
        tags = set(tags)
        for key, asset in self._bank.items():
            if tags & asset.tags:
                asset.destroy(reasons)
                del self._bank[key]
