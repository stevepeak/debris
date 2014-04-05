version = VERSION = __version__ = '0.0.3'

from debris.object import Object
from debris.storage import banks

try:
    import tornado.web
    from debris.wrappers import tornado
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
