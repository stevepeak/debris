version = VERSION = __version__ = '0.0.2'

from . import cashier
from .object import Object

try:
    import tornado.web
    from .wrappers import tornado
except:
    # no tornado package found...
    pass

def setup():
    """
    # The Golden Rules.
    Establish some standars for all the assets
    passing through Debris. Any asset created will 
    require to pass through these rules.
    """
    pass
