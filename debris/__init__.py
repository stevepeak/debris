version = VERSION = __version__ = '0.0.2'

from . import locale
from .object import Object

try:
    import tornado.web
    from .wrappers import tornado
except:
    # no tornado package found...
    pass
