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
        pass

    @classmethod
    def foreign(self, data):
        pass
