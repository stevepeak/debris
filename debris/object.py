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
        insp.args.pop(0)
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

    def getmany(cls, route, args, kwargs, keys):
        """
        1. build name space
        2. look locally for copies
        3. build group for batch
        4. fetch the new ones
        5. return found + new list
        """
        returning = []
        returning_append = returning.append
        namespaces = {} # ns: key
        keys = {} # key: ns
        memory_get = debris.banks.memory.get
        memory_set = debris.banks.memory.set

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
            obj = memory_get(namespace)
            if obj:
                # found in memory! return the obj
                returning_append(obj)
            else:
                keys[key] = namespace
                namespaces[namespace] = key

        # -----------------
        # Retrieve the Data
        # -----------------
        insp = inspect.getargspec(cls.__init__)
        insp.args.pop(0)
        data = None
        for r in route['get']:
            if not namespaces:
                break

            if r['service'] == 'postgresql':
                iwargs = dict([(k, args[i] if len(args) > i else None) for i, k in enumerate(insp.args[:-1])])
                iwargs[insp.args[-1]] = tuple(keys.keys())
                # create a limit, speed up the query
                iwargs['limit'] = len(namespaces)
                results = r["bank"].getmany(r['query[]'], **iwargs)
                if results:
                    # retrieve the key from the results. hacky way, but works
                    key = insp.args[-1]
                    # pop out the "key" for each row, ex. "id", then switch to the namespace
                    # keys[row.pop('id')] => "user.1"
                    results = [(keys[row.pop(key)], row) for row in results]

            else:
                results = r["bank"].getmany(namespaces.values())

            # Results Found
            # -------------
            if results:
                # [(ns, data), ...]
                for namespace, data in results:
                    if data:
                        # clean inline args out
                        # ---------------------
                        [data.pop(k) for k in insp.args if k in data]

                        # substiture class w/ known data
                        # ------------------------------
                        _cls = call(route.get('substitute'), args, data) or cls

                        # initialize class
                        # ----------------
                        _args = args + [namespaces.pop(namespace)]
                        keys.pop(_args[-1])
                        obj = _cls.__new__(_cls, *_args, **data)
                        obj.__init__(*_args, **data)

                        # store in memory
                        # ---------------
                        memory_set(namespace, obj)

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
        route = debris.ROUTES[cls.__name__]

        # ---------------
        # Multi Construct
        # ---------------
        if type(args[-1]) in (list, tuple):
            return Object.getmany(cls, route, list(args[:-1]), kwargs, args[-1])

        # -------------
        # Single Method
        # -------------
        return Object.get(cls, route, args, kwargs)
