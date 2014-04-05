from debris.storage.memory import Memory
from debris.storage.memcache import Memcache


class banks:
    memory = Memory()
    memcache = Memcache()

    @classmethod
    def use(self, name):
        name = name.lower()
        if name == "memory":
            return self.memory
        elif name == "memcache":
            return self.memcache
        else:
            raise TypeError("Requested debris bank does not exist.")
