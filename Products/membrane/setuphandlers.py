from StringIO import StringIO

from Products.CMFCore.utils import getToolByName

from Products.PluggableAuthService.interfaces.plugins \
     import IPropertiesPlugin
from Products.PluggableAuthService.interfaces.plugins \
     import IUserFactoryPlugin

from Products.PlonePAS.Extensions.Install import activatePluginInterfaces

from interfaces import IUserAdder
from config import TOOLNAME
from config import USE_COLLECTIVE_INDEXING


def _doRegisterUserAdderUtility(context, step_name, profile_id,
                                utility_name, utility):
    """ registers utility for adding ExampleMembers """
    portal = context.getSite()

    sm = portal.getSiteManager()
    logger = context.getLogger(step_name)
    if sm.queryUtility(IUserAdder, name=utility_name) is None:
        try:
            sm.registerUtility(provided=IUserAdder, component=utility,
                               name=utility_name)
        except TypeError:
            # BBB For Five 1.4 compatibility
            sm.registerUtility(interface=IUserAdder, utility=utility,
                               name=utility_name)
        logger.info("Registered IUserAdder utility: %s" %
                    utility_name)
        mbtool = getToolByName(portal, TOOLNAME)
        if not mbtool.user_adder:
            # we become the default if one isn't already specified
            mbtool.user_adder = utility_name
    else:
        logger.info("IUserAdder utility '%s' already registered" %
                    utility_name)


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
        plugins.movePluginsUp(IPropertiesPlugin, ['membrane_properties'])

    if 'membrane_user_factory' not in existing:
        membrane.addMembraneUserFactory('membrane_user_factory')
        print >> out, "Added User Factory."
        activatePluginInterfaces(portal, 'membrane_user_factory', out)

        plugins = uf.plugins
        plugins.movePluginsUp(IUserFactoryPlugin, ['membrane_user_factory'])


def setupPlugins(context):
    """ initialize membrane plugins """
    if context.readDataFile('membrane-setup-plugins.txt') is None:
        return

    portal = context.getSite()
    out = StringIO()
    if USE_COLLECTIVE_INDEXING:
         setup_tool = getToolByName(portal, 'portal_setup')
         try:
             setup_tool.runAllImportStepsFromProfile(
                 'profile-collective.indexing:default')
         except KeyError:
             # collective.indexing 2.0 has no install and needs no install.
             pass
    _setupPlugins(portal, out)
    logger = context.getLogger("plugins")
    logger.info(out.getvalue())
