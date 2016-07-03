"""
Group interface
"""

from Products.PlonePAS.interfaces.plugins import IMutablePropertiesPlugin
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
