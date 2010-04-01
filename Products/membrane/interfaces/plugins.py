"""
Membrane PAS plugin interfaces
------------------------------

The interfaces defined in this module define the PAS plugins implemented
by `Products.membrane`.
"""

from Products.PlonePAS.interfaces.capabilities import IDeleteCapability
from Products.PlonePAS.interfaces.capabilities import IPasswordSetCapability
from Products.PlonePAS.interfaces.group import IGroupIntrospection
from Products.PlonePAS.interfaces.plugins import IUserIntrospection
from Products.PlonePAS.interfaces.plugins import IUserManagement
from Products.PluggableAuthService.interfaces.plugins import (
    IAuthenticationPlugin)
from Products.PluggableAuthService.interfaces.plugins import (
    IGroupEnumerationPlugin)
from Products.PluggableAuthService.interfaces.plugins import IGroupsPlugin
from Products.PluggableAuthService.interfaces.plugins import IRolesPlugin
from Products.PluggableAuthService.interfaces.plugins import (
    IUserEnumerationPlugin)
from Products.PluggableAuthService.interfaces.plugins import IUserFactoryPlugin


class IMembraneUserManagerPlugin(IAuthenticationPlugin, IUserEnumerationPlugin,
                                 IUserIntrospection, IUserManagement,
                                 IPasswordSetCapability, IDeleteCapability):
    """
    Marks membrane user manager plugin.
    """


class IMembraneUserFactoryPlugin(IUserFactoryPlugin):
    """
    Marks membrane user factory plugin.
    """


class IMembraneGroupManagerPlugin(IGroupsPlugin, IGroupEnumerationPlugin,
                                  IGroupIntrospection):
    """
    Marks membrane group manager plugin.
    """


class IMembraneRoleManagerPlugin(IRolesPlugin):
    """
    Marks membrane role manager plugin.
    """
