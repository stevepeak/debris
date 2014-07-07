import debris
import functools


def retrieve_property(method, self):
    value = "Joe Smoe"
    return method(self, value)

def _property(_f):
    @property
    @functools.wraps(_f)
    def wrapped(self, *a, **k):
        """This method will automatically find the 
        property of this object following the paths 
        of debris config.

        The function is passed the results for post-processing
        the value(s) which will be cached for all future request.
        """
        print "\033[95m....\033[0m", self, a, k
        name = _f.__name__
        if name in self.__properties__:
            return self.__properties__[name]
        else:
            return self.__properties__.setdefault(name, retrieve_property(_f, self))
        
    return wrapped
