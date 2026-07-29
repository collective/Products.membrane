from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing.layers import IntegrationTesting
from plone.testing import zope as zope_testing
from Products.CMFPlone.utils import _createObjectByType
from Products.membrane.config import TOOLNAME
from Products.membrane.tests import dummy


class MembraneBaseLayer(PloneSandboxLayer):
    """Base layer for Products.membrane.

    It jut sets up the basic Plone site with membrane installed.
    This is used as a base for other layers that need to build on top of it.
    """

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import Products.membrane

        self.loadZCML(package=Products.membrane)
        zope_testing.installProduct(app, "Products.membrane")

    def setUpPloneSite(self, portal):
        applyProfile(portal, "Products.membrane:default")

    def tearDownZope(self, app):
        zope_testing.uninstallProduct(app, "Products.membrane")


MEMBRANE_BASE_FIXTURE = MembraneBaseLayer()


class MembraneTestingBaseLayer(PloneSandboxLayer):
    """Base layer for testing Products.membrane.

    This layers builds on top of the MembraneBaseLayer and sets up a Plone site
    with the necessary configurations for testing membrane functionality.

    It registers the membrane types and adds a test folder to the portal.
    """

    defaultBases = (MEMBRANE_BASE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import Products.membrane.tests

        self.loadZCML(package=Products.membrane.tests, name="testing.zcml")

    def setUpPloneSite(self, portal):
        applyProfile(portal, "Products.membrane.tests:test")


MEMBRANE_TESTING_BASE_FIXTURE = MembraneTestingBaseLayer()


class MembraneTestingLayer(PloneSandboxLayer):

    defaultBases = (MEMBRANE_TESTING_BASE_FIXTURE,)

    def setUpPloneSite(self, portal):
        portal.acl_users.userFolderAddUser("admin", "secret", ["Manager"], [])

        setRoles(portal, TEST_USER_ID, ["Manager"])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory("Folder", id="test-folder", title="Test Folder")

        mbtool = getattr(portal, TOOLNAME)
        mbtool.registerMembraneType(dummy.TestMember.portal_type)
        mbtool.registerMembraneType(dummy.AlternativeTestMember.portal_type)
        mbtool.registerMembraneType(dummy.TestGroup.portal_type)
        logout()


MEMBRANE_TESTING_FIXTURE = MembraneTestingLayer()


def addUser(obj, username="testuser", title="full name"):
    member = _createObjectByType("TestMember", obj, username)
    member.setUserName(username)
    member.setPassword("testpassword")
    # Title is mapped to the user property fullname using
    # user_property='fullname'
    member.setTitle(title)
    member.setMobilePhone("555-1212")
    member.reindexObject()
    return member


class MembraneAddUserLayer(PloneSandboxLayer):
    """Layer for testing adding users to the membrane."""

    defaultBases = (MEMBRANE_TESTING_BASE_FIXTURE,)

    def setUpPloneSite(self, portal):
        login(portal, TEST_USER_NAME)
        addUser(portal)
        logout()


MEMBRANE_ADD_USER_FIXTURE = MembraneAddUserLayer()


class MembraneOneUserLayer(PloneSandboxLayer):
    """Layer for testing with a single membrane user."""

    defaultBases = (MEMBRANE_TESTING_FIXTURE,)

    def setUpPloneSite(self, portal):
        login(portal, TEST_USER_NAME)
        addUser(portal)
        logout()


MEMBRANE_ONE_USER_FIXTURE = MembraneOneUserLayer()


class MembraneUserManagerLayer(PloneSandboxLayer):
    """Layer for testing with a membrane user manager."""

    defaultBases = (MEMBRANE_ADD_USER_FIXTURE,)

    def setUpPloneSite(self, portal):
        from Products.membrane.plugins.usermanager import MembraneUserManager

        portal.acl_users.pmm = MembraneUserManager(id="pmm")


MEMBRANE_USER_MANAGER_FIXTURE = MembraneUserManagerLayer()


class MembraneUserManagerTwoUsersLayer(PloneSandboxLayer):
    """Layer for testing with a membrane user manager and two users."""

    defaultBases = (MEMBRANE_USER_MANAGER_FIXTURE,)

    def setUpPloneSite(self, portal):
        addUser(portal, username="testuser2", title="full name 2")


MEMBRANE_USER_MANAGER_TWO_USERS_FIXTURE = MembraneUserManagerTwoUsersLayer()


MEMBRANE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MEMBRANE_TESTING_FIXTURE,), name="MembraneTestingLayer:Integration"
)

MEMBRANE_ONE_USER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MEMBRANE_ONE_USER_FIXTURE,), name="MembraneOneUserLayer:Integration"
)

MEMBRANE_ADD_USER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MEMBRANE_ADD_USER_FIXTURE,), name="MembraneAddUserLayer:Integration"
)
MEMBRANE_USER_MANAGER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MEMBRANE_USER_MANAGER_FIXTURE,), name="MembraneUserManagerLayer:Integration"
)
MEMBRANE_USER_MANAGER_TWO_USERS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MEMBRANE_USER_MANAGER_TWO_USERS_FIXTURE,),
    name="MembraneUserManagerTwoUsersLayer:Integration",
)
