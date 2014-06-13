import tornado.web
from tornado.testing import AsyncHTTPTestCase

from debris.tornado import cached


class MainHandler(tornado.web.RequestHandler):
    @cached("homepage")
    def get(self):
        self.application._i +=1
        self.finish(str(self.application._i))


class Tests(AsyncHTTPTestCase):
    def get_app(self):
        app = tornado.web.Application([(r"/", MainHandler)])
        app._i = 0
        return app

    def test(self):
        data = self.fetch("/")
        self.assertEqual(data.body, "1")

        data = self.fetch("/")
        # if this is equal to "2" then it failed...
        self.assertEqual(data.body, "1")

        data = self.fetch("/")
        # if this is equal to "3" then it failed...
        self.assertEqual(data.body, "1")
