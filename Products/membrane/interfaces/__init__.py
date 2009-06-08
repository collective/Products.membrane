"""Membrane interfaces"""

from Products.membrane.interfaces.membrane_tool import IMembraneTool
IMembraneTool                                           # make pyflakes happy

from Products.membrane.interfaces.user import IMembraneUser
from Products.membrane.interfaces.user import IMembraneUserObject
from Products.membrane.interfaces.user import IMembraneUserAuth
from Products.membrane.interfaces.user import IMembraneUserProperties
from Products.membrane.interfaces.user import IMembraneUserRoles
from Products.membrane.interfaces.user import IMembraneUserGroups
from Products.membrane.interfaces.user import IMembraneUserChanger
from Products.membrane.interfaces.user import IMembraneUserDeleter
from Products.membrane.interfaces.user import IMembraneUserManagement
IMembraneUser, IMembraneUserObject, IMembraneUserAuth          # make pyflakes happy
IMembraneUserProperties, IMembraneUserRoles, IMembraneUserGroups
IMembraneUserChanger, IMembraneUserDeleter, IMembraneUserManagement

from Products.membrane.interfaces.plugins import IMembraneGroupManagerPlugin
from Products.membrane.interfaces.plugins import IMembraneRoleManagerPlugin
from Products.membrane.interfaces.plugins import IMembraneUserManagerPlugin
from Products.membrane.interfaces.plugins import IMembraneUserFactoryPlugin
IMembraneGroupManagerPlugin, IMembraneRoleManagerPlugin # make pyflakes happy
IMembraneUserManagerPlugin, IMembraneUserFactoryPlugin

from group import IGroup
IGroup                                                  # make pyflakes happy

from Products.membrane.interfaces.plugin_markers import IUserAuthProvider
from Products.membrane.interfaces.plugin_markers import IUserAuthentication
from Products.membrane.interfaces.plugin_markers import IPropertiesProvider
from Products.membrane.interfaces.plugin_markers import ISchemataPropertiesProvider
from Products.membrane.interfaces.plugin_markers import IGroupsProvider
from Products.membrane.interfaces.plugin_markers import IUserRoles
from Products.membrane.interfaces.plugin_markers import IRolesProvider
from Products.membrane.interfaces.plugin_markers import IGroupAwareRolesProvider
from Products.membrane.interfaces.plugin_markers import ISelectedGroupsProvider
from Products.membrane.interfaces.plugin_markers import IUserChanger
from Products.membrane.interfaces.plugin_markers import IUserDeleter
from zope.deprecation import deprecated
for iface in [ IUserAuthProvider, IUserAuthentication, IPropertiesProvider,
        ISchemataPropertiesProvider, IGroupsProvider, IUserRoles,
        IRolesProvider, IGroupAwareRolesProvider, ISelectedGroupsProvider,
        IUserChanger, IUserDeleter ]:
    deprecated(iface.__name__,
            "Please import AT support interfaces from Products.membrane.at.interfaces")

from Products.membrane.interfaces.categorymapper import ICategoryMapper
ICategoryMapper                                         # make pyflakes happy

from Products.membrane.interfaces.events import IMembraneTypeRegisteredEvent
from Products.membrane.interfaces.events import IMembraneTypeUnregisteredEvent
IMembraneTypeRegisteredEvent, IMembraneTypeUnregisteredEvent

from utilities import IUserAdder
IUserAdder                                              # make pyflakes happy
