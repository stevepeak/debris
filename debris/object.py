import inspect

import debris


def call(_callable, args, kwargs):
    return _callable(*args, **kwargs) if hasattr(_callable, "__call__") else None

def callattr(cls, attr, args, kwargs):
    if hasattr(attr, '__call___'):
        return attr(args, kwargs)
    elif hasattr(cls, attr):
        return getattr(cls, attr)(args, kwargs)

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
        if None in args:
            namespace = None
        else:
            namespace = call(route.get('namespace'), args, kwargs) if route.get('namespace') \
                        else ".".join(map(str, [cls.__name__] + list(args)))

        # bool, can store in memory
        # _in_memory = route.get('memory', True)

        # ---------------
        # Get from Memory
        # ---------------
        # if _in_memory and namespace:
        # check for this namespace
        try:
            return debris.services.memory.get(namespace)
        except LookupError:
            pass

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
            if namespace:
                debris.services.memory.set(namespace, obj)
            return obj

        elif not namespace:
            raise LookupError("No id/key provided to initialize object "+namespace.replace('.', '(', 1).replace('.', ', ')+")")

        # -----------------
        # Retrieve the Data
        # -----------------
        insp = inspect.getargspec(cls.__init__)
        data = None
        if route.get('get'):
            for r in route['get']:
                if r['service'] == 'postgresql':
                    iwargs = dict([(k, args[i] if len(args) > i else None) for i, k in enumerate(insp.args[1:])])
                    data = r["bank"].get(r['query'], **iwargs)
                else:
                    data = r["bank"].get(namespace)
                if data:
                    break

            # -----------------
            # Retrieve the Data
            # -----------------
            if not data:
                raise LookupError("Data could not be found for "+namespace.replace('.', '(', 1).replace('.', ', ')+")")

        if not data:
            data = {}

        # --------------------
        # Manage Args / Kwargs
        # --------------------
        # remove the default "self" argument
        insp.args.pop(0)
        [data.pop(k) for k in insp.args if k in data]

        # substiture class w/ known data
        if route.get('substitute'):
            cls = callattr(cls, route['substitute'], args, data) or cls

        # ----------------
        # Initialize Class
        # ----------------
        obj = cls.__new__(cls, *args, **data)
        obj.__init__(*args, **data)

        # ---------------
        # Store in Memory
        # ---------------
        if namespace:
            debris.services.memory.set(namespace, obj)

        # return the constructed object
        return obj

    def getmany(cls, route, args, kwargs, _keys):
        """
        1. build name space
        2. look locally for copies
        3. build group for batch
        4. fetch the new ones
        5. return found + new list
        """
        # copy the list of keys
        keys = [] + _keys
        # build a list of returning objects
        returning = []
        # dictionary of references
        namespaces = {} # key: ns
        namespace_keys = {} # ns: key
        
        # shorthand
        returning_append = returning.append
        memory_get = debris.services.memory.get
        memory_set = debris.services.memory.set

        # ---------------
        # Get from Memory
        # ---------------
        for key in keys:
            # ---------
            # Namespace
            # ---------
            namespace = call(route.get('namespace'), args + [key], kwargs) if route.get('namespace') \
                        else ".".join(map(str, [cls.__name__] + args + [key]))
            
            # check for this namespace
            try:
                returning_append(memory_get(namespace))
            except LookupError:
                # not found, add to namespace list
                namespaces[key] = namespace
                namespace_keys[namespace] = key

        if not namespaces:
            # all data found, return the findings
            return returning

        # -----------------
        # Retrieve the Data
        # -----------------
        insp = inspect.getargspec(cls.__init__)
        insp.args.pop(0) # self
        data = None
        for r in route['get']:
            if r['service'] == 'postgresql':
                iwargs = dict([(k, args[i] if len(args) > i else None) for i, k in enumerate(insp.args[:-1])])
                iwargs[insp.args[-1]] = namespaces.keys()
                # create a limit, speed up the query
                iwargs['limit'] = len(namespaces)
                results = r["bank"].getmany(r['query[]'], **iwargs)
                if results:
                    # retrieve the key from the results. hacky way, but works
                    key = insp.args[-1]
                    # pop out the "key" for each row, ex. "id", then switch to the namespace
                    # keys[row.pop('id')] => "user.1"
                    results = [(namespaces[row[key]], row) for row in results]

            else:
                results = r["bank"].getmany(namespaces.values())

            # Results Found
            # -------------
            if results:
                # [(ns, data), ...]
                for namespace, data in results:
                    if data:
                        # substiture class w/ known data
                        # ------------------------------
                        if route.get('substitute'):
                            _cls = callattr(cls, route.get('substitute'), args, data) or cls
                        else:
                            _cls = cls

                        # initialize class
                        # ----------------
                        obj = _cls.__new__(_cls, *args, **data)
                        obj.__init__(*args, **data)

                        # store in memory
                        # ---------------
                        memory_set(namespace, obj)
                        namespaces.pop(namespace_keys.pop(namespace))

                        # add the constructed object
                        # --------------------------
                        returning_append(obj)

        return returning

    def __call__(cls, *args, **kwargs):
        """Get any piece of data through a series of locations
        """
        # -------------------
        # Routes and Settings
        # -------------------
        route = debris.CONFIG.get("objects", {}).get(cls.__name__, {})

        # ---------------
        # Multi Construct
        # ---------------
        if type(args[-1]) in (list, tuple):
            return Object.getmany(cls, route, list(args[:-1]), kwargs, args[-1])

        # -------------
        # Single Method
        # -------------
        return Object.get(cls, route, args, kwargs)
