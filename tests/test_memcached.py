import unittest

import debris


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        debris.config({
            "services": {
                "memcached": {}
            }
        })
    
    def setUp(self):
        debris.services.memcached.remove('*')

    def test_single(self):
        debris.services.memcached.set('key1', '1')
        data = debris.services.memcached.get('key1')
        self.assertEqual(data, '1')

    def test_multi(self):
        debris.services.memcached.set('key2', '2')
        debris.services.memcached.set('key3', '3')
        data = debris.services.memcached.getmany(('key2', 'key3'))
        self.assertItemsEqual(data, [('key3', '3'), ('key2', '2')])
