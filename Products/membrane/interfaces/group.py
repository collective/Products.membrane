# -*- coding: utf-8 -*-
"""
Group interface
"""

from Products.PlonePAS.interfaces.plugins import IMutablePropertiesPlugin
from Products.PluggableAuthService.interfaces.plugins import IGroupsPlugin
from zope.interface import Interface


class IGroup(Interface):

    def getGroupId():
        """
        return the group id
        """

    def Title():
        """
        return the title
        """

    def getGroupMembers():
        """
        return the members of the given group
        """

    def getRoles():
        """
        return the roles that group members should gain
        """


class IMembraneGroupProperties(IGroup, IMutablePropertiesPlugin):
    """
    Used for objects that can provide group properties.
    """


class IMembraneGroupGroups(IGroup, IGroupsPlugin):
    """
    Used for objects that can provide group groups.
    So: groups that belong to groups.
    """
