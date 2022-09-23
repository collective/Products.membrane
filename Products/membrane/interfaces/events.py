from zope.interface import Attribute
from zope.interface import Interface


class IMembraneTypeEvent(Interface):
    """
    Base interface for membrane type related events.
    """

    tool = Attribute("Tool")
    portal_type = Attribute("Portal Type")


class IMembraneTypeRegisteredEvent(IMembraneTypeEvent):
    """
    Interface for MembraneTypeRegisteredEvents.
    """


class IMembraneTypeUnregisteredEvent(IMembraneTypeEvent):
    """
    Interface for MembraneTypeUnregisteredEvents.
    """
