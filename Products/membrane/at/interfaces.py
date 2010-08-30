"""
Archetypes marker interfaces
----------------------------

The interfaces in this module can be used for Archetypes content
classes. This allows them to use the default implementattions for the
membrane interfaces from Products.membrane.interfaces.user that
are included in membrane.
"""
from zope.interface import Interface

from Products.Archetypes.interfaces import IBaseObject
from Products.Archetypes.interfaces import IReferenceable

from Products.membrane.interfaces import user as user_ifaces


class IUserAuthProvider(IReferenceable):
    """
    Marks the object as a Membrane user authentication provider. Objects must
    also provide or adapt to IUserAuthentication to perform the actual
    authentication.
    """


class IUserAuthentication(Interface):
    """
    Provides authentication against an object. Typically, an IUserAuthProvider
    will either be adaptable to this or provide this interface itself.
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


class IUserRoles(Interface):
    """
    Obtains roles for a given user. Typically, a member object would
    provide this or adapt to this, and also provide one of
    IRolesProvider and IGroupAwareRolesProvider.
    """

    def getRoles():
        """
        Returns a sequence of the user's roles.
        """


class IRolesProvider(Interface):
    """
    Marks the object as a Membrane roles provider using the default
    roles computation mechanism defined in the Roles adapter. Objects
    must also provide or adapt to IUserRoles.
    """


class IGroupAwareRolesProvider(IRolesProvider):
    """
    Marks the object as a Membrane roles provider using the
    group-aware roles computation mechanism defined in the
    GroupAwareRoles adapter.
    """


class IGroupsProvider(IReferenceable,):
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


class IUserChanger(IReferenceable):
    """
    Change the password for a user
    """
    def setPassword(password):
        """change the password for a user"""


class IUserDeleter(IReferenceable):
    """
    delete a user
    """
    def delete(login):
        """delete the user with name login"""
