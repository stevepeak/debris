import tornado.ioloop
import tornado.web
import tornado.httpclient

import os

import debris

class MainHandler(tornado.web.RequestHandler):
    @debris.tornado.stash("home-page")
    def get(self):
        self.application._i +=1
        self.finish(str(self.application._i))

application = tornado.web.Application([(r"/", MainHandler)])
application._i = 0

if __name__ == '__main__':
    application.listen(int(os.getenv('PORT', 5000)))
    tornado.ioloop.IOLoop.instance().start()
