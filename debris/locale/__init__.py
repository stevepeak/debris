from .memory import memory

try:
    import bmemcached
    from .memcache import memcache
except ImportError:
    pass
