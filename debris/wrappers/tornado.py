import functools

import debris
from debris import helpers


def _replace_finish(handler, namespace, locale):
    _rp = handler.finish
    def finish(chunk):
        status = handler.get_status()
        # send back the data first
        _rp(chunk)
        # now stash it
        if status == 200:
            locale.set(namespace, chunk)
        handler.finish = _rp
    handler.finish = finish

def request(namespace=None, locale=None):
    """
    Wrapper for tornado requests. Example

    ```
    class MainHandler(tornado.web.RequestHandler):
        @debris.tornado.request("home-page", debris.locale.MEMORY)
        def get(self):
            self.write("Hello, world")

    ```

    """
    def wrapper(_f):
        @functools.wraps(_f)
        def _stash(self, *a, **k):
            _namespace = helpers.call(namespace)
            if _namespace:
                _locale = helpers.call(locale, self, namespace) or debris.locale.Memory
                # this request is cacheable
                if _locale:
                    data = _locale.get(namespace)
                    # return the cache result
                    if data:
                        self.finish(data)
                    else:
                        _replace_finish(self, namespace, _locale)
                        # get the result of this request
                        _f(self, *a, **k)
                    return
            # request is not cacheable
            _f(self, *a, **k)
        return _stash
    return wrapper
