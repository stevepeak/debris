version = VERSION = __version__ = '0.0.2'

from debris.object import Object
from debris.addons.memory import Memory
from .property import _property as property


class services:
    # set by default, ok to replace
    memory = Memory()

CONFIG = {}

def config(settings):
    global CONFIG
    CONFIG = settings

    services.memory = Memory(settings["services"].get("memory", None))

    if 'memcached' in settings['services']:
        from debris.addons.memcached import Memcached
        services.memcached = Memcached(settings["services"]["memcached"])

    if 'redis' in settings['services']:
        from debris.addons._redis import Redis
        services.redis = Redis(settings["services"]["redis"])

    if 'postgresql' in settings["services"]:
        from debris.addons.postgresql import PostgreSQL
        services.postgresql = PostgreSQL(settings["services"]["postgresql"])
    
    # Manage Routes
    for cls, obj in settings.get('objects', {}).iteritems():
        for service in obj.get("get", []):
            service["bank"] = getattr(services, service["service"])
