from zope.interface import implements

from Products.membrane.at.interfaces import IUserChanger
from Products.membrane.interfaces.user import IMembraneUserChanger


class UserChanger(object):
    """
    provide a default adaptation from IUserChanger to IMembraneUserChanger
    """
    implements(IMembraneUserChanger)

    def __init__(self, context):
        self.context = context

    def doChangeUser(self, login, password, **kwargs):
        """
        adapt to the IMembraneUserChanger by setting a password
        """
        IUserChanger(self.context).setPassword(password)
