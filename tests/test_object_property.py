import unittest

import debris


class User:
    __properties__ = {}
    def __init__(self, id):
        self.id = id

    @debris.property
    def name(self, value):
        print "\033[92m....\033[0m", 'post processing'
        return value


class Tests(unittest.TestCase):
    def test_single(self):
        u = User(10)
        self.assertEqual(u.name, "Joe Smoe")
        self.assertEqual(u.name, "Joe Smoe")
        self.assertEqual(u.name, "Joe Smoe")

        u.name = "hello"
