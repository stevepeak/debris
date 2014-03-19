import unittest

import debris


class Tests(unittest.TestCase):
    def test_single(self):
        debris.storage.memcache.remove('*')
        debris.storage.memcache.set('key1', '1')
        data = debris.storage.memcache.get('key1')
        self.assertEqual(data, '1')

    def test_multi(self):
        debris.storage.memcache.remove('*')
        debris.storage.memcache.set('key2', '2')
        debris.storage.memcache.set('key3', '3')
        data = debris.storage.memcache.get('key2', 'key3')
        self.assertListEqual(data, ['3','2'])

if __name__ == '__main__':
    unittest.main()
