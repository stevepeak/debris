import unittest

import debris


class Tests(unittest.TestCase):
    def setUp(self):
        debris.banks.memcached.remove('*')

    def test_single(self):
        debris.banks.memcached.set('key1', '1')
        data = debris.banks.memcached.get('key1')
        self.assertEqual(data, '1')

    def test_multi(self):
        debris.banks.memcached.set('key2', '2')
        debris.banks.memcached.set('key3', '3')
        data = debris.banks.memcached.getmany(('key2', 'key3'))
        self.assertItemsEqual(data, [('key3', '3'), ('key2', '2')])
