import debris


def _property(_f):

    def setter(self, value):
        try:
            self.__properties__[_f.func_name] = _f(self, NotImplemented, value)
        except TypeError:
            self.__properties__[_f.func_name] = value

    def getter(self):
        if _f.func_name in self.__properties__:
            return self.__properties__[_f.func_name]
        else:
            route = debris.CONFIG.get("objects", {})\
                                 .get(self.__class__.__name__, {})\
                                 .get('properties', {})\
                                 .get(_f.func_name, {})
            value = None
            if route.get('get'):
                for r in route['get']:
                    import redis
                    r = redis.Redis()
                    value = r.hget(".".join([self.__class__.__name__, str(self.id)]), _f.func_name)
                    # value = debris.services.get(r["bank"]).get(namespace)
                    if value:
                        break
            
            try:
                value = _f(self, value, NotImplemented)
            except TypeError:
                pass
            return self.__properties__.setdefault(_f.func_name, value)

    return property(getter, setter)
