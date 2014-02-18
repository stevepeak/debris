from .memory import memory

try:
    import bmemcached
    from .memcache import memcache
except ImportError:
    pass

def use(name):
    name = name.lower()
    if name == "memory":
        return memory
    elif name == "memcache":
        return memcache
    else:
        raise TypeError("Request debris.storage does not exist.")
