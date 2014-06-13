import unittest

import debris


class Tests(unittest.TestCase):
    def test_single(self):
        debris.banks.memcached.remove('*')
        debris.banks.memcached.set('key1', '1')
        data = debris.banks.memcached.get('key1')
        self.assertEqual(data, '1')

    def test_multi(self):
        debris.banks.memcached.remove('*')
        debris.banks.memcached.set('key2', '2')
        debris.banks.memcached.set('key3', '3')
        data = debris.banks.memcached.get('key2', 'key3')
        self.assertListEqual(data, ['3','2'])

if __name__ == '__main__':
    unittest.main()
