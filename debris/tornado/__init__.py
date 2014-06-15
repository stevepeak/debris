import functools

import debris


def _replace_finish(handler, namespace, service):
    _rp = handler.finish
    def finish(chunk):
        status = handler.get_status()
        # send back the data first
        _rp(chunk)
        # now stash it
        if status == 200:
            service.set(namespace, chunk)
        handler.finish = _rp
    handler.finish = finish

def cached(namespace=None, service="memory", debug=False):
    """
    Wrapper for tornado requests. Example

    ```
    class MainHandler(tornado.web.RequestHandler):
        @debris.tornado.cached("home-page")
        def get(self):
            self.write("Hello, world")

    ```

    """
    _service = getattr(debris.services, service)
    def wrapper(_f):
        @functools.wraps(_f)
        def _stash(self, *a, **k):
            if debug is False:
                # this request is cacheable
                print "\033[92m....\033[0m", _service, dir(_service)
                data = _service.get(namespace)
                # return the cache result
                if data:
                    self.finish(data)
                else:
                    _replace_finish(self, namespace, _service)
                    # get the result of this request
                    _f(self, *a, **k)
                return
            # request is not cacheable
            _f(self, *a, **k)
        return _stash
    return wrapper
