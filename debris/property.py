import debris
import functools



def _property(_f):

    def setter(self, value):
        print "\033[95m@setter\033[0m", self, value
        self.__properties__[_f.__name___] = _f(None, value)

    def getter(self):
        """This method will automatically find the 
        property of this object following the paths 
        of debris config.

        The function is passed the results for post-processing
        the value(s) which will be cached for all future request.
        """
        print "\033[95m@getter\033[0m", self
        name = _f.__name__
        if name in self.__properties__:
            return self.__properties__[name]
        else:
            value = "Joe Smoe"
            value = _f(self, value, None)
            return self.__properties__.setdefault(name, value)

    return property(getter, setter)
