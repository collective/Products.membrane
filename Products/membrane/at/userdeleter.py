from zope.interface import implements

from Products.membrane.at.interfaces import IUserDeleter
from Products.membrane.interfaces.user import IMembraneUserDeleter


class UserDeleter(object):
    """
    provide a default adaptation from IUserDeleter to IMembraneUserDeleter
    """
    implements(IMembraneUserDeleter)

    def __init__(self, context):
        self.context = context

    def doDeleteUser(self, login):
        """
        adapt to the IMembraneUserDeleter by calling delete on the IUserDeleter
        """
        IUserDeleter(self.context).delete(login)
