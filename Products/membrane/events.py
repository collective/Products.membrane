# -*- coding: utf-8 -*-
from Products.membrane.interfaces.events import IMembraneTypeRegisteredEvent
from Products.membrane.interfaces.events import IMembraneTypeUnregisteredEvent
from zope.interface import implements


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
