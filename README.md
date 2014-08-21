# :leaves: Debris [![Build Status](https://secure.travis-ci.org/stevepeak/debris.png)](http://travis-ci.org/stevepeak/debris) [![Version](https://pypip.in/v/debris/badge.png)](https://github.com/stevepeak/debris) [![codecov.io](https://codecov.io/github/stevepeak/debris/coverage.png)](https://codecov.io/github/stevepeak/debris)

### Install
`pip install debris`

### Featuring

1. Distribution network for data
    - retreive data from different sources to distribute retrieval work loads
    - simply: free up sql requests
1. Schema driven cache routing
    - Optimize your applications data gets/puts
1. Reduce bottlenecks from addon services
    - keep data integrity cross many services including `redis`, `mongodb`, `memcached` and more
1. Class instance continuity
    - python classes constructed with the same arguments will not create **new** object but use the one already constructed

# Usage

### :gemini: Same-Same Instances

Traditionally in python these objects would **not** be the exact same on memory. 


```python
import debris

class User(object):
    __metaclass__ = debris.Object
    def __init__(self, id, **data):
        self.name = data['name']

>>> User(1) is User(1)
True # w/out debris this would be False
>>> id(User(1)) == id(User(1))
True
>>> User(1).name = "Steve"
>>> User(1).name
"Steve"
```


### :octopus: Initializing

```python
import debris

debris.config({
    "services": {
        "postgresql": {"url": "postgresql://..."}
    },
    "objects": {
        "User": {
            "get": [
                {
                    "service": "postgresql",
                    "query": "select name, email from users where id=%(id)s limit 1;"
                }
            ]
        }
    }
})

class User(object):
    __metaclass__ = debris.Object
    def __init__(self, id, **data):
        self.id = id
        self.name = data['name']
        self.email = data['email']

>>> User(15).name
"John"
```

Constructing your objects typically is a query to the database. So lets establish this with debris. We configure debris to initiate `postgresql` service so we can **get** our Users from the database. This, at first glance, may look unnecessary and not *fixing* any problem. So lets add some more services to see the full benefits.

> ...
> Need to add more content here.
> ...


#### Rules
1. **No data, no instance** when no data is found the requested object will not initialize and a `LookupError` will be raises.
1. **Same, Same** instances with the same arguments will be considered equivelent
    - the first initialized instance will be returned, therefore **not** initializing a new instance






## :candy: Wrapping Web Requests

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
