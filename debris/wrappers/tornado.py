import functools

import debris
from debris import helpers


def _replace_finish(handler, namespace, cashier):
    _rp = handler.finish
    def finish(chunk):
        status = handler.get_status()
        # send back the data first
        _rp(chunk)
        # now stash it
        if status == 200:
            cashier.set(namespace, chunk)
        handler.finish = _rp
    handler.finish = finish

def request(namespace=None, cashier=None):
    """
    Wrapper for tornado requests. Example

    ```
    class MainHandler(tornado.web.RequestHandler):
        @debris.tornado.request("home-page", cashier=debris.cashier.memory)
        def get(self):
            self.write("Hello, world")

    ```

    """
    def wrapper(_f):
        @functools.wraps(_f)
        def _stash(self, *a, **k):
            _namespace = helpers.call(namespace)
            if _namespace:
                _cashier = helpers.call(cashier, self, namespace) or debris.cashier.memory
                # this request is cacheable
                if _cashier:
                    data = _cashier.get(namespace)
                    # return the cache result
                    if data:
                        self.finish(data)
                    else:
                        _replace_finish(self, namespace, _cashier)
                        # get the result of this request
                        _f(self, *a, **k)
                    return
            # request is not cacheable
            _f(self, *a, **k)
        return _stash
    return wrapper
