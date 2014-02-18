import re

from debris.asset import Asset


class memory:
    SETTINGS = {}
    STOCKPILE = {}

    @classmethod
    def get(self, key):
        return self.STOCKPILE.get(key, Asset(None)).data

    @classmethod
    def set(self, key, data, **kwargs):
        self.STOCKPILE[key] = Asset(data, **kwargs)

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
            self.STOCKPILE = {}
            return None
        elif key in self.STOCKPILE:
            self.STOCKPILE[key].destroy(reasons)
            del self.STOCKPILE[key]
            return True
        return False

    @classmethod
    def empty(self, tags, **reasons):
        """Destroy Assets based on the tags
        provide additional `**reasons` to inform
        the assets why they will be destroyed
        """
        tags = set(tags)
        for key, asset in self.STOCKPILE.items():
            if tags & asset.tags:
                asset.destroy(reasons)
                del self.STOCKPILE[key]

    @classmethod
    def stats(self, key):
        pass

    @classmethod
    def default(self, **settings):
        self.SETTINGS.update(settings)
