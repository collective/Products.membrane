# -*- coding: utf-8 -*-
from Products.membrane.interfaces.events import IMembraneTypeRegisteredEvent
from Products.membrane.interfaces.events import IMembraneTypeUnregisteredEvent
from zope.interface import implementer


class MembraneTypeEvent(object):
    """
    Base class for membrane type related events.
    """

    def __init__(self, tool, portal_type):
        self.tool = tool
        self.portal_type = portal_type


@implementer(IMembraneTypeRegisteredEvent)
class MembraneTypeRegisteredEvent(MembraneTypeEvent):
    """
    A membrane type has been registered.
    """


@implementer(IMembraneTypeUnregisteredEvent)
class MembraneTypeUnregisteredEvent(MembraneTypeEvent):
    """
    A membrane type has been registered.
    """
