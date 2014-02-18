from .memory import memory

try:
    import bmemcached
    from .memcache import memcache
except ImportError:
    memcache = None

class storage:
    memory = memory
    memcache = memcache
    @classmethod
    def use(self, name):
        name = name.lower()
        if name == "memory":
            return memory
        elif name == "memcache":
            return memcache
        else:
            raise TypeError("Request debris.storage does not exist.")
