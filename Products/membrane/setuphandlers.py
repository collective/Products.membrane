from StringIO import StringIO

from Products.CMFCore.utils import getToolByName

from Products.PluggableAuthService.interfaces.plugins \
     import IPropertiesPlugin
from Products.PluggableAuthService.interfaces.plugins \
     import IUserFactoryPlugin

from Products.PlonePAS.Extensions.Install import activatePluginInterfaces

def _setupPlugins(portal, out):
    """
    Install and prioritize the membrane PAS plug-ins.
    """
    uf = getToolByName(portal, 'acl_users')

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

        plugins = uf.plugins
        plugins.movePluginsUp(IPropertiesPlugin, ['membrane_properties'])

    if 'membrane_user_factory' not in existing:
        membrane.addMembraneUserFactory('membrane_user_factory')
        print >> out, "Added User Factory."
        activatePluginInterfaces(portal, 'membrane_user_factory', out)

        plugins = uf.plugins
        plugins.movePluginsUp(IUserFactoryPlugin, ['membrane_user_factory'])


def setupPlugins(context):
    out = StringIO()
    portal = context.getSite()
    _setupPlugins(portal, out)
    logger = context.getLogger("plugins")
    logger.info(out.getvalue())
