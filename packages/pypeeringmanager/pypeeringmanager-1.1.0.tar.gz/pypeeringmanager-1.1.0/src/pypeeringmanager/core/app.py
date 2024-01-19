from pynetbox.core.app import App as PyNetboxApp
from pypeeringmanager.models import peering, net, extras

class App(PyNetboxApp):
    """ Represents apps in Peering-Manager.
    Calls to attributes are returned as Endpoint objects.
    :returns: :py:class:`.Endpoint` matching requested attribute.
    :raises: :py:class:`.RequestError`
        if requested endpoint doesn't exist.
    """

    models = {
        "peering": peering,
        "net": net,
        "extras": extras,
    }
