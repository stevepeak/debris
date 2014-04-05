import functools

import debris
from debris import helpers


def _replace_finish(handler, namespace, bank):
    _rp = handler.finish
    def finish(chunk):
        status = handler.get_status()
        # send back the data first
        _rp(chunk)
        # now stash it
        if status == 200:
            bank.set(namespace, chunk)
        handler.finish = _rp
    handler.finish = finish

def request(namespace=None, bank=None, debug=False):
    """
    Wrapper for tornado requests. Example

    ```
    class MainHandler(tornado.web.RequestHandler):
        @debris.tornado.request("home-page", bank=debris.banks.memory)
        def get(self):
            self.write("Hello, world")

    ```

    """
    def wrapper(_f):
        @functools.wraps(_f)
        def _stash(self, *a, **k):
            if debug is False:
                # easy way to skip the stash
                _namespace = helpers.call(namespace)
                if _namespace:
                    _storage = helpers.call(bank, self, namespace) or debris.banks.memory
                    # this request is cacheable
                    if _storage:
                        data = _storage.get(namespace)
                        # return the cache result
                        if data:
                            self.finish(data)
                        else:
                            _replace_finish(self, namespace, _storage)
                            # get the result of this request
                            _f(self, *a, **k)
                        return
            # request is not cacheable
            _f(self, *a, **k)
        return _stash
    return wrapper
