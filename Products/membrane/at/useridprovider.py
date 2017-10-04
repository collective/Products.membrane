# -*- coding: utf-8 -*-
from Products.membrane.interfaces.user import IMembraneUserObject
from zope.interface import implementer


@implementer(IMembraneUserObject)
class UserIdProvider(object):
    """
    Adapts from IUserAuthProvider to IMembraneUserObject.  Provides the
    default implementation which simply uses UID.
    """

    def __init__(self, context):
        self.context = context

    def getUserId(self):
        return self.context.UID()

    def getUserName(self):
        return self.context.getUserName()
