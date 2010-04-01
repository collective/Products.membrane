from zope.interface import implements
from Products.membrane.interfaces.user import IMembraneUserObject


class UserIdProvider(object):
    """
    Adapts from IUserAuthProvider to IMembraneUserObject.  Provides the
    default implementation which simply uses UID.
    """
    implements(IMembraneUserObject)

    def __init__(self, context):
        self.context = context

    def getUserId(self):
        return self.context.UID()

    def getUserName(self):
        return self.context.getUserName()
