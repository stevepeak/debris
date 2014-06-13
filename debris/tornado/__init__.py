import functools

import debris


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

def cached(namespace=None, bank=debris.banks.memory, debug=False):
    """
    Wrapper for tornado requests. Example

    ```
    class MainHandler(tornado.web.RequestHandler):
        @debris.tornado.cached("home-page", bank=debris.banks.memory)
        def get(self):
            self.write("Hello, world")

    ```

    """
    def wrapper(_f):
        @functools.wraps(_f)
        def _stash(self, *a, **k):
            if debug is False:
                # this request is cacheable
                data = bank.get(namespace)
                # return the cache result
                if data:
                    self.finish(data)
                else:
                    _replace_finish(self, namespace, bank)
                    # get the result of this request
                    _f(self, *a, **k)
                return
            # request is not cacheable
            _f(self, *a, **k)
        return _stash
    return wrapper
