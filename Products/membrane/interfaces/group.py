""" 
Group interface
"""
try:
    from zope.interface import Interface
except ImportError:
    from Interface import Interface

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
