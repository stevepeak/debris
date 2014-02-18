try:
    from cPickle import loads, dumps
except ImportError:
    from pickle import loads, dumps


class Asset(object):
    def __init__(self, data, expires=None, tags=None):
        self.data = data
        self.tags = set(tags if type(tags) is list else []) 

    def destory(self, reasons):
        pass

    def stats(self):
        pass

    def dump(self):
        # this will change in the very, very near future
        # to be a small collection of data that includes the
        # cache tags
        return self.data

    @classmethod
    def foreign(self, data):
        return Asset(data)
