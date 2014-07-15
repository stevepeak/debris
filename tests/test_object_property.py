import redis
import unittest

import debris


class Customer(object):
    __properties__ = {}
    def __init__(self, id):
        self.id = id

    @debris.property
    def age(self, get, set):
        if get is not NotImplemented:
            # process the set variable
            return int(get) + 1
        elif set is not NotImplemented:
            # process the set value before it gets scattered to cache
            return set

    @debris.property
    def name(self):
        pass

    email = debris.property("email")


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        r = redis.Redis()
        r.hmset("Customer.1", dict(age=1, name="Joe Smoe", email="joe@smoeworld.com"))

        debris.config({
            "services": {
                "redis": {}
            },
            "objects": {
                "Customer": {
                    "properties": {
                        "age": {
                            "get": [
                                {
                                    "service": "redis",
                                    "method": "hash"
                                }
                            ]
                        },
                        "name": {
                            "get": [
                                {
                                    "service": "redis",
                                    "method": "hash"
                                }
                            ]
                        },
                        "email": {
                            "get": [
                                {
                                    "service": "redis",
                                    "method": "hash"
                                }
                            ]
                        }
                    }
                }
            }
        })

    def test_single(self):
        u = Customer(1)
        self.assertEqual(u.age, 2)
        self.assertEqual(u.age, 2)
        self.assertEqual(u.age, 2)

        u.age = 10
        self.assertEqual(u.age, 10)
        self.assertEqual(u.age, 10)

    def test_name(self):
        u = Customer(1)
        self.assertEqual(u.name, "Joe Smoe")

    def test_email(self):
        u = Customer(1)
        self.assertEqual(u.email, "joe@smoeworld.com")
