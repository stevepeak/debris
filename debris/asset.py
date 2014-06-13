try:
    from cPickle import loads, dumps
except ImportError:
    from pickle import loads, dumps

from json import loads as json_decode
from json import dumps as json_encode


class Asset(object):
    def __init__(self, data, expires=None, tags=None):
        if type(data) is str and data[0] in ('[', '{'):
            self.data = json_decode(data)
        else:
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
