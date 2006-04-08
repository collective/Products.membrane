"""
Marker interfaces used for specifying alternate PAS plug-in
adapters.
"""
from zope.interface import Interface

from Products.Archetypes.interfaces import IBaseObject
from Products.Archetypes.interfaces import IReferenceable

class IUserAuthProvider(IReferenceable):
    """
    Extends IReferenceable to include add'l authentication related methods.
    """
    def getUserName():
        """
        Return the name used for login.
        """

    def verifyCredentials(credentials):
        """
        Returns True is password is authenticated, False if not.
        """

class IPropertiesProvider(IReferenceable, IBaseObject):
    """
    Marks the object as a Membrane properties provider using the
    default properties computation mechanism defined in the Properties
    adapter (i.e. 'user_property' attribute on the schema fields).
    """

class ISchemataPropertiesProvider(IReferenceable, IBaseObject):
    """
    Marks the object as a Membrane properties provider using the
    SchemataProperties adapter instead of the default Properties
    adapter when adapting to IPropertiesPlugin.
    """
    def getUserPropertySchemata():
        """
        Returns a sequence of schemata names to be used for determining
        user properties.
        """

class IRolesProvider(Interface):
    """
    Marks the object as a Membrane roles provider using the default
    roles computation mechanism defined in the Roles adapter.
    """
    def getRoles():
        """
        Returns a sequence of the user's roles.
        """

class IGroupAwareRolesProvider(IRolesProvider):
    """
    Marks the object as a Membrane roles provider using the
    group-aware roles computation mechanism defined in the
    GroupAwareRoles adapter.
    """

class IGroupsProvider(IReferenceable):
    """
    Marks the object as a Membrane groups provider using the default
    group computation mechanism defined in the Groups adapter.
    """
    
class ISelectedGroupsProvider(IReferenceable):
    """
    Use SelectedGroups adapter instead of the default Groups
    adapter when adapting to IGroupsPlugin.
    """
    def getGroupRelationships():
        """
        Return a sequence of strings that are the relationship names
        to use when looking up the group references.
        """
