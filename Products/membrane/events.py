from zope.interface import implements

from interfaces import IMembraneTypeRegisteredEvent
from interfaces import IMembraneTypeUnregisteredEvent

class MembraneTypeEvent(object):
    """
    Base class for membrane type related events.
    """
    def __init__(self, tool, portal_type):
        self.tool = tool
        self.portal_type = portal_type

class MembraneTypeRegisteredEvent(MembraneTypeEvent):
    """
    A membrane type has been registered.
    """
    implements(IMembraneTypeRegisteredEvent)

class MembraneTypeUnregisteredEvent(MembraneTypeEvent):
    """
    A membrane type has been registered.
    """
    implements(IMembraneTypeUnregisteredEvent)

