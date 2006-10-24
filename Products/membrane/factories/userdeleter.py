from Products.membrane.interfaces import IUserDeleter
from Products.membrane.interfaces import IMembraneUserDeleter

class UserDeleter(object):
    """
    provide a default adaptation from IUserDeleter to IMembraneUserDeleter
    """
    implements(IMembraneUserDeleter)

    def __init__(self, context):
        self.context = context

    def doDeleteUser(self, login):
        """
        adapt to the IMembraneUserDeleter by setting a password
        """
        IUserDeleter(self.context).delete(login)
