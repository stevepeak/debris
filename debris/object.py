import inspect

import debris

def call(_callable, args, kwargs):
    return _callable(*args, **kwargs) if hasattr(_callable, "__call__") else None


class Object(type):
    def get(cls, route, args, kwargs):
        """
        :cls        (class) <Class> of the object requested
        :route      (dict) Debris route schema
        :args       (list) of argument provided for initializing
        :kwargs     (dict) of given data to construct the object
        """
        # ---------
        # Namespace
        # ---------
        namespace = call(route.get('namespace'), args, kwargs) if route.get('namespace') \
                    else ".".join(map(str, [cls.__name__] + list(args)))

        # bool, can store in memory
        _in_memory = route.get('memory', True)

        # ------------------------
        # Constructed w/ init args
        # ------------------------
        # - this method bypasses many of the debris
        #   features for cacheing because the 
        #   kwargs should contain all the construction information
        # - replaces existing object in memory beceause this data is 
        #   given to be "newer" data
        if len(kwargs) > 0:
            cls = call(route.get('substitute'), args, kwargs) or cls
            obj = cls.__new__(cls, *args, **kwargs)
            obj.__init__(*args, **kwargs)
            if namespace and _in_memory:
                debris.banks.memory.set(namespace, obj)
            return obj

        # ---------------
        # Get from Memory
        # ---------------
        if _in_memory:
            # check for this namespace
            obj = debris.banks.memory.get(namespace)
            if obj:
                # found in memory! return the obj
                return obj

        # -----------------
        # Retrieve the Data
        # -----------------
        insp = inspect.getargspec(cls.__init__)
        data = None
        for r in route['get']:
            if r['service'] == 'postgresql':
                iwargs = dict([(k, args[i] if len(args) > i else None) for i, k in enumerate(insp.args[1:])])
                # iwargs['limit'] = len(args[-1])
                data = r["bank"].get(r['query'], **iwargs)
            else:
                data = r["bank"].get(namespace)
            if data:
                break

        # -----------------
        # Retrieve the Data
        # -----------------
        if not data:
            raise LookupError()

        # --------------------
        # Manage Args / Kwargs
        # --------------------
        # remove the default "self" argument
        insp.args.remove('self') # insp.args.pop(0)
        [data.pop(k) for k in insp.args if k in data]

        # substiture class w/ known data
        cls = call(route.get('substitute'), args, data) or cls

        # ----------------
        # Initialize Class
        # ----------------
        obj = cls.__new__(cls, *args, **data)
        obj.__init__(*args, **data)

        # ---------------
        # Store in Memory
        # ---------------
        if _in_memory:
            debris.banks.memory.set(namespace, obj)

        # return the constructed object
        return obj

    def generater(cls, route, args, kwargs, keys):
        # this method needs to change for getting keys by batch
        for key in keys:
            yield Object.get(cls, route, args + [key], kwargs)

    def __call__(cls, *args, **kwargs):
        """Get any piece of data through a series of locations
        """
        # -------------------
        # Routes and Settings
        # -------------------
        route = debris.ROUTES[cls.__name__]

        # ---------------
        # Multi Construct
        # ---------------
        if type(args[-1]) in (list, tuple):
            return Object.generater(cls, route, list(args[:-1]), kwargs, args[-1])

        # -------------
        # Single Method
        # -------------
        return Object.get(cls, route, args, kwargs)
