import unittest
import tornado.httpclient
import os


class Tests(unittest.TestCase):
    def test(self):
        port = int(os.getenv('PORT', 5000))
        c = tornado.httpclient.HTTPClient()
        data = c.fetch('http://localhost:%d' % port)
        self.assertEqual(data.body, "1")

        c = tornado.httpclient.HTTPClient()
        data = c.fetch('http://localhost:%d' % port)
        # if this is equal to "2" then it failed...
        self.assertEqual(data.body, "1")

        c = tornado.httpclient.HTTPClient()
        data = c.fetch('http://localhost:%d' % port)
        # if this is equal to "3" then it failed...
        self.assertEqual(data.body, "1")


if __name__ == '__main__':
    unittest.main()
