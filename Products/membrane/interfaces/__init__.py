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
IMembraneUser, IMembraneUserObject, IMembraneUserAuth  # make pyflakes happy
IMembraneUserProperties, IMembraneUserRoles, IMembraneUserGroups
IMembraneUserChanger, IMembraneUserDeleter, IMembraneUserManagement

from Products.membrane.interfaces.plugins import IMembraneGroupManagerPlugin
from Products.membrane.interfaces.plugins import IMembraneRoleManagerPlugin
from Products.membrane.interfaces.plugins import IMembraneUserManagerPlugin
from Products.membrane.interfaces.plugins import IMembraneUserFactoryPlugin
IMembraneGroupManagerPlugin, IMembraneRoleManagerPlugin  # make pyflakes happy
IMembraneUserManagerPlugin, IMembraneUserFactoryPlugin

from group import IGroup
IGroup                                                  # make pyflakes happy

from Products.membrane.at.interfaces import IUserAuthProvider
from Products.membrane.at.interfaces import IUserAuthentication
from Products.membrane.at.interfaces import IPropertiesProvider
from Products.membrane.at.interfaces import ISchemataPropertiesProvider
from Products.membrane.at.interfaces import IGroupsProvider
from Products.membrane.at.interfaces import IUserRoles
from Products.membrane.at.interfaces import IRolesProvider
from Products.membrane.at.interfaces import IGroupAwareRolesProvider
from Products.membrane.at.interfaces import ISelectedGroupsProvider
from Products.membrane.at.interfaces import IUserChanger
from Products.membrane.at.interfaces import IUserDeleter
from zope.deprecation import deprecated
for iface in [
    IUserAuthProvider, IUserAuthentication, IPropertiesProvider,
    ISchemataPropertiesProvider, IGroupsProvider, IUserRoles,
    IRolesProvider, IGroupAwareRolesProvider, ISelectedGroupsProvider,
    IUserChanger, IUserDeleter]:
    deprecated(iface.__name__,
               "Please import AT support interfaces from "
               "Products.membrane.at.interfaces")

from Products.membrane.interfaces.events import IMembraneTypeRegisteredEvent
from Products.membrane.interfaces.events import IMembraneTypeUnregisteredEvent
IMembraneTypeRegisteredEvent, IMembraneTypeUnregisteredEvent

from utilities import IUserAdder
IUserAdder                                              # make pyflakes happy
