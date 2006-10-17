""" 
Membrane tool interface
"""

from zope.interface import Interface
from zope.interface import Attribute

class IMembraneTool(Interface):
    '''This tool interacts with a customized ZCatalog.
    '''
    id = Attribute('id', 'Must be set to "membrane_tool"')
    user_adder = Attribute('user_adder',
                           'Name of the IUserAdder utility to use when '
                           'adding new users.')

    def registerMembraneType(portal_type):
        """Register a member type,
        by manipulating AT catalog multiplex registry"""

    def unregisterMembraneType(portal_type):
        """Unregister a member type,
        by manipulating AT catalog multiplex registry"""

    def listMembraneTypes():
        """Lists all currently registered member types"""
