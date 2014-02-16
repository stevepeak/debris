import inspect

import debris
from debris import helpers


class Object(type):
    def __call__(cls, *args, **kwargs):
        """Get any piece of data through a series of locations
        """
        if len(kwargs) > 0:
            obj = cls.__new__(cls, *args, **kwargs)
            obj.__init__(*args, **kwargs)
            # STASH HERE...
            return obj

        _ = getattr(cls, "__debris__", {})

        # Build the collection of initializing variables
        # this will be used for varius callable requests
        _kwargs = {}
        insp = inspect.getargspec(cls.__init__)
        # remove the default "self" and "__debris__" argument
        insp.args.remove('self')
        # set all the arguments provided
        for i, value in enumerate(args):
            _kwargs[insp.args[i]] = value
        # set the defaults
        if insp.defaults:
            for i, value in enumerate(insp.defaults):
                _kwargs.setdefault(insp.args[i*-1], value)

        # bool, can store in memory
        _in_memory = helpers.call(_.get('memory'), cls=cls, **_kwargs)

        # namespace
        namespace = helpers.callattr(cls, _.get('namespace', "__namespace__"), **_kwargs)
        nsv = {"clsname": cls.__name__}
        nsv.update(_kwargs)

        # ------------------
        # Multi Method
        # ------------------
        if type(namespace) is tuple:
            args = list(args)
            namespace, key, _list = namespace
            # arg index of the key
            _i = insp.args.index(key)
            # list of object found in memory
            _got = []
            # list of objects (keys) that need to be found
            _need = []
            # list of objects (namespace) that need to be found
            _need_ns = []
            # foreach requested cache by key
            for n in _list:
                # build this obj namespace
                nsv[key] = n
                ns = namespace % nsv
                # check cache
                if _in_memory:
                    obj = debris.locale.Memory.get(namespace)
                    if obj:
                        # found in cache, next!
                        _got.append(obj)
                        continue
                # not found in cache, NEED to get it.
                _need.append(n)
                _need_ns.append(ns)

            # replace the kwargs [key]
            _kwargs[key] = _need
            # request for the data...
            datas = helpers.callattr(cls, _.get("retreive", "__assemble__"), **_kwargs)
            # copy the original class
            _ocls = cls
            # foreach data -> build object
            for i, data in enumerate(datas):
                # replace the key inside the construction args
                args[_i] = data.pop(key)
                # substiture class w/ known data
                _kwargs.update(data)
                cls = helpers.callattr(_ocls, _.get('substitute', '__substitute__'), **_kwargs) if _.get('substitute', '__substitute__') else _ocls
                # construct the class
                obj = cls.__new__(cls, *args, **data)
                obj.__init__(*args, **data)
                # put in memory
                if _in_memory:
                    debris.locale.Memory.set(_need_ns[i], obj)
                # add to the _got[s]!
                _got.append(obj)

            # return our list of cached objects
            return _got

        # ------------------
        # Single Method
        # ------------------
        else:
            namespace = namespace % nsv
            if _in_memory:
                # check for this namespace
                obj = debris.locale.Memory.get(namespace)
                if obj:
                    return obj

            # get the data via the "retreive" method
            # which is required to be an attribute of the class, or a callable
            data = helpers.callattr(cls, _.get("retreive", "__assemble__"), **_kwargs)

            # substiture class w/ known data
            if _.get('substitute'):
                cls = helpers.callattr(cls, _.get('substitute', '__substitute__'), _kwargs, data)

            obj = cls.__new__(cls, *args, **data)
            obj.__init__(*args, **data)
            if _.get('stash') is not False:
                pile = helpers.callattr(obj, _.get('locale'), **_kwargs)
                if type(pile) is str:
                    pile = getattr(debris, pile)
                if pile:
                    if _.get('stash') is not True:
                        data = helpers.callattr(obj, _.get('stash'))
                    pile.stash(data, namespace)
            if _in_memory:
                debris.locale.Memory.set(namespace, obj)
            return obj
  

        # namespace was not found true therfore
        # construct the object normally, dont stash it.
        obj = cls.__new__(cls, *args, **kwargs)
        obj.__init__(*args, **kwargs)
        return obj