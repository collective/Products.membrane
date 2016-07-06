"""Membrane interfaces"""

from Products.membrane.interfaces.membrane_tool import IMembraneTool  # noqa

from Products.membrane.interfaces.user import IMembraneUser  # noqa
from Products.membrane.interfaces.user import IMembraneUserObject  # noqa
from Products.membrane.interfaces.user import IMembraneUserAuth  # noqa
from Products.membrane.interfaces.user import IMembraneUserProperties  # noqa
from Products.membrane.interfaces.user import IMembraneUserRoles  # noqa
from Products.membrane.interfaces.user import IMembraneUserGroups  # noqa
from Products.membrane.interfaces.user import IMembraneUserChanger  # noqa
from Products.membrane.interfaces.user import IMembraneUserDeleter  # noqa
from Products.membrane.interfaces.user import IMembraneUserManagement  # noqa

from Products.membrane.interfaces.plugins import IMembraneGroupManagerPlugin  # noqa
from Products.membrane.interfaces.plugins import IMembraneRoleManagerPlugin  # noqa
from Products.membrane.interfaces.plugins import IMembraneUserManagerPlugin  # noqa
from Products.membrane.interfaces.plugins import IMembraneUserFactoryPlugin  # noqa

from Products.membrane.interfaces.group import IGroup  # noqa
from Products.membrane.interfaces.group import IMembraneGroupProperties  # noqa
from Products.membrane.interfaces.group import IMembraneGroupGroups  # noqa

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

from Products.membrane.interfaces.events import IMembraneTypeRegisteredEvent  # noqa
from Products.membrane.interfaces.events import IMembraneTypeUnregisteredEvent  # noqa

from utilities import IUserAdder  # noqa
