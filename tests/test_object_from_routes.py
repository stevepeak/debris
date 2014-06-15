import os
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
    def setUpClass(self):
        r = redis.Redis()
        r.set("User.3", json.dumps(self.data["3"]))
        r.set("User.6", json.dumps(self.data["6"]))

        m = bmemcached.Client()
        m.set("User.4", json.dumps(self.data["4"]))
        m.set("User.9", json.dumps(self.data["9"]))

        debris.config({
            "services": {
                "redis": {},
                "memcached": {},
                "postgresql": {},
                "memory": {}
            },
            "objects": {
                "User": {
                    "get": [
                        {"service": "redis"},
                        {"service": "memcached"},
                        {
                            "service": "postgresql",
                            "query": "select name, email from users where id=%(id)s limit 1;",
                            "query[]": "select id, name, email from users where id in %(id)s limit %(limit)s;"
                        }
                    ],
                    "put": [
                        {
                            "service": "redis"
                            # "ttl": 3600 # future
                        }
                    ]
                }
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
        ids = [1,4,5,7,9]
        users = User(ids)
        for u in users:
            self.assertIsInstance(u, User)
            self.assertIs(u, User(u.id), "not the same id on ram")
            self.assertIn(int(u.id), ids)
            ids.remove(int(u.id))
            self.assertEqual(u.name, self.data[u.id]["name"])
            self.assertEqual(u.email, self.data[u.id]["email"])

    def test_same_same(self):
        "objects with same arguments will always be the same on ram"
        self.assertIs(User(1), User(1))
        self.assertIsNot(User(1), User(2))
        self.assertIs(User(1), User(1, name="john"))
        self.assertEqual(User(1, name="john", email="").name, "Elaina Dach")
