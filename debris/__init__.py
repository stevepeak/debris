version = VERSION = __version__ = '0.0.3'

from debris.object import Object
from debris.storage import banks


def setup():
    """
    # The Golden Rules.
    Establish some standars for all the assets
    passing through Debris. Any asset created will 
    require to pass through these rules.
    """
    pass


ROUTES = {}

def routes(_routes):
    global ROUTES
    ROUTES = _routes
    for cls, route in _routes.iteritems():
        for service in route["get"]:
            service["bank"] = getattr(banks, service["service"])
