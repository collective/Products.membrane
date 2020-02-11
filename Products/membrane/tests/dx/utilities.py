# -*- coding: utf-8 -*-
from OFS.SimpleItem import SimpleItem
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from Products.membrane.interfaces import IUserAdder
from zope.interface import implementer


@implementer(IUserAdder)
class UserAdder(SimpleItem):
    """
    UserAdder utility that knows how to add SimpleMembers.
    """

    def addUser(self, login, password):
        """
        Adds a Test object at the root of the Plone site.
        """
        portal = getToolByName(self, 'portal_url').getPortalObject()
        _createObjectByType('TestMember', portal, login, password=password,
                            username=login)
