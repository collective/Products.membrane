from io import StringIO
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import INonInstallable
from Products.membrane.config import TOOLNAME
from Products.membrane.interfaces import IUserAdder
from Products.PlonePAS.setuphandlers import activatePluginInterfaces
from Products.PluggableAuthService.interfaces.plugins import IGroupsPlugin
from Products.PluggableAuthService.interfaces.plugins import IPropertiesPlugin
from Products.PluggableAuthService.interfaces.plugins import IUserFactoryPlugin
from zope.component.hooks import getSite
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles:
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "Products.membrane:uninstall",
        ]


def _doRegisterUserAdderUtility(context, step_name, profile_id, utility_name, utility):
    """registers utility for adding ExampleMembers"""
    portal = getSite()

    sm = portal.getSiteManager()
    logger = context.getLogger(step_name)
    if sm.queryUtility(IUserAdder, name=utility_name) is None:
        sm.registerUtility(provided=IUserAdder, component=utility, name=utility_name)
        logger.info("Registered IUserAdder utility: %s" % utility_name)
        mbtool = getToolByName(portal, TOOLNAME)
        if not mbtool.user_adder:
            # we become the default if one isn't already specified
            mbtool.user_adder = utility_name
    else:
        logger.info("IUserAdder utility '%s' already registered" % utility_name)


def _setupPlugins(portal, out):
    """
    Install and prioritize the membrane PAS plug-ins.
    """
    uf = getToolByName(portal, "acl_users")
    plugins = uf.plugins

    membrane = uf.manage_addProduct["membrane"]
    existing = uf.objectIds()

    if "membrane_users" not in existing:
        membrane.addMembraneUserManager("membrane_users")
        print("Added User Manager.", file=out)
        activatePluginInterfaces(portal, "membrane_users", out)

    if "membrane_groups" not in existing:
        membrane.addMembraneGroupManager("membrane_groups")
        print("Added Group Manager.", file=out)
        activatePluginInterfaces(portal, "membrane_groups", out)
        plugins.movePluginsUp(IGroupsPlugin, ["membrane_groups"])

    if "membrane_roles" not in existing:
        membrane.addMembraneRoleManager("membrane_roles")
        print("Added Role Manager.", file=out)
        activatePluginInterfaces(portal, "membrane_roles", out)

    if "membrane_properties" not in existing:
        membrane.addMembranePropertyManager("membrane_properties")
        print("Added Property Manager.", file=out)
        activatePluginInterfaces(portal, "membrane_properties", out)
        plugins.movePluginsUp(IPropertiesPlugin, ["membrane_properties"])
        plugins.movePluginsUp(IPropertiesPlugin, ["membrane_properties"])

    if "membrane_user_factory" not in existing:
        membrane.addMembraneUserFactory("membrane_user_factory")
        print("Added User Factory.", file=out)
        activatePluginInterfaces(portal, "membrane_user_factory", out)
        plugins.movePluginsUp(IUserFactoryPlugin, ["membrane_user_factory"])


def setupPlugins(context):
    """initialize membrane plugins"""
    if context.readDataFile("membrane-setup-plugins.txt") is None:
        return

    portal = getSite()
    out = StringIO()
    _setupPlugins(portal, out)
    logger = context.getLogger("plugins")
    logger.info(out.getvalue())


def _removePlugins(portal):
    """
    uninstall the membrane PAS plug-ins.
    """
    uf = getToolByName(portal, "acl_users")
    existing = uf.objectIds()

    if "membrane" in existing:
        uf.manage_delObjects(
            [
                "membrane",
            ]
        )

    if "membrane_users" in existing:
        uf.manage_delObjects(
            [
                "membrane_users",
            ]
        )

    if "membrane_groups" in existing:
        uf.manage_delObjects(
            [
                "membrane_groups",
            ]
        )

    if "membrane_roles" in existing:
        uf.manage_delObjects(
            [
                "membrane_roles",
            ]
        )

    if "membrane_properties" in existing:
        uf.manage_delObjects(
            [
                "membrane_properties",
            ]
        )

    if "membrane_user_factory" in existing:
        uf.manage_delObjects(
            [
                "membrane_user_factory",
            ]
        )


def uninstall(context):
    portal = getSite()
    _removePlugins(portal)
