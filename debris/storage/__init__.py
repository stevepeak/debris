from debris.storage.memory import Memory
from debris.storage.memcache import Memcache


class storage:
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
            raise TypeError("Request debris.storage does not exist.")
