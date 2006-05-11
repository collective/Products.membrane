from zope.interface import implements

from Products.membrane.interfaces import IUserRelated

class UserIdProvider(object):
    """
    Adapts from IUserAuthProvider to IUserRelated.  Provides the
    default implementation which simply uses UID.
    """
    implements(IUserRelated)

    def __init__(self, context):
        self.context = context

    def getUserId(self):
        return self.context.UID()
