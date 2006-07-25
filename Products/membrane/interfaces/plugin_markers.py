"""
Marker interfaces used for specifying alternate PAS plug-in
adapters.
"""
from zope.interface import Interface

from Products.Archetypes.interfaces import IBaseObject
from Products.Archetypes.interfaces import IReferenceable

# XXX [optilude] - Ideally, we'd like to make it possible to write
# AT objects that don't implement anything beyond what AT requires, using
# adapters for any membrane-specific functionality. 
# 
# However, the object_implements index and various adapter lookups assume that 
# we are "one step" away from the basic content object. For example, 
# IMembraneUserAuth is used extensively, and is registered as an adapter
# from IUserAuthProvider. To function, therefore, the member object must
# directly implement IUserAuthProvider (and its two methods). 
#
# A better pattern would be to only assume marker interfaces for the object. 
# For example, IAuthenticationProvider could be a marker interface for 
# content objects supporting authentication. The content object would also
# need an additional marker interface, e.g. IMyMember. A general adapter
# in membrane could adapt from IAuthenticationProvider to IMembraneUserAuth.
# Inside this adapter, the context could be adapted to IUserAuthProvider to
# get the verifyCredentials() method. The adapter from IMyMember (which would
# be a marker on the same context object as the one that was obtained by
# adapting from IAuthenticationProvider, our new fictional interface) to 
# IUserAuthProvider would be provided by the product where IMyMember was
# defined.
#
# This pattern would apply to all non-marker interfaces below and in 
# plugin_markers that were used in a 'for' attribute for any adapter
# registration: 
#  - IUserRelated
#  - IUserAuthProvider
#  - IRolesProvider
#  - ISelectedGroupsProvider (but this would need to be divorced from
#       IReferenceable in the process)


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
