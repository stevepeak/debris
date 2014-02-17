import unittest
import debris

class Cacheme(object):
    __metaclass__ = debris.Object
    __debris__ = {
        "namespace": "namespace", # default "%(clsname)s.[args[]]"
        "stash": True, # default True, callable? return the data to stash
        "substitute": False, # default False
        "cashier": None, # default None, where to store the data
        "retreive": "_retreive", # classmethods to get data
        "memory": True # default True, use the one in memory if found (F) -or- rebuild a new object (T)
    }
    __example_data = [dict(city="Madison", state="WI")]
    def __init__(self, id, **data):
        self.id = id
        self.data = data

    @classmethod
    def namespace(self, id):
        if type(id) is list:
            return ("element.%(id)s", "id", id)
        else:
            return "element.%(id)s"

    @classmethod
    def _retreive(self, id):
        """
        This would be a database call...
        Likely to return a row of data
        """
        if type(id) is list:
            return [dict(id=0, city="Philly", state="PA"),
                    dict(id=1, city="San Fransisco", state="CA"),
                    dict(id=2, city="Boston", state="MA")]
        else:
            return self.__example_data.pop()


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

    def test_multi(self):
        users = Cacheme([1,2,3])
        self.assertEqual(users[0].id, 0)
        self.assertEqual(users[0].data["city"], "Philly")
        self.assertEqual(users[0].data["state"], "PA")
        self.assertEqual(users[1].id, 1)
        self.assertEqual(users[1].data["city"], "San Fransisco")
        self.assertEqual(users[1].data["state"], "CA")
        self.assertEqual(users[2].id, 2)
        self.assertEqual(users[2].data["city"], "Boston")
        self.assertEqual(users[2].data["state"], "MA")


if __name__ == '__main__':
    unittest.main()
