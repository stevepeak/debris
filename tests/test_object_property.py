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


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        r = redis.Redis()
        r.hset("Customer.1", "age", 1)
        r.hset("Customer.1", "name", "Joe Smoe")

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

    def _test_name(self):
        u = Customer(1)
        self.assertEqual(u.name, "Joe Smoe")
