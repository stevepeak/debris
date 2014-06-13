import json
import redis
import unittest
import bmemcached

import debris


class User(object):
    __metaclass__ = debris.Object
    def __init__(self, id, **data):
        self.id = str(id)
        self.name = data['name']
        self.email = data['email']



class Tests(unittest.TestCase):
    data = {
        "1":  {"name": "Elaina Dach", "email": "hane.ebba@wolf.com"},
        "2":  {"name": "Lucas Jaskolski", "email": "chad.cummings@hotmail.com"},
        "3":  {"name": "Ms. Agustin Walter", "email": "johnnie.jast@hotmail.com"},
        "4":  {"name": "Mr. Agustina Ward IV", "email": "guiseppe85@metz.info"},
        "5":  {"name": "Dr. Brock Sanford IV", "email": "hilpert.beryl@langworthryan.com"},
        "6":  {"name": "Itzel Schimmel", "email": "myost@hagenesklein.com"},
        "7":  {"name": "Ms. Desiree Simonis", "email": "liliana23@beer.net"},
        "8":  {"name": "Gabe Kling", "email": "jordyn.lynch@yahoo.com"},
        "9":  {"name": "Raheem Kreiger", "email": "lindgren.tanya@yahoo.com"},
        "10": {"name": "Maximilian Kulas", "email": "tomas45@hotmail.com"}
    }

    @classmethod
    def setupClass(self):
        r = redis.Redis()
        [r.set("User.%d"%uid, json.dumps(self.data[str(uid)])) for uid in xrange(1, 6)]

        m = bmemcached.Client()
        [m.set("User.%d"%uid, json.dumps(self.data[str(uid)])) for uid in xrange(6, 11)]
        
        debris.routes({
            "User": {
                "get": [
                    {
                        "service": "redis"
                    },
                    {
                        "service": "memcached"
                    }
                ]
            }
        })

    def test_single(self):
        for uid in xrange(1, 11):
            u = User(uid)
            self.assertEqual(u.id, str(uid))
            self.assertEqual(u.name, self.data[str(uid)]["name"])
            self.assertEqual(u.email, self.data[str(uid)]["email"])
            self.assertIs(u, User(uid), "not the same id on ram")

    def test_multi(self):
        users = User([1,4,5,7,9])

        for u in users:
            self.assertIsInstance(u, User)
            self.assertIs(u, User(u.id), "not the same id on ram")
            self.assertEqual(u.name, self.data[u.id]["name"])
            self.assertEqual(u.email, self.data[u.id]["email"])


if __name__ == '__main__':
    unittest.main()
