from debris.storage._redis import Redis
from debris.storage.memory import Memory
from debris.storage.memcached import Memcached
from debris.storage.postgresql import PostgreSQL


class banks:
    redis = Redis()
    memory = Memory()
    memcached = Memcached()
    postgresql = PostgreSQL()
