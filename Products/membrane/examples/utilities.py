from zope.interface import implements

from OFS.SimpleItem import SimpleItem

from Products.CMFCore.utils import getToolByName

from Products.membrane.interfaces import IUserAdder

class UserAdder(SimpleItem):
    """
    UserAdder utility that knows how to add SimpleMembers.
    """
    implements(IUserAdder)
    
    def addUser(self, login, password):
        """
        Adds a SimpleMember object at the root of the Plone site.
        """
        portal = getToolByName(self, 'portal_url').getPortalObject()
        portal.invokeFactory('SimpleMember', login, password=password,
                             userName=login)
