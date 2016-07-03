from pkg_resources import DistributionNotFound
from pkg_resources import get_distribution
from plone.app.testing import applyProfile
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing.layers import IntegrationTesting
from plone.testing import z2
from Products import membrane
from Products.CMFPlone.utils import _createObjectByType
from Products.membrane import examples
from Products.membrane import tests
from Products.membrane.config import TOOLNAME
from Products.membrane.tests import dummy
from zope.configuration import xmlconfig

try:
    get_distribution('collective.indexing')
    HAS_INDEXING = True
except DistributionNotFound:
    HAS_INDEXING = False
try:
    get_distribution('Products.remember')
    HAS_REMEMBER = True
except DistributionNotFound:
    HAS_REMEMBER = False

PLONE_VERSION = get_distribution('Products.CMFPlone').version
MAJOR_PLONE_VERSION = int(PLONE_VERSION[0])
orig_initialize = membrane.initialize


def initialize(context):
    orig_initialize(context)
    examples.initialize(context)
    tests.initialize(context)

# TODO We are patching the installation here, and should find a better way to
# do this
membrane.initialize = initialize


class Session(dict):

    def set(self, key, value):
        self[key] = value


class MembraneProfilesLayer(PloneSandboxLayer):

    def setUpZope(self, app, configurationContext):
        import Products.membrane
        self.loadZCML(package=Products.membrane)
        z2.installProduct(app, 'Products.membrane')
        xmlconfig.file(
            'testing.zcml',
            Products.membrane.tests,
            context=configurationContext)
        app.REQUEST['SESSION'] = Session()
        if HAS_INDEXING:
            import collective.indexing
            z2.installProduct(app, 'collective.indexing')
            self.loadZCML(package=collective.indexing)
        if HAS_REMEMBER:
            # We do not need this ourselves, but it is nice if we can at least
            # load it without breaking anything.
            import Products.remember
            z2.installProduct(app, 'Products.remember')
            self.loadZCML(package=Products.remember)
        if MAJOR_PLONE_VERSION >= 5:
            import plone.app.contenttypes
            self.loadZCML(package=plone.app.contenttypes)
            # We need to load Archetypes because our example and test profiles
            # need this.  We could turn the types into dexterity types and
            # depend on collective.indexing instead.
            import Products.Archetypes
            self.loadZCML(package=Products.Archetypes)

    def setUpPloneSite(self, portal):
        if MAJOR_PLONE_VERSION >= 5:
            applyProfile(portal, 'plone.app.contenttypes:default')
        applyProfile(portal, 'Products.membrane:default')
        applyProfile(portal, 'Products.membrane.tests:test')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.acl_users.userFolderAddUser('admin',
                                           'secret',
                                           ['Manager'],
                                           [])
        portal.invokeFactory(
            "Folder",
            id="test-folder",
            title=u"Test Folder"
        )
        logout()

        mbtool = getattr(portal, TOOLNAME)
        mbtool.registerMembraneType(dummy.TestMember.portal_type)
        mbtool.registerMembraneType(dummy.AlternativeTestMember.portal_type)
        mbtool.registerMembraneType(dummy.TestGroup.portal_type)

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'collective.indexing')
        z2.uninstallProduct(app, 'Products.membrane')


def addUser(obj, username='testuser', title='full name'):
    member = _createObjectByType('TestMember', obj, username)
    member.setUserName(username)
    member.setPassword('testpassword')
    # Title is mapped to the user property fullname using
    # user_property='fullname'
    member.setTitle(title)
    member.setMobilePhone('555-1212')
    member.reindexObject()
    return member


class AddUserLayer(MembraneProfilesLayer):

    def setUpPloneSite(self, portal):
        if MAJOR_PLONE_VERSION >= 5:
            applyProfile(portal, 'plone.app.contenttypes:default')
        applyProfile(portal, 'Products.membrane:default')
        applyProfile(portal, 'Products.membrane.tests:test')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        addUser(portal)
        logout()


class MembraneUserManagerLayer(AddUserLayer):

    def setUpPloneSite(self, portal):
        if MAJOR_PLONE_VERSION >= 5:
            applyProfile(portal, 'plone.app.contenttypes:default')
        applyProfile(portal, 'Products.membrane:default')
        applyProfile(portal, 'Products.membrane.tests:test')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        addUser(portal)
        from Products.membrane.plugins.usermanager import MembraneUserManager
        portal.acl_users.pmm = MembraneUserManager(id='pmm')
        logout()


class MembraneUserManagerTwoUsersLayer(MembraneUserManagerLayer):

    def setUpPloneSite(self, portal):
        if MAJOR_PLONE_VERSION >= 5:
            applyProfile(portal, 'plone.app.contenttypes:default')
        applyProfile(portal, 'Products.membrane:default')
        applyProfile(portal, 'Products.membrane.tests:test')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        addUser(portal)
        from Products.membrane.plugins.usermanager import MembraneUserManager
        portal.acl_users.pmm = MembraneUserManager(id='pmm')
        member = _createObjectByType('TestMember', portal,
                                     'testuser2')
        member.setUserName('testuser2')
        member.setPassword('testpassword2')
        member.setTitle('full name 2')
        member.reindexObject()
        logout()


MEMBRANE_PROFILES_FIXTURE = MembraneProfilesLayer()
MEMBRANE_ADD_USER_FIXTURE = AddUserLayer()
MEMBRANE_USER_MANAGER_FIXTURE = MembraneUserManagerLayer()
MEMBRANE_USER_MANAGER_TWO_USERS_FIXTURE = MembraneUserManagerTwoUsersLayer()

MEMBRANE_PROFILES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MEMBRANE_PROFILES_FIXTURE,),
    name="MembraneProfilesLayer:Integration")
MEMBRANE_ADD_USER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MEMBRANE_ADD_USER_FIXTURE,),
    name="MembraneAddUserLayer:Integration")
MEMBRANE_USER_MANAGER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MEMBRANE_USER_MANAGER_FIXTURE,),
    name="MembraneUserManagerLayer:Integration")
MEMBRANE_USER_MANAGER_TWO_USERS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MEMBRANE_USER_MANAGER_TWO_USERS_FIXTURE,),
    name="MembraneUserManagerTwoUsersLayer:Integration")
