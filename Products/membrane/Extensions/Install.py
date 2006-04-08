from StringIO import StringIO
from Products.membrane.config import PROJECTNAME, INSTALL_TEST_TYPES, TOOLNAME

from Products.Archetypes import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin

from Products.PluggableAuthService.interfaces.plugins \
    import IPropertiesPlugin
from Products.PluggableAuthService.interfaces.plugins \
    import IUserFactoryPlugin

from Products.PlonePAS.Extensions.Install import activatePluginInterfaces

from Products.membrane.tools.membrane import MembraneTool


def setupPlugins(portal, out):
    uf = portal.acl_users
    print >> out, "\nPlugin setup"

    membrane = uf.manage_addProduct['membrane']
    existing = uf.objectIds()

    if 'membrane_users' not in existing:
        membrane.addMembraneUserManager('membrane_users')
        print >> out, "Added User Manager."
        activatePluginInterfaces(portal, 'membrane_users', out)

    if 'membrane_groups' not in existing:
        membrane.addMembraneGroupManager('membrane_groups')
        print >> out, "Added Group Manager."
        activatePluginInterfaces(portal, 'membrane_groups', out)

    if 'membrane_roles' not in existing:
        membrane.addMembraneRoleManager('membrane_roles')
        print >> out, "Added Role Manager."
        activatePluginInterfaces(portal, 'membrane_roles', out)

    if 'membrane_properties' not in existing:
        membrane.addMembranePropertyManager('membrane_properties')
        print >> out, "Added Property Manager."
        activatePluginInterfaces(portal, 'membrane_properties', out)

        plugins = portal.acl_users.plugins
        #plist = plugins.listPlugins(IPropertiesPlugin)
        plugins.movePluginsUp(IPropertiesPlugin, ['membrane_properties'])

    if 'membrane_user_factory' not in existing:
        membrane.addMembraneUserFactory('membrane_user_factory')
        print >> out, "Added User Factory."
        activatePluginInterfaces(portal, 'membrane_user_factory', out)

        plugins = portal.acl_users.plugins
        #plist = plugins.listPlugins(IUserFactoryPlugin)
        plugins.movePluginsUp(IUserFactoryPlugin, ['membrane_user_factory'])


def setupTool(portal, out):
    if not TOOLNAME in portal.objectIds():
        m = portal.manage_addProduct[PROJECTNAME]
        m.manage_addTool(MembraneTool.meta_type)


def install(self):
    out = StringIO()

    setupTool(self, out)

    classes = listTypes(PROJECTNAME)
    installTypes(self, out, classes, PROJECTNAME)

    if INSTALL_TEST_TYPES:
        mtool = getattr(self, TOOLNAME)
        mtool.registerMembraneType('SimpleMember')
        mtool.registerMembraneType('SimpleGroup')

    #installTools(self, out)

    setupPlugins(self, out)

    return out.getvalue()
