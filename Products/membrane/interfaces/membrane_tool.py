"""
Membrane tool interface
"""

from zope.interface import Interface
from zope.interface import Attribute
from zope.interface import interfaces as iinterfaces


class IMembraneTool(Interface):
    '''This tool interacts with a customized ZCatalog.
    '''
    id = Attribute('id', 'Must be set to "membrane_tool"')
    user_adder = Attribute('user_adder',
                           'Name of the IUserAdder utility to use when '
                           'adding new users.')
    case_sensitive_auth = Attribute('case_sensitive_logins',
                                    'Boolean value specifying whether '
                                    'or not auth provider lookup should be '
                                    'case sensitive.')

# XXX membrane type logic should be ripped out - the membrane interfaces
# can be checked directly.
    def registerMembraneType(portal_type):
        """Register a member type, by manipulating AT catalog multiplex
        registry"""

    def unregisterMembraneType(portal_type):
        """Unregister a member type,
        by manipulating AT catalog multiplex registry"""

    def listMembraneTypes():
        """Lists all currently registered member types"""

    def getUserAuthProvider(login):
        """
        Returns the unique object that is the authentication provider
        for the provided login.
        """

    def getOriginalUserIdCase(userid):
        """
        Given any casing of a specific userid, returns the canonical
        casing of the same userid.  Facilitates consistent behaviour
        in sites that allow case-insensitive logins.
        """
        # XXX: user ids are essentialy binary strings, so this does not
        # make any sense. Should this be related to login names??


class IMembraneQueryableInterface(iinterfaces.IInterface):
    """Marker interface for interfaces by which membrane members can
    be queried.
    """
