from .memory import memory

try:
    import bmemcached
    from .memcache import memcache
except ImportError:
    pass

def use(cashier):
    cashier = cashier.lower()
    if cashier == "memory":
        return memory
    elif cashier == "memcache":
        return memcache
    else:
        raise TypeError("Request debris.cashier does not exist.")
