from debris.storage._redis import Redis
from debris.storage.memory import Memory
from debris.storage.memcached import Memcached


class banks:
    redis = Redis()
    memory = Memory()
    memcached = Memcached()
