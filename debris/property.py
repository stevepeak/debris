import debris


def _property(_f):
    if callable(_f):
        name = _f.func_name
    else:
        name = _f
        _f = None
    assert type(name) is str, "invalid key"

    def setter(self, value):
        try:
            self.__properties__[name] = _f(self, NotImplemented, value) if _f else value
        except TypeError:
            self.__properties__[name] = value

    def getter(self):
        
        if name in self.__properties__:
            return self.__properties__[name]
        else:
            route = debris.CONFIG.get("objects", {})\
                                 .get(self.__class__.__name__, {})\
                                 .get('properties', {})\
                                 .get(name, {})

            value = None
            if route.get('get'):
                for r in route['get']:
                    import redis
                    r = redis.Redis()
                    value = r.hget(".".join([self.__class__.__name__, str(self.id)]), name)
                    # value = debris.services.get(r["bank"]).get(namespace)
                    if value:
                        break
            
            try:
                value = _f(self, value, NotImplemented) if _f else value
            except TypeError:
                pass
            return self.__properties__.setdefault(name, value)

    return property(getter, setter)
