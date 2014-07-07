import unittest

import debris


class User:
    __properties__ = {}
    def __init__(self, id):
        self.id = id

    @debris.property
    def name(self, get, set):
        print "\033[92m@name\033[0m", get, set
        return get


class Tests(unittest.TestCase):
    def test_single(self):
        u = User(10)
        self.assertEqual(u.name, "Joe Smoe")
        self.assertEqual(u.name, "Joe Smoe")
        self.assertEqual(u.name, "Joe Smoe")

        u.name = "hello"
