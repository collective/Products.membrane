""" 
Group interface
"""

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

class IGroupAvail(Interface):
    """A membrane content object that provides or can be adapted to
    IGroup"""

IGroupAvail.setTaggedValue('interface', IGroup)
