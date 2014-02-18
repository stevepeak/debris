import unittest
import debris

DATABASE = [dict(city="Madison", state="WI")]

class Cacheme(object, metaclass=debris.Object):
    __debris__ = {
        "namespace": "%(clsname)s.%(id)s", # default "%(clsname)s.[args[]]"
        "stash": True, # default True, callable? return the data to stash
        "substitute": False, # default False
        "storage": None, # default None, where to store the data
        "retreive": "_retreive", # classmethods to get data
        "memory": True # default True, use the one in memory if found (F) -or- rebuild a new object (T)
    }
    def __init__(self, id, **data):
        self.id = id
        self.data = data

    @classmethod
    def _retreive(self, id):
        """
        This would be a database call...
        Likely to return a row of data
        """
        global DATABASE
        return DATABASE.pop()


class Tests(unittest.TestCase):
    def test_single(self):
        obj = Cacheme(10)
        self.assertEqual(obj.id, 10)
        self.assertEqual(obj.data['city'], "Madison")
        self.assertEqual(obj.data['state'], "WI")

        new_obj = Cacheme(10)
        self.assertEqual(new_obj.data['city'], "Madison")
        self.assertEqual(new_obj.data['state'], "WI")

        # same object
        self.assertEqual(id(obj), id(new_obj))


if __name__ == '__main__':
    unittest.main()
