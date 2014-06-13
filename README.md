# :recycle: Debris [![Build Status](https://secure.travis-ci.org/stevepeak/debris.png)](http://travis-ci.org/stevepeak/debris) [![Version](https://pypip.in/v/debris/badge.png)](https://github.com/stevepeak/debris) [![Coverage Status](https://coveralls.io/repos/stevepeak/debris/badge.png?branch=master)](https://coveralls.io/r/stevepeak/debris?branch=master)

> Recycling your objects and web requests with ease.

## Install
`pip install debris`

## Usage

### :octopus: Objects

> Cache objects to speed up construction.

```python
import debris

class User(object):
    __metaclass__ = debris.Object
<<<<<<< HEAD
    def __init__(self, id, **data):
        self.id = id
        self.name = data['name']
        self.email = data['email']
=======
    __debris__ = {
        "namespace": "%(clsname)s.%(id)s"
    }
    def __init__(self, id, __debris__=None):
        self.id = id
        self.data = __debris__

    @classmethod
    def __assemble__(self, id):
        # this method should hit the database for the data
        return database.get("select * from users where id=%s;", id)
>>>>>>> FETCH_HEAD
```

Your **User** data is store in a database, at least I hope so. Traditionally, doing a simple
`select name, email from users where id=1;` is perfectly find for reteriving your customers.
Debris can assist in this, but, debris is a distribution system. Your user data can be
cached in many other locations. This can reduce bottlenecks, for example if the database
went down we can still get customer data from memecached, redis, mongodb and others.

**Ok!** Now lets get a user.

```python
>>> user = User(1) # this will construct the user from the database
>>> user.name = "Steve"
```

#### Consistancy

Debris will maintain the continuity of your objects. Heres how:

```python
>>> id(User(1)) == id(User(1))
True
```

Traditionally in python these objects would **not** be the exact same on memory. 
Therefore doing something set data (like in this next example) would fail, but
with debris this is perfectly ok.

```python
>>> User(1).name = "Steve"
>>> User(1).name
"Steve"
```


### :candy: Wrapping Web Requests

> Decorate your web request handlers for quicker request times.

Use [python decorators](https://wiki.python.org/moin/PythonDecorators) to stash your request results. This process can **dramatically** speed up your web server requests by storing the results for later use, instead of rendering them on the fly each request.

**Supported Frameworks**
- [Tornado Web](https://github.com/facebook/tornado)

#### Wrapping [Tornado Web](https://github.com/facebook/tornado)
```python
import tornado.ioloop
import tornado.web
import tornado.httpclient
import time
from debris.tornado import cached

class MainHandler(tornado.web.RequestHandler):
    @cached("homepage")
    def get(self):
        # example request that takes some time()
        time.sleep(5)       
        # finsih with anything: html, json, xml etc.
        self.finish("<html>This is now prebuilt</html>")

application = tornado.web.Application([(r"/", MainHandler)])

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
```

**Cool!** Now run the server via `python server.py` and curl some requests.

```sh
$ curl http://localhost:8888/ -w %{time_total}s
5.110s
$ curl http://localhost:8888/ -w %{time_total}s
0.098s
```
Your second request was cached in memory and was able to return the request results very quickly.

## Roadmap
- Switch to a `Debris` asset class container for all cached data.
    - Set the `expiration`,  `callback` and more preferences
    - Expritation may be based on `eta`, `date` or `size`
- Support for storing the cache results in other databases for data redundancy.
    - Known already as `banks` inc. support for `memcache`, `redis` and `mongodb`
- Create methods to clear the stashed assets through request handlers and system events
- Metrics on cache size, requests and frequency
- **Golden Rules** what all assets will comply with before being cached
